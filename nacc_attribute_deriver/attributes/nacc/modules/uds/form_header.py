"""Derived variables that come from the header variables."""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import datetime_from_form_date

from .uds_namespace import UDSNamespace


class UDSHeaderAttributeCollection(AttributeCollection):
    """Class to collect UDS header attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)

    def _create_uds_visitdates(self) -> Optional[str]:
        """Gets the visitdate - temporary derived variable."""
        visitdate = datetime_from_form_date(self.__uds.get_value("visitdate"))
        return str(visitdate.date()) if visitdate else None
