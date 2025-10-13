"""Derived variables from form A2: Co-participant Demographics.

Form A2 is optional, so may not have been submitted. From
a2structrdd.sas
"""

from nacc_attribute_deriver.attributes.collection.uds_attribute import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.symbol_table import SymbolTable

from .helpers.generate_race import generate_race


class UDSFormA2Attribute(UDSAttributeCollection):
    """Class to collect UDS A2 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

    @property
    def submitted(self) -> bool:
        return self.uds.get_value("a2sub", int) == 1

    def _create_naccninr(self) -> int:
        """Creates NACCNINR (co-participant race) if first form or NEWINF (new
        co-participant).

        NOTE: After discussing with RT, we want to return whatever is on the current
        form and don't carry forward. If not specified, return -4.
        """
        if not self.submitted:
            return INFORMED_MISSINGNESS

        newinf = self.uds.get_value("newinf", int)
        if not self.uds.is_initial() and newinf != 1:
            return INFORMED_MISSINGNESS

        result = generate_race(
            race=self.uds.get_value("inrace", int),
            racex=self.uds.get_value("inracex", str),
            racesec=self.uds.get_value("inrasec", int),
            racesecx=self.uds.get_value("inrasecx", str),
            raceter=self.uds.get_value("inrater", int),
            raceterx=self.uds.get_value("inraterx", str),
        )

        return result
