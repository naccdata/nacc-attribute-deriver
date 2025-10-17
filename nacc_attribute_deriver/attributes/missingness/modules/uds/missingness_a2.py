"""Class to handle A2-specific missingness values."""

from typing import Optional

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
        return self.handle_v4_blank("incntmdx")
