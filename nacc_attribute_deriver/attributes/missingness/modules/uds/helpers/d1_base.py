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

    def handle_normcog_gate(self, field: str, ignore_normcog_0: bool = False) -> int:
        """Handles NORMCOG-gated variables, which follow:

        If FIELD is blank:
            If NORMCOG = 1, FIELD = 8
            If NORMCOG = 0, FIELD = 0 (optional, some values don't consider this)
        """
        value = self.uds.get_value(field, int)
        if value is None:
            if self.normcog == 1:
                return 8
            if not ignore_normcog_0 and self.normcog == 0:
                return 0

            return INFORMED_MISSINGNESS

        return value

    def handle_normcog_with_other_gate(self, gate: str, field: str) -> int:
        """Handles NORMCOG with another gate logic, which follows:

        If FIELD is blank:
            If NORMCOG = 0 and GATE is blank/0, then FIELD = 7.
            Else if NORMCOG = 1, FIELD = 8
        """
        value = self.uds.get_value(field, int)
        if value is None:
            gate_value = self.uds.get_value(gate, int)
            if self.normcog == 0 and (gate_value is None or gate_value == 0):
                return 7
            if self.normcog == 1:
                return 8

            return INFORMED_MISSINGNESS

        return value

    def handle_cognitive_impairment_gate(
        self,
        gate: str,
        field: str,
        override_value: Optional[int] = None,
    ) -> int:
        """Handles variables dependent on cognitive impairment (DEMENTED, MCI,
        IMPNOMCI) and another gate, e.g:

        If any(DEMENTED, MCI, IMPNOMCI = 1) and GATE is 0 or blank and FIELD is blank, FIELD = 7
        Else if NORMCOG = 1 and FIELD is blank, FIELD = 8

        Args:
            gate: The gate to check - must be none/blank for condition to succeed
            field: The field
            override_value: REGRESSION ARG - some legacy variables set the value
                beforehand based on other logic, see below, see below

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
        value = self.uds.get_value(field, int)

        # main logic we actually care about
        if value is None:
            if (
                self.has_cognitive_impairment()
                and (gate_value is None or gate_value == 0)
                and (
                    override_value is None
                    or override_value not in [INFORMED_MISSINGNESS, 1]
                )
            ):
                return 7

            if override_value is not None:
                return override_value

            if self.normcog == 1:
                return 8

            return INFORMED_MISSINGNESS

        return value
