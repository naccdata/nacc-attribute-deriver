"""Class to handle ADGC missingness values.

See NP missingness for NEURODIAG.
"""

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)


class ADGCMissingness(SubjectMissingnessCollection):
    """Class to handle ADGC missingness values."""

    def _missingness_clindiag(self) -> int:
        """Handles CLINDIAG."""
        return self.handle_subject_missing("clindiag", int, INFORMED_MISSINGNESS)

    def _missingness_incad(self) -> int:
        """Handles INCAD."""
        return self.handle_subject_missing("incad", int, INFORMED_MISSINGNESS)

    def _missingness_prevad(self) -> int:
        """Handles PREVAD."""
        return self.handle_subject_missing("prevad", int, INFORMED_MISSINGNESS)
