"""Class to handle UDS missingness variables.

In general, returns -4 unless otherwise specified.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_attribute_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS


class UDSMissingness(UDSAttributeCollection):
    """Class to handle UDS missingness values."""

    def _missingness_uds(self, field: str) -> Optional[int]:
        """Defines missingness for UDS; -4 if missing."""
        if self.uds.get_value(field, str) is None:
            return INFORMED_MISSINGNESS

        return None
