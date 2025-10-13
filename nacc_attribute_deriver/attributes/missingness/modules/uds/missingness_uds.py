"""Class to handle UDS missingness variables.

In general, returns -4 unless otherwise specified.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSMissingness(AttributeCollection):
    """Class to handle UDS missingness values."""

    def __init__(self, table: SymbolTable):
        # TODO - may or may not be the actual form data depending on
        # where this is run, so namespace may change
        self.__uds = UDSNamespace(table)

    @property
    def uds(self) -> UDSNamespace:
        return self.__uds

    def _missingness_uds(self, field: str) -> Optional[int]:
        """Defines missingness for UDS; -4 if missing."""
        if self.uds.get_value(field, str) is None:
            return INFORMED_MISSINGNESS

        return None
