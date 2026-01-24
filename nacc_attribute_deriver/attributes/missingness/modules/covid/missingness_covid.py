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
    def _missingness_covid(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for COVID F1 and F2/F3 form
        variables."""
        return self.generic_missingness(field, attr_type)

    def __fix_covid_year(self, field: str) -> int:
        """Fix improperly formatted covid years, e.g. 88 to 8888 and 99 to
        9999."""
        year = self.form.get_value(field, int)
        if not year:
            return INFORMED_MISSINGNESS

        if year == 88:
            return 8888
        if year == 99:
            return 9999

        return year

    def _missingness_c19t1yr(self) -> int:
        """Handles missingness for C19T1YR."""
        return self.__fix_covid_year("c19t1yr")

    def _missingness_c19t2yr(self) -> int:
        """Handles missingness for C19T2YR."""
        return self.__fix_covid_year("c19t2yr")

    def _missingness_c19t3yr(self) -> int:
        """Handles missingness for C19T3YR."""
        return self.__fix_covid_year("c19t3yr")
