"""All longtitudinal MQT derived variables.

Assumes NACC-derived variables are already set
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import get_unique_years


class LongitudinalAttributeCollection(AttributeCollection):
    """Class to collect longitudinal attributes."""

    def __init__(self, table: SymbolTable):
        self.__subject_derived = SubjectDerivedNamespace(
            table=table, required=frozenset(["uds-visitdates"])
        )

    def _create_total_uds_visits(self) -> Optional[int]:
        """Total number of UDS visits."""
        return self.__subject_derived.get_count("uds-visitdates")

    def _create_years_of_uds(self) -> Optional[int]:
        """Creates subject.info.longitudinal-data.uds.year-count."""
        attribute_value = self.__subject_derived.get_value("uds-visitdates")
        if attribute_value is None:
            return None

        return len(get_unique_years(attribute_value))
