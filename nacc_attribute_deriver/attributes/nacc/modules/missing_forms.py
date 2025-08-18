"""Handles when other forms do not exist so their NACC derived variables are
not "set", but that "unset" value is something other than -4/None."""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class MissingFormAttributes(AttributeCollection):
    """Class to handle derived variables dependent on optional/missing
    forms."""

    def __init__(self, table: SymbolTable):
        self.__derived = SubjectDerivedNamespace(table=table)

    def handle_missing(self, attribute: str, default: int) -> Optional[int]:
        """Handle missing values."""
        value = self.__derived.get_cross_sectional_value(attribute, str)
        if value is None:
            return default

        # we could return the value itself, that also works, but in this
        # context returning None means "don't replace what's already there"
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

    def _create_uds_ngdsgwas(self) -> Optional[int]:
        """Handles NGDSGWAS (from NIAGADS)."""
        return self.handle_missing("ngdsgwas", 0)

    def _create_uds_ngdsexom(self) -> Optional[int]:
        """Handles NGDSEXOM (from NIAGADS)."""
        return self.handle_missing("ngdsexom", 0)

    def _create_uds_ngdswgs(self) -> Optional[int]:
        """Handles NGDSWGS (from NIAGADS)."""
        return self.handle_missing("ngdswgs", 0)

    def _create_uds_ngdswes(self) -> Optional[int]:
        """Handles NGDSWES (from NIAGADS)."""
        return self.handle_missing("ngdswes", 0)

    def _create_uds_ngdsgwac(self) -> Optional[int]:
        """Handles NGDSGWAC (from NIAGADS)"""
        return self.handle_missing("ngdsgwac", 88)

    def _create_uds_ngdsexac(self) -> Optional[int]:
        """Handles NGDSEXAC (from NIAGADS)."""
        return self.handle_missing("ngdsexac", 88)

    def _create_uds_ngdswgac(self) -> Optional[int]:
        """Handles NGDSWGAC (from NIAGADS)."""
        return self.handle_missing("ngdswgac", 88)

    def _create_uds_ngdsweac(self) -> Optional[int]:
        """Handles NGDSWEAC (from NIAGADS)."""
        return self.handle_missing("ngdsweac", 88)

    def _create_uds_naccapoe(self) -> Optional[int]:
        """Handles NACCAPOE (from NCRAD)."""
        return self.handle_missing("naccapoe", 9)

    def _create_uds_naccne4s(self) -> Optional[int]:
        """Handles NACCNE4S (from NCRAD)."""
        return self.handle_missing("naccne4s", 9)

    def _create_uds_naccftd(self) -> Optional[int]:
        """Handles NACCFTD (from FTLD)."""
        return self.handle_missing("naccftd", 0)

    def _create_uds_nacclbdm(self) -> Optional[int]:
        """Handles NACCLBDM (from LBD)."""
        return self.handle_missing("nacclbdm", 0)
