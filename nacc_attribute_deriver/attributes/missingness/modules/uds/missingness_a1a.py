"""Class to handle A1a-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness


class UDSFormA1aMissingness(UDSMissingness):
    def __handle_a1a_missingness(self, field: str) -> Optional[int]:
        """Handle A1a missingness; basically need to set the default to 0 for
        all of these."""
        return self.generic_missingness(field, int, default=0)

    def _missingness_expancest(self) -> Optional[int]:
        """Handles missingness for EXPANCEST."""
        return self.__handle_a1a_missingness("expancest")

    def _missingness_expgender(self) -> Optional[int]:
        """Handles missingness for EXPGENDER."""
        return self.__handle_a1a_missingness("expgender")

    def _missingness_exprace(self) -> Optional[int]:
        """Handles missingness for EXPRACE."""
        return self.__handle_a1a_missingness("exprace")

    def _missingness_expage(self) -> Optional[int]:
        """Handles missingness for EXPAGE."""
        return self.__handle_a1a_missingness("expage")

    def _missingness_exprelig(self) -> Optional[int]:
        """Handles missingness for EXPRELIG."""
        return self.__handle_a1a_missingness("exprelig")

    def _missingness_expheight(self) -> Optional[int]:
        """Handles missingness for EXPHEIGHT."""
        return self.__handle_a1a_missingness("expheight")

    def _missingness_expweight(self) -> Optional[int]:
        """Handles missingness for EXPWEIGHT."""
        return self.__handle_a1a_missingness("expweight")

    def _missingness_expappear(self) -> Optional[int]:
        """Handles missingness for EXPAPPEAR."""
        return self.__handle_a1a_missingness("expappear")

    def _missingness_expsexorn(self) -> Optional[int]:
        """Handles missingness for EXPSEXORN."""
        return self.__handle_a1a_missingness("expsexorn")

    def _missingness_expeducinc(self) -> Optional[int]:
        """Handles missingness for EXPEDUCINC."""
        return self.__handle_a1a_missingness("expeducinc")

    def _missingness_expdisab(self) -> Optional[int]:
        """Handles missingness for EXPDISAB."""
        return self.__handle_a1a_missingness("expdisab")

    def _missingness_expskin(self) -> Optional[int]:
        """Handles missingness for EXPSKIN."""
        return self.__handle_a1a_missingness("expskin")

    def _missingness_expother(self) -> Optional[int]:
        """Handles missingness for EXPOTHER."""
        return self.__handle_a1a_missingness("expother")

    def _missingness_expnotapp(self) -> Optional[int]:
        """Handles missingness for EXPNOTAPP."""
        return self.__handle_a1a_missingness("expnotapp")

    def _missingness_expnoans(self) -> Optional[int]:
        """Handles missingness for EXPNOANS."""
        return self.__handle_a1a_missingness("expnoans")

    def _missingness_expstrs(self) -> Optional[int]:
        """Handles missingness for EXPSTRS."""
        expnotapp = self.uds.get_value("expnotapp", int)
        expstrs = self.uds.get_value("expstrs", int)

        if expnotapp == 1 and expstrs is None:
            return 5

        return None
