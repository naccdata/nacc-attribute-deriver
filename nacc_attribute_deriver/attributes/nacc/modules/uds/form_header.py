"""Derived variables that come from the header variables."""
from typing import Optional

from nacc_attribute_deriver.utils.date import datetime_from_form_date

from .uds_attribute import UDSAttribute


class UDSHeaderAttribute(UDSAttribute):
    """Class to collect UDS header attributes."""

    def _create_uds_year(self) -> Optional[int]:
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
