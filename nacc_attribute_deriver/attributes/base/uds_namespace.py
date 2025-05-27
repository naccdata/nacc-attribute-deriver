"""Class to define UDS-specific attributes."""

from datetime import date, datetime
from typing import Iterable, Optional

from nacc_attribute_deriver.attributes.base.namespace import (
    FormNamespace,
    NamespaceScope,
    ScopeDefinitionError,
)
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSNamespace(FormNamespace):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is a UDS form."""
        super().__init__(table)

        module = self.get_value("module")
        if not module or module.upper() != "UDS":
            raise InvalidFieldError(
                f"Current file is not an UDS form: found {module}",
            )

    def is_initial(self) -> bool:
        """Returns whether or not this is an initial packet."""
        packet = self.get_value("packet")
        if packet is not None:
            return str(packet).startswith("I")

        return False

    def scope(
        self,
        *,
        name: Optional[str] = None,
        fields: Optional[Iterable[str]] = None,
    ) -> NamespaceScope:
        if not fields:
            raise ScopeDefinitionError("Unable to define UDS scope")
        return super().scope(name="uds", fields=fields)

    def normalized_formver(self) -> Optional[int]:
        """Returns the normalized form version.

        Handles cases where the form version is listed as 3.2 for
        example.
        """
        attribute_value = self.scope(fields=["formver"]).get_value("formver")
        if attribute_value is None:
            return None

        try:
            return int(float(attribute_value))
        except (ValueError, TypeError) as e:
            msg = f"Current file does not have a numerical formver: {attribute_value}"
            raise InvalidFieldError(msg) from e

    def generate_uds_dob(self) -> Optional[date]:
        """Creates UDS DOB, which is used to calculate ages."""
        birthmo = self.get_value("birthmo")
        birthyr = self.get_value("birthyr")
        formdate = self.get_value("visitdate")

        if birthmo is None:
            return None
        if birthyr is None:
            return None
        if formdate is None:
            return None

        return datetime(int(birthyr), int(birthmo), 1).date()
