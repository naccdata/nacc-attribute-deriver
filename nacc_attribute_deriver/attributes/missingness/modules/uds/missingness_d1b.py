"""Class to handle D1b-specific missingness values."""

from typing import Optional

from .missingness_uds import UDSMissingness


class UDSFormD1bMissingness(UDSMissingness):
    ######################
    # Write-in variables #
    ######################

    def _missingness_ftldsubx(self) -> Optional[str]:
        """Handles missingness for FTLDSUBX."""
        return self.generic_writein("ftldsubx")

    def _missingness_othcogx(self) -> Optional[str]:
        """Handles missingness for OTHCOGX."""
        return self.generic_writein("othcogx")
