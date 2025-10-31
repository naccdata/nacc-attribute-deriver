"""Class to handle NP form missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)


class NPMissingness(FormMissingnessCollection):
    """Class to handle NP missingness values."""

    def _missingness_np(self, field: str) -> Optional[int]:
        """Defines general missingness for NP; -4 if missing."""
        return self.generic_missingness(field)
