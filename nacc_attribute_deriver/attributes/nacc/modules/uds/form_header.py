"""Derived variables that come from the header variables."""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import datetime_from_form_date


class UDSHeaderAttributeCollection(AttributeCollection):
    """Class to collect UDS header attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)

    def _create_uds_visitdates(self) -> str:
        """Gets the visitdate - temporary derived variable."""
        raw_visitdate = self.__uds.get_required("visitdate", str)
        visitdate = datetime_from_form_date(raw_visitdate)

        if not visitdate:
            raise InvalidFieldError(
                f"Failed to parse visitdate: {raw_visitdate}"
            )

        return str(visitdate.date())
