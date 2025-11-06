"""Class to handle MP missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
)


class MPMissingness(SubjectMissingnessCollection):
    """Class to handle MP missingness values."""

    def _missingness_naccmrsa(self) -> Optional[int]:
        """Handles NACCMRSA."""
        return self.handle_subject_missing("naccmrsa", 0)

    def _missingness_naccnmri(self) -> Optional[int]:
        """Handles NACCNMRI."""
        return self.handle_subject_missing("naccnmri", 88)

    def _missingness_naccapsa(self) -> Optional[int]:
        """Handles NACCAPSA."""
        return self.handle_subject_missing("naccapsa", 0)

    def _missingness_naccnapa(self) -> Optional[int]:
        """Handles NACCNAPA."""
        return self.handle_subject_missing("naccnapa", 88)
