"""Class to handle A2-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

from .missingness_uds import UDSMissingness


class UDSFormA2Missingness(UDSMissingness):
    def _handle_inlivwth_gate(self, field: str) -> Optional[int]:
        """Handles missingness for gated by INLIVWTH.

        If INLIVWTH=1 then VAR=8
        """
        inlivwth = self.uds.get_value("inlivwth", int)
        if inlivwth == 1:
            return 8

        return self.generic_missingness(field)

    def _missingness_incntmod(self) -> Optional[int]:
        """Handles missingness for INCNTMOD.

        If INLIVWTH=1 then INCNTMOD=8
        """
        return self._handle_inlivwth_gate("incntmod")

    def _missingness_incnttim(self) -> Optional[int]:
        """Handles missingness for INCNTTIM.

        If INLIVWTH=1 then INCNTTIM=8
        """
        return self._handle_inlivwth_gate("incnttim")

    def _missingness_incntmdx(self) -> Optional[str]:
        """Handles missingness for INCNTMDX.

        If INCNTMDX is blank then INCNTMDX should remain blank
        """
        return self.generic_writein("incntmdx")

    ##########################
    # NEWINF-gated variables #
    ##########################

    def __handle_newinf_gate(self, field: str) -> Optional[int]:
        """Handles missingness for variables gated by NEWINF.

        NEWINF only provided in FVP.
        """
        if self.uds.get_value("newinf", int) == 0:
            return INFORMED_MISSINGNESS

        return self.generic_missingness(field)

    def _missingness_inknown(self) -> Optional[int]:
        """Handles missingness for INKNOWN"""
        return self.__handle_newinf_gate('inknown')

    def _missingness_inhisp(self) -> Optional[int]:
        """Handles missingness for INHISP"""
        return self.__handle_newinf_gate('inhisp')

    def _missingness_inhispor(self) -> Optional[int]:
        """Handles missingness for INHISPOR"""
        return self.__handle_newinf_gate('inhispor')

    def _missingness_inrace(self) -> Optional[int]:
        """Handles missingness for INRACE"""
        return self.__handle_newinf_gate('inrace')

    def _missingness_inrasec(self) -> Optional[int]:
        """Handles missingness for INRASEC"""
        return self.__handle_newinf_gate('inrasec')

    def _missingness_inrater(self) -> Optional[int]:
        """Handles missingness for INRATER"""
        return self.__handle_newinf_gate('inrater')

    def _missingness_ineduc(self) -> Optional[int]:
        """Handles missingness for INEDUC"""
        return self.__handle_newinf_gate('ineduc')
