"""Class to handle CSF missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.subject_missingness import (
    SubjectMissingnessCollection,
)


class CSFMissingness(SubjectMissingnessCollection):
    """Class to handle CSF missingness values."""

    def _missingness_naccacsf(self) -> Optional[int]:
        """Handles NACCACSF."""
        return self.handle_missing("naccacsf", 0)

    def _missingness_naccpcsf(self) -> Optional[int]:
        """Handles NACCPCSF."""
        return self.handle_missing("naccpcsf", 0)

    def _missingness_nacctcsf(self) -> Optional[int]:
        """Handles NACCTCSF."""
        return self.handle_missing("nacctcsf", 0)
