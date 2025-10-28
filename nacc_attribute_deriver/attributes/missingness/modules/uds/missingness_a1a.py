"""Class to handle A1a-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS

from .missingness_uds import VersionedUDSMissingness


class UDSFormA1aMissingness(VersionedUDSMissingness):
    def _missingness_expancest(self) -> Optional[int]:
        """Handles missingness for EXPANCEST."""
        return self.handle_formver_missingness("expancest")

    def _missingness_expgender(self) -> Optional[int]:
        """Handles missingness for EXPGENDER."""
        return self.handle_formver_missingness("expgender")

    def _missingness_exprace(self) -> Optional[int]:
        """Handles missingness for EXPRACE."""
        return self.handle_formver_missingness("exprace")

    def _missingness_expage(self) -> Optional[int]:
        """Handles missingness for EXPAGE."""
        return self.handle_formver_missingness("expage")

    def _missingness_exprelig(self) -> Optional[int]:
        """Handles missingness for EXPRELIG."""
        return self.handle_formver_missingness("exprelig")

    def _missingness_expheight(self) -> Optional[int]:
        """Handles missingness for EXPHEIGHT."""
        return self.handle_formver_missingness("expheight")

    def _missingness_expweight(self) -> Optional[int]:
        """Handles missingness for EXPWEIGHT."""
        return self.handle_formver_missingness("expweight")

    def _missingness_expappear(self) -> Optional[int]:
        """Handles missingness for EXPAPPEAR."""
        return self.handle_formver_missingness("expappear")

    def _missingness_expsexorn(self) -> Optional[int]:
        """Handles missingness for EXPSEXORN."""
        return self.handle_formver_missingness("expsexorn")

    def _missingness_expeducinc(self) -> Optional[int]:
        """Handles missingness for EXPEDUCINC."""
        return self.handle_formver_missingness("expeducinc")

    def _missingness_expdisab(self) -> Optional[int]:
        """Handles missingness for EXPDISAB."""
        return self.handle_formver_missingness("expdisab")

    def _missingness_expskin(self) -> Optional[int]:
        """Handles missingness for EXPSKIN."""
        return self.handle_formver_missingness("expskin")

    def _missingness_expother(self) -> Optional[int]:
        """Handles missingness for EXPOTHER."""
        return self.handle_formver_missingness("expother")

    def _missingness_expnotapp(self) -> Optional[int]:
        """Handles missingness for EXPNOTAPP."""
        return self.handle_formver_missingness("expnotapp")

    def _missingness_expnoans(self) -> Optional[int]:
        """Handles missingness for EXPNOANS."""
        return self.handle_formver_missingness("expnoans")

    def _missingness_expstrs(self) -> Optional[int]:
        """Handles missingness for EXPSTRS."""
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        expnotapp = self.uds.get_value("expnotapp", int)
        expstrs = self.uds.get_value("expstrs", int)

        if expnotapp == 1 and expstrs is None:
            return 5

        return None
