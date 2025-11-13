"""Handles core D1 functionality.

In V4, form D1 was split into D1a and D1b. However they still share a
lot of core functionality, so extract base class for them to use.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class UDSFormD1Missingness(UDSMissingness):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table)

        # variables a majority of these missingness values rely on
        self.normcog = self.uds.get_value("normcog", int)
        self.demented = self.uds.get_value("demented", int)
        self.impnomci = self.uds.get_value("impnomci", int)
        self.mci = self.generate_mci()

    def generate_mci(self) -> int:
        """(This is copied from the derived variable code; should probably
        figure out a better pattern to avoid duplication."""
        if self.formver >= 4:
            mci = self.uds.get_value("mci", int)
            return 1 if mci == 1 else 0

        # all of these fields can be null, 0, or 1
        mci_vars = self.uds.group_attributes(
            ["mciamem", "mciaplus", "mcinon1", "mcinon2"], int
        )

        return 1 if any(x == 1 for x in mci_vars) else 0

    def has_cognitive_impairment(self) -> bool:
        """Check DEMENTED, MCI, and IMPNOMCI for cognitive impairment."""
        return self.demented == 1 or self.generate_mci() == 1 or self.impnomci == 1

    def handle_normcog_gate(
        self, field: str, ignore_normcog_0: bool = False
    ) -> Optional[int]:
        """Handles NORMCOG-gated variables, which follow:

        If NORMCOG = 1 and FIELD is blank, FIELD = 8
        """
        if self.uds.get_value(field, int) is None:
            if self.normcog == 1:
                return 8
            if not ignore_normcog_0 and self.normcog == 0:
                return 0

            return INFORMED_MISSINGNESS

        return None

    def handle_cognitive_impairment_gate(
        self, gate: str, field: str, ignore_normcog_0: bool = False
    ) -> Optional[int]:
        """Handles variables dependent on NORMCOG and another gate:

        If NORMCOG = 0 and GATE is 0 or blank and FIELD is blank, FIELD = 7
        Else if NORMCOG = 1 and FIELD is blank, FIELD = 8
        """
        gate_value = self.uds.get_value(gate, int)
        value = self.uds.get_value(field, int)

        if (
            self.has_cognitive_impairment()
            and (gate_value is None or gate_value == 0)
            and value is None
        ):
            return 7

        return self.handle_normcog_gate(field, ignore_normcog_0=ignore_normcog_0)
