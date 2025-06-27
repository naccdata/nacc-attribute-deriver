"""UDS Attribute collection."""

import datetime
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
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

    @property
    def submitted(self) -> bool:
        """By default, a form is expected to have been submitted."""
        return True

    def get_date(self) -> datetime.date:
        """All UDS visits must have a visitdate."""
        visitdate = self.__uds.get_date()
        if not visitdate:
            raise AttributeDeriverError("Cannot determine visitdate for UDS visit")

        return visitdate
