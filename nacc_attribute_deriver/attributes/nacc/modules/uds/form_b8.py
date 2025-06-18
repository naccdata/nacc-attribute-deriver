"""Derived variables from form B8: Neurological Examination Findings.

Form B8 is required and expected to have been filled out.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormB8Attribute(AttributeCollection):
    """Class to collect UDS B8 attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)
        self.__formver = self.__uds.normalized_formver()

    def _create_naccnrex(self) -> Optional[int]:
        """Creates NACCNREX, were all findings unremarkable?
        """
        normal = self.__uds.get_value('normal', int)
        normexam = self.__uds.get_value('normexam', int)

        if normal == 1 or normexam in [0, 2]:
            return 1
        if normal == 0 or normexam == 1:
            return 0
        if normal == 9:
            return 9

        return None
