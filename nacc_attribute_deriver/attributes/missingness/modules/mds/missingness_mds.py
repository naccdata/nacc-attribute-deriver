"""Class to handle MDS form missingness values."""

from typing import Optional, Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T


class MDSMissingness(FormMissingnessCollection):
    """Class to handle MDS missingness values at the file-level."""

    def _missingness_mds(self, field: str, attr_type: Type[T]) -> Optional[T]:
        """Defines general missingness for MDS."""
        return self.generic_missingness(field, attr_type)
