"""UDS Attribute collection."""

import datetime
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSAttributeCollection(AttributeCollection):
    def __init__(
        self, table: SymbolTable, uds_required: Optional[frozenset] = None
    ) -> None:
        self.__uds = UDSNamespace(table, required=uds_required)
        self.__formver = self.uds.normalized_formver()

    @property
    def uds(self) -> UDSNamespace:
        return self.__uds

    @property
    def formver(self) -> int:
        return self.__formver

    def get_date(self) -> Optional[datetime.date]:
        return self.uds.get_date()
