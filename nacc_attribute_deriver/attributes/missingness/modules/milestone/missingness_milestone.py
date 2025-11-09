"""Class to handle Milestone form missingness values."""

from typing import Optional, Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T


class MilestoneMissingness(FormMissingnessCollection):
    def _missingness_milestone(self, field: str, attr_type: Type[T]) -> Optional[T]:
        """Defines general missingness for Milestone form variables."""
        return self.generic_missingness(field, attr_type)


class MilestoneSubjectMissingness(SubjectMissingnessCollection):
    """Class to handle Milestone missingness values at the subject level."""

    def _missingness_naccnrdy(self) -> Optional[int]:
        """Handles NACCNRDY."""
        return self.handle_subject_missing("naccnrdy", 88)

    def _missingness_naccnrmo(self) -> Optional[int]:
        """Handles NACCNRMO."""
        return self.handle_subject_missing("naccnrmo", 88)

    def _missingness_naccnryr(self) -> Optional[int]:
        """Handles NACCNRYR."""
        return self.handle_subject_missing("naccnryr", 8888)
