"""Class to define UDS-specific attributes."""

from datetime import date, datetime
from typing import Optional

from nacc_attribute_deriver.attributes.base.namespace import FormNamespace
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSNamespace(FormNamespace):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is a UDS form."""
        super().__init__(table)

        module = self.get_value("module")
        if not module or module.upper() != "UDS":
            raise MissingRequiredError("Current file is not an UDS form")

    def generate_uds_dob(self) -> Optional[date]:
        """Creates UDS DOB, which is used to calculate ages."""
        birthmo = self.get_value("birthmo")
        birthyr = self.get_value("birthyr")
        formdate = self.get_value("visitdate")

        if None in [birthmo, birthyr, formdate]:
            return None

        return datetime(int(birthyr), int(birthmo), 1).date()
