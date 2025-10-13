"""Class to handle LBD missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.subject_missingness import (
    SubjectMissingnessCollection,
)


class LBDMissingness(SubjectMissingnessCollection):
    """Class to handle LBD missingness values."""

    def _missingness_nacclbdm(self) -> Optional[int]:
        """Handles NACCLBDM."""
        return self.handle_missing("nacclbdm", 0)
