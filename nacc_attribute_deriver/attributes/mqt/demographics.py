"""All demographic MQT derived variables.

Assumes NACC-derived variables are already set
"""

from types import MappingProxyType
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.base_attribute import (
    AttributeValue,
    DerivedNamespace,
)
from nacc_attribute_deriver.attributes.nacc.modules.uds.uds_attribute import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class DemographicsAttributeCollection(AttributeCollection):
    """Class to collect demographic attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)

    SEX_MAPPING = MappingProxyType(
        {1: "Male", 2: "Female", 8: "Prefer not to answer", 9: "Don't know"}
    )

    def _create_uds_sex(self) -> Optional[AttributeValue]:
        """UDS sex."""
        sex = self.__uds.get_value("sex")
        if sex is None:
            return None

        try:
            return AttributeValue(
                value=self.SEX_MAPPING.get(int(sex), None), date=self.__uds.get_date()
            )
        except TypeError:
            return None

    PRIMARY_LANGUAGE_MAPPING = MappingProxyType(
        {
            1: "English",
            2: "Spanish",
            3: "Mandarin",
            4: "Cantonese",
            5: "Russian",
            6: "Japanese",
            8: "Other primary language (specify)",
            9: "Unknown",
        }
    )

    def _create_uds_primary_language(self) -> AttributeValue:
        """UDS primary language."""
        primlang = self.__uds.get_value("primlang", 9)
        return AttributeValue(
            value=self.PRIMARY_LANGUAGE_MAPPING.get(primlang, "Unknown"),
            date=self.__uds.get_date(),
        )

    def _create_uds_education_level(self) -> AttributeValue:
        """UDS education level."""
        return self.__uds.get_dated_value("educ", None)


class DerivedDemographicsAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)
        self.__derived = DerivedNamespace(table)

    def _create_uds_age(self) -> AttributeValue:
        """UDS age at form date, mapped from NACCAGE."""
        self.__derived.assert_required(["naccage"])
        return AttributeValue(
            value=self.__derived.get_value("naccage"), date=self.__uds.get_date()
        )

    RACE_MAPPING = MappingProxyType(
        {
            1: "White",
            2: "Black or African American",
            3: "American Indian or Alaska Native",
            4: "Native Hawaiian or Pacific Islander",
            5: "Asian",
            6: "Multiracial",
            7: "Middle Eastern or Northern African",
            8: "Hispanic or Latino",  # TODO for UDSv4?
            99: "Unknown or ambiguous",
        }
    )

    def _create_uds_race(self) -> AttributeValue:
        """UDS race."""
        self.__derived.assert_required(["naccnihr"])
        return AttributeValue(
            value=self.RACE_MAPPING.get(
                self.__derived.get_value("naccnihr"), "Unknown or ambiguous"
            ),
            date=self.__uds.get_date(),
        )

    def _create_age_at_death(self) -> int:
        """Age at death, mapped from NACCDAGE."""
        self.__derived.assert_required(["naccdage"])
        return self.__derived.get_value("naccdage")

    VITAL_STATUS_MAPPINGS = MappingProxyType({0: "Not deceased/unknown", 1: "Deceased"})

    def _create_vital_status(self) -> AttributeValue:
        """Creates subject.info.demographics.uds.vital-status.latest."""
        self.__derived.assert_required(["naccdied"])
        return AttributeValue(
            value=self.VITAL_STATUS_MAPPINGS.get(
                self.__derived.get_value("naccdied"), "Unknown"
            ),
            date=self.__uds.get_date(),
        )
