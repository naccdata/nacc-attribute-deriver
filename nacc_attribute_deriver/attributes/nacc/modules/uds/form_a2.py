"""Derived variables from form A2: Co-participant Demographics."""

from typing import Optional

from .helpers.generate_race import generate_race
from .uds_attribute_collection import UDSAttributeCollection


class UDSFormA2Attribute(UDSAttributeCollection):
    """Class to collect UDS A2 attributes."""

    def _create_naccninr(self) -> Optional[int]:
        """Creates NACCNINR (co-participant race) if first form or NEWINF (new
        co-participant)."""
        newinf = self.uds.get_value("newinf", int)
        if not self.uds.is_initial() and newinf != 1:
            return None

        result = generate_race(
            race=self.uds.get_value("inrace", int),
            racex=self.uds.get_value("inracex", str),
            racesec=self.uds.get_value("inracesec", int),
            racesecx=self.uds.get_value("inracesecx", str),
            raceter=self.uds.get_value("inraceter", int),
            raceterx=self.uds.get_value("inraceterx", str),
        )

        return result
