"""Class to handle B2-specific missingness values.

Only in V2.
"""

from typing import Optional

from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)

from .missingness_uds import UDSMissingness


class UDSFormB2Missingness(UDSMissingness):
    def __handle_cvdimag_gate(self, field: str) -> Optional[int]:
        """Handles missingness for values gated by CVDIMG."""
        if self.formver != 2:
            return INFORMED_MISSINGNESS

        if self.uds.get_value("cvdimg", int) in [0, 8]:
            return 8

        return self.generic_missingness(field)

    def _missingness_cvdimag1(self) -> Optional[int]:
        """Handles missingness for CVDIMAG1."""
        return self.__handle_cvdimag_gate("cvdimag1")

    def _missingness_cvdimag2(self) -> Optional[int]:
        """Handles missingness for CVDIMAG2."""
        return self.__handle_cvdimag_gate("cvdimag2")

    def _missingness_cvdimag3(self) -> Optional[int]:
        """Handles missingness for CVDIMAG3."""
        return self.__handle_cvdimag_gate("cvdimag3")

    def _missingness_cvdimag4(self) -> Optional[int]:
        """Handles missingness for CVDIMAG4."""
        return self.__handle_cvdimag_gate("cvdimag4")

    def _missingness_cvdimagx(self) -> Optional[str]:
        """Handles missingness for CVDIMAGX."""
        return self.generic_writein("cvdimagx")
