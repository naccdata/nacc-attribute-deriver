"""Class to handle CSF missingness values."""

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
)


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
