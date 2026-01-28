"""Class to handle CSF missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class CSFMissingness(SubjectMissingnessCollection):
    """Class to handle CSF missingness values."""

    def _missingness_naccacsf(self) -> int:
        """Handles NACCACSF."""
        return self.handle_subject_missing("naccacsf", int, 0)

    def _missingness_naccpcsf(self) -> int:
        """Handles NACCPCSF."""
        return self.handle_subject_missing("naccpcsf", int, 0)

    def _missingness_nacctcsf(self) -> int:
        """Handles NACCTCSF."""
        return self.handle_subject_missing("nacctcsf", int, 0)


class CSFFormMissingness(FormMissingnessCollection):
    def _missingness_csf(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for CLS form variables."""
        return self.generic_missingness(field, attr_type)

    def __enforce_range(self, field: str, minimum: float, maximum: float) -> float:
        """Enforce a float range."""
        result = self.generic_missingness(field, float)

        if result != INFORMED_MISSINGNESS:
            return min(max(minimum, result), maximum)

        return result

    def _missingness_csfabeta(self) -> float:
        """Handles missingness for CSFABETA."""
        return self.__enforce_range("csfabeta", 1.0, 2000.0)

    def _missingness_csfttau(self) -> float:
        """Handles missingness for CSFTTAU."""
        return self.__enforce_range("csfttau", 1.0, 2500.0)

    def _missingness_csfptau(self) -> float:
        """Handles missingness for CSFPTAU."""
        return self.__enforce_range("csfptau", 1.0, 500.0)
