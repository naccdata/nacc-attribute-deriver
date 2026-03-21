"""Class to handle BDS missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T


class BDSFormMissingness(FormMissingnessCollection):
    def _missingness_bds(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for BDS form variables."""
        return self.generic_missingness(field, attr_type)
