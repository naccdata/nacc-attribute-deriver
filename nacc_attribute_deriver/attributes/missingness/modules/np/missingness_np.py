"""Class to handle NP form missingness values.

See derivenp.sas. There is a lot of recode logic but I think just using
general missingness resolves most of them since they boil down to "if
the variable doesn't exist in this version, set to -4".
"""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class NPMissingness(FormMissingnessCollection):
    """Class to handle NP missingness values at the file-level."""

    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table, required=frozenset(["formver"]))
        self.formver = self.form.get_required("formver", int)

    def _missingness_np(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for NP;

        -4 / 4.4 / blank if missing.
        """
        return self.generic_missingness(field, attr_type)

    ####################################
    # Form version-dependent variables #
    ####################################

    def _missingness_nppatho(self) -> int:
        """Handles missingness for NPPATHO."""
        nppath = self.form.get_value("nppath", int)
        if self.formver in [10, 11] and nppath == 0:
            return 0

        return self.generic_missingness("nppatho", int)

    ####################
    # NPINFX variables #
    ####################

    def __handle_npinfx_int(self, field: str) -> int:
        """Handle NPINFX variables (ints)."""
        npinfx = self.form.get_value(field, int)
        if self.formver in [10, 11] and npinfx is None:
            return 88

        return self.generic_missingness(field, int)

    def _missingness_npinf1a(self) -> int:
        """Handles missingness for NPINF1A."""
        return self.__handle_npinfx_int("npinf1a")

    def _missingness_npinf2a(self) -> int:
        """Handles missingness for NPINF2A."""
        return self.__handle_npinfx_int("npinf2a")

    def _missingness_npinf3a(self) -> int:
        """Handles missingness for NPINF3A."""
        return self.__handle_npinfx_int("npinf3a")

    def _missingness_npinf4a(self) -> int:
        """Handles missingness for NPINF4A."""
        return self.__handle_npinfx_int("npinf4a")

    def __handle_npinfx_float(self, field: str) -> float:
        """Handle NPINFX variables (floats)."""
        npinfx = self.form.get_value(field, float)
        if self.formver in [10, 11] and npinfx is None:
            return 88.8

        return self.generic_missingness(field, float)

    def _missingness_npinf1b(self) -> float:
        """Handles missingness for NPINF1B."""
        return self.__handle_npinfx_float("npinf1b")

    def _missingness_npinf1d(self) -> float:
        """Handles missingness for NPINF1D."""
        return self.__handle_npinfx_float("npinf1d")

    def _missingness_npinf1f(self) -> float:
        """Handles missingness for NPINF1F."""
        return self.__handle_npinfx_float("npinf1f")

    def _missingness_npinf2b(self) -> float:
        """Handles missingness for NPINF2B."""
        return self.__handle_npinfx_float("npinf2b")

    def _missingness_npinf2d(self) -> float:
        """Handles missingness for NPINF2D."""
        return self.__handle_npinfx_float("npinf2d")

    def _missingness_npinf2f(self) -> float:
        """Handles missingness for NPINF2F."""
        return self.__handle_npinfx_float("npinf2f")

    def _missingness_npinf3b(self) -> float:
        """Handles missingness for NPINF3B."""
        return self.__handle_npinfx_float("npinf3b")

    def _missingness_npinf3d(self) -> float:
        """Handles missingness for NPINF3D."""
        return self.__handle_npinfx_float("npinf3d")

    def _missingness_npinf3f(self) -> float:
        """Handles missingness for NPINF3F."""
        return self.__handle_npinfx_float("npinf3f")

    def _missingness_npinf4b(self) -> float:
        """Handles missingness for NPINF4B."""
        return self.__handle_npinfx_float("npinf4b")

    def _missingness_npinf4d(self) -> float:
        """Handles missingness for NPINF4D."""
        return self.__handle_npinfx_float("npinf4d")

    def _missingness_npinf4f(self) -> float:
        """Handles missingness for NPINF4F."""
        return self.__handle_npinfx_float("npinf4f")


class NPSubjectMissingness(SubjectMissingnessCollection):
    """Class to handle NP missingness values when the entire form is
    missing."""

    def _missingness_npformver(self) -> int:
        return self.handle_subject_missing("npformver", int, INFORMED_MISSINGNESS)

    # this is actually curated in the context of an UDS visit
