"""Class to handle Milestone form missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.subject_missingness import (
    SubjectMissingnessCollection,
)


class MilestoneMissingness(SubjectMissingnessCollection):
    """Class to handle Milestone missingness values."""

    def _missingness_naccnrdy(self) -> Optional[int]:
        """Handles NACCNRDY."""
        return self.handle_missing("naccnrdy", 88)

    def _missingness_naccnrmo(self) -> Optional[int]:
        """Handles NACCNRMO."""
        return self.handle_missing("naccnrmo", 88)

    def _missingness_naccnryr(self) -> Optional[int]:
        """Handles NACCNRYR."""
        return self.handle_missing("naccnyr", 8888)
