"""Class to define UDS-specific attributes."""

from datetime import datetime
from typing import Optional

from nacc_attribute_deriver.attributes.base.base_attribute import NACCAttribute
from nacc_attribute_deriver.schema.errors import MissingRequiredException


class UDSAttribute(NACCAttribute):
    def __init__(self, *args, **kwargs) -> None:
        """Check that this is an UDS form."""
        super().__init__(*args, **kwargs)

        module = self.get_value("module")
        if not module or module.upper() != "UDS":
            raise MissingRequiredException("Current file is not an UDS form")

    def generate_uds_dob(self) -> Optional[datetime]:
        """Creates UDS DOB, which is used to calculate ages."""
        birthmo = self.get_value("birthmo")
        birthyr = self.get_value("birthyr")
        formdate = self.get_value("visitdate")

        if None in [birthmo, birthyr, formdate]:
            return None

        return datetime(int(birthyr), int(birthmo), 1)
