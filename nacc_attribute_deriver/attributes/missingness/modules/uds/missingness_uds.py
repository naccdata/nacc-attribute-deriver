"""Class to handle UDS missingness variables.

In general, returns -4 unless otherwise specified.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_attribute import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.schema.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)


class UDSMissingness(UDSAttributeCollection):
    """Class to handle UDS missingness values."""

    def handle_v4_missingness(
        self, field: str, missing_value: int = 0
    ) -> Optional[int]:
        """Handles generic V4 missingness, which follows the logic:

        If FORMVER=4 and VAR is blank, VAR should = VALUE
        else if FORMVER < 4, VAR should be -4

        Args:
            field: The field to check and set missingness for
            missing_value: The value to set if the field is missing;
                defaults to 0
        Returns:
            Missingness value if missing, None otherwise (so it isn't
            set)
        """
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        # if value exists, return None so we don't override
        value = self.uds.get_value(field, int)
        if value is not None:
            return None

        return missing_value

    def handle_v4_blank(self, field: str) -> Optional[str]:
        """Handles generic V4 blank missingness, which follows the logic:

        If FORMVER < 4 or VAR is blank, VAR should remain blank
        """
        if self.formver < 4:
            return INFORMED_BLANK

        # if value exists, return None so we don't override
        value = self.uds.get_value(field, str)
        if value is not None:
            return None

        return INFORMED_BLANK

    def _missingness_uds(self, field: str) -> Optional[int]:
        """Defines general missingness for UDS; -4 if missing."""
        if self.uds.get_value(field, str) is None:
            return INFORMED_MISSINGNESS

        return None

    def generic_missingness(self, field: str) -> Optional[int]:
        """Generic missingness for internal calls."""
        return self._missingness_uds(field)
