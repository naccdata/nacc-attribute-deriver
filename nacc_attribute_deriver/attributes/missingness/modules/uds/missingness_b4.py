"""Class to handle B4-specific missingness values.

Really just handles making floats -4.0 instead ofo -4.4
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class UDSFormB4Missingness(UDSMissingness):
    def __handle_b4_float(self, field: str) -> Optional[float]:
        return self.generic_missingness(field, float, default=INFORMED_MISSINGNESS)

    def _missingness_memory(self) -> Optional[float]:
        """Handles missingness for MEMORY."""
        return self.__handle_b4_float("memory")

    def _missingness_orient(self) -> Optional[float]:
        """Handles missingness for ORIENT."""
        return self.__handle_b4_float("orient")

    def _missingness_judgment(self) -> Optional[float]:
        """Handles missingness for JUDGMENT."""
        return self.__handle_b4_float("judgment")

    def _missingness_commun(self) -> Optional[float]:
        """Handles missingness for COMMUN."""
        return self.__handle_b4_float("commun")

    def _missingness_homehobb(self) -> Optional[float]:
        """Handles missingness for HOMEHOBB."""
        return self.__handle_b4_float("homehobb")

    def _missingness_perscare(self) -> Optional[float]:
        """Handles missingness for PERSCARE."""
        return self.__handle_b4_float("perscare")

    def _missingness_cdrsum(self) -> Optional[float]:
        """Handles missingness for CDRSUM."""
        return self.__handle_b4_float("cdrsum")

    def _missingness_cdrglob(self) -> Optional[float]:
        """Handles missingness for CDRGLOB."""
        return self.__handle_b4_float("cdrglob")

    def _missingness_comport(self) -> Optional[float]:
        """Handles missingness for COMPORT."""
        return self.__handle_b4_float("comport")

    def _missingness_cdrlang(self) -> Optional[float]:
        """Handles missingness for CDRLANG."""
        return self.__handle_b4_float("cdrlang")
