"""Derived variables from form A3: Family History.

Form A3 is optional, so may not have been submitted.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormA3Attribute(AttributeCollection):
    """Class to collect UDS A2 attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)

        # TODO - for v4 this will be modea3
        self.__submitted = self.__uds.get('a3sub', int) == 1

    def _create_naccam(self) -> Optional[int]:
        """Creates NACCAM - In this family, is there evidence
        of an AD mutation?

        Only in V3+.
        """
        if not self.__submitted:
            return None

        if self.__uds.normalized_formver() < 3:
            return None

        fadmut = self.__uds.get('fadmut', int)
        if fadmut in [0, 1, 2, 3, 8]:
            return fadmut

        return 9        
