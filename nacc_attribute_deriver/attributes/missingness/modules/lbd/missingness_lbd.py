"""Class to handle LBD missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T


class LBDMissingness(SubjectMissingnessCollection):
    """Class to handle LBD missingness values."""

    def _missingness_nacclbdm(self) -> int:
        """Handles NACCLBDM."""
        return self.handle_subject_missing("nacclbdm", int, 0)


class LBDFormMissingness(FormMissingnessCollection):
    """
    TODO: THIS IS ONLY REQUIRED TO BACKFILL WRITE-IN/KNOWN BLANK VARIABLES TO AVOID
    THE NOT-IN-CONTAINER ERROR. REMOVE ONCE FEATURE IS ADDED TO ETL GEAR.
    """

    def _missingness_lbd(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for LBD form variables."""
        return self.generic_missingness(field, attr_type)
