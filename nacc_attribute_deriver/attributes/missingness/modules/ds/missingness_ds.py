"""Class to handle DS missingness values."""

from typing import Callable, Optional, Tuple, Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    SubjectMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.utils.errors import AttributeDeriverError

# Q16 diagnostic history checkboxes and the other boxes in the question
_Q16_OTHERS = {
    "dsdxhs_no": ("dsdxhs_mci", "dsdxhs_dem"),
    "dsdxhs_mci": ("dsdxhs_no", "dsdxhs_dem"),
    "dsdxhs_dem": ("dsdxhs_no", "dsdxhs_mci"),
}


class DSMissingness(SubjectMissingnessCollection):
    """Class to handle DS subject-level missingness values."""

    def _missingness_naccds(self) -> int:
        """Handles NACCDS; 0 if the subject has no DS visits."""
        return self.handle_subject_missing("naccds", int, 0)


class DSFormMissingness(FormMissingnessCollection):
    def _missingness_ds(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for DS form variables."""
        return self.generic_missingness(field, attr_type)

    def __carry_forward(
        self, field: str, prev_code: int, invalid: Tuple[int, ...] = ()
    ) -> int:
        """Returns the previous DS visit's value for FIELD = PREV_CODE.

        A "provided at previous visit" code needs a valid previous
        value. If there is none (no previous visit, -4, the code itself,
        or one of INVALID), the submission is incorrect, so raise an
        error and fail the file.
        """
        result = self.handle_prev_visit(field, int, prev_code=prev_code)
        if result in [INFORMED_MISSINGNESS, prev_code, *invalid]:
            raise AttributeDeriverError(
                f"{field.upper()} = {prev_code} (provided at previous visit) "
                + "but no previous value found"
            )

        return result

    def __handle_prev_code(self, field: str, prev_code: int) -> int:
        """Handles values that can be provided at the previous visit (A1D ages,
        D1D).

        If FIELD = PREV_CODE, FIELD = previous DS visit's value (error if none)
        Else generic missingness
        """
        value = self.form.get_value(field, int)
        if value == prev_code:
            return self.__carry_forward(field, prev_code)

        if value is not None:
            return value

        return self.generic_missingness(field, int)

    def __handle_year(self, field: str, gate: str) -> int:
        """Handles A1D surgery/procedure years, which can be carried forward
        from the previous visit and are only asked if GATE = 1.

        If FIELD = 7777, FIELD = previous visit's value
            - error if none, or if it is 8888 (not applicable), since the
              procedure is now reported but no year was ever given
        If FIELD is blank and GATE = 0 or 9, FIELD = 8888
        Else generic missingness
        """
        value = self.form.get_value(field, int)
        if value == 7777:
            return self.__carry_forward(field, 7777, invalid=(8888,))

        if value is not None:
            return value

        if self.form.get_value(gate, int) in [0, 9]:
            return 8888

        return self.generic_missingness(field, int)

    #######
    # A1D #
    #######

    def _missingness_dsmomage(self) -> int:
        """Handles missingness for DSMOMAGE."""
        return self.__handle_prev_code("dsmomage", 777)

    def _missingness_dsmnsage(self) -> int:
        """Handles missingness for DSMNSAGE."""
        return self.__handle_prev_code("dsmnsage", 777)

    def _missingness_dsmnpage(self) -> int:
        """Handles missingness for DSMNPAGE."""
        return self.__handle_prev_code("dsmnpage", 777)

    def _missingness_dsagehrt(self) -> int:
        """Handles missingness for DSAGEHRT."""
        return self.__handle_prev_code("dsagehrt", 777)

    def _missingness_dshrtryr(self) -> int:
        """Handles missingness for DSHRTRYR."""
        return self.__handle_year("dshrtryr", "dshrtrpr")

    def _missingness_dscrdsyr(self) -> int:
        """Handles missingness for DSCRDSYR."""
        return self.__handle_year("dscrdsyr", "dscrdsrg")

    def _missingness_dsspinyr(self) -> int:
        """Handles missingness for DSSPINYR."""
        return self.__handle_year("dsspinyr", "dsspin")

    def _missingness_dslworyr(self) -> int:
        """Handles missingness for DSLWORYR."""
        return self.__handle_year("dslworyr", "dslworth")

    def _missingness_dsuporyr(self) -> int:
        """Handles missingness for DSUPORYR."""
        return self.__handle_year("dsuporyr", "dsuporth")

    def _missingness_dsthysyr(self) -> int:
        """Handles missingness for DSTHYSYR."""
        return self.__handle_year("dsthysyr", "dsthysrg")

    def _missingness_dsoncsyr(self) -> int:
        """Handles missingness for DSONCSYR."""
        return self.__handle_year("dsoncsyr", "dsoncsrg")

    def _missingness_dsothsyr(self) -> int:
        """Handles missingness for DSOTHSYR."""
        return self.__handle_year("dsothsyr", "dsothsrg")

    #######
    # B1D #
    #######
    # Write-ins (DSLIVX, DSDXOTHX, DSLEOTHX, DSDXTYPE, DSDXBYX, DSDEMCOM,
    # DSMHOTHX, DSCANCX) are strings, so generic missingness already
    # leaves them blank.
    #
    # Checkboxes arrive blank when unchecked; a blank box is 0 when its
    # question was answered:
    #   - DSDX_*, DSCN_*, DSLE_*, DSRE_*: if B1D was completed (FRMDATEB1D)
    #   - DSDXHS_NO/MCI/DEM (Q16): if another Q16 box is checked
    # Gated numerics get a "not applicable" code when the gate box resolves
    # to 0, so an unanswered gate (-4) leaves them at -4 too. DSREPMO is the
    # one float; it uses 888 / -4 as floats.

    def __handle_skipped(
        self, field: str, skipped: Callable[[], bool], code: int
    ) -> int:
        """Handles B1D integers that are skipped by a gate question.

        If FIELD is submitted, keep it
        If FIELD is blank and SKIPPED(), FIELD = CODE
        Else generic missingness

        SKIPPED is only evaluated when FIELD is blank.
        """
        value = self.form.get_value(field, int)
        if value is not None:
            return value

        if skipped():
            return code

        return self.generic_missingness(field, int)

    def __b1d_completed(self) -> bool:
        """Whether B1D was completed (FRMDATEB1D is not blank)."""
        return self.form.get_value("frmdateb1d", str) not in [None, ""]

    def __any_checked(self, *fields: str) -> bool:
        """Whether any of FIELDS = 1."""
        return any(self.form.get_value(x, int) == 1 for x in fields)

    def __box_applies(self, field: str) -> bool:
        """Whether a blank checkbox FIELD should be 0."""
        others = _Q16_OTHERS.get(field)
        if others:
            return self.__any_checked(*others)

        return self.__b1d_completed()

    def __resolved_box(self, field: str) -> Optional[int]:
        """The checkbox's resolved value: submitted value, else 0 if its
        question was answered, else None."""
        value = self.form.get_value(field, int)
        if value is not None:
            return value

        return 0 if self.__box_applies(field) else None

    def __handle_box(self, field: str) -> int:
        """Handles a checkbox.

        If FIELD is blank and its question was answered, FIELD = 0
        Else generic missingness
        """
        return self.__handle_skipped(field, lambda: self.__box_applies(field), 0)

    def __no_dx_history(self) -> bool:
        """Whether DSDXHS_NO = 1 (no diagnosis of MCI or dementia)."""
        return self.form.get_value("dsdxhs_no", int) == 1

    def __gate_is_0(self, gate: str) -> bool:
        """Whether the GATE checkbox resolves to 0."""
        return self.__resolved_box(gate) == 0

    # Q9 diagnosed conditions
    def _missingness_dsdx_aut(self) -> int:
        """Handles missingness for DSDX_AUT."""
        return self.__handle_box("dsdx_aut")

    def _missingness_dsdx_cp(self) -> int:
        """Handles missingness for DSDX_CP."""
        return self.__handle_box("dsdx_cp")

    def _missingness_dsdx_ds(self) -> int:
        """Handles missingness for DSDX_DS."""
        return self.__handle_box("dsdx_ds")

    def _missingness_dsdx_frx(self) -> int:
        """Handles missingness for DSDX_FRX."""
        return self.__handle_box("dsdx_frx")

    def _missingness_dsdx_id(self) -> int:
        """Handles missingness for DSDX_ID."""
        return self.__handle_box("dsdx_id")

    def _missingness_dsdx_pw(self) -> int:
        """Handles missingness for DSDX_PW."""
        return self.__handle_box("dsdx_pw")

    def _missingness_dsdx_oth(self) -> int:
        """Handles missingness for DSDX_OTH."""
        return self.__handle_box("dsdx_oth")

    # Q10 co-occurring conditions
    def _missingness_dscn_vim(self) -> int:
        """Handles missingness for DSCN_VIM."""
        return self.__handle_box("dscn_vim")

    def _missingness_dscn_bld(self) -> int:
        """Handles missingness for DSCN_BLD."""
        return self.__handle_box("dscn_bld")

    def _missingness_dscn_gls(self) -> int:
        """Handles missingness for DSCN_GLS."""
        return self.__handle_box("dscn_gls")

    def _missingness_dscn_him(self) -> int:
        """Handles missingness for DSCN_HIM."""
        return self.__handle_box("dscn_him")

    def _missingness_dscn_df(self) -> int:
        """Handles missingness for DSCN_DF."""
        return self.__handle_box("dscn_df")

    def _missingness_dscn_had(self) -> int:
        """Handles missingness for DSCN_HAD."""
        return self.__handle_box("dscn_had")

    def _missingness_dscn_mim(self) -> int:
        """Handles missingness for DSCN_MIM."""
        return self.__handle_box("dscn_mim")

    def _missingness_dscn_uw(self) -> int:
        """Handles missingness for DSCN_UW."""
        return self.__handle_box("dscn_uw")

    def _missingness_dscn_miw(self) -> int:
        """Handles missingness for DSCN_MIW."""
        return self.__handle_box("dscn_miw")

    # Q14 significant life events
    def _missingness_dsle_cd(self) -> int:
        """Handles missingness for DSLE_CD."""
        return self.__handle_box("dsle_cd")

    def _missingness_dsle_chl(self) -> int:
        """Handles missingness for DSLE_CHL."""
        return self.__handle_box("dsle_chl")

    def _missingness_dsle_chs(self) -> int:
        """Handles missingness for DSLE_CHS."""
        return self.__handle_box("dsle_chs")

    def _missingness_dsle_nrm(self) -> int:
        """Handles missingness for DSLE_NRM."""
        return self.__handle_box("dsle_nrm")

    def _missingness_dsle_ill(self) -> int:
        """Handles missingness for DSLE_ILL."""
        return self.__handle_box("dsle_ill")

    def _missingness_dsle_sem(self) -> int:
        """Handles missingness for DSLE_SEM."""
        return self.__handle_box("dsle_sem")

    def _missingness_dsle_sei(self) -> int:
        """Handles missingness for DSLE_SEI."""
        return self.__handle_box("dsle_sei")

    def _missingness_dsle_sev(self) -> int:
        """Handles missingness for DSLE_SEV."""
        return self.__handle_box("dsle_sev")

    def _missingness_dsle_oth(self) -> int:
        """Handles missingness for DSLE_OTH."""
        return self.__handle_box("dsle_oth")

    # Q16 diagnostic history
    def _missingness_dsdxhs_no(self) -> int:
        """Handles missingness for DSDXHS_NO; 0 if DSDXHS_MCI or DSDXHS_DEM =
        1."""
        return self.__handle_box("dsdxhs_no")

    def _missingness_dsdxhs_mci(self) -> int:
        """Handles missingness for DSDXHS_MCI; 0 if DSDXHS_NO or DSDXHS_DEM =
        1."""
        return self.__handle_box("dsdxhs_mci")

    def _missingness_dsdxhs_dem(self) -> int:
        """Handles missingness for DSDXHS_DEM; 0 if DSDXHS_NO or DSDXHS_MCI =
        1."""
        return self.__handle_box("dsdxhs_dem")

    def _missingness_dsmcimo(self) -> int:
        """Handles missingness for DSMCIMO; 88 if DSDXHS_MCI = 0."""
        return self.__handle_skipped(
            "dsmcimo", lambda: self.__gate_is_0("dsdxhs_mci"), 88
        )

    def _missingness_dsmciyr(self) -> int:
        """Handles missingness for DSMCIYR; 8888 if DSDXHS_MCI = 0."""
        return self.__handle_skipped(
            "dsmciyr", lambda: self.__gate_is_0("dsdxhs_mci"), 8888
        )

    def _missingness_dsdemmo(self) -> int:
        """Handles missingness for DSDEMMO; 88 if DSDXHS_DEM = 0."""
        return self.__handle_skipped(
            "dsdemmo", lambda: self.__gate_is_0("dsdxhs_dem"), 88
        )

    def _missingness_dsdemyr(self) -> int:
        """Handles missingness for DSDEMYR; 8888 if DSDXHS_DEM = 0."""
        return self.__handle_skipped(
            "dsdemyr", lambda: self.__gate_is_0("dsdxhs_dem"), 8888
        )

    def _missingness_dsdxby(self) -> int:
        """Handles missingness for DSDXBY; 8 if DSDXHS_NO = 1."""
        return self.__handle_skipped("dsdxby", self.__no_dx_history, 8)

    def _missingness_dsonstmo(self) -> int:
        """Handles missingness for DSONSTMO; 88 if DSDXHS_NO = 1."""
        return self.__handle_skipped("dsonstmo", self.__no_dx_history, 88)

    def _missingness_dsonstyr(self) -> int:
        """Handles missingness for DSONSTYR; 8888 if DSDXHS_NO = 1."""
        return self.__handle_skipped("dsonstyr", self.__no_dx_history, 8888)

    # Q30 next steps / recommendations
    def _missingness_dsre_ref(self) -> int:
        """Handles missingness for DSRE_REF."""
        return self.__handle_box("dsre_ref")

    def _missingness_dsre_int(self) -> int:
        """Handles missingness for DSRE_INT."""
        return self.__handle_box("dsre_int")

    def _missingness_dsre_ann(self) -> int:
        """Handles missingness for DSRE_ANN."""
        return self.__handle_box("dsre_ann")

    def _missingness_dsre_rep(self) -> int:
        """Handles missingness for DSRE_REP."""
        return self.__handle_box("dsre_rep")

    def _missingness_dsrepmo(self) -> float:
        """Handles missingness for DSREPMO, which is a float.

        If DSREPMO is blank and DSRE_REP = 0, DSREPMO = 888.0
        Else generic missingness (-4.0 if blank)
        """
        value = self.form.get_value("dsrepmo", float)
        if value is not None:
            return value

        if self.__gate_is_0("dsre_rep"):
            return 888.0

        return self.generic_missingness("dsrepmo", float)

    #######
    # D1D #
    #######

    def _missingness_dsheadcm(self) -> int:
        """Handles missingness for DSHEADCM; 777 carries forward."""
        return self.__handle_prev_code("dsheadcm", 777)

    def _missingness_dschrom(self) -> int:
        """Handles missingness for DSCHROM; 7 carries forward."""
        return self.__handle_prev_code("dschrom", 7)
