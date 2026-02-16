"""Class to handle B2-specific missingness values.

Only in V2, so mainly just enforcing -4 if V1.
"""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class UDSFormB2Missingness(UDSMissingness):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table=table)

        self.__formverb2 = self.uds.get_value("formverb2", int)
        if not self.__formverb2:
            self.__formverb2 = self.formver

    def __handle_b2_missingness(self, field: str) -> int:
        """Ensure anything < V2 gets set to -4."""
        if self.__formverb2 < 2:
            return INFORMED_MISSINGNESS

        return self.generic_missingness(field, int)

    def _missingness_cvdcog(self) -> int:
        """Handles missingness for CVDCOG."""
        return self.__handle_b2_missingness("cvdcog")

    def _missingness_strokcog(self) -> int:
        """Handles missingness for STROKCOG."""
        return self.__handle_b2_missingness("strokcog")

    def _missingness_cvdimag(self) -> int:
        """Handles missingness for CVDIMAG."""
        return self.__handle_b2_missingness("cvdimag")

    def __handle_cvdimag_gate(self, field: str) -> int:
        """Handles missingness for values gated by CVDIMAG."""
        if self.__formverb2 < 2:
            return INFORMED_MISSINGNESS

        if self.uds.get_value("cvdimag", int) in [0, 8]:
            return 8

        return self.generic_missingness(field, int)

    def _missingness_cvdimag1(self) -> int:
        """Handles missingness for CVDIMAG1."""
        return self.__handle_cvdimag_gate("cvdimag1")

    def _missingness_cvdimag2(self) -> int:
        """Handles missingness for CVDIMAG2."""
        return self.__handle_cvdimag_gate("cvdimag2")

    def _missingness_cvdimag3(self) -> int:
        """Handles missingness for CVDIMAG3."""
        return self.__handle_cvdimag_gate("cvdimag3")

    def _missingness_cvdimag4(self) -> int:
        """Handles missingness for CVDIMAG4."""
        return self.__handle_cvdimag_gate("cvdimag4")
