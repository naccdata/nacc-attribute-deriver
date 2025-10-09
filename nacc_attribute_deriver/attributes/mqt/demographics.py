"""All demographic MQT derived variables.

Assumes NACC-derived variables are already set
"""

import datetime
from types import MappingProxyType
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.schema.errors import (
    InvalidFieldError,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class DemographicsAttributeCollection(AttributeCollection):
    """Class to collect demographic attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table, required=frozenset(["sex"]))

    def get_date(self) -> Optional[datetime.date]:
        return self.__uds.get_date()

    SEX_MAPPING = MappingProxyType(
        {1: "Male", 2: "Female", 8: "Prefer not to answer", 9: "Don't know"}
    )

    def _create_uds_sex(self) -> str:
        """UDS sex.

        Always required.
        """
        sex = self.__uds.get_required("sex", int)
        mapped_sex = self.SEX_MAPPING.get(sex)

        if not mapped_sex:
            raise InvalidFieldError(f"Invalid/unknown sex code: {sex}")

        return mapped_sex

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

    def _create_uds_primary_language(self) -> Optional[str]:
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

        return mapped_primlang


class DerivedDemographicsAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table=table)
        self.__subject_derived = SubjectDerivedNamespace(
            table=table,
            required=frozenset(
                [f"cross-sectional.{x}" for x in ["naccnihr", "naccdied"]]
            ),
        )

    def get_date(self) -> Optional[datetime.date]:
        return self.__uds.get_date()

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

    def _create_uds_race(self) -> str:
        """UDS race."""
        naccnihr = self.__subject_derived.get_cross_sectional_value("naccnihr", int)
        mapped_naccnihr = self.RACE_MAPPING.get(naccnihr)  # type: ignore

        if not mapped_naccnihr:
            raise InvalidFieldError(f"Invalid/unknown naccnihr code: {naccnihr}")

        return mapped_naccnihr

    VITAL_STATUS_MAPPINGS = MappingProxyType({0: "unknown", 1: "deceased"})

    def _create_vital_status(self) -> str:
        """Creates subject.info.demographics.uds.vital-status.latest."""
        naccdied = self.__subject_derived.get_cross_sectional_value("naccdied", int)
        mapped_naccdied = self.VITAL_STATUS_MAPPINGS.get(naccdied)  # type: ignore

        if not mapped_naccdied:
            raise InvalidFieldError(f"Invalid/unknown naccdied code: {naccdied}")

        return mapped_naccdied
