"""All longtitudinal MQT derived variables.

Assumes NACC-derived variables are already set
"""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.base_attribute import (
    SubjectDerivedAttribute,
    SubjectInfoAttribute,
)
from nacc_attribute_deriver.attributes.nacc.modules.uds.uds_attribute import (
    UDSAttribute,
)
from nacc_attribute_deriver.utils.date import get_unique_years


class LongitudinalAttributeCollection(AttributeCollection):
    """Class to collect longitudinal attributes."""

    def __init__(self, table):
        self.__uds = UDSAttribute(table)
        self.__subject_derived = SubjectDerivedAttribute(table)
        self.__subject_info = SubjectInfoAttribute(table)

    def _create_total_uds_visits(self) -> int:
        """Total number of UDS visits.

        This is an accumulative variable, assumes its called for each
        form
        """
        count = self.__subject_info.get_value(
            "longitudinal-data.uds.count.latest.value", 0
        )
        module = self.__uds.get_value("module")

        if module and module.lower() == "uds":
            count += 1

        return count

    def _create_years_of_uds(self) -> int:
        """Creates subject.info.longitudinal-data.uds.year-count."""
        result = self.__subject_derived.assert_required(["uds-visitdates"])
        return len(get_unique_years(result["uds-visitdates"]))
