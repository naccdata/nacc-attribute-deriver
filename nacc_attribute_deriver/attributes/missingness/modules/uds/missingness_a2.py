"""Class to handle A2-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.schema.constants import (
    INFORMED_MISSINGNESS,
)

from .missingness_uds import UDSMissingness


class UDSFormA2Missingness(UDSMissingness):
    def _missingness_incntmod(self) -> Optional[int]:
        """Handles missingness for INCNTMOD.

        If INLIVWTH=1 then INCNTMOD=8
        """
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        inlivwth = self.uds.get_value("inlivwth", int)
        if inlivwth == 1:
            return 8

        return None

    def _missingness_incnttim(self) -> Optional[int]:
        """Handles missingness for INCNTTIM.

        If INLIVWTH=1 then INCNTTIM=8
        """
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        inlivwth = self.uds.get_value("inlivwth", int)
        if inlivwth == 1:
            return 8

        return None

    def _missingness_incntmdx(self) -> Optional[str]:
        """Handles missingness for INCNTMDX.

        If INCNTMDX is blank then INCNTMDX should remain blank
        """
        return self.handle_v4_blank("incntmdx")
