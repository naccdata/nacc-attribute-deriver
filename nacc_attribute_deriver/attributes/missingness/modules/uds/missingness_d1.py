"""Class to handle D1-specific missingness values.

These are variables that only exist in V3 and earlier for D1; others
will now be found in either D1a or D1b.
"""

from typing import Optional

from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)

from .helpers.d1_base import UDSFormD1Missingness


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
        # REGRESSION - RDD does not specify DEMUN can be 8
        # but it IS happening in the legacy when NORMCOG == 1
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
        # REGRESSION: Legacy SAS doesn't explicitly use the cognitive impairment
        # gate but seems like what it does is effectively the same thing
        # it also does an additional check based on PROBAD
        return self.handle_cognitive_impairment_gate(
            "possad", "possadif", other_gate="probad"
        )

    def _missingness_vascps(self) -> Optional[int]:
        """Handles missingness for VASCPS."""
        # REGRESSION: consideres VASC and FORMVERD1
        if self.uds.get_value("vascps", int) is None:
            if self.uds.get_value("formverd1", float) == 1.0:
                return INFORMED_MISSINGNESS

            if self.uds.get_value("vasc", int) == 1:
                return 0

        return self.handle_normcog_gate("vascps")

    def _missingness_vascpsif(self) -> Optional[int]:
        """Handles missingness for VASCPSIF."""
        # REGRESSION: does additional checks based on VASC and FORMVERD1
        return self.handle_cognitive_impairment_gate(
            "vascps", "vascpsif", other_gate="vasc", consider_formverd1=True
        )

    #######################
    # CVD-gated variables #
    #######################

    def __handle_cvd_gate(
        self, field: str, return_value: int, evaluate_prevstk: bool = False
    ) -> Optional[int]:
        """Handles variables gated by CVD."""
        cvd = self.uds.get_value("cvd", int)
        value = self.uds.get_value(field, int)

        if value is None:
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
        if self.uds.get_value("alcabuse", int) is not None:
            return None

        if self.uds.get_value("alcdem", int) == 0:
            return 8

        return self.generic_missingness("alcabuse", int)

    def _missingness_deptreat(self) -> Optional[int]:
        """Handles missingness for DEPTREAT."""
        if self.uds.get_value("deptreat", int) is not None:
            return None

        if self.uds.get_value("dep", int) == 0:
            return 8

        return self.generic_missingness("deptreat", int)

    def _missingness_brnincte(self) -> Optional[int]:
        """Handles missingness for BRNINCTE."""
        if self.uds.get_value("brnincte", int) is not None:
            return None

        if self.uds.get_value("brninj", int) == 0:
            return 8

        return self.generic_missingness("brnincte", int)

    def _missingness_park(self) -> Optional[int]:
        """Handles missingness for PARK."""
        if self.uds.get_value("park", int) is not None:
            return None

        if self.uds.get_value("lbdis", int) == 0:
            return 0

        return self.generic_missingness("park", int)
