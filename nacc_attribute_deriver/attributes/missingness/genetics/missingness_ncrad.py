"""Class to handle NCRAD missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.subject_missingness import (
    SubjectMissingnessCollection,
)


class NCRADMissingness(SubjectMissingnessCollection):
    """Class to handle NCRAD missingness values."""

    def _missingness_naccapoe(self) -> Optional[int]:
        """Handles NACCAPOE."""
        return self.handle_missing("naccapoe", 9)

    def _missingness_naccne4s(self) -> Optional[int]:
        """Handles NACCNE4S."""
        return self.handle_missing("naccne4s", 9)

    def _missingness_naccncrd(self) -> Optional[int]:
        """Handles NACCNCRD."""
        return self.handle_missing("naccncrd", 0)
