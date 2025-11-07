"""Class to handle B1-specific missingness values.

Only in V3 and earlier.
"""

from typing import Optional

from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
    INFORMED_MISSINGNESS_FLOAT,
)

from .missingness_uds import UDSMissingness


class UDSFormB1Missingness(UDSMissingness):
    def _missingness_viswcorr(self) -> Optional[int]:
        """Handles missingness for VISWCORR.

        Only in V3 and earlier - see b1structrdd.sas
        """
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
        hearaid = self.uds.get_value("hearaid", int)
        if hearaid == 0:
            return 8
        if hearaid == 9:
            return INFORMED_MISSINGNESS

        return None

    def _missingness_height(self) -> Optional[float]:
        """Handle missingness for HEIGHT.

        This is less of a missingness and more just resolving,
        because in early versions we may need to add the decimal.

        Min 36 UDSv3+, max is 87.9, UDSv2 and earlier max is 96.0
        """
        height = self.uds.get_value("height", float)
        if height is None:
            return INFORMED_MISSINGNESS_FLOAT

        heigdec = self.uds.get_value("heigdec", float)
        if heigdec is not None and heigdec != 0:
            height_with_dec = height + heigdec / 10
            if height != height_with_dec:
                return height_with_dec

        return None
