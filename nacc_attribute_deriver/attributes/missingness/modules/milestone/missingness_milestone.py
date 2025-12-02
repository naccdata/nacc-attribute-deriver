"""Class to handle Milestone form missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T


class MilestoneMissingness(FormMissingnessCollection):
    def _missingness_milestone(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for Milestone form variables."""
        return self.generic_missingness(field, attr_type)


class MilestoneSubjectMissingness(SubjectMissingnessCollection):
    """Class to handle Milestone missingness values at the subject level."""

    def _missingness_naccnrdy(self) -> int:
        """Handles NACCNRDY."""
        return self.handle_subject_missing("naccnrdy", int, 88)

    def _missingness_naccnrmo(self) -> int:
        """Handles NACCNRMO."""
        return self.handle_subject_missing("naccnrmo", int, 88)

    def _missingness_naccnryr(self) -> int:
        """Handles NACCNRYR."""
        return self.handle_subject_missing("naccnryr", int, 8888)
