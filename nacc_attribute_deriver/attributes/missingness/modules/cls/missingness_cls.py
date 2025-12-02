"""Class to handle CLS missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class CLSMissingness(SubjectMissingnessCollection):
    """Class to handle CLS missingness values."""

    def _missingness_naccengl(self) -> int:
        """Handles NACCENGL."""
        return self.handle_subject_missing("naccengl", int, INFORMED_MISSINGNESS)

    def _missingness_naccspnl(self) -> int:
        """Handles NACCSPNL."""
        return self.handle_subject_missing("naccspnl", int, INFORMED_MISSINGNESS)


class CLSFormMissingness(FormMissingnessCollection):
    """
    TODO: THIS IS ONLY REQUIRED TO BACKFILL WRITE-IN/KNOWN BLANK VARIABLES TO AVOID
    THE NOT-IN-CONTAINER ERROR. REMOVE ONCE FEATURE IS ADDED TO ETL GEAR.

    CLS additionally doesn't even have write-ins/blanks, so is even more unnecessary,
    but for now keep for consistency.
    """

    def _missingness_cls(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for CLS form variables."""
        return self.generic_missingness(field, attr_type)
