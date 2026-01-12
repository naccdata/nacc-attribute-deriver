"""Class to handle FTLD missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T


class FTLDMissingness(SubjectMissingnessCollection):
    """Class to handle FTLD missingness values."""

    def _missingness_naccftd(self) -> int:
        """Handles NACCFTD."""
        return self.handle_subject_missing("naccftd", int, 0)


class FTLDFormMissingness(FormMissingnessCollection):
    """
    TODO: THIS IS ONLY REQUIRED TO BACKFILL WRITE-IN/KNOWN BLANK VARIABLES TO AVOID
    THE NOT-IN-CONTAINER ERROR. REMOVE ONCE FEATURE IS ADDED TO ETL GEAR.
    """

    def _missingness_ftld(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for FTLD form variables."""
        return self.generic_missingness(field, attr_type)

    def _missingness_ftdinfyr(self) -> int:
        """Handles missingness for FTDINFYR."""
        # some forms set this to 99; correct to 9999
        if self.form.get_value("ftdinfyr", int) == 99:
            return 9999

        return self.generic_missingness("ftdinfyr", int)
