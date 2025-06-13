"""Derived variables from form A2: Co-participant Demographics.

From a2structrdd.sas
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from .helpers.generate_race import generate_race


class UDSFormA2Attribute(AttributeCollection):
    """Class to collect UDS A2 attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)

    def _create_naccninr(self) -> Optional[int]:
        """Creates NACCNINR (co-participant race) if first form or NEWINF (new
        co-participant)."""
        newinf = self.__uds.get_value("newinf", int)
        if not self.__uds.is_initial() and newinf != 1:
            return None

        result = generate_race(
            race=self.__uds.get_value("inrace", int),
            racex=self.__uds.get_value("inracex", str),
            racesec=self.__uds.get_value("inracesec", int),
            racesecx=self.__uds.get_value("inracesecx", str),
            raceter=self.__uds.get_value("inraceter", int),
            raceterx=self.__uds.get_value("inraceterx", str),
        )

        return result
