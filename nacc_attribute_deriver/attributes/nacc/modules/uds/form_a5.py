"""Derived variables from form A5: Subject Health History.

From a5structrdd.sas.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormA45ttribute(AttributeCollection):
    """Class to collect UDS A5 attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)

    def _create_naccstyr(self) -> Optional[int]:
        """Creates NACCSTYR - Most recently reported year of stroke
        as of the initial visit.
        """

    def _create_nacctbi(self) -> Optional[int]:
        """Creates NACCTBI - History of traumatic brain injury (TBI)."""

    def _create_nacctiyr(self) -> Optional[int]:
        """Creates NACCTIYR - Most recently reported year of TIA as of the Initial Visit."""
