"""Derived variables from form A2: Co-participant Demographics.

Form A2 is optional, so may not have been submitted. From
a2structrdd.sas
"""

from typing import Optional

from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable

from .helpers.generate_race import generate_race
from .uds_attribute_collection import UDSAttributeCollection


class UDSFormA2Attribute(UDSAttributeCollection):
    """Class to collect UDS A2 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

    @property
    def submitted(self) -> bool:
        return self.uds.get_value("a2sub", int) == 1

    def _create_naccninr(self) -> Optional[int]:
        """Creates NACCNINR (co-participant race) if first form or NEWINF (new
        co-participant)."""
        # grab prev if available
        prev_naccninr = self.__subject_derived.get_prev_value("naccninr", int)

        newinf = self.uds.get_value("newinf", int)
        if newinf != 1 or not self.submitted:
            return prev_naccninr

        result = generate_race(
            race=self.uds.get_value("inrace", int),
            racex=self.uds.get_value("inracex", str),
            racesec=self.uds.get_value("inrasec", int),
            racesecx=self.uds.get_value("inrasecx", str),
            raceter=self.uds.get_value("inrater", int),
            raceterx=self.uds.get_value("inraterx", str),
        )

        return result
