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
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
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
        if not self.submitted or self.formver == 4:
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

    def _create_naccincntfq(self) -> int:
        """Creates NACCINCNTFQ - frequency of contact."""
        if not self.submitted:
            return INFORMED_MISSINGNESS

        if self.formver == 4:
            inlivwth = self.uds.get_value('inlivwth', int)
            if inlivwth is None:
                raise AttributeDeriverError(
                    "INLIVWTH required if A2 submitted")

            if inlivwth == 1:
                return 8

            # if INLIVWTH == 0 then INCNTFRQ must be defined
            # so if it is missing then throw an error
            incntfrq = self.uds.get_value('incntfrq', int)
            if incntfrq is None:
                raise AttributeDeriverError(
                    "If INLIVWTH == 0, INCNTFRQ must be present")
            return incntfrq

        # V3 and earlier
        invisits = self.uds.get_value('invisits', int)
        incalls = self.uds.get_value('incalls', int)
        if invisits is not None and incalls is not None:
            return min(invisits, incalls)
