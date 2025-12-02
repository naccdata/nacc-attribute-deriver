"""Class to handle LBD missingness values."""

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
)


class LBDMissingness(SubjectMissingnessCollection):
    """Class to handle LBD missingness values."""

    def _missingness_nacclbdm(self) -> int:
        """Handles NACCLBDM."""
        return self.handle_subject_missing("nacclbdm", int, 0)
