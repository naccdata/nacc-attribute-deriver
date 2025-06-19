"""All demographic MQT derived variables.

Assumes NACC-derived variables are already set
"""

from types import MappingProxyType
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    DateTaggedValue,
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.schema.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class DemographicsAttributeCollection(AttributeCollection):
    """Class to collect demographic attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table, required=frozenset(["sex"]))

    SEX_MAPPING = MappingProxyType(
        {1: "Male", 2: "Female", 8: "Prefer not to answer", 9: "Don't know"}
    )

    def _create_uds_sex(self) -> DateTaggedValue[str]:
        """UDS sex.

        Always required.
        """
        sex = self.__uds.get_required("sex", int)
        mapped_sex = self.SEX_MAPPING.get(sex)

        if not mapped_sex:
            raise InvalidFieldError(f"Invalid/unknown sex code: {sex}")

        return DateTaggedValue(value=mapped_sex, date=self.__uds.get_date())

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

        primlang = self.__uds.get_value("primlang", int)
        mapped_primlang = (
            self.PRIMARY_LANGUAGE_MAPPING.get(primlang) if primlang else None
        )

        if not mapped_primlang:
            raise InvalidFieldError(f"Invalid/unknown primlang code: {primlang}")

        return DateTaggedValue(
            value=mapped_primlang,
            date=self.__uds.get_date(),
        )

    def _create_uds_education_level(self) -> Optional[DateTaggedValue[int]]:
        """UDS education level."""
        educ = self.__uds.get_value("educ", int)
        if not educ:
            return None

        return DateTaggedValue(
            value=educ,
            date=self.__uds.get_date(),
        )


class DerivedDemographicsAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table=table)
        self.__subject_derived = SubjectDerivedNamespace(
            table=table,
            required=frozenset(
                [f"cross-sectional.{x}" for x in ["naccnihr", "naccdage", "naccdied"]]
                + [f"longitudinal.{x}" for x in ["naccage"]]
            ),
        )

    def _create_uds_age(self) -> DateTaggedValue[int]:
        """UDS age at form date, mapped from NACCAGE."""
        ages = self.__subject_derived.get_longitudinal_value(
            "naccage", list, required=True
        )

        # grab latest age, which should correspond to this visit
        # TODO - should update to use dated list from other PR
        if not ages:
            raise AttributeDeriverError("Cannot determine age for current visit")

        return DateTaggedValue(
            value=ages[-1],
            date=self.__uds.get_date(),
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

    def _create_uds_race(self) -> DateTaggedValue[str]:
        """UDS race."""
        naccnihr = self.__subject_derived.get_cross_sectional_value(
            "naccnihr", int, required=True
        )
        mapped_naccnihr = self.RACE_MAPPING.get(naccnihr)

        if not mapped_naccnihr:
            raise InvalidFieldError(f"Invalid/unknown naccnihr code: {naccnihr}")

        return DateTaggedValue(value=mapped_naccnihr, date=self.__uds.get_date())

    def _create_age_at_death(self) -> int:
        """Age at death, mapped from NACCDAGE."""
        return self.__subject_derived.get_cross_sectional_value(
            "naccdage", int, required=True
        )

    VITAL_STATUS_MAPPINGS = MappingProxyType({0: "unknown", 1: "deceased"})

    def _create_vital_status(self) -> DateTaggedValue[str]:
        """Creates subject.info.demographics.uds.vital-status.latest."""
        naccdied = self.__subject_derived.get_cross_sectional_value(
            "naccdied", int, required=True
        )
        mapped_naccdied = self.VITAL_STATUS_MAPPINGS.get(naccdied)

        if not mapped_naccdied:
            raise InvalidFieldError(f"Invalid/unknown naccdied code: {naccdied}")

        return DateTaggedValue(value=mapped_naccdied, date=self.__uds.get_date())

    def _create_np_available(self) -> bool:
        """NP available, which is just checking for the existence of
        np_death_age."""
        return self.__subject_derived.get_value("np_death_age", str) is not None
