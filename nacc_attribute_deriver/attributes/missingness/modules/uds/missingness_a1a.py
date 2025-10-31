"""Class to handle A1a-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

from .missingness_uds import UDSMissingness


class UDSFormA1aMissingness(UDSMissingness):
    def _handle_a1a_missingness(self, field: str) -> Optional[int]:
        """A1a missingness logic:

        If FORMVER=4 and VAR is blank, VAR should = 0
        else if FORMVER < 4, VAR should be -4
        """
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        result = self.uds.get_value(field, int)
        if result is not None:
            return None

        return 0

    def _missingness_expancest(self) -> Optional[int]:
        """Handles missingness for EXPANCEST."""
        return self._handle_a1a_missingness("expancest")

    def _missingness_expgender(self) -> Optional[int]:
        """Handles missingness for EXPGENDER."""
        return self._handle_a1a_missingness("expgender")

    def _missingness_exprace(self) -> Optional[int]:
        """Handles missingness for EXPRACE."""
        return self._handle_a1a_missingness("exprace")

    def _missingness_expage(self) -> Optional[int]:
        """Handles missingness for EXPAGE."""
        return self._handle_a1a_missingness("expage")

    def _missingness_exprelig(self) -> Optional[int]:
        """Handles missingness for EXPRELIG."""
        return self._handle_a1a_missingness("exprelig")

    def _missingness_expheight(self) -> Optional[int]:
        """Handles missingness for EXPHEIGHT."""
        return self._handle_a1a_missingness("expheight")

    def _missingness_expweight(self) -> Optional[int]:
        """Handles missingness for EXPWEIGHT."""
        return self._handle_a1a_missingness("expweight")

    def _missingness_expappear(self) -> Optional[int]:
        """Handles missingness for EXPAPPEAR."""
        return self._handle_a1a_missingness("expappear")

    def _missingness_expsexorn(self) -> Optional[int]:
        """Handles missingness for EXPSEXORN."""
        return self._handle_a1a_missingness("expsexorn")

    def _missingness_expeducinc(self) -> Optional[int]:
        """Handles missingness for EXPEDUCINC."""
        return self._handle_a1a_missingness("expeducinc")

    def _missingness_expdisab(self) -> Optional[int]:
        """Handles missingness for EXPDISAB."""
        return self._handle_a1a_missingness("expdisab")

    def _missingness_expskin(self) -> Optional[int]:
        """Handles missingness for EXPSKIN."""
        return self._handle_a1a_missingness("expskin")

    def _missingness_expother(self) -> Optional[int]:
        """Handles missingness for EXPOTHER."""
        return self._handle_a1a_missingness("expother")

    def _missingness_expnotapp(self) -> Optional[int]:
        """Handles missingness for EXPNOTAPP."""
        return self._handle_a1a_missingness("expnotapp")

    def _missingness_expnoans(self) -> Optional[int]:
        """Handles missingness for EXPNOANS."""
        return self._handle_a1a_missingness("expnoans")

    def _missingness_expstrs(self) -> Optional[int]:
        """Handles missingness for EXPSTRS."""
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        expnotapp = self.uds.get_value("expnotapp", int)
        expstrs = self.uds.get_value("expstrs", int)

        if expnotapp == 1 and expstrs is None:
            return 5

        return None
