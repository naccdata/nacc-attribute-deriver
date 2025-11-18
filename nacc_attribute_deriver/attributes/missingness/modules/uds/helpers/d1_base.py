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
        self,
        gate: str,
        field: str,
        ignore_normcog_0: bool = False,
        other_gate: Optional[str] = None,
        consider_formverd1: bool = False,
    ) -> Optional[int]:
        """Handles variables dependent on NORMCOG and another gate:

        If NORMCOG = 0 and GATE is 0 or blank and FIELD is blank, FIELD = 7
        Else if NORMCOG = 1 and FIELD is blank, FIELD = 8

        REGRESSION: Some variables look at an additional gate and/or formverd1, so consideer
            that if specified. Mainly for POSSADIF, VASCPSIF, and COGOTH variables because
            of these lines in the SAS:
            %recode4g(gvar=d1formver,varlist=COGOTH2 COGOTH2F COGOTH3 COGOTH3F VASCPS VASCPSIF,
                      qvalue=.,result=-4,vallist=1);
            %recode4gg(gvarlist=PROBAD PROBAD VASC VASC,
                       varlist=POSSAD POSSADIF VASCPS VASCPSIF
                       ,qvalue=.,result=0,vallist=1);

            The formverd1 case mainly occurs when formver == 2 but formverd1 == 1. Does
            not seem as applicable for V3.

            Because PROBAD/VASC are gates themselves, seem to not be as effected (?
            or at least no regression errors raised for those in relation to this.)
        """
        gate_value = self.uds.get_value(gate, int)
        current_value = self.uds.get_value(field, int)

        # REGRESSION
        if current_value is None:
            other_gate_value = (
                self.uds.get_value(other_gate, int) if other_gate else None
            )

            # formverd1 can be different from the overall form version
            formver_d1 = (
                self.uds.get_value("formverd1", float) if consider_formverd1 else None
            )

            if other_gate_value == 1:
                current_value = 0

            if formver_d1 == 1:
                current_value = INFORMED_MISSINGNESS

        if (
            self.has_cognitive_impairment()
            and (gate_value is None or gate_value == 0)
            and (
                current_value is None or current_value not in [INFORMED_MISSINGNESS, 1]
            )
        ):
            return 7

        # REGRESSION
        if current_value is not None:
            return current_value

        return self.handle_normcog_gate(field, ignore_normcog_0=ignore_normcog_0)
