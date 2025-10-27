"""Class to handle A4-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.schema.constants import INFORMED_BLANK, INFORMED_MISSINGNESS

from .missingness_uds import UDSMissingness


class UDSFormA4Missingness(UDSMissingness):
    def _missingness_rxnorm(self) -> Optional[str]:
        """V4+. Handles missingness for all RXNORMX (1-40) values.

        If ANYMEDS ir 0 or -4, then RXNORM1-40 should be blank
        """
        if self.formver < 4:
            return INFORMED_BLANK

        if self.uds.get_value("anymeds", int) in [None, 0, -4]:
            return INFORMED_BLANK

        return None

    def _missingness_drug(self) -> Optional[str]:
        """V3 and earlier. Handles missingness for all DRUGX (1-40) values.

        If ANYMEDS ir 0 or -4, then DRUG1-40 should be blank
        """
        if self.formver >= 4:
            return INFORMED_BLANK

        if self.uds.get_value("anymeds", int) in [None, 0, -4]:
            return INFORMED_BLANK

        return None
