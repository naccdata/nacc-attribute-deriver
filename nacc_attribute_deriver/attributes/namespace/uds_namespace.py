"""Class to define UDS-specific attributes."""

from datetime import date, datetime

from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)


class UDSNamespace(FormNamespace):
    def __init__(
        self,
        table: SymbolTable,
        required: frozenset[str] = frozenset(),
        date_attribute: str | None = "visitdate",
    ) -> None:
        """UDS form namespace."""
        super().__init__(
            table=table,
            required=required.union(
                {
                    "module",
                    "packet",
                    "formver",
                    "birthmo",
                    "birthyr",
                    "naccid",
                    "adcid",
                }
            ),
            date_attribute=date_attribute,
        )

        # ensure this is an UDS form
        module = self.get_required("module", str)
        if module.upper() != "UDS":
            raise InvalidFieldError(
                f"Current file is not an UDS form: found {module}",
            )

        self.__working = WorkingNamespace(table=table)

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

        Grab from subject.info.working.cross-sectional.birthmo/birthyr
        which is assumed to be the latest DOB. This is to account
        for the fact that sometimes these values change over the
        visits. Because many things rely on DOB, we pre-compute
        this to get the latest. But if not found, default to
        the file's metadata.
        """
        birthmo = self.__working.get_cross_sectional_value(
            "birthmo", int, default=self.get_required("birthmo", int)
        )
        birthyr = self.__working.get_cross_sectional_value(
            "birthyr", int, default=self.get_required("birthyr", int)
        )

        if not birthmo or not birthyr:
            raise AttributeDeriverError(
                "Cannot determine UDS DOB: missing BIRTHMO and/or BIRTHYR"
            )

        # No birth day provided, so default to 1.
        return datetime(birthyr, birthmo, 1).date()
