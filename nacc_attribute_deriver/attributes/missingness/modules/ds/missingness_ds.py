"""Class to handle DS missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T


class DSFormMissingness(FormMissingnessCollection):
    def _missingness_ds(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for DS form variables."""
        return self.generic_missingness(field, attr_type)
