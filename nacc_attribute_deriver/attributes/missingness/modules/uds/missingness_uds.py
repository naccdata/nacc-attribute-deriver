"""Class to handle UDS missingness variables.

In general, returns -4 unless otherwise specified.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_attribute import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSMissingness(UDSAttributeCollection):
    """Class to handle UDS missingness values."""

    def handle_v4_missingness(self, field: str) -> Optional[int]:
        """Handles V4 missingness, which in many cases follows the logic:

        If FORMVER=4 and VAR is blank, VAR should = 0
        else if FORMVER < 4, VAR should be -4
        """
        # if value exists, return None so we don't override
        value = self.uds.get_value(field, str)
        if value is not None:
            return None

        if self.formver == 4:
            return 0

        return INFORMED_MISSINGNESS

    def _missingness_uds(self, field: str) -> Optional[int]:
        """Defines general missingness for UDS; -4 if missing."""
        if self.uds.get_value(field, str) is None:
            return INFORMED_MISSINGNESS

        return None
