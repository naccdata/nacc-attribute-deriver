"""Class to handle MP missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    RawNamespace,
    T,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class MPMissingness(FormMissingnessCollection):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table=table, namespace=RawNamespace, date_attribute=None)

    def _missingness_mri_dicom(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for MRI DICOM."""
        return self.generic_missingness(field, attr_type)

    def _missingness_pet_dicom(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for PET DICOM."""
        return self.generic_missingness(field, attr_type)


class MPSubjectMissingness(SubjectMissingnessCollection):
    """Class to handle MP missingness values."""

    def _missingness_naccmrsa(self) -> int:
        """Handles NACCMRSA."""
        return self.handle_subject_missing("naccmrsa", int, 0)

    def _missingness_naccnmri(self) -> int:
        """Handles NACCNMRI.

        REGRESSION: Should be 88, but legacy always set to 0
        """
        return self.handle_subject_missing("naccnmri", int, 0)

    def _missingness_naccapsa(self) -> int:
        """Handles NACCAPSA."""
        return self.handle_subject_missing("naccapsa", int, 0)

    def _missingness_naccnapa(self) -> int:
        """Handles NACCNAPA.

        REGRESSION: Should be 88, but legacy always set to 0
        """
        return self.handle_subject_missing("naccnapa", int, 0)
