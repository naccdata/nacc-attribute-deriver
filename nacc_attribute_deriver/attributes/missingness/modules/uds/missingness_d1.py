"""Class to handle D1-specific missingness values.

These are variables that only exist in V3 and earlier for D1; others
will now be found in either D1a or D1b.
"""

from typing import Optional

from .missingness_uds import UDSMissingness


class UDSFormD1Missingness(UDSMissingness):
    ######################
    # Write-in variables #
    ######################

    def _missingness_othbiomx(self) -> Optional[str]:
        """Handles missingness for OTHBIOMX."""
        return self.generic_writein("othbiomx")

    def _missingness_othmutx(self) -> Optional[str]:
        """Handles missingness for OTHMUTX."""
        return self.generic_writein("othmutx")
