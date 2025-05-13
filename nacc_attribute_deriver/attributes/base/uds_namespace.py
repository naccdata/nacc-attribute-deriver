"""Class to define UDS-specific attributes."""

from datetime import date, datetime
from typing import Optional

from nacc_attribute_deriver.attributes.base.namespace import FormNamespace
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSNamespace(FormNamespace):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is a UDS form."""
        super().__init__(table)

        module = self.get_value("module")
        if not module or module.upper() != "UDS":
            raise InvalidFieldError(
                field="module",
                expected="uds",
                value=module,
                message=f"Current file is not an UDS form: found {module}",
            )

    def is_initial(self) -> bool:
        """Returns whether or not this is an initial packet."""
        packet = self.get_value("packet")
        if packet is not None:
            return str(packet).startswith("I")

        return False

    def normalized_formver(self) -> int:
        """Returns the normalized form version.

        Handles cases where the form version is listed as 3.2 for
        example.
        """
        try:
            raw_formver = self.get_value("formver")
            formver = int(float(raw_formver))
        except (ValueError, TypeError) as e:
            msg = f"Current file does not have a numerical formver: {raw_formver}"
            raise InvalidFieldError(
                field="formver",
                expected="numerical formver",
                value="raw_formver",
                message=msg,
            ) from e

        return formver

    def generate_uds_dob(self) -> Optional[date]:
        """Creates UDS DOB, which is used to calculate ages."""
        birthmo = self.get_value("birthmo")
        birthyr = self.get_value("birthyr")
        formdate = self.get_value("visitdate")

        if None in [birthmo, birthyr, formdate]:
            return None

        return datetime(int(birthyr), int(birthmo), 1).date()
