"""Class to handle B9-specific missingness values."""

from typing import List, Optional

from .missingness_uds import UDSMissingness


class UDSFormB9Missingness(UDSMissingness):
    def _handle_cascading_gates(
        self, gates: List[str], field: str, missingness_value: int
    ) -> Optional[int]:
        """Handle cascading gates, all of which specify:

        If GATE = 0, then VAR must be MISSINGNESS_VALUE
        If no conditions apply, return generic missingness.
        """
        for gate in gates:
            if self.uds.get_value(gate, int) == 0:
                return missingness_value

        return self.generic_missingness(field)

    #################
    # DECCLCOG GATES #
    ##################

    def _missingness_decclcog(self) -> Optional[int]:
        """Handles missingness for decclcog.

        MUST BE HANDLED FIRST
        """
        return self._handle_cascading_gates(["decclin"], "decclcog", 0)

    def _missingness_cogmem(self) -> Optional[int]:
        """Handles missingness for COGMEM."""
        return self._handle_cascading_gates(["decclin", "decclcog"], "cogmem", 0)

    def _missingness_corogi(self) -> Optional[int]:
        """Handles missingness for COROGI."""
        return self._handle_cascading_gates(["decclin", "decclcog"], "corogi", 0)

    def _missingness_cogjudg(self) -> Optional[int]:
        """Handles missingness for COGJUDG."""
        return self._handle_cascading_gates(["decclin", "decclcog"], "cogjudg", 0)

    def _missingness_coglang(self) -> Optional[int]:
        """Handles missingness for COGLANG."""
        return self._handle_cascading_gates(["decclin", "decclcog"], "coglang", 0)

    def _missingness_cogvis(self) -> Optional[int]:
        """Handles missingness for COGVIS."""
        return self._handle_cascading_gates(["decclin", "decclcog"], "cogvis", 0)

    def _missingness_cogattn(self) -> Optional[int]:
        """Handles missingness for COGATTN."""
        return self._handle_cascading_gates(["decclin", "decclcog"], "cogattn", 0)

    def _missingness_cogfluc(self) -> Optional[int]:
        """Handles missingness for COGFLUC."""
        return self._handle_cascading_gates(["decclin", "decclcog"], "cogfluc", 0)

    def _missingness_cogothr(self) -> Optional[int]:
        """Handles missingness for COGOTHR."""
        return self._handle_cascading_gates(["decclin", "decclcog"], "cogothr", 0)

    def _missingness_cogmode(self) -> Optional[int]:
        """Handles missingness for COGMODE."""
        return self._handle_cascading_gates(["decclin", "decclcog"], "cogmode", 0)

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
        return self._handle_cascading_gates(["decclin", "decclbe"], "beapathy", 0)

    def _missingness_bedep(self) -> Optional[int]:
        """Handles missingness for BEDEP."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "bedep", 0)

    def _missingness_beanx(self) -> Optional[int]:
        """Handles missingness for BEANX."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beanx", 0)

    def _missingness_beeuph(self) -> Optional[int]:
        """Handles missingness for BEEUPH."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beeuph", 0)

    def _missingness_beirrit(self) -> Optional[int]:
        """Handles missingness for BEIRRIT."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beirrit", 0)

    def _missingness_beagit(self) -> Optional[int]:
        """Handles missingness for BEAGIT."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beagit", 0)

    def _missingness_bevhall(self) -> Optional[int]:
        """Handles missingness for BEVHALL."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "bevhall", 0)

    def _missingness_bevpatt(self) -> Optional[int]:
        """Handles missingness for BEVPATT."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "bevpatt", 0)

    def _missingness_bevwell(self) -> Optional[int]:
        """Handles missingness for BEVWELL."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "bevwell", 0)

    def _missingness_beahall(self) -> Optional[int]:
        """Handles missingness for BEAHALL."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beahall", 0)

    def _missingness_beahsimp(self) -> Optional[int]:
        """Handles missingness for BEAHSIMP."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beahsimp", 0)

    def _missingness_beahcomp(self) -> Optional[int]:
        """Handles missingness for BEAHCOMP."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beahcomp", 0)

    def _missingness_bedel(self) -> Optional[int]:
        """Handles missingness for BEDEL."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "bedel", 0)

    def _missingness_beaggrs(self) -> Optional[int]:
        """Handles missingness for BEAGGRS."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beaggrs", 0)

    def _missingness_bedisin(self) -> Optional[int]:
        """Handles missingness for BEDISIN."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "bedisin", 0)

    def _missingness_beperch(self) -> Optional[int]:
        """Handles missingness for BEPERCH."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beperch", 0)

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

    def _missingness_berem(self) -> Optional[int]:
        """Handles missingness for BEREM."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "berem", 0)

    def _missingness_beremconf(self) -> Optional[int]:
        """Handles missingness for BEREMCONF."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beremconf", 0)

    def _missingness_beothr(self) -> Optional[int]:
        """Handles missingness for BEOTHR."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "beothr", 0)

    def _missingness_bemode(self) -> Optional[int]:
        """Handles missingness for BEMODE."""
        return self._handle_cascading_gates(["decclin", "decclbe"], "bemode", 0)

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
        return self._handle_cascading_gates(["decclin", "decclmot"], "mogait", 0)

    def _missingness_mofalls(self) -> Optional[int]:
        """Handles missingness for MOFALLS."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "mofalls", 0)

    def _missingness_moslow(self) -> Optional[int]:
        """Handles missingness for MOSLOW."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "moslow", 0)

    def _missingness_motrem(self) -> Optional[int]:
        """Handles missingness for MOTREM."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "motrem", 0)

    def _missingness_molimb(self) -> Optional[int]:
        """Handles missingness for MOLIMB."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "molimb", 0)

    def _missingness_moface(self) -> Optional[int]:
        """Handles missingness for MOFACE."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "moface", 0)

    def _missingness_mospeech(self) -> Optional[int]:
        """Handles missingness for MOSPEECH."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "mospeech", 0)

    def _missingness_momode(self) -> Optional[int]:
        """Handles missingness for MOMODE."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "momode", 0)

    def _missingness_momopark(self) -> Optional[int]:
        """Handles missingness for MOMOPARK."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "momopark", 0)

    def _missingness_momoals(self) -> Optional[int]:
        """Handles missingness for MOMOALS."""
        return self._handle_cascading_gates(["decclin", "decclmot"], "momoals", 0)

    ###########################################
    # If DECCLIN = 0, the following must be 8 #
    ###########################################

    def _missingness_course(self) -> Optional[int]:
        """Handles missingness for COURSE."""
        return self._handle_cascading_gates(["decclin"], "course", 8)

    def _missingness_frstchg(self) -> Optional[int]:
        """Handles missingness for FRSTCHG. Has two rules:

        1. If DECCLIN = 0, VAR must be 8
        2. If VAR = 777, Var must be equal to
        """
        if self.uds.get_value("decclin", int) == 0:
            return self._handle_cascading_gates(["decclin"], "frstchg", 8)

        return self.handle_prev_visit("frstchg")

    ###############################################
    # If VAR is blank, tn VAR should remain blank #
    ###############################################

    def _missingness_cogothrx(self) -> Optional[str]:
        """Handles missingness for COGOTHRX."""
        return self.generic_writein("cogothrx")

    def _missingness_cogmodex(self) -> Optional[str]:
        """Handles missingness for COGMODEX."""
        return self.generic_writein("cogmodex")

    def _missingness_othsubusex(self) -> Optional[str]:
        """Handles missingness for OTHSUBUSEX."""
        return self.generic_writein("othsubusex")

    def _missingness_beothrx(self) -> Optional[str]:
        """Handles missingness for BEOTHRX."""
        return self.generic_writein("beothrx")

    def _missingness_bemodex(self) -> Optional[str]:
        """Handles missingness for BEMODEX."""
        return self.generic_writein("bemodex")

    def _missingness_momodex(self) -> Optional[str]:
        """Handles missingness for MOMODEX."""
        return self.generic_writein("momodex")

    ######################################################
    # If VAR = 777, then VAR = value from previous visit #
    ######################################################

    def handle_prev_visit(self, field: str, prev_code: int = 777) -> Optional[int]:
        """Handle when the value is provided by the previous visit.

        If VAR == PREV_CODE, VAR must be equal to PREV_VISIT. ELIF VAR
        is not blank and not PREV_CODE, return None (do not override)
        ELSE generic missingness
        """
        value = self.uds.get_value(field, int)
        if value == prev_code and self.prev_record is not None:
            prev_value = self.prev_record.get_resolved_value(
                field, int, prev_code=prev_code
            )
            if prev_value is not None:
                return prev_value

        elif value is not None:
            return None

        return self.generic_missingness(field)

    def _missingness_behage(self) -> Optional[int]:
        """Handles missingness for BEHAGE."""
        return self.handle_prev_visit("behage")

    def _missingness_psychage(self) -> Optional[int]:
        """Handles missingness for PSYCHAGE."""
        return self.handle_prev_visit("psychage")

    def _missingness_perchage(self) -> Optional[int]:
        """Handles missingness for PERCHAGE."""
        return self.handle_prev_visit("perchage")

    def _missingness_beremago(self) -> Optional[int]:
        """Handles missingness for BEREMAGO."""
        return self.handle_prev_visit("beremago")

    def _missingness_motorage(self) -> Optional[int]:
        """Handles missingness for MOTORAGE."""
        return self.handle_prev_visit("motorage")

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

        return self.generic_missingness(field)

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
