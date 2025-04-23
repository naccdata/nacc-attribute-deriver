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

    def is_initial(self) -> bool:
        """Returns whether or not this is an initial packet."""
        return self.get_value("packet") in ["I", "I4"]

    def normalized_formver(self) -> int:
        """Returns the normalized form version.

        Handles cases where the form version is listed as 3.2 for
        example.
        """
        try:
            formver = int(float(self.get_value("formver")))
        except (ValueError, TypeError) as e:
            raise MissingRequiredError(
                "Current file does not have a numerical formver"
            ) from e

        return formver

    def get_cross_sectional_value(self, attribute: str, default: Optional[Any] = None) -> Any:
        """Returns a cross-sectional value.

        Args:
          key: the attribute name
          default: the default value
        Returns:
          the value for the attribute in the table
        """
        return self.__subject_derived.get_value(f'cross-sectional.{attribute}', default)

    def get_longitudinal_value(self, attribute: str, default: Optional[Any] = None) -> Any:
        """Returns a longitudinal value.

        Args:
          key: the attribute name
          default: the default value
        Returns:
          the value for the attribute in the table
        """
        return self.__subject_derived.get_value(f'longitudinal.{attribute}', default)

    def generate_uds_dob(self) -> Optional[date]:
        """Creates UDS DOB, which is used to calculate ages."""
        birthmo = self.get_value("birthmo")
        birthyr = self.get_value("birthyr")
        formdate = self.get_value("visitdate")

        if None in [birthmo, birthyr, formdate]:
            return None

        return datetime(int(birthyr), int(birthmo), 1).date()
