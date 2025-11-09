"""UDS Attribute collection."""

import datetime
from typing import Optional, Type

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace,
    T,
)
from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)


class UDSAttributeCollection(AttributeCollection):
    def __init__(
        self, table: SymbolTable, uds_required: Optional[frozenset] = None
    ) -> None:
        self.__uds = UDSNamespace(table, required=uds_required)
        self.__formver = self.uds.normalized_formver()

        module = self.__uds.get_required("module", str)
        if module.upper() != "UDS":
            msg = f"Current file is not a UDS form: found {module}"
            raise InvalidFieldError(msg)

        self.__prev_record = None
        # prev record should exist for non-initial visits
        if not self.uds.is_initial() or self.uds.is_i4():
            self.__prev_record = PreviousRecordNamespace(table=table)

    @property
    def prev_record(self) -> Optional[PreviousRecordNamespace]:
        return self.__prev_record

    def get_propagated_value(
        self, attribute: str, attr_type: Type[T], default: Optional[T] = None
    ) -> Optional[T]:
        """Several values are only provided on IVP and need to be propogated
        through for calculations on FVP forms.

        Need to resolve from current and previous records.
        """
        if self.__uds.is_initial() or not self.__prev_record:
            return self.__uds.get_value(attribute, attr_type, default=default)

        return self.__prev_record.get_resolved_value(
            attribute, attr_type, default=default
        )

    @property
    def uds(self) -> UDSNamespace:
        return self.__uds

    @property
    def formver(self) -> int:
        return self.__formver

    @property
    def submitted(self) -> bool:
        return True

    def get_date(self) -> datetime.date:
        """All UDS visits must have a visitdate."""
        visitdate = self.__uds.get_date()
        if not visitdate:
            raise AttributeDeriverError("Cannot determine visitdate for UDS visit")

        return visitdate

    def get_prev_value(
        self,
        field: str,
        attr_type: Type[T],
        prev_code: Optional[T] = None,
        default: Optional[T] = None,
    ) -> Optional[T]:
        """Get the previous value."""
        if self.__prev_record is not None:
            return self.__prev_record.get_resolved_value(
                field, attr_type, prev_code=prev_code, default=default
            )

        return None
