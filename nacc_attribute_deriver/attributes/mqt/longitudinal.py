"""All longtitudinal MQT derived variables.

Assumes NACC-derived variables are already set
"""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    SubjectDerivedNamespace,
    SubjectInfoNamespace,
)
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.utils.date import get_unique_years


class LongitudinalAttributeCollection(AttributeCollection):
    """Class to collect longitudinal attributes."""

    def __init__(self, table):
        self.__uds = UDSNamespace(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)
        self.__subject_info = SubjectInfoNamespace(table=table)

    def _create_total_uds_visits(self) -> int:
        """Total number of UDS visits."""
        self.__subject_derived.assert_required(["uds-visitdates"])
        return len(self.__subject_derived.get_value("uds-visitdates"))

    def _create_years_of_uds(self) -> int:
        """Creates subject.info.longitudinal-data.uds.year-count."""
        self.__subject_derived.assert_required(["uds-visitdates"])
        return len(get_unique_years(self.__subject_derived.get_value("uds-visitdates")))
