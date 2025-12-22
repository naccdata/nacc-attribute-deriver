"""Class to handle CSF missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T


class CSFMissingness(SubjectMissingnessCollection):
    """Class to handle CSF missingness values."""

    def _missingness_naccacsf(self) -> int:
        """Handles NACCACSF."""
        return self.handle_subject_missing("naccacsf", int, 0)

    def _missingness_naccpcsf(self) -> int:
        """Handles NACCPCSF."""
        return self.handle_subject_missing("naccpcsf", int, 0)

    def _missingness_nacctcsf(self) -> int:
        """Handles NACCTCSF."""
        return self.handle_subject_missing("nacctcsf", int, 0)


class CSFFormMissingness(FormMissingnessCollection):
    """
    TODO: THIS IS ONLY REQUIRED TO BACKFILL WRITE-IN/KNOWN BLANK VARIABLES TO AVOID
    THE NOT-IN-CONTAINER ERROR. REMOVE ONCE FEATURE IS ADDED TO ETL GEAR.
    """

    def _missingness_csf(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for CLS form variables."""
        return self.generic_missingness(field, attr_type)

    def _missingness_csf_adcid(self) -> int:
        """Handles missingness for CSF ADCID."""
        return self.generic_missingness("adcid", int)
