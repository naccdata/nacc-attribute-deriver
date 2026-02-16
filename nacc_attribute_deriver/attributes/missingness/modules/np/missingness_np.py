"""Class to handle NP form missingness values.

See derivenp.sas. This particular form has a lot of recode macros to
handle missingness variables.
"""

from typing import Optional, Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
    INFORMED_MISSINGNESS_FLOAT,
)
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
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
        # in the legacy system, NP used visitdate, but in new system
        # it uses npformdate, so use that if visitdate is missing
        date_attribute = "visitdate"
        if table.get("file.info.forms.json.visitdate") is None:
            date_attribute = "npformdate"

        super().__init__(
            table, required=frozenset(["formver"]), date_attribute=date_attribute
        )
        raw_formver = self.form.get_required("formver", float)
        self.formver = int(raw_formver)
        if self.formver != raw_formver:
            raise AttributeDeriverError(f"Unexpected formver for NP: {raw_formver}")

    def generic_missingness(
        self, attribute: str, attr_type: Type[T], default: Optional[T] = None
    ) -> T:
        """For NP only, the default for floats is -4.4 not -4.0."""
        if default is None and attr_type == float:  # noqa: E721
            default = INFORMED_MISSINGNESS_FLOAT  # type: ignore

        return super().generic_missingness(attribute, attr_type, default=default)

    def _missingness_np(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for NP;

        -4 / 4.4 / blank if missing.
        """
        return self.generic_missingness(field, attr_type)

    #############################################
    # Header variables
    # Due to issue with visitdate vs npformdate,
    # can't use generic methods
    #############################################

    def _missingness_np_adcid(self) -> int:
        """NP ADCID."""
        return self.generic_missingness("adcid", int)

    def _missingness_np_formver(self) -> float:
        """NP formver."""
        return self.generic_missingness("formver", float)

    def _missingness_np_visitdate(self) -> str:
        """NP visitdate/formdate can come from either variable."""
        visitdate = self.get_visitdate()
        if not visitdate:
            raise AttributeDeriverError("No date attribute defined for NP form")

        return visitdate

    ####################################
    # Form version-dependent variables #
    ####################################

    def _missingness_nppatho(self) -> int:
        """Handles missingness for NPPATHO."""
        nppath = self.form.get_value("nppath", int)
        if self.formver in [10, 11] and nppath == 0:
            return 0

        return self.generic_missingness("nppatho", int)

    #####################
    # Decimal variables #
    #####################

    def _missingness_nppmih(self) -> float:
        """Handles missingness for NPPMIH.

        This may have a decimal variable, NPPMIM, added to it.
        In the old code this used the rec9b macro but it honestly
        doesn't make sense to do it (it gated itself) and
        also the other fields that use rec9b also use rec10b,
        which this doesn't. So separating out to ensure it's
        its own thing.
        """
        nppmih = self.form.get_value("nppmih", float)
        nppmim = self.form.get_value("nppmim", float)

        if nppmih == 99:
            return 99.9

        if nppmih is not None:
            if nppmim is not None:
                return nppmih + (nppmim / 10)

            return nppmih

        return self.generic_missingness("nppmih", float)

    ###################
    # Other variables #
    ###################

    def _missingness_nplewycs(self) -> int:
        """Handles missingness for NPLEWYCS."""
        # cast 0s to -4
        if self.form.get_value("nplewycs", int) == 0:
            return INFORMED_MISSINGNESS

        return self.generic_missingness("nplewycs", int)

    #############################################
    # RECODE 10a + RECODE 9a (NPINFx variables) #
    #############################################

    def __recode_10a(self, field: str) -> int:
        """Handles variables that use the rec10a (v10, 11) and rec9a
        (other versions) macros."""
        # rec10a macro
        npinf = self.form.get_value("npinf", int)
        if self.formver in [10, 11]:
            if npinf == 8:
                return 88
            if npinf == 9:
                return 99

        # rec9a macro; unnecessary but keeping it here
        # to reference the SAS code; can remove once
        # we're more comfortable with the output
        else:
            value = self.form.get_value(field, int)
            if npinf is None and value is None:
                return INFORMED_MISSINGNESS

        return self.generic_missingness(field, int)

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

    ##########################
    # RECODE 10b + RECODE 9b #
    ##########################

    def __recode_10b(self, field: str, gate: str, num_infarcts: int) -> float:
        """Handles variables that use the rec10b (v10, 11),
        and rec9b macros (other versions), which need to handle both a value
        and its decimal.

        The gates are NPINF and NPINFxA (the latter is passed in).

        We grab the field's decimanl counterpart by looking at the last
        last character of the field, namely
            NPINFxB, NPINFxD, and NPINFxF: main field
            NPINFxC, NPINFxE, and NPINFxG: its decimal counterpart
        """
        npinf = self.form.get_value("npinf", int)
        gate_value = self.form.get_value(gate, int)
        value = self.form.get_value(field, int)

        # rec10b macro
        if self.formver in [10, 11]:
            if npinf == 8 or gate_value == 88 or gate_value == 0:  # noqa: SIM114
                return 88.8
            elif (
                npinf == 1
                and gate_value is not None
                and (gate_value > 0 and gate_value < num_infarcts)
            ):
                return 88.8
            elif npinf == 9 or gate_value == 99:
                return 99.9
            elif npinf == 0:
                return INFORMED_MISSINGNESS_FLOAT

        # rec9b macro; unnecessary but keeping it here
        # to reference the SAS code; can remove once
        # we're more comfortable with the output
        elif gate_value is None and value is None:
            return INFORMED_MISSINGNESS_FLOAT

        if value is None:
            return INFORMED_MISSINGNESS_FLOAT

        # combining the field with its decimal counterpart
        decimal_mapping = {
            "b": "c",
            "d": "e",
            "f": "g"
        }

        last_char = decimal_mapping.get(field[-1].lower())
        if not last_char:
            raise AttributeDeriverError(
                f"Cannot determine decimal counterpart to {field}"
            )

        value_dec = self.form.get_value(f"{field[0:-1]}{last_char}", int)
        if value_dec is not None and value_dec != 0:
            value += value_dec / 10

        # fix flat 88s/99s to 88.8/99.9, since sometimes the decimal
        # is not set correctly
        if value == 88:
            return 88.8
        if value == 8:
            return 8.8
        if value == 99:
            return 99.9
        if value == 9:
            return 9.9

        return value

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

    ##########################
    # RECODE 10c + RECODE 9a #
    ##########################

    def __recode_10c(self, field: str, gate: str) -> int:
        """Handles the rec10c (formver 10, 11) and rec9a
        (formver 1-9) macros. Both are called for the same
        variables just dependent on version.
        """
        gate_value = self.form.get_value(gate, int)
        value = self.form.get_value(field, int)

        if self.formver in [10, 11]:
            if gate_value == 8:
                return 8
            if gate_value == 9:
                return 9

            if gate_value == 0 and value is None:
                return INFORMED_MISSINGNESS

        # rec9a macro; unnecessary but keeping it here
        # to reference the SAS code; can remove once
        # we're more comfortable with the output
        else:
            if gate_value is None and value is None:
                return INFORMED_MISSINGNESS

        return self.generic_missingness(field, int)

    def _missingness_nphemo1(self) -> int:
        """Handles missingness for NPHEMO1."""
        return self.__recode_10c("nphemo1", "nphemo")

    def _missingness_nphemo2(self) -> int:
        """Handles missingness for NPHEMO2."""
        return self.__recode_10c("nphemo2", "nphemo")

    def _missingness_nphemo3(self) -> int:
        """Handles missingness for NPHEMO3."""
        return self.__recode_10c("nphemo3", "nphemo")

    def _missingness_npold1(self) -> int:
        """Handles missingness for NPOLD1."""
        return self.__recode_10c("npold1", "npold")

    def _missingness_npold2(self) -> int:
        """Handles missingness for NPOLD2."""
        return self.__recode_10c("npold2", "npold")

    def _missingness_npold3(self) -> int:
        """Handles missingness for NPOLD3."""
        return self.__recode_10c("npold3", "npold")

    def _missingness_npold4(self) -> int:
        """Handles missingness for NPOLD4."""
        return self.__recode_10c("npold4", "npold")

    def _missingness_npoldd1(self) -> int:
        """Handles missingness for NPOLDD1."""
        return self.__recode_10c("npoldd1", "npoldd")

    def _missingness_npoldd2(self) -> int:
        """Handles missingness for NPOLDD2."""
        return self.__recode_10c("npoldd2", "npoldd")

    def _missingness_npoldd3(self) -> int:
        """Handles missingness for NPOLDD3."""
        return self.__recode_10c("npoldd3", "npoldd")

    def _missingness_npoldd4(self) -> int:
        """Handles missingness for NPOLDD4."""
        return self.__recode_10c("npoldd4", "npoldd")

    def _missingness_nppath2(self) -> int:
        """Handles missingness for NPPATH2."""
        return self.__recode_10c("nppath2", "nppath")

    def _missingness_nppath3(self) -> int:
        """Handles missingness for NPPATH3."""
        return self.__recode_10c("nppath3", "nppath")

    def _missingness_nppath4(self) -> int:
        """Handles missingness for NPPATH4."""
        return self.__recode_10c("nppath4", "nppath")

    def _missingness_nppath5(self) -> int:
        """Handles missingness for NPPATH5."""
        return self.__recode_10c("nppath5", "nppath")

    def _missingness_nppath6(self) -> int:
        """Handles missingness for NPPATH6."""
        return self.__recode_10c("nppath6", "nppath")

    def _missingness_nppath7(self) -> int:
        """Handles missingness for NPPATH7."""
        return self.__recode_10c("nppath7", "nppath")

    def _missingness_nppath8(self) -> int:
        """Handles missingness for NPPATH8."""
        return self.__recode_10c("nppath8", "nppath")

    def _missingness_nppath9(self) -> int:
        """Handles missingness for NPPATH9."""
        return self.__recode_10c("nppath9", "nppath")

    def _missingness_nppath10(self) -> int:
        """Handles missingness for NPPATH10."""
        return self.__recode_10c("nppath10", "nppath")

    def _missingness_nppath11(self) -> int:
        """Handles missingness for NPPATH11."""
        return self.__recode_10c("nppath11", "nppath")

    def _missingness_npftdt2(self) -> int:
        """Handles missingness for NPFTDT2."""
        return self.__recode_10c("npftdt2", "npftdtau")

    def _missingness_npftdt5(self) -> int:
        """Handles missingness for NPFTDT5."""
        return self.__recode_10c("npftdt5", "npftdtau")

    def _missingness_npftdt6(self) -> int:
        """Handles missingness for NPFTDT6."""
        return self.__recode_10c("npftdt6", "npftdtau")

    def _missingness_npftdt7(self) -> int:
        """Handles missingness for NPFTDT7."""
        return self.__recode_10c("npftdt7", "npftdtau")

    def _missingness_npftdt8(self) -> int:
        """Handles missingness for NPFTDT8."""
        return self.__recode_10c("npftdt8", "npftdtau")

    def _missingness_npftdt9(self) -> int:
        """Handles missingness for NPFTDT9."""
        return self.__recode_10c("npftdt9", "npftdtau")

    def _missingness_npftdt10(self) -> int:
        """Handles missingness for NPFTDT10."""
        return self.__recode_10c("npftdt10", "npftdtau")

    def _missingness_npoftd1(self) -> int:
        """Handles missingness for NPOFTD1."""
        return self.__recode_10c("npoftd1", "npoftd")

    def _missingness_npoftd2(self) -> int:
        """Handles missingness for NPOFTD2."""
        return self.__recode_10c("npoftd2", "npoftd")

    def _missingness_npoftd3(self) -> int:
        """Handles missingness for NPOFTD3."""
        return self.__recode_10c("npoftd3", "npoftd")

    def _missingness_npoftd4(self) -> int:
        """Handles missingness for NPOFTD4."""
        return self.__recode_10c("npoftd4", "npoftd")

    def _missingness_npoftd5(self) -> int:
        """Handles missingness for NPOFTD5."""
        return self.__recode_10c("npoftd5", "npoftd")

    #############
    # Write-ins #
    #############

    def _missingness_nppathox(self) -> str:
        """Handles NPPATHOX."""
        if self.form.get_value("nppath") is None:
            return INFORMED_BLANK

        return self.generic_missingness("nppathox", str)
