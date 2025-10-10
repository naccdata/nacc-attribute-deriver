"""Class to handle B5-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.schema.constants import INFORMED_BLANK

from .missingness_uds import UDSMissingness


class UDSFormB5Missingness(UDSMissingness):
    def _missingness_npiqinfx(self) -> Optional[str]:
        """Handle missingness for NPIQINF."""
        if self.uds.get_value("npiqinf", int) != 3:
            return INFORMED_BLANK

        return None
