"""Class to handle B9-specific missingness values.

This form has a lot of weird legacy recode logic. Stuff related to B9CHG
in particular is extremely odd.
"""

from typing import List, Optional

from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)

from .missingness_uds import UDSMissingness


class UDSFormB9Missingness(UDSMissingness):
    def __handle_b9chg_decclin(  # noqa: C901
        self, field: str, overall: bool = False, check_88: bool = False
    ) -> Optional[int]:
        """In V1, there's some weird B9CHG recode logic with DECCLIN and its
        previous value...

        TBH I'm really not clear what this is doing, I just translated
        it verbatim. It will most definitely need to be worked on
        backwards back from regression testing
        """
        decclin = self.handle_prev_visit("decclin", int)
        b9chg = self.uds.get_value("b9chg", int)
        value = self.uds.get_value(field, int)
        prev_value = self.handle_prev_visit(field, int)

        if check_88:
            if value == 88:
                return 0

            # what are the r variables like rdecclin??????? omitting for now
            if b9chg in [1, 3] and value is None:
                if decclin == 0:
                    return 0
                if decclin == 1 and prev_value == 88:
                    return 0
                if decclin == 1 and prev_value is not None:
                    return prev_value

        if not overall:
            if b9chg == 1 and value is None:
                if decclin == 0:
                    return 0
                if decclin == 1:
                    return prev_value
            elif b9chg == 2 and decclin == 0 and value != 1:
                return 0
        else:
            if b9chg in [1, 3] and value is None:
                if decclin == 0:
                    return 8
                if decclin == 1:
                    return prev_value
            if b9chg == 2 and decclin == 0 and value != 1:
                return 8

        # the code seems to do the exact same thing in a different recode after
        # the above??? leaving out for now
        return None

    def _handle_cascading_gates(
        self,
        gates: List[str],
        field: str,
        missingness_value: int,
        run_v1: bool = False,
        overall: bool = False,
        check_88: bool = False,
    ) -> Optional[int]:
        """Handle cascading gates, all of which specify:

        If GATE = 0, then VAR must be MISSINGNESS_VALUE
        If no conditions apply, return generic missingness.
        """
        for gate in gates:
            # if gate == "decclin" and run_v1 and self.formver == 1:
            #     result = self.__handle_b9chg_decclin(
            #             field, overall=overall, check_88=check_88)
            #     if result is not None:
            #         return result

            if self.uds.get_value(gate, int) == 0:
                return missingness_value

        return self.generic_missingness(field, int)

    ##################
    # DECCLCOG GATES #
    ##################

    def _missingness_decclcog(self) -> Optional[int]:
        """Handles missingness for decclcog.

        MUST BE HANDLED FIRST
        """
        return self._handle_cascading_gates(["decclin"], "decclcog", 0)

    def _missingness_cogmem(self) -> Optional[int]:
        """Handles missingness for COGMEM."""
        return self._handle_cascading_gates(
            ["decclin", "decclcog"], "cogmem", 0, run_v1=True
        )

    def _missingness_cogjudg(self) -> Optional[int]:
        """Handles missingness for COGJUDG."""
        return self._handle_cascading_gates(
            ["decclin", "decclcog"], "cogjudg", 0, run_v1=True
        )

    def _missingness_coglang(self) -> Optional[int]:
        """Handles missingness for COGLANG."""
        return self._handle_cascading_gates(
            ["decclin", "decclcog"], "coglang", 0, run_v1=True
        )

    def _missingness_cogvis(self) -> Optional[int]:
        """Handles missingness for COGVIS."""
        return self._handle_cascading_gates(
            ["decclin", "decclcog"], "cogvis", 0, run_v1=True
        )

    def _missingness_cogattn(self) -> Optional[int]:
        """Handles missingness for COGATTN."""
        return self._handle_cascading_gates(
            ["decclin", "decclcog"], "cogattn", 0, run_v1=True
        )

    def _missingness_cogothr(self) -> Optional[int]:
        """Handles missingness for COGOTHR."""
        return self._handle_cascading_gates(
            ["decclin", "decclcog"], "cogothr", 0, run_v1=True
        )

    def _missingness_cogmode(self) -> Optional[int]:
        """Handles missingness for COGMODE."""
        return self._handle_cascading_gates(
            ["decclin", "decclcog"],
            "cogmode",
            0,
            run_v1=True,
            overall=True,
            check_88=True,
        )

    def _missingness_cogfluc(self) -> Optional[int]:
        """Handles missingness for COGFLUC."""
        gate_list = ["decclcog"] if self.formver < 4 else ["decclin", "decclcog"]
        return self._handle_cascading_gates(gate_list, "cogfluc", 0)

    def _missingness_cogori(self) -> Optional[int]:
        """Handles missingness for COGORI."""
        return self._handle_cascading_gates(["decclin", "decclcog"], "cogori", 0)

    #################
    # DECCLBE GATES #
    #################

    def _missingness_decclbe(self) -> Optional[int]:
        """Handles missingness for DECCLBE.

        MUST BE HANDLED FIRST.
        """
        return self._handle_cascading_gates(["decclin"], "decclbe", 0)

    def _missingness_beapathy(self) -> Optional[int]:
        """Handles missingness for BEAPATHY."""
        return self._handle_cascading_gates(
            ["decclin", "decclbe"], "beapathy", 0, run_v1=True
        )

    def _missingness_bedep(self) -> Optional[int]:
        """Handles missingness for BEDEP."""
        return self._handle_cascading_gates(
            ["decclin", "decclbe"], "bedep", 0, run_v1=True
        )

    def _missingness_beirrit(self) -> Optional[int]:
        """Handles missingness for BEIRRIT."""
        return self._handle_cascading_gates(
            ["decclin", "decclbe"], "beirrit", 0, run_v1=True
        )

    def _missingness_beagit(self) -> Optional[int]:
        """Handles missingness for BEAGIT."""
        return self._handle_cascading_gates(
            ["decclin", "decclbe"], "beagit", 0, run_v1=True
        )

    def _missingness_bevhall(self) -> Optional[int]:
        """Handles missingness for BEVHALL."""
        return self._handle_cascading_gates(
            ["decclin", "decclbe"], "bevhall", 0, run_v1=True
        )

    def _missingness_beahall(self) -> Optional[int]:
        """Handles missingness for BEAHALL."""
        return self._handle_cascading_gates(
            ["decclin", "decclbe"], "beahall", 0, run_v1=True
        )

    def _missingness_bedel(self) -> Optional[int]:
        """Handles missingness for BEDEL."""
        return self._handle_cascading_gates(
            ["decclin", "decclbe"], "bedel", 0, run_v1=True
        )

    def _missingness_bedisin(self) -> Optional[int]:
        """Handles missingness for BEDISIN."""
        return self._handle_cascading_gates(
            ["decclin", "decclbe"], "bedisin", 0, run_v1=True
        )

    def _missingness_beperch(self) -> Optional[int]:
        """Handles missingness for BEPERCH."""
        return self._handle_cascading_gates(
            ["decclin", "decclbe"], "beperch", 0, run_v1=True
        )

    def _missingness_beothr(self) -> Optional[int]:
        """Handles missingness for BEOTHR."""
        return self._handle_cascading_gates(
            ["decclin", "decclbe"], "beothr", 0, run_v1=True
        )

    def _missingness_bemode(self) -> Optional[int]:
        """Handles missingness for BEMODE."""
        return self._handle_cascading_gates(
            ["decclin", "decclbe"],
            "bemode",
            0,
            run_v1=True,
            overall=True,
            check_88=True,
        )

    def _missingness_berem(self) -> Optional[int]:
        """Handles missingness for BEREM."""
        gate_list = ["decclbe"] if self.formver < 4 else ["decclin", "decclbe"]
        return self._handle_cascading_gates(gate_list, "berem", 0)

    def _missingness_bevwell(self) -> Optional[int]:
        """Handles missingness for BEVWELL."""
        gate_list = ["decclbe"] if self.formver < 4 else ["decclin", "decclbe"]
        return self._handle_cascading_gates(gate_list, "bevwell", 0)

    def _missingness_beanx(self) -> Optional[int]:
        """Handles missingness for BEANX."""
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

    ##################
    # DECCLMOT GATES #
    ##################

    def _missingness_decclmot(self) -> Optional[int]:
        """Handles missingness for DECCLMOT.

        MUST BE HANDLED FIRST.
        """
        return self._handle_cascading_gates(["decclin"], "decclmot", 0)

    def _missingness_mogait(self) -> Optional[int]:
        """Handles missingness for MOGAIT."""
        return self._handle_cascading_gates(
            ["decclin", "decclmot"], "mogait", 0, run_v1=True
        )

    def _missingness_mofalls(self) -> Optional[int]:
        """Handles missingness for MOFALLS."""
        return self._handle_cascading_gates(
            ["decclin", "decclmot"], "mofalls", 0, run_v1=True
        )

    def _missingness_moslow(self) -> Optional[int]:
        """Handles missingness for MOSLOW."""
        return self._handle_cascading_gates(
            ["decclin", "decclmot"], "moslow", 0, run_v1=True
        )

    def _missingness_motrem(self) -> Optional[int]:
        """Handles missingness for MOTREM."""
        return self._handle_cascading_gates(
            ["decclin", "decclmot"], "motrem", 0, run_v1=True
        )

    def _missingness_momode(self) -> Optional[int]:
        """Handles missingness for MOMODE."""
        return self._handle_cascading_gates(
            ["decclin", "decclmot"],
            "momode",
            0,
            run_v1=True,
            overall=True,
            check_88=True,
        )

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
        return self._handle_cascading_gates(["decclin", "decclmot"], "momopark", 0)

    def _missingness_momoals(self) -> Optional[int]:
        """Handles missingness for MOMOALS."""
        return_value = 8 if self.formver < 4 else 0
        return self._handle_cascading_gates(
            ["decclin", "decclmot"], "momoals", return_value
        )

    ###########################################
    # If DECCLIN = 0, the following must be 8 #
    ###########################################

    def _missingness_course(self) -> Optional[int]:
        """Handles missingness for COURSE."""
        return self._handle_cascading_gates(
            ["decclin"], "course", 8, run_v1=True, overall=True
        )

    def _missingness_frstchg(self) -> Optional[int]:
        """Handles missingness for FRSTCHG. Has two rules:

        1. If DECCLIN = 0, VAR must be 8
        2. If VAR = 777, Var must be equal to
        """
        # # This V1 code makes no sense to me; if we can figure out what it
        # # was intending to do this could probably be greatly simplified
        # if self.formver == 1 or self.uds.get_value("decclin", int) == 0:
        #     result = self._handle_cascading_gates(["decclin"], "frstchg", 8,
        #         run_v1=True, overall=True)

        #     if result is None:
        #         frstchg = self.uds.get_value("frstchg", int)
        #         if frstchg == 0:
        #             p_frstchg = self.handle_prev_visit("frstchg", int, prev_code=0)
        #             if p_frstchg is not None:
        #                 return p_frstchg

        #             return 9

        result = self._handle_cascading_gates(
            ["decclin"], "frstchg", 8, run_v1=True, overall=True
        )
        if result is not None:
            return result

        return self.handle_prev_visit("frstchg", int, prev_code=777)

    ######################################################
    # If VAR = 777, then VAR = value from previous visit #
    ######################################################

    def _missingness_behage(self) -> Optional[int]:
        """Handles missingness for BEHAGE."""
        return self.handle_prev_visit("behage", int, prev_code=777)

    def _missingness_psychage(self) -> Optional[int]:
        """Handles missingness for PSYCHAGE."""
        return self.handle_prev_visit("psychage", int, prev_code=777)

    def _missingness_perchage(self) -> Optional[int]:
        """Handles missingness for PERCHAGE."""
        return self.handle_prev_visit("perchage", int, prev_code=777)

    def _missingness_motorage(self) -> Optional[int]:
        """Handles missingness for MOTORAGE."""
        return self.handle_prev_visit("motorage", int, prev_code=777)

    def __handle_prev_with_gate(self, gate: str, field: str) -> Optional[int]:
        """From b9structrdd.sas.

        If GATE = 1, return PREV_FIELD
        If GATE is None, 0, 9, return 888
        """
        gate_value = self.uds.get_value(gate, int)
        if gate_value == 1:
            return self.handle_prev_visit(field, int, prev_code=777)
        if gate_value is None or gate_value in [0, 9]:
            return 888

        return self.generic_missingness(field, int)

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

        return self.handle_prev_visit("beremago", int, prev_code=777)

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
        prev_code = 0 if self.formver == 3 else None
        return self.handle_prev_visit("befpred", int, prev_code=prev_code)

    def _missingness_cogfpred(self) -> Optional[int]:
        """Handles missingness for COGFPRED."""
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
        return self.handle_prev_visit("decclin", int)

    #########
    # Other #
    #########

    def _missingness_decage(self) -> Optional[int]:
        """Handles missingness for DECAGE.

        See b9structrdd.sas.
        """
        decage = self.uds.get_value("decage", int)

        # SAS checks overall for DECAGE = 777, although not sure it could
        # ever be 777?
        if decage == 777:
            return self.handle_prev_visit("decage", int, prev_code=777)

        if decage is not None:
            return None

        if self.formver == 1 and not self.uds.is_initial():
            b9chg = self.uds.get_value("b9chg", int)
            p_decclin = None
            p_decage = None

            if self.prev_record:
                p_decclin = self.prev_record.get_resolved_value("decclin", int)
                p_decage = self.prev_record.get_resolved_value("decage", int)

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

    ###################
    # B9CHG Variables - variables related to B9CHG,
    # which seems to be mainly a 1.0 and 3.1 thing?
    ###################

    # def __missingness_b9chg(self) -> Optional[int]:
    #     """Handles missingness for B9CHG."""
    #     raw_formver = self.uds.get_required("formver", float)
    #     if raw_formver in [2.0, 3.0, 3.2]:
    #         return INFORMED_MISSINGNESS

    #     if self.uds.is_initial() and raw_formver == 1.0:
    #         return INFORMED_MISSINGNESS

    #     return self.generic_missingness("b9chg", int)

    # def __missingness_decin(self) -> Optional[int]:
    #     """Handles missingness for DECIN."""
    #     b9chg = self.uds.get_value("b9chg")
    #     if self.formver == 1 and b9chg in [1, 3]:
    #         return 9

    #     if self.formver < 3:
    #         return 9

    #     return self.generic_missingness("decin", int)

    # def __missingness_decsub(self) -> Optional[int]:
    #     """Handles missingness for DECSUB."""
    #     b9chg = self.uds.get_value("b9chg")
    #     if self.formver == 1 and b9chg in [1, 3]:
    #         return 9

    #     return self.generic_missingness("decsub", int)

    # def __missingness_decclin(self) -> Optional[int]:
    #     """Handles missingness for DECCLIN."""
    #     b9chg = self.uds.get_value("b9chg")
    #     if self.formver == 1:
    #         if b9chg == 1:
    #             return self.handle_prev_visit("decclin", int)
    #         if b9chg == 3:
    #             return 1

    #     return self.generic_missingness("decclin", int)
