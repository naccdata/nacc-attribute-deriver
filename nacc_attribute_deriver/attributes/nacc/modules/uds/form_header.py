"""Derived variables that come from the header variables."""

from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.utils.date import datetime_from_form_date

from .uds_attribute_collection import UDSAttributeCollection


class UDSHeaderAttributeCollection(UDSAttributeCollection):
    """Class to collect UDS header attributes."""

    def _create_uds_visitdates(self) -> str:
        """Gets the visitdate - temporary derived variable."""
        raw_visitdate = self.uds.get_required("visitdate", str)
        visitdate = datetime_from_form_date(raw_visitdate)

        if not visitdate:
            raise InvalidFieldError(f"Failed to parse visitdate: {raw_visitdate}")

        return str(visitdate.date())
