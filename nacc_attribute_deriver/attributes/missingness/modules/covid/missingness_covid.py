"""Class to handle COVID missingness values.

TODO: THIS IS ONLY REQUIRED TO BACKFILL WRITE-IN/KNOWN BLANK VARIABLES TO AVOID
THE NOT-IN-CONTAINER ERROR. REMOVE ONCE FEATURE IS ADDED TO ETL GEAR.
"""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T


class CovidFormMissingness(FormMissingnessCollection):
    def _missingness_covid(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for COVID F1 and F2/F3 form
        variables."""
        return self.generic_missingness(field, attr_type)
