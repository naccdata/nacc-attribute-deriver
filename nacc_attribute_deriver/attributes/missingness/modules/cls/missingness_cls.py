"""Class to handle CLS missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
    UDSCorrelatedFormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class CLSMissingness(SubjectMissingnessCollection):
    """Class to handle CLS missingness values."""

    def _missingness_naccengl(self) -> int:
        """Handles NACCENGL."""
        return self.handle_subject_missing("naccengl", int, INFORMED_MISSINGNESS)

    def _missingness_naccspnl(self) -> int:
        """Handles NACCSPNL."""
        return self.handle_subject_missing("naccspnl", int, INFORMED_MISSINGNESS)


class CLSFormMissingness(UDSCorrelatedFormMissingnessCollection):
    """Handles CLS missingness.

    Need to correlate with latest UDS visit.
    """

    def _missingness_cls(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for CLS form variables."""
        return self.generic_missingness(field, attr_type)

    def _missingness_uds_to_cls_visitdate(self) -> str:
        """Get the closest UDS visitdate."""
        visitdate, _ = self.find_closest_uds_visit()
        return visitdate

    def _missingness_cls_naccvnum(self) -> int:
        """Get the closest UDS visit, and set as this form's NACCVNUM.

        Even though NACCVNUM is technically a derived variable, in this
        instance we are treating it as a resolved variable.
        """
        _, naccvnum = self.find_closest_uds_visit()
        return naccvnum
