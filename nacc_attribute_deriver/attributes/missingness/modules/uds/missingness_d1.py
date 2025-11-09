"""Class to handle D1-specific missingness values.

These are variables that only exist in V3 and earlier for D1; others
will now be found in either D1a or D1b.
"""

from typing import Optional

from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

from .missingness_uds import UDSMissingness


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


class UDSFormD1LegacyMissingness(UDSFormD1Missingness):
    """For variables not applicable to or didn't change in V4."""

    ###########################
    # NORMCOG-gated variables #
    ###########################

    def _missingness_dysill(self) -> Optional[int]:
        """Handles missingness for DYSILL."""
        return self.handle_normcog_gate("dysill")

    def _missingness_probad(self) -> Optional[int]:
        """Handles missingness for PROBAD."""
        return self.handle_normcog_gate("probad")

    def _missingness_ftd(self) -> Optional[int]:
        """Handles missingness for FTD."""
        return self.handle_normcog_gate("ftd")

    def _missingness_ppaph(self) -> Optional[int]:
        """Handles missingness for PPAPH."""
        return self.handle_normcog_gate("ppaph")

    def _missingness_vasc(self) -> Optional[int]:
        """Handles missingness for VASC."""
        return self.handle_normcog_gate("vasc")

    def _missingness_stroke(self) -> Optional[int]:
        """Handles missingness for STROKE."""
        return self.handle_normcog_gate("stroke")

    def _missingness_demun(self) -> Optional[int]:
        """Handles missingness for DEMUN."""
        return self.handle_normcog_gate("demun")

    ########################################
    # Cognitive impairment-gated variables #
    ########################################

    def _missingness_esstreif(self) -> Optional[int]:
        """Handles missingness for ESSTREIF."""
        return self.handle_cognitive_impairment_gate("esstrem", "esstreif")

    def _missingness_dysillif(self) -> Optional[int]:
        """Handles missingness for DYSILLIF."""
        return self.handle_cognitive_impairment_gate("dysill", "dysillif")

    def _missingness_probadif(self) -> Optional[int]:
        """Handles missingness for PROBADIF."""
        return self.handle_cognitive_impairment_gate("probad", "probadif")

    def _missingness_ftdif(self) -> Optional[int]:
        """Handles missingness for FTDIF."""
        return self.handle_cognitive_impairment_gate("ftd", "ftdif")

    def _missingness_ppaphif(self) -> Optional[int]:
        """Handles missingness for PPAPHIF."""
        return self.handle_cognitive_impairment_gate("ppaph", "ppaphif")

    def _missingness_vascif(self) -> Optional[int]:
        """Handles missingness for VASCIF."""
        return self.handle_cognitive_impairment_gate("vasc", "vascif")

    def _missingness_strokif(self) -> Optional[int]:
        """Handles missingness for STROKIF."""
        return self.handle_cognitive_impairment_gate("stroke", "strokif")

    def _missingness_demunif(self) -> Optional[int]:
        """Handles missingness for DEMUNIF."""
        return self.handle_cognitive_impairment_gate("demun", "demunif")

    def _missingness_depif(self) -> Optional[int]:
        """Handles missingness for DEPIF."""
        return self.handle_cognitive_impairment_gate("dep", "depif")

    def _missingness_brninjif(self) -> Optional[int]:
        """Handles missingness for BRNINJIF."""
        return self.handle_cognitive_impairment_gate("brninj", "brninjif")

    ######################################
    # NORMCOG and another gate variables #
    ######################################

    def _missingness_possad(self) -> Optional[int]:
        """Handles missingness for POSSAD."""
        if self.uds.get_value("probad", int) == 1:
            return 0

        return self.handle_normcog_gate("possad")

    def _missingness_possadif(self) -> Optional[int]:
        """Handles missingness for POSSADIF."""
        if self.uds.get_value("possad", int) != 1:
            return 7

        # TODO: not sure why this one doesn't use the cognitive impairment
        # gate in legacy SAS code? should it just do so?
        return self.handle_normcog_gate("possadif")

    def _missingness_vascps(self) -> Optional[int]:
        """Handles missingness for VASCPS."""
        if self.uds.get_value("vasc", int) == 1:
            return 0

        return self.handle_normcog_gate("vascps")

    def _missingness_vascpsif(self) -> Optional[int]:
        """Handles missingness for VASCPSIF."""
        if self.uds.get_value("vasc", int) == 1:
            return 0

        return self.handle_cognitive_impairment_gate("vascps", "vascpsif")

    #######################
    # CVD-gated variables #
    #######################

    def __handle_cvd_gate(
        self, field: str, return_value: int, evaluate_prevstk: bool = False
    ) -> Optional[int]:
        """Handles variables gated by CVD."""
        cvd = self.uds.get_value("cvd", int)
        if cvd == 0:
            return return_value
        if evaluate_prevstk and cvd == 1:
            prevstk = self.uds.get_value("prevstk", int)
            if prevstk == 0:
                return return_value

        return self.generic_missingness(field, int)

    def _missingness_prevstk(self) -> Optional[int]:
        """Handles missingness for PREVSTK."""
        return self.__handle_cvd_gate("prevstk", 0)

    def _missingness_infwmh(self) -> Optional[int]:
        """Handles missingness for INFWMH."""
        return self.__handle_cvd_gate("infwmh", 9)

    def _missingness_infnetw(self) -> Optional[int]:
        """Handles missingness for INFNETW."""
        return self.__handle_cvd_gate("infnetw", 9)

    def _missingness_strokdec(self) -> Optional[int]:
        """Handles missingness for STROKDEC."""
        return self.__handle_cvd_gate("strokdec", 8, evaluate_prevstk=True)

    def _missingness_stkimag(self) -> Optional[int]:
        """Handles missingness for STKIMAG."""
        return self.__handle_cvd_gate("stkimag", 8, evaluate_prevstk=True)

    ###################
    # Other variables #
    ###################

    def _missingness_alcabuse(self) -> Optional[int]:
        """Handles missingness for ALCABUSE."""
        if self.uds.get_value("alcdem", int) == 0:
            return 8

        return self.generic_missingness("alcabuse", int)

    def _missingness_deptreat(self) -> Optional[int]:
        """Handles missingness for DEPTREAT."""
        if self.uds.get_value("dep", int) == 0:
            return 8

        return self.generic_missingness("deptreat", int)

    def _missingness_brnincte(self) -> Optional[int]:
        """Handles missingness for BRNINCTE."""
        if self.uds.get_value("brninj", int) == 0:
            return 8

        return self.generic_missingness("brnincte", int)
