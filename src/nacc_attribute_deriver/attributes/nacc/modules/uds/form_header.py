"""
Derived variables that come from the header variables.
"""
from .uds_attribute import UDSAttribute


class UDSHeaderAttribute(UDSAttribute):
    """Class to collect UDS header attributes."""

    def _create_uds_visitdate(self) -> int:
        """Gets visitdate

        Location:
            subject.info.derived.initial_uds_visit
            subject.info.derived.latest_uds_visit
        Event:
            initial
            latest
        Type:
            longitudinal
        Description:
            Date of UDS visit
        """
        return self.get_value('visitdate')
