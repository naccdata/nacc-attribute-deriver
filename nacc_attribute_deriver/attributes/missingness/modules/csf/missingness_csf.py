"""Class to handle CSF missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
)


class CSFMissingness(SubjectMissingnessCollection):
    """Class to handle CSF missingness values."""

    def _missingness_naccacsf(self) -> Optional[int]:
        """Handles NACCACSF."""
        return self.handle_subject_missing("naccacsf", 0)

    def _missingness_naccpcsf(self) -> Optional[int]:
        """Handles NACCPCSF."""
        return self.handle_subject_missing("naccpcsf", 0)

    def _missingness_nacctcsf(self) -> Optional[int]:
        """Handles NACCTCSF."""
        return self.handle_subject_missing("nacctcsf", 0)
