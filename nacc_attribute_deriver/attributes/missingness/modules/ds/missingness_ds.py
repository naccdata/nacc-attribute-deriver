"""Class to handle DS missingness values."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T


class DSFormMissingness(FormMissingnessCollection):
    def _missingness_ds(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for DS form variables."""
        return self.generic_missingness(field, attr_type)

    def __handle_age(self, field: str) -> int:
        """Handles A1D ages that can be carried forward from the previous
        visit.

        If FIELD = 777, FIELD = previous visit's value (999 if none)
        Else generic missingness
        """
        if self.form.get_value(field, int) == 777:
            return self.handle_prev_visit(field, int, prev_code=777, default=999)

        return self.generic_missingness(field, int)

    def __handle_year(self, field: str, gate: str) -> int:
        """Handles A1D surgery/procedure years, which can be carried forward
        from the previous visit and are only asked if GATE = 1.

        If FIELD = 7777, FIELD = previous visit's value (9999 if none)
        If FIELD is blank and GATE = 0 or 9, FIELD = 8888
        Else generic missingness
        """
        value = self.form.get_value(field, int)
        if value == 7777:
            return self.handle_prev_visit(field, int, prev_code=7777, default=9999)

        if value is None and self.form.get_value(gate, int) in [0, 9]:
            return 8888

        return self.generic_missingness(field, int)

    #######
    # A1D #
    #######

    def _missingness_dsmomage(self) -> int:
        """Handles missingness for DSMOMAGE."""
        return self.__handle_age("dsmomage")

    def _missingness_dsmnsage(self) -> int:
        """Handles missingness for DSMNSAGE."""
        return self.__handle_age("dsmnsage")

    def _missingness_dsmnpage(self) -> int:
        """Handles missingness for DSMNPAGE."""
        return self.__handle_age("dsmnpage")

    def _missingness_dsagehrt(self) -> int:
        """Handles missingness for DSAGEHRT."""
        return self.__handle_age("dsagehrt")

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
    # leaves them blank. Skipped integers get a "not applicable" code.

    def __handle_skipped(self, field: str, skipped: bool, code: int) -> int:
        """Handles B1D integers that are skipped by a gate question.

        If FIELD is blank and SKIPPED, FIELD = CODE
        Else generic missingness
        """
        if skipped and self.form.get_value(field, int) is None:
            return code

        return self.generic_missingness(field, int)

    def __no_dx_history(self) -> bool:
        """Whether DSDXHS_NO = 1 (no diagnosis of MCI or dementia)."""
        return self.form.get_value("dsdxhs_no", int) == 1

    def __gate_ne_1(self, gate: str) -> bool:
        """Whether GATE ne 1."""
        return self.form.get_value(gate, int) != 1

    def _missingness_dsdxhs_mci(self) -> int:
        """Handles missingness for DSDXHS_MCI; 0 if DSDXHS_NO = 1."""
        return self.__handle_skipped("dsdxhs_mci", self.__no_dx_history(), 0)

    def _missingness_dsdxhs_dem(self) -> int:
        """Handles missingness for DSDXHS_DEM; 0 if DSDXHS_NO = 1."""
        return self.__handle_skipped("dsdxhs_dem", self.__no_dx_history(), 0)

    def _missingness_dsmcimo(self) -> int:
        """Handles missingness for DSMCIMO; 88 if DSDXHS_MCI ne 1."""
        return self.__handle_skipped("dsmcimo", self.__gate_ne_1("dsdxhs_mci"), 88)

    def _missingness_dsmciyr(self) -> int:
        """Handles missingness for DSMCIYR; 8888 if DSDXHS_MCI ne 1."""
        return self.__handle_skipped("dsmciyr", self.__gate_ne_1("dsdxhs_mci"), 8888)

    def _missingness_dsdemmo(self) -> int:
        """Handles missingness for DSDEMMO; 88 if DSDXHS_DEM ne 1."""
        return self.__handle_skipped("dsdemmo", self.__gate_ne_1("dsdxhs_dem"), 88)

    def _missingness_dsdemyr(self) -> int:
        """Handles missingness for DSDEMYR; 8888 if DSDXHS_DEM ne 1."""
        return self.__handle_skipped("dsdemyr", self.__gate_ne_1("dsdxhs_dem"), 8888)

    def _missingness_dsdxby(self) -> int:
        """Handles missingness for DSDXBY; 8 if DSDXHS_NO = 1."""
        return self.__handle_skipped("dsdxby", self.__no_dx_history(), 8)

    def _missingness_dsonstmo(self) -> int:
        """Handles missingness for DSONSTMO; 88 if DSDXHS_NO = 1."""
        return self.__handle_skipped("dsonstmo", self.__no_dx_history(), 88)

    def _missingness_dsonstyr(self) -> int:
        """Handles missingness for DSONSTYR; 8888 if DSDXHS_NO = 1."""
        return self.__handle_skipped("dsonstyr", self.__no_dx_history(), 8888)

    def _missingness_dsrepmo(self) -> int:
        """Handles missingness for DSREPMO; 888 if DSRE_REP ne 1."""
        return self.__handle_skipped("dsrepmo", self.__gate_ne_1("dsre_rep"), 888)
