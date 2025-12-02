"""Class to handle NCRAD missingness values."""

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
)


class NCRADMissingness(SubjectMissingnessCollection):
    """Class to handle NCRAD missingness values."""

    def _missingness_naccapoe(self) -> int:
        """Handles NACCAPOE."""
        return self.handle_subject_missing("naccapoe", int, 9)

    def _missingness_naccne4s(self) -> int:
        """Handles NACCNE4S."""
        return self.handle_subject_missing("naccne4s", int, 9)

    def _missingness_naccncrd(self) -> int:
        """Handles NACCNCRD."""
        return self.handle_subject_missing("naccncrd", int, 0)
