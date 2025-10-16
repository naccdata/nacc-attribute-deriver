"""Class to handle FTLD missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.subject_missingness import (
    SubjectMissingnessCollection,
)


class FTLDMissingness(SubjectMissingnessCollection):
    """Class to handle FTLD missingness values."""

    def _missingness_naccftd(self) -> Optional[int]:
        """Handles NACCFTD."""
        return self.handle_missing("naccftd", 0)
