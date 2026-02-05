"""Class to handle FTLD missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class FTLDMissingness(SubjectMissingnessCollection):
    """Class to handle FTLD missingness values."""

    def _missingness_naccftd(self) -> int:
        """Handles NACCFTD."""
        return self.handle_subject_missing("naccftd", int, 0)


class FTLDFormMissingness(FormMissingnessCollection):
    def _missingness_ftld(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for FTLD form variables."""
        return self.generic_missingness(field, attr_type)

    def _missingness_ftdinfyr(self) -> int:
        """Handles missingness for FTDINFYR."""
        # some forms set this to 99; correct to 9999
        if self.form.get_value("ftdinfyr", int) == 99:
            return 9999

        return self.generic_missingness("ftdinfyr", int)

    def _missingness_ftdlengt(self) -> int:
        """Handles missingness for FTDLENGT."""
        ftdlengt = self.form.get_value("ftdlengt", int)

        if ftdlengt is None:
            return INFORMED_MISSINGNESS

        # set 0 to 999
        if ftdlengt in [0, 999]:
            return 999

        # otherwise, enforce range 20 - 240
        return min(max(20, ftdlengt), 240)

    def _missingness_ftdratio(self) -> float:
        # correct 88 to 88.88
        if self.form.get_value("ftdratio", float) == 88:
            return 88.88

        return self.generic_missingness("ftdratio", float)
