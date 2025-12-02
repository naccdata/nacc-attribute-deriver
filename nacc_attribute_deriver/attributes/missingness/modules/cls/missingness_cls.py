"""Class to handle CLS missingness values."""

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class CLSMissingness(SubjectMissingnessCollection):
    """Class to handle CLS missingness values."""

    def _missingness_naccengl(self) -> int:
        """Handles NACCENGL."""
        return self.handle_subject_missing("naccengl", int, INFORMED_MISSINGNESS)

    def _missingness_naccspnl(self) -> int:
        """Handles NACCSPNL."""
        return self.handle_subject_missing("naccspnl", int, INFORMED_MISSINGNESS)
