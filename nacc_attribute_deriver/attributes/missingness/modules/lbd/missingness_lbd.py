"""Class to handle LBD missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
)


class LBDMissingness(SubjectMissingnessCollection):
    """Class to handle LBD missingness values."""

    def _missingness_nacclbdm(self) -> Optional[int]:
        """Handles NACCLBDM."""
        return self.handle_subject_missing("nacclbdm", 0)
