"""Derived variables that come from the header variables."""
from .uds_attribute import UDSAttribute
from nacc_attribute_deriver.utils.date import datetime_from_form_date


class UDSHeaderAttribute(UDSAttribute):
    """Class to collect UDS header attributes."""

    def _create_uds_year(self) -> int:
        """Gets the year of the visitdate.

        Location:
            subject.info.derived.uds_years
        Operation:
            set
        Type:
            longitudinal
        Description:
            Year of UDS visit
        """
        formdate = datetime_from_form_date(self.get_value('visitdate'))
        return formdate.year if formdate else None
