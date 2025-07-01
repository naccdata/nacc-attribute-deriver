"""All longtitudinal MQT derived variables.

Assumes NACC-derived variables are already set
"""
from typing import Any, List
from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import get_unique_years


class LongitudinalAttributeCollection(AttributeCollection):
    """Class to collect longitudinal attributes."""

    def __init__(self, table: SymbolTable):
        self.__working_derived = WorkingDerivedNamespace(
            table=table, required=frozenset(["cross-sectional.uds-visitdates"])
        )

    def get_visitdates(self) -> List[Any]:
        """Get UDS visits."""
        visitdates: list[Any] | None = self.__working_derived.get_cross_sectional_value(
            "uds-visitdates", list
        )
        if not visitdates:
            return []

        return visitdates

    def _create_total_uds_visits(self) -> int:
        """Total number of UDS visits."""
        return len(self.get_visitdates())

    def _create_years_of_uds(self) -> int:
        """Creates subject.info.longitudinal-data.uds.year-count."""
        return len(get_unique_years(self.get_visitdates()))
