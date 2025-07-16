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

    def handle_missing(self, attribute: str, default: int) -> Optional[int]:
        """Handle missing values."""
        if not self.__derived.get_cross_sectional_value(attribute, str):
            return default

        return None

    def _create_uds_naccnrdy(self) -> Optional[int]:
        """Handles NACCNRDY (from Milestones)."""
        return self.handle_missing("naccnrdy", 88)

    def _create_uds_naccnrmo(self) -> Optional[int]:
        """Handles NACCNRMO (from Milestones)."""
        return self.handle_missing("naccnrmo", 88)

    def _create_uds_naccnryr(self) -> Optional[int]:
        """Handles NACCNRYR (from Milestones)."""
        return self.handle_missing("naccnyr", 8888)

    def _create_uds_ngdsgwas(self) -> int:
        """Handles NGDSGWAS (from NIAGADS)."""
        return self.handle_missing("ngdsgwas", 0)

    def _create_uds_ngdsexom(self) -> int:
        """Handles NGDSEXOM (from NIAGADS)."""
        return self.handle_missing("ngdsexom", 0)

    def _create_uds_ngdswgs(self) -> int:
        """Handles NGDSWGS (from NIAGADS)."""
        return self.handle_missing("ngdswgs", 0)

    def _create_uds_ngdswes(self) -> int:
        """Handles NGDSWES (from NIAGADS)."""
        return self.handle_missing("ngdswes", 0)

    def _create_uds_ngdsgwac(self) -> str:
        """Handles NGDSGWAC (from NIAGADS)"""
        return self.handle_missing("ngdsgwac", 88)

    def _create_uds_ngdsexac(self) -> str:
        """Handles NGDSEXAC (from NIAGADS)."""
        return self.handle_missing("ngdsexac", 88)

    def _create_uds_ngdswgac(self) -> str:
        """Handles NGDSWGAC (from NIAGADS)."""
        return self.handle_missing("ngdswgac", 88)

    def _create_uds_ngdsweac(self) -> str:
        """Handles NGDSWEAC (from NIAGADS)."""
        return self.handle_missing("ngdsweac", 88)
