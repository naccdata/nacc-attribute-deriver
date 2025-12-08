"""Class to handle NP form missingness values.

See derivenp.sas. This particular form has a lot of recode macros
for to handle missingness variables.
"""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
    INFORMED_MISSINGNESS_FLOAT,
)


class NPSubjectMissingness(SubjectMissingnessCollection):
    """Class to handle NP missingness values when the entire form is
    missing."""

    def _missingness_npformver(self) -> int:
        # curated in the context of an UDS visit
        return self.handle_subject_missing("npformver", int, INFORMED_MISSINGNESS)


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

    def __recode_10a(self, field: str) -> int:
        """Handles the rec10a macro."""
        if self.formver in [10, 11]:
            npinf = self.form.get_value("npinf", int)
            if npinf == 8:
                return 88
            if npinf == 9:
                return 99

        return self.generic_missingness(field, int)

    def __recode_10b(self, field: str, gate: str, num_infarcts: int) -> float:
        """Handles the rec10b macro, which actually handles two values at once.
        Also treats them as integers so not sure if they somehow get translated
        to floats elsewhere?

        The legacy recode macro actually handles two values at once; here
        we differentiate by looking at the last character of the field, namely

            NPINFxB, NPINFxD, and NPINFxF = 2 digits (e.g. 88)
            NPINFxC, NPINFxE, and NPINFxG = 1 digit (e.g. 8)
                ^ these values do not appear in the DEDs so not sure where they come from?
        """
        if self.formver in [10, 11]:
            is_two_digits = field[-1].lower() in ["b", "d", "f"]

            npinf = self.form.get_value("npinf", int)
            gate_value = self.form.get_value(gate, int)

            if npinf == 8 or gate_value == 88 or gate_value == 0:
                return 88.8 if is_two_digits else 8.8
            elif (npinf == 1 and gate_value is not None and
                 (gate_value > 0 and gate_value < num_infarcts)):
                return 88.8 if is_two_digits else 8.8
            elif npinf == 9 or gate_value == 99:
                return 99.9 if is_two_digits else 9.9
            elif npinf == 0:
                return INFORMED_MISSINGNESS_FLOAT

        return self.generic_missingness(field, float)

    # REGRESSION: aside from the difference of -4 and blanks
    # (which we are overriding anyways), not applying the other
    # recodes doesn't seem to raise regression errors, so
    # leaving out for now. it's possible they are functionally
    # useless if existing error checks ensure things are correctly
    # set to begin with

    def _missingness_npinf1a(self) -> int:
        """Handles missingness for NPINF1A."""
        return self.__recode_10a("npinf1a")

    def _missingness_npinf2a(self) -> int:
        """Handles missingness for NPINF2A."""
        return self.__recode_10a("npinf2a")

    def _missingness_npinf3a(self) -> int:
        """Handles missingness for NPINF3A."""
        return self.__recode_10a("npinf3a")

    def _missingness_npinf4a(self) -> int:
        """Handles missingness for NPINF4A."""
        return self.__recode_10a("npinf4a")

    def _missingness_npinf1b(self) -> float:
        """Handles missingness for NPINF1B."""
        return self.__recode_10b("npinf1b", "npinf1a", 1)

    def _missingness_npinf1d(self) -> float:
        """Handles missingness for NPINF1D."""
        return self.__recode_10b("npinf1d", "npinf1a", 2)

    def _missingness_npinf1f(self) -> float:
        """Handles missingness for NPINF1F."""
        return self.__recode_10b("npinf1f", "npinf1a", 3)

    def _missingness_npinf2b(self) -> float:
        """Handles missingness for NPINF2B."""
        return self.__recode_10b("npinf2b", "npinf2a", 1)

    def _missingness_npinf2d(self) -> float:
        """Handles missingness for NPINF2D."""
        return self.__recode_10b("npinf2d", "npinf2a", 2)

    def _missingness_npinf2f(self) -> float:
        """Handles missingness for NPINF2F."""
        return self.__recode_10b("npinf2f", "npinf2a", 3)

    def _missingness_npinf3b(self) -> float:
        """Handles missingness for NPINF3B."""
        return self.__recode_10b("npinf3b", "npinf3a", 1)

    def _missingness_npinf3d(self) -> float:
        """Handles missingness for NPINF3D."""
        return self.__recode_10b("npinf3d", "npinf3a", 2)

    def _missingness_npinf3f(self) -> float:
        """Handles missingness for NPINF3F."""
        return self.__recode_10b("npinf3f", "npinf3a", 3)

    def _missingness_npinf4b(self) -> float:
        """Handles missingness for NPINF4B."""
        return self.__recode_10b("npinf4b", "npinf4a", 1)

    def _missingness_npinf4d(self) -> float:
        """Handles missingness for NPINF4D."""
        return self.__recode_10b("npinf4d", "npinf4a", 2)

    def _missingness_npinf4f(self) -> float:
        """Handles missingness for NPINF4F."""
        return self.__recode_10b("npinf4f", "npinf4a", 3)
