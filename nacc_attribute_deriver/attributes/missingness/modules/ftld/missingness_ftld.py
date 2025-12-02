"""Class to handle FTLD missingness values."""

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
)


class FTLDMissingness(SubjectMissingnessCollection):
    """Class to handle FTLD missingness values."""

    def _missingness_naccftd(self) -> int:
        """Handles NACCFTD."""
        return self.handle_subject_missing("naccftd", int, 0)
