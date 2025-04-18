"""Class to define UDS-specific attributes."""

from datetime import date, datetime
from typing import Any, Optional

from nacc_attribute_deriver.attributes.base.namespace import (
    FormNamespace,
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSNamespace(FormNamespace):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is a UDS form."""
        super().__init__(table)

        module = self.get_value("module")
        if not module or module.upper() != "UDS":
            raise MissingRequiredError("Current file is not an UDS form")

        self.__subject_derived = SubjectDerivedNamespace(table)

    def is_followup(self) -> bool:
        """Returns whether or not this is a follow-up form."""
        return self.get_value("packet") == "F"

    def normalized_formver(self) -> int:
        """Returns the normalized form version. Handles cases where the
        form version is listed as 3.2 for example."""
        try:
            formver = int(float(self.get_value("formver")))
        except (ValueError, TypeError) as e:
            raise MissingRequiredError("Current file does not have a numerical formver")

        return formver

    def check_default(self, attribute: str, default: Optional[Any] = None) -> Any:
        """Check for the default by:

            1. If a follow-up packet and result is None/777, check
                subject.info.derived.<attribute>
            2. If still None, then return the specified default

        NOTE: The 777 will often NOT be attached to the derived attribute,
            but one of the sources it looks at. It's here to cover the case,
            but in general it is expected a 777 value should fall to the
            default case that calls this method for that specific rule.

        Args:
            attribute: the target attribute name
            default: the default value
        Returns:
            the value for the attribute in the table
        """
        if not self.is_followup():
            return default

        result = self.get_value(attribute)
        if result in [None, 777, "777"]:
            result = self.__subject_derived.get_value(attribute, None)

        return default if result is None else result

    def generate_uds_dob(self) -> Optional[date]:
        """Creates UDS DOB, which is used to calculate ages."""
        birthmo = self.get_value("birthmo")
        birthyr = self.get_value("birthyr")
        formdate = self.get_value("visitdate")

        if None in [birthmo, birthyr, formdate]:
            return None

        return datetime(int(birthyr), int(birthmo), 1).date()
