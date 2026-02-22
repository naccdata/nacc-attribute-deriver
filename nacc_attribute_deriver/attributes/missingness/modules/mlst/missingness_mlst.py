"""Class to handle Milestone form missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class MilestoneMissingness(FormMissingnessCollection):
    def _missingness_mlst(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for Milestone form variables."""
        return self.generic_missingness(field, attr_type)

    def _missingness_protocol(self) -> int:
        """Handles PROTOCOL (V2+)."""
        # sometimes they set both PROTOCOL and UDSACTV, return
        # based on the version
        formver = self.form.get_value("formver", float)
        if formver and formver < 2:
            return INFORMED_MISSINGNESS

        return self.generic_missingness("protocol", int)

    def _missingness_udsactiv(self) -> int:
        """Handles UDSACTIV (V1 only)."""
        # sometimes they set both PROTOCOL and UDSACTV, return
        # based on the version
        formver = self.form.get_value("formver", float)
        if formver and formver > 1:
            return INFORMED_MISSINGNESS

        return self.generic_missingness("udsactiv", int)


class MilestoneSubjectMissingness(SubjectMissingnessCollection):
    """Class to handle Milestone missingness values at the subject level."""

    def _missingness_naccnrdy(self) -> int:
        """Handles NACCNRDY."""
        return self.handle_subject_missing("naccnrdy", int, 88)

    def _missingness_naccnrmo(self) -> int:
        """Handles NACCNRMO."""
        return self.handle_subject_missing("naccnrmo", int, 88)

    def _missingness_naccnryr(self) -> int:
        """Handles NACCNRYR."""
        return self.handle_subject_missing("naccnryr", int, 8888)
