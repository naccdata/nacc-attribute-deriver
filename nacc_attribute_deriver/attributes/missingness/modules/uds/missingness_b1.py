"""Class to handle B1-specific missingness values.

Only in V3 and earlier.
"""

from typing import Optional

from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)

from .missingness_uds import UDSMissingness


class UDSFormB1Missingness(UDSMissingness):

    def _missingness_viswcorr(self) -> Optional[int]:
        """Handles missingness for VISWCORR.

        Only in V3 and earlier - see b1structrdd.sas
        """
        if self.formver >= 4:
            return INFORMED_MISSINGNESS

        viscorr = self.uds.get_value("viscorr", int)
        if viscorr == 0:
            return 8
        if viscorr == 9:
            return INFORMED_MISSINGNESS

        return None

    def _missingness_hearwaid(self) -> Optional[int]:
        """Handles missingness for HEARWAID.

        Only in V3 and earlier - see b1structrdd.sas
        """
        if self.formver >= 4:
            return INFORMED_MISSINGNESS

        hearaid = self.uds.get_value("hearaid", int)
        if hearaid == 0:
            return 8
        if hearaid == 9:
            return INFORMED_MISSINGNESS

        return None
