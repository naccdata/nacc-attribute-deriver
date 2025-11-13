# ruff: noqa: SIM114
"""Class to handle B9-specific missingness values.

This form has a lot of weird legacy recode logic. Stuff related to B9CHG
in particular is extremely odd.
"""

from typing import List, Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.attributes.namespace.namespace import WorkingNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)


class UDSFormB9Missingness(UDSMissingness):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table=table)

        # to grab the last time a variable was ever set,
        # not necessarily previous form
        self.__working = WorkingNamespace(table=table)

        # b9chg is used extensively in V1 missingness logic
        self.__b9chg = self.uds.get_value("b9chg", int)

    def __handle_b9_prev_value(
        self, field: str, prev_code: int = 777, default: Optional[int] = None
    ) -> Optional[int]:
        """B9 potentially pulls across multiple visits to get the last time the
        field was ever set, so need to pass the working namespace."""
        return self.handle_prev_visit(
            field, int, prev_code=prev_code, default=default, working=self.__working
        )

    def _handle_cascading_gates(
        self,
        gates: List[str],
        field: str,
        missingness_value: int,
        skip_generic: bool = False,
        default: Optional[int] = None,
    ) -> Optional[int]:
        """Handle cascading gates, all of which specify:

        If GATE = 0, then VAR must be MISSINGNESS_VALUE
        If no conditions apply, return generic missingness.
        """
        for gate in gates:
            if self.uds.get_value(gate, int) == 0:
                return missingness_value

        # some need to do more logic before it hits the generic
        # missingness case
        if skip_generic:
            return None

        return self.generic_missingness(field, int, default=default)

    ########################################
    # DECCLCOG GATES - Cognitive variables #
    ########################################

    def _missingness_decclcog(self) -> Optional[int]:
        """Handles missingness for decclcog.

        MUST BE HANDLED FIRST
        """
        if self.__check_v3_distinction("decclcog"):
            return INFORMED_MISSINGNESS

        return self._handle_cascading_gates(["decclin"], "decclcog", 0)

    def __handle_cognitive_variables(
        self,
        gates: List[str],
        field: str,
        missingness_value: int = 0,
        skip_prev_check: bool = False,
    ) -> Optional[int]:
        """Handle cognitive varialbes, which have some weird recoding logic in
        V1 for FVP."""
        if self.formver == 1 and not self.uds.is_initial():
            return self.__handle_cognitive_v1_fvp(field, skip_prev_check)

        return self._handle_cascading_gates(gates, field, missingness_value)

    def _missingness_cogmem(self) -> Optional[int]:
        """Handles missingness for COGMEM."""
        return self.__handle_cognitive_variables(
            ["decclin", "decclcog"], "cogmem", 0, skip_prev_check=True
        )

    def _missingness_cogjudg(self) -> Optional[int]:
        """Handles missingness for COGJUDG."""
        return self.__handle_cognitive_variables(["decclin", "decclcog"], "cogjudg", 0)

    def _missingness_coglang(self) -> Optional[int]:
        """Handles missingness for COGLANG."""
        return self.__handle_cognitive_variables(["decclin", "decclcog"], "coglang", 0)

    def _missingness_cogvis(self) -> Optional[int]:
        """Handles missingness for COGVIS."""
        return self.__handle_cognitive_variables(["decclin", "decclcog"], "cogvis", 0)

    def _missingness_cogattn(self) -> Optional[int]:
        """Handles missingness for COGATTN."""
        return self.__handle_cognitive_variables(["decclin", "decclcog"], "cogattn", 0)

    def _missingness_cogothr(self) -> Optional[int]:
        """Handles missingness for COGOTHR."""
        return self.__handle_cognitive_variables(
            ["decclin", "decclcog"], "cogothr", 0, skip_prev_check=True
        )

    def _missingness_cogmode(self) -> Optional[int]:
        """Handles missingness for COGMODE."""
        if self.formver < 3:
            result = self.__handle_xmode_v1("cogmode")
            if result is not None:
                return result

        return self._handle_cascading_gates(["decclin", "decclcog"], "cogmode", 0)

    def _missingness_cogfluc(self) -> Optional[int]:
        """Handles missingness for COGFLUC."""
        # this explicitly checks for blanks, not just 0 like the usual
        cogfluc = self.uds.get_value("cogfluc", int)
        decclcog = self.uds.get_value("decclcog", int)
        if self.formver < 4 and decclcog is None and cogfluc is None:
            return INFORMED_MISSINGNESS

        gate_list = ["decclcog"] if self.formver < 4 else ["decclin", "decclcog"]
        default = 0 if self.formver < 4 else None

        return self._handle_cascading_gates(gate_list, "cogfluc", 0, default=default)

    def _missingness_cogori(self) -> Optional[int]:
        """Handles missingness for COGORI."""
        if self.__check_v3_distinction("cogori"):
            return INFORMED_MISSINGNESS

        return self._handle_cascading_gates(["decclin", "decclcog"], "cogori", 0)

    ######################################
    # DECCLBE GATES - Behavior variables #
    ######################################

    def _missingness_decclbe(self) -> Optional[int]:
        """Handles missingness for DECCLBE.

        MUST BE HANDLED FIRST.
        """
        if self.__check_v3_distinction("decclbe"):
            return INFORMED_MISSINGNESS

        return self._handle_cascading_gates(["decclin"], "decclbe", 0)

    def __handle_behavior_variables(
        self, gates: List[str], field: str, missingness_value: int = 0
    ) -> Optional[int]:
        """Handle behavior varialbes, which have some weird recoding logic in
        V1."""
        if self.formver == 1 and not self.uds.is_initial():
            return self.__handle_behavior_motor_v1_fvp(field)

        return self._handle_cascading_gates(gates, field, missingness_value)

    def _missingness_beapathy(self) -> Optional[int]:
        """Handles missingness for BEAPATHY."""
        return self.__handle_behavior_variables(["decclin", "decclbe"], "beapathy", 0)

    def _missingness_bedep(self) -> Optional[int]:
        """Handles missingness for BEDEP."""
        return self.__handle_behavior_variables(["decclin", "decclbe"], "bedep", 0)

    def _missingness_beirrit(self) -> Optional[int]:
        """Handles missingness for BEIRRIT."""
        return self.__handle_behavior_variables(["decclin", "decclbe"], "beirrit", 0)

    def _missingness_beagit(self) -> Optional[int]:
        """Handles missingness for BEAGIT."""
        return self.__handle_behavior_variables(["decclin", "decclbe"], "beagit", 0)

    def _missingness_bevhall(self) -> Optional[int]:
        """Handles missingness for BEVHALL."""
        return self.__handle_behavior_variables(["decclin", "decclbe"], "bevhall", 0)

    def _missingness_beahall(self) -> Optional[int]:
        """Handles missingness for BEAHALL."""
        return self.__handle_behavior_variables(["decclin", "decclbe"], "beahall", 0)

    def _missingness_bedel(self) -> Optional[int]:
        """Handles missingness for BEDEL."""
        return self.__handle_behavior_variables(["decclin", "decclbe"], "bedel", 0)

    def _missingness_bedisin(self) -> Optional[int]:
        """Handles missingness for BEDISIN."""
        return self.__handle_behavior_variables(["decclin", "decclbe"], "bedisin", 0)

    def _missingness_beperch(self) -> Optional[int]:
        """Handles missingness for BEPERCH."""
        return self.__handle_behavior_variables(["decclin", "decclbe"], "beperch", 0)

    def _missingness_beothr(self) -> Optional[int]:
        """Handles missingness for BEOTHR."""
        result = self.__handle_behavior_variables(["decclin", "decclbe"], "beothr", 0)
        if result is None:
            if self.uds.get_value("beothr", int) == 9:
                return 0

        return result

    def _missingness_bemode(self) -> Optional[int]:
        """Handles missingness for BEMODE."""
        if self.formver < 3:
            result = self.__handle_xmode_v1("bemode")
            if result is not None:
                return result

        return self._handle_cascading_gates(["decclin", "decclbe"], "bemode", 0)

    def _missingness_berem(self) -> Optional[int]:
        """Handles missingness for BEREM."""
        # this explicitly checks for blanks, not just 0 like the usual
        berem = self.uds.get_value("berem", int)
        decclbe = self.uds.get_value("decclbe", int)
        if self.formver < 4 and decclbe is None and berem is None:
            return INFORMED_MISSINGNESS

        gate_list = ["decclbe"] if self.formver < 4 else ["decclin", "decclbe"]
        default = 0 if self.formver < 4 else None

        return self._handle_cascading_gates(gate_list, "berem", 0, default=default)

    def _missingness_bevwell(self) -> Optional[int]:
        """Handles missingness for BEVWELL.

        In the SAS code there is a check on RBEVHALL, RDECCLIN, and
        RDECCLBE. Not clear what this is, is it different from P_X vars
        (prev)?
        """
        # this explicitly checks for blanks, not just 0 like the usual
        bevwell = self.uds.get_value("bevwell", int)
        decclbe = self.uds.get_value("decclbe", int)
        if self.formver < 4 and decclbe is None and bevwell is None:
            return INFORMED_MISSINGNESS

        gate_list = ["decclbe"] if self.formver < 4 else ["decclin", "decclbe"]
        default = 0 if self.formver < 4 else None
        return self._handle_cascading_gates(gate_list, "bevwell", 0, default=default)

    def _missingness_beanx(self) -> Optional[int]:
        """Handles missingness for BEANX."""
        if self.__check_v3_distinction("beanx"):
            return INFORMED_MISSINGNESS

        return self._handle_cascading_gates(["decclin", "decclbe"], "beanx", 0)

    def _missingness_bevpatt(self) -> Optional[int]:
        """Handles missingness for BEVPATT."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "bevpatt", 0)

    def _missingness_beeuph(self) -> Optional[int]:
        """Handles missingness for BEEUPH."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beeuph", 0)

    def _missingness_beahsimp(self) -> Optional[int]:
        """Handles missingness for BEAHSIMP."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beahsimp", 0)

    def _missingness_beahcomp(self) -> Optional[int]:
        """Handles missingness for BEAHCOMP."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beahcomp", 0)

    def _missingness_beaggrs(self) -> Optional[int]:
        """Handles missingness for BEAGGRS."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beaggrs", 0)

    def _missingness_beempath(self) -> Optional[int]:
        """Handles missingness for BEEMPATH."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beempath", 0)

    def _missingness_beobcom(self) -> Optional[int]:
        """Handles missingness for BEOBCOM."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beobcom", 0)

    def _missingness_beanger(self) -> Optional[int]:
        """Handles missingness for BEANGER."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beanger", 0)

    def _missingness_besubab(self) -> Optional[int]:
        """Handles missingness for BESUBAB."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "besubab", 0)

    def _missingness_beremconf(self) -> Optional[int]:
        """Handles missingness for BEREMCONF."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beremconf", 0)

    ####################################
    # DECCLMOT GATES - motor variables #
    ####################################

    def _missingness_decclmot(self) -> Optional[int]:
        """Handles missingness for DECCLMOT.

        MUST BE HANDLED FIRST.
        """
        if self.__check_v3_distinction("decclmot"):
            return INFORMED_MISSINGNESS

        return self._handle_cascading_gates(["decclin"], "decclmot", 0)

    def __handle_motor_variables(
        self, gates: List[str], field: str, missingness_value: int = 0
    ) -> Optional[int]:
        """Handle motor varialbes, which have some weird recoding logic in
        V1."""
        if self.formver == 1 and not self.uds.is_initial():
            return self.__handle_behavior_motor_v1_fvp(field)

        return self._handle_cascading_gates(gates, field, missingness_value)

    def _missingness_mogait(self) -> Optional[int]:
        """Handles missingness for MOGAIT."""
        return self.__handle_motor_variables(["decclin", "decclmot"], "mogait", 0)

    def _missingness_mofalls(self) -> Optional[int]:
        """Handles missingness for MOFALLS."""
        return self.__handle_motor_variables(["decclin", "decclmot"], "mofalls", 0)

    def _missingness_moslow(self) -> Optional[int]:
        """Handles missingness for MOSLOW."""
        return self.__handle_motor_variables(["decclin", "decclmot"], "moslow", 0)

    def _missingness_motrem(self) -> Optional[int]:
        """Handles missingness for MOTREM."""
        return self.__handle_motor_variables(["decclin", "decclmot"], "motrem", 0)

    def _missingness_momode(self) -> Optional[int]:
        """Handles missingness for MOMODE."""
        if self.formver < 3:
            result = self.__handle_xmode_v1("momode")
            if result is not None:
                return result

        return self._handle_cascading_gates(["decclin", "decclmot"], "momode", 0)

    def _missingness_molimb(self) -> Optional[int]:
        """Handles missingness for MOLIMB."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "molimb", 0)

    def _missingness_moface(self) -> Optional[int]:
        """Handles missingness for MOFACE."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "moface", 0)

    def _missingness_mospeech(self) -> Optional[int]:
        """Handles missingness for MOSPEECH."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "mospeech", 0)

    def _missingness_momopark(self) -> Optional[int]:
        """Handles missingness for MOMOPARK."""
        # REGRESSION: SAS code has this line
        # %recode4g(gvar=b9formver,varlist=MOMOPARK,qvalue=.,result=-4,vallist=%str(1,2,3,3.2));
        # which ALWAYS sets momopark to -4 if it's missing at all
        # seems like an error/weird but allowing for now for regression tests
        # once we remove this, MOMOPARK usually = 0 in these cases
        if self.uds.get_value("momopark", int) is None:
            return -4

        result = self._handle_cascading_gates(["decclin", "decclmot"], "momopark", 0)
        if result is None:
            if self.uds.get_value("momopark", int) == 88:
                return 8

        return result

    def _missingness_momoals(self) -> Optional[int]:
        """Handles missingness for MOMOALS."""
        if self.__check_v3_distinction("momoals"):
            return INFORMED_MISSINGNESS

        return_value = 8 if self.formver < 4 else 0
        return self._handle_cascading_gates(
            ["decclin", "decclmot"], "momoals", return_value
        )

    ###########################################
    # If DECCLIN = 0, the following must be 8 #
    ###########################################

    def _missingness_course(self) -> Optional[int]:
        """Handles missingness for COURSE."""
        if self.formver < 4:
            course = None
            if self.formver == 1:
                course = self._handle_recodecbm("course", overall=True)

            if course is not None:
                return course
            if self.__b9chg in [1, 3]:
                return 9

        return self._handle_cascading_gates(["decclin"], "course", 8)

    def _missingness_frstchg(self) -> Optional[int]:
        """Handles missingness for FRSTCHG. Has two rules:

        1. If DECCLIN = 0, VAR must be 8
        2. If VAR = 777, Var must be equal to
        """
        # legacy code - this is very weird
        # in general, I feel like a lot of the logic related to b9chg
        # could be handled differently, but trying to make it match
        # once things are more stable we can rework this
        if self.formver < 4:
            frstchg = None
            if self.formver == 1:
                frstchg = self._handle_recodecbm("frstchg", overall=True)

            if frstchg is None:
                frstchg = self.uds.get_value("frstchg", int)
                if frstchg is None and self.__b9chg in [1, 3]:
                    frstchg = 9

            if frstchg == 0:
                p_frstchg = self.__get_last_set("frstchg")
                if p_frstchg is not None:
                    return p_frstchg
                return 9

            if frstchg is not None:
                return frstchg

        result = self._handle_cascading_gates(
            ["decclin"], "frstchg", 8, skip_generic=True
        )
        if result is not None:
            return result

        return self.__handle_b9_prev_value("frstchg")

    ######################################################
    # If VAR = 777, then VAR = value from previous visit #
    ######################################################

    def _missingness_behage(self) -> Optional[int]:
        """Handles missingness for BEHAGE."""
        return self.__handle_b9_prev_value("behage")

    def _missingness_psychage(self) -> Optional[int]:
        """Handles missingness for PSYCHAGE."""
        return self.__handle_b9_prev_value("psychage")

    def _missingness_perchage(self) -> Optional[int]:
        """Handles missingness for PERCHAGE."""
        return self.__handle_b9_prev_value("perchage")

    def _missingness_motorage(self) -> Optional[int]:
        """Handles missingness for MOTORAGE."""
        return self.__handle_b9_prev_value("motorage")

    def __handle_prev_with_gate(self, gate: str, field: str) -> Optional[int]:
        """From b9structrdd.sas.

        If GATE = 1, return PREV_FIELD
        If GATE is None, 0, 9, return 888
        """
        if self.__check_v3_distinction(field):
            return INFORMED_MISSINGNESS

        # it seems these specific variables are
        # set to 888 if the below conditions aren't fulfilled,
        # they are are blank, and it's V3
        default = 888 if self.formver == 3 else None

        gate_value = self.uds.get_value(gate, int)
        if gate_value == 1:
            return self.__handle_b9_prev_value(field, default=default)
        if gate_value is None or gate_value in [0, 9]:
            return 888

        return self.generic_missingness(field, int, default=default)

    def _missingness_cogflago(self) -> Optional[int]:
        """Handles missingness for COGFLAGO."""
        # # TODO: extra recode logic in SAS - do we need?
        # if self.uds.get_value("decclcog", int) == 0:
        #     return 888
        return self.__handle_prev_with_gate("cogfluc", "cogflago")

    def _missingness_bevhago(self) -> Optional[int]:
        """Handles missingness for BEVHAGO."""
        return self.__handle_prev_with_gate("bevhall", "bevhago")

    def _missingness_beage(self) -> Optional[int]:
        """Handles missingness for BEAGE."""
        return self.__handle_prev_with_gate("decclbe", "beage")

    def _missingness_parkage(self) -> Optional[int]:
        """Handles missingness for PARKAGE."""
        return self.__handle_prev_with_gate("momopark", "parkage")

    def _missingness_alsage(self) -> Optional[int]:
        """Handles missingness for ALSAGE."""
        return self.__handle_prev_with_gate("momoals", "alsage")

    def _missingness_moage(self) -> Optional[int]:
        """Handles missingness for MOAGE."""
        return self.__handle_prev_with_gate("decclmot", "moage")

    def _missingness_beremago(self) -> Optional[int]:
        """Handles missingness for BEREMAGO."""
        if self.formver < 4:
            return self.__handle_prev_with_gate("berem", "beremago")

        return self.__handle_b9_prev_value("beremago")

    #######################################################
    # If BESUBAB =1 and VAR is blank, then VAR should = 0 #
    #######################################################

    def _handle_besubab_gate(self, field: str) -> Optional[int]:
        """Handles missingness values gated by BESUBAB:

        If BESUBAB =1 and VAR is blank, then VAR should = 0

        If condition does not apply, return generic missingness.
        """
        besubab = self.uds.get_value("besubab", int)
        value = self.uds.get_value(field, int)
        if besubab == 1 and value is None:
            return 0

        return self.generic_missingness(field, int)

    def _missingness_alcuse(self) -> Optional[int]:
        """Handles missingness for ALCUSE."""
        return self._handle_besubab_gate("alcuse")

    def _missingness_seduse(self) -> Optional[int]:
        """Handles missingness for SEDUSE."""
        return self._handle_besubab_gate("seduse")

    def _missingness_opiateuse(self) -> Optional[int]:
        """Handles missingness for OPIATEUSE."""
        return self._handle_besubab_gate("opiateuse")

    def _missingness_cocaineuse(self) -> Optional[int]:
        """Handles missingness for COCAINEUSE."""
        return self._handle_besubab_gate("cocaineuse")

    def _missingness_cannabuse(self) -> Optional[int]:
        """Handles missingness for CANNABUSE."""
        return self._handle_besubab_gate("cannabuse")

    def _missingness_othsubuse(self) -> Optional[int]:
        """Handles missingness for OTHSUBUSE."""
        return self._handle_besubab_gate("othsubuse")

    #######################################
    # Derived variable-related fields and #
    # variables we need to pull through   #
    #######################################

    def _missingness_mofrst(self) -> Optional[int]:
        """Handles missingness for MOFRST."""
        prev_code = 0 if self.formver == 3 else None
        return self.handle_prev_visit("mofrst", int, prev_code=prev_code)

    def _missingness_befpred(self) -> Optional[int]:
        """Handles missingness for BEFPRED."""
        if self.__check_v3_distinction("befpred"):
            return INFORMED_MISSINGNESS

        prev_code = 0 if self.formver == 3 else None
        return self.handle_prev_visit("befpred", int, prev_code=prev_code)

    def _missingness_cogfpred(self) -> Optional[int]:
        """Handles missingness for COGFPRED."""
        if self.__check_v3_distinction("cogfpred"):
            return INFORMED_MISSINGNESS

        prev_code = 0 if self.formver == 3 else None
        return self.handle_prev_visit("cogfpred", int, prev_code=prev_code)

    def _missingness_befrst(self) -> Optional[int]:
        """Handles missingness for BEFRST."""
        return self.handle_prev_visit("befrst", int)

    def _missingness_cogfrst(self) -> Optional[int]:
        """Handles missingness for COGFRST."""
        return self.handle_prev_visit("cogfrst", int)

    def _missingness_decclin(self) -> Optional[int]:
        """Handles missingness for DECCLIN."""
        if self.formver == 1:
            if self.__b9chg == 3:
                return 1
            if self.__b9chg == 1:
                return self.handle_prev_visit("decclin", int)

        return self.handle_prev_visit("decclin", int)

    #########
    # Other #
    #########

    def __get_last_set(self, field: str) -> Optional[int]:
        """B9 potentially pulls across multiple visits to get the last time the
        field was ever set, so need to pass the working namespace."""
        return self.get_prev_value(field, int, working=self.__working)

    def _missingness_decage(self) -> Optional[int]:
        """Handles missingness for DECAGE.

        See b9structrdd.sas.
        """
        decage = self.uds.get_value("decage", int)

        # SAS checks overall for DECAGE = 777
        if decage == 777:
            return self.__handle_b9_prev_value("decage")

        if decage is not None:
            return None

        if self.formver == 1 and not self.uds.is_initial():
            b9chg = self.uds.get_value("b9chg", int)
            p_decclin = None
            p_decage = None

            if self.prev_record:
                p_decclin = self.__get_last_set("decclin")
                p_decage = self.__get_last_set("decage")

            if b9chg in [1, 3] and p_decclin == 1:
                if p_decage is not None:
                    return p_decage

                return 999

        cog_attr = self.uds.group_attributes(
            [
                "cogmem",
                "cogori",
                "cogjudg",
                "coglang",
                "cogvis",
                "cogattn",
                "cogfluc",
                "cogothr",
            ],
            int,
        )
        if any(x != 1 for x in cog_attr):
            return 888

        return INFORMED_MISSINGNESS

    #############################################
    # V1-specific logic related to B9CHG in FVP #
    # See b9structrdd.sas                       #
    #############################################

    def _handle_recodecbm(self, field: str, overall: bool = False) -> Optional[int]:
        """This is an attempt at translating the recodecbm (recode cognitive,
        behavior, and motor) macro that is found in b9structrdd.sas. It is
        heavily based on B9CHG and DECCLIN.

        Returns None of the value was not recoded, otherwise the recoded
        value.
        """
        p_decclin = self.__get_last_set("decclin")
        p_value = self.__get_last_set(field)

        decclin = self.uds.get_value("decclin", int)
        value = self.uds.get_value(field, int)

        if not overall:
            if self.__b9chg == 1 and value is None:
                if p_decclin == 0:
                    return 0
                if p_decclin == 1:
                    return p_value
            if self.__b9chg == 2 and decclin == 0 and value != 1:
                return 0
        else:
            if self.__b9chg in [1, 3] and value is None:
                if p_decclin == 0:
                    return 8
                if p_decclin == 1:
                    return p_value
            if self.__b9chg == 2 and decclin == 0 and value != 1:
                return 8

        return None

    def __handle_cognitive_v1_fvp(
        self, field: str, skip_prev_check: bool = False
    ) -> Optional[int]:
        """Handles recoding of cognitive variables in V1 on FVP."""
        value = self._handle_recodecbm(field)
        if value is not None:
            return value

        if value is None and not skip_prev_check:
            p_decclin = self.__get_last_set("decclin")
            p_field = self.__get_last_set(field)

            if p_decclin == 1 and p_field == 9:
                return 9

        return self.generic_missingness(field, int)

    def __handle_behavior_motor_v1_fvp(self, field: str) -> Optional[int]:
        """Handles recoding of behavior/motor variables in V1 on FVP."""
        value = self._handle_recodecbm(field)
        if value is not None:
            return value

        p_decclin = self.__get_last_set("decclin")
        if p_decclin == 1 and self.__b9chg == 1:
            return 9

        return self.generic_missingness(field, int)

    def __handle_xmode_v1(self, field: str) -> Optional[int]:
        """Handles V1 COGMODE, BEMODE, and MOMODE.

        Returns None if the value was not recoded, recoded
        variable otherwise.

        See b9structrdd.sas. These use rdecclin, which sort of
        seems like most recent DECCLIN, but not sure how this
        is any different from pdecclin (prev DECCLIN)? For now
        omitting.
        """
        value = self.uds.get_value(field, int)
        if value == 88:
            return 0

        if self.__b9chg in [1, 3] and value is None:
            p_decclin = self.__get_last_set("decclin")
            if p_decclin == 0:
                return 0

            elif p_decclin == 1:
                p_value = self.__get_last_set(field)
                if p_value == 88:
                    return 0
                if p_value is not None:
                    return p_value

        return None

    def _missingness_decin(self) -> Optional[int]:
        """Handles missingness for DECIN."""
        # recodes to 9 on v1/v2 if blank
        decin = self.uds.get_value("decin", int)
        if self.formver < 3 and decin is None:
            return 9

        if self.formver == 1 and self.__b9chg in [1, 3]:
            return 9

        return self.generic_missingness("decin", int)

    def _missingness_decsub(self) -> Optional[int]:
        """Handles missingness for DECSUB."""
        if self.formver == 1 and self.__b9chg in [1, 3]:
            return 9

        return self.generic_missingness("decsub", int)

    def __check_v3_distinction(self, field: str) -> bool:
        """REGRESSION: I think this check is a bug in the legacy
        SAS code, as it treats 3.2 differently from 3.0 in a
        weird way since these variables DO exist in 3.2. But
        done so it isn't flagged so much in regression testing.
        Once verified, this behavior should probably be
        fixed/removed.

        Basically - if in 3.2 and blank, return -4. So this
        method returns True if it's in 3.2 and blank, else False.
        """

        raw_formver = self.uds.get_required("formver", float)
        value = self.uds.get_value(field, int)
        return raw_formver == 3.2 and value is None
