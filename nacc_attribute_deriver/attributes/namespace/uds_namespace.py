"""Class to define UDS-specific attributes."""

from datetime import date, datetime
from typing import Optional

from nacc_attribute_deriver.attributes.namespace.namespace import FormNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import InvalidFieldError


class UDSNamespace(FormNamespace):
    def __init__(
        self, table: SymbolTable, required: frozenset[str] = frozenset()
    ) -> None:
        """UDS form namespace."""
        super().__init__(
            table=table,
            required=required.union({
                "module",
                "packet",
                "formver",
                "birthmo",
                "birthyr",
                "naccid",
                "adcid",
            }),
            date_attribute="visitdate",
        )

        # ensure this is an UDS form
        module = self.get_required("module", str)
        if module.upper() != "UDS":
            raise InvalidFieldError(
                f"Current file is not an UDS form: found {module}",
            )

    def is_initial(self) -> bool:
        """Returns whether or not this is an initial packet."""
        packet = self.get_required("packet", str)
        return packet.upper().startswith("I")

    def is_i4(self) -> bool:
        """Returns whether or not this is specifically an I4 packet."""
        packet = self.get_required("packet", str)
        return packet.upper() == "I4"

    def is_in_person(self) -> bool:
        """Returns whethher or not this is an in-person visit."""
        packet = self.get_required("packet", str)
        return packet.upper() in ["I", "F", "IT"]

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
        """Creates UDS DOB, which is used to calculate ages.

        No birth day provided, so default to 1.
        """
        birthmo = self.get_required("birthmo", int)
        birthyr = self.get_required("birthyr", int)

        return datetime(birthyr, birthmo, 1).date()
