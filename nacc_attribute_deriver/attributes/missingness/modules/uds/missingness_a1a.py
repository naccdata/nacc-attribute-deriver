"""Class to handle A1a-specific missingness values."""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class UDSFormA1aMissingness(UDSMissingness):
    def __handle_a1a_missingness(self, field: str) -> int:
        """Handle A1a missingness; basically need to set the default to 0 for
        all of these if V4."""
        default = INFORMED_MISSINGNESS if self.formver < 4 else 0
        return self.generic_missingness(field, int, default=default)

    def _missingness_expancest(self) -> int:
        """Handles missingness for EXPANCEST."""
        return self.__handle_a1a_missingness("expancest")

    def _missingness_expgender(self) -> int:
        """Handles missingness for EXPGENDER."""
        return self.__handle_a1a_missingness("expgender")

    def _missingness_exprace(self) -> int:
        """Handles missingness for EXPRACE."""
        return self.__handle_a1a_missingness("exprace")

    def _missingness_expage(self) -> int:
        """Handles missingness for EXPAGE."""
        return self.__handle_a1a_missingness("expage")

    def _missingness_exprelig(self) -> int:
        """Handles missingness for EXPRELIG."""
        return self.__handle_a1a_missingness("exprelig")

    def _missingness_expheight(self) -> int:
        """Handles missingness for EXPHEIGHT."""
        return self.__handle_a1a_missingness("expheight")

    def _missingness_expweight(self) -> int:
        """Handles missingness for EXPWEIGHT."""
        return self.__handle_a1a_missingness("expweight")

    def _missingness_expappear(self) -> int:
        """Handles missingness for EXPAPPEAR."""
        return self.__handle_a1a_missingness("expappear")

    def _missingness_expsexorn(self) -> int:
        """Handles missingness for EXPSEXORN."""
        return self.__handle_a1a_missingness("expsexorn")

    def _missingness_expeducinc(self) -> int:
        """Handles missingness for EXPEDUCINC."""
        return self.__handle_a1a_missingness("expeducinc")

    def _missingness_expdisab(self) -> int:
        """Handles missingness for EXPDISAB."""
        return self.__handle_a1a_missingness("expdisab")

    def _missingness_expskin(self) -> int:
        """Handles missingness for EXPSKIN."""
        return self.__handle_a1a_missingness("expskin")

    def _missingness_expother(self) -> int:
        """Handles missingness for EXPOTHER."""
        return self.__handle_a1a_missingness("expother")

    def _missingness_expnotapp(self) -> int:
        """Handles missingness for EXPNOTAPP."""
        return self.__handle_a1a_missingness("expnotapp")

    def _missingness_expnoans(self) -> int:
        """Handles missingness for EXPNOANS."""
        return self.__handle_a1a_missingness("expnoans")

    def _missingness_expstrs(self) -> int:
        """Handles missingness for EXPSTRS."""
        expnotapp = self.uds.get_value("expnotapp", int)
        expstrs = self.uds.get_value("expstrs", int)

        if expnotapp == 1 and expstrs is None:
            return 5

        return self.generic_missingness("expstrs", int)
