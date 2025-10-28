"""Class to handle B5-specific missingness values."""

from typing import Optional

from .missingness_uds import UDSMissingness


class UDSFormB5Missingness(UDSMissingness):
    def _missingness_npiqinfx(self) -> Optional[str]:
        """Handle missingness for NPIQINF."""
        return self.handle_gated_writein("npiqinf", 3)
