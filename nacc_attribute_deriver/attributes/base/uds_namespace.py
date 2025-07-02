"""Class to define UDS-specific attributes."""

from datetime import date, datetime
from typing import Optional

from nacc_attribute_deriver.attributes.base.namespace import FormNamespace
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSNamespace(FormNamespace):
    def __init__(
        self, table: SymbolTable, required: Optional[frozenset[str]] = None
    ) -> None:
        """Check that this is a UDS form."""
        if required is None:
            required = frozenset()

        default_required = ["module", "packet", "formver", "birthmo", "birthyr"]
        super().__init__(
            table=table,
            required=required.union(default_required),
            date_attribute="visitdate",
        )

        module = self.get_required("module", str)
        if module.upper() != "UDS":
            raise InvalidFieldError(
                f"Current file is not an UDS form: found {module}",
            )

    def is_initial(self) -> bool:
        """Returns whether or not this is an initial packet."""
        packet = self.get_required("packet", str)
        return packet.startswith("I")

    def is_in_person(self) -> bool:
        """Returns whethher or not this is an in-person visit."""
        packet = self.get_required("packet", str)
        return packet in ["I", "F"]

    def normalized_formver(self) -> int:
        """Returns the normalized form version.

        Handles cases where the form version is listed as 3.2 for
        example.
        """
        raw_formver = self.get_required("formver", float)

        try:
            return int(raw_formver)
        except (ValueError, TypeError) as e:
            raise InvalidFieldError(
                f"Cannot determine normalized formver: {raw_formver}"
            ) from e

    def generate_uds_dob(self) -> date:
        """Creates UDS DOB, which is used to calculate ages."""
        birthmo = self.get_required("birthmo", int)
        birthyr = self.get_required("birthyr", int)

        return datetime(birthyr, birthmo, 1).date()
