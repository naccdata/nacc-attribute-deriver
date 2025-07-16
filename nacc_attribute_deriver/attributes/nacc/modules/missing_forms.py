"""
Handles when other forms do not exist so their
NACC derived variables are not "set", but that "unset"
value is something other than -4/None.
"""
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class MissingFormAttributes(AttributeCollection):
    """Class to handle derived variables dependent on optional/missing forms."""

    def __init__(self, table: SymbolTable):
        self.__derived = SubjectDerivedNamespace(table=table)

    def _create_uds_naccnrdy(self) -> Optional[int]:
        """Handles NACCNRDY (from Milestones)."""
        if not self.__derived.get_cross_sectional_value("naccnrdy", int):
            return 88

        return None

    def _create_uds_naccnrmo(self) -> Optional[int]:
        """Handles NACCNRMO (from Milestones)."""
        if not self.__derived.get_cross_sectional_value("naccnrmo", int):
            return 88

        return None

    def _create_uds_naccnryr(self) -> Optional[int]:
        """Handles NACCNRYR (from Milestones)."""
        if not self.__derived.get_cross_sectional_value("naccnyr", int):
            return 8888

        return None

