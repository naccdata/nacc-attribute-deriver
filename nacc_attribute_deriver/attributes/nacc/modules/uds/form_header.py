"""Derived variables that come from the header variables."""
from typing import Optional

from nacc_attribute_deriver.utils.date import datetime_from_form_date

from .uds_attribute import UDSAttribute


class UDSHeaderAttribute(UDSAttribute):
    """Class to collect UDS header attributes."""

    def _create_uds_visitdate(self) -> Optional[str]:
        """Gets the visitdate - temporary derived variable.

        Location:
            subject.info.derived.uds_visitdates
        Operation:
            sortedlist
        Type:
            longitudinal
        Description:
            UDS visitdate, as a string
        """
        visitdate = datetime_from_form_date(self.get_value('visitdate'))
        return str(visitdate.date()) if visitdate else None
