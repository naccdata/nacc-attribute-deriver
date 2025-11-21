"""Class to handle A2-specific missingness values."""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class UDSFormA2Missingness(UDSMissingness):
    ############################
    # INLIVWTH-gated variables #
    ############################

    def _handle_inlivwth_gate(self, field: str) -> int:
        """Handles missingness for gated by INLIVWTH.

        If INLIVWTH=1 then VAR=8
        """
        inlivwth = self.uds.get_value("inlivwth", int)
        if inlivwth == 1:
            return 8

        return self.generic_missingness(field, int)

    def _missingness_incntmod(self) -> int:
        """Handles missingness for INCNTMOD."""
        return self._handle_inlivwth_gate("incntmod")

    def _missingness_incnttim(self) -> int:
        """Handles missingness for INCNTTIM."""
        return self._handle_inlivwth_gate("incnttim")

    def _missingness_invisits(self) -> int:
        """Handles missingness for INVISITS."""
        return self._handle_inlivwth_gate("invisits")

    def _missingness_incalls(self) -> int:
        """Handles missingness for INCALLS."""
        return self._handle_inlivwth_gate("incalls")

    ##########################
    # NEWINF-gated variables #
    ##########################

    def __handle_newinf_gate(self, field: str) -> int:
        """Handles missingness for variables gated by NEWINF.

        NEWINF only provided in FVP.
        """
        if self.uds.get_value("newinf", int) == 0:
            return INFORMED_MISSINGNESS

        return self.generic_missingness(field, int)

    def _missingness_inknown(self) -> int:
        """Handles missingness for INKNOWN."""
        return self.__handle_newinf_gate("inknown")

    def _missingness_inhisp(self) -> int:
        """Handles missingness for INHISP."""
        return self.__handle_newinf_gate("inhisp")

    def _missingness_inhispor(self) -> int:
        """Handles missingness for INHISPOR."""
        if self.uds.get_value("inhisp", int) in [0, 9]:
            return 88

        return self.__handle_newinf_gate("inhispor")

    def _missingness_inrace(self) -> int:
        """Handles missingness for INRACE."""
        return self.__handle_newinf_gate("inrace")

    def _missingness_inrasec(self) -> int:
        """Handles missingness for INRASEC."""
        return self.__handle_newinf_gate("inrasec")

    def _missingness_inrater(self) -> int:
        """Handles missingness for INRATER."""
        return self.__handle_newinf_gate("inrater")

    def _missingness_ineduc(self) -> int:
        """Handles missingness for INEDUC."""
        return self.__handle_newinf_gate("ineduc")
