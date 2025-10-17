"""Class to handle B6-specific missingness values."""

from typing import Optional

from .missingness_uds import UDSMissingness


class UDSFormB6Missingness(UDSMissingness):
    def _missingness_nogds(self) -> Optional[int]:
        """Handle missingness for NOGDS."""
        if self.uds.get_value("nogds", int) is None:
            return 0

        return None
