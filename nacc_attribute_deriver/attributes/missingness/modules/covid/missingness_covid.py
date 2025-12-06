"""Class to handle COVID missingness values.

TODO: THIS IS ONLY REQUIRED TO BACKFILL WRITE-IN/KNOWN BLANK VARIABLES TO AVOID
THE NOT-IN-CONTAINER ERROR. REMOVE ONCE FEATURE IS ADDED TO ETL GEAR.
"""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class CovidFormMissingness(FormMissingnessCollection):
    def _missingness_covid_f1(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for COVID F1 form variables."""
        return self.generic_missingness(field, attr_type)

    def _missingness_covid_f2f3(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for COVID F2/F3 form variables."""
        return self.generic_missingness(field, attr_type)

    def _missingness_c19test(self) -> int:
        """C19TEST in V1 but C19TESTED in V2. This missingness logic
        requires F2/F3 Covid forms do need info.resolved.

        TODO: NEED TO ASK RT ABOUT HARMONIZATION SINCE ACCEPTED VALUES
            DIFFER BETWEEN VERSIONS, DO NOT MAP TOGETHER
        """
        c19test = self.form.get_value("c19test", int)
        if c19test is not None:
            return c19test

        c19tested = self.form.get_value("c19tested", int)
        if c19tested is not None:
            return c19tested

        return INFORMED_MISSINGNESS
