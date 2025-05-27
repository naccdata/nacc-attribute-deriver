"""All demographic MQT derived variables.

Assumes NACC-derived variables are already set
"""

from types import MappingProxyType
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    DateTaggedValue,
    DerivedNamespace,
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable


class DemographicsAttributeCollection(AttributeCollection):
    """Class to collect demographic attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)

    SEX_MAPPING = MappingProxyType(
        {1: "Male", 2: "Female", 8: "Prefer not to answer", 9: "Don't know"}
    )

    def _create_uds_sex(self) -> Optional[DateTaggedValue[str]]:
        """UDS sex."""
        attribute_value = self.__uds.get_dated_value("sex")
        if attribute_value is None:
            return None

        try:
            attribute_value.value = self.SEX_MAPPING.get(int(attribute_value.value))
        except ValueError as error:
            raise InvalidFieldError("sex must be an integer") from error

        return attribute_value

    PRIMARY_LANGUAGE_MAPPING = MappingProxyType(
        {
            1: "English",
            2: "Spanish",
            3: "Mandarin",
            4: "Cantonese",
            5: "Russian",
            6: "Japanese",
            8: "Other",
            9: "Unknown",
        }
    )

    def _create_uds_primary_language(self) -> Optional[DateTaggedValue[str]]:
        """UDS primary language.

        Only for initial forms.
        """
        if not self.__uds.is_initial():
            return None

        attribute_value = self.__uds.get_dated_value("primlang")
        if not attribute_value:
            return None

        try:
            attribute_value.value = self.PRIMARY_LANGUAGE_MAPPING.get(
                int(attribute_value.value), "Unknown"
            )
        except ValueError as e:
            raise InvalidFieldError("primlang must be an integer") from e

        return attribute_value

    def _create_uds_education_level(self) -> Optional[DateTaggedValue[int]]:
        """UDS education level."""
        attribute_value = self.__uds.get_dated_value("educ", None)
        if not attribute_value:
            return None

        try:
            attribute_value.value = int(attribute_value.value)
        except ValueError as error:
            raise InvalidFieldError("educ must be an integer") from error

        return attribute_value


class DerivedDemographicsAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)
        self.__derived = DerivedNamespace(table)
        self.__subject_derived = SubjectDerivedNamespace(table)

    def _create_uds_age(self) -> Optional[DateTaggedValue[int]]:
        """UDS age at form date, mapped from NACCAGE."""
        return self.__derived.scope(fields=["naccage"]).create_dated_value(
            attribute="naccage", date=self.__uds.get_date()
        )

    RACE_MAPPING = MappingProxyType(
        {
            1: "White",
            2: "Black or African American",
            3: "American Indian or Alaska Native",
            4: "Native Hawaiian or Other Pacific Islander",
            5: "Asian",
            6: "Multiracial",
            7: "Middle Eastern or Northern African",
            8: "Hispanic or Latino",  # TODO for UDSv4?
            99: "Unknown or ambiguous",
        }
    )

    def _create_uds_race(self) -> Optional[DateTaggedValue[str]]:
        """UDS race."""
        attribute_value = self.__derived.scope(fields=["naccnihr"]).create_dated_value(
            attribute="naccnihr", date=self.__uds.get_date()
        )
        if attribute_value is None:
            return None

        attribute_value.value = self.RACE_MAPPING.get(
            attribute_value.value, "Unknown or ambiguous"
        )

        return attribute_value

    def _create_age_at_death(self) -> Optional[int]:
        """Age at death, mapped from NACCDAGE."""
        return self.__derived.scope(fields=["naccdage"]).get_value("naccdage")

    VITAL_STATUS_MAPPINGS = MappingProxyType({0: "unknown", 1: "deceased"})

    def _create_vital_status(self) -> Optional[DateTaggedValue[str]]:
        """Creates subject.info.demographics.uds.vital-status.latest."""
        attribute_value = self.__derived.scope(fields=["naccdied"]).create_dated_value(
            attribute="naccdied", date=self.__uds.get_date()
        )
        if attribute_value is None:
            return None

        attribute_value.value = self.VITAL_STATUS_MAPPINGS.get(
            attribute_value.value, "unknown"
        )
        return attribute_value

    def _create_np_available(self) -> bool:
        """NP available, which is just checking for the existence of
        np_death_age."""
        return self.__subject_derived.get_value("np_death_age") is not None
