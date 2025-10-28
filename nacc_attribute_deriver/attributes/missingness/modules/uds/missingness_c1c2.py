"""Class to handle C1/C2-specific missingness values.

It is arguably overkill to write a _missingness_ function for every
variable, when many could call a common rule instead (e.g. all MINTTOTS-
dependent variables could call the same rule) but due to the sheer
number of them and slight nuances I decided to be extremely explicit
here to make sure we aren't accidentally missing or duplicating any.
"""

from typing import Optional

from .missingness_uds import UDSMissingness


class UDSFormC1C2Missingness(UDSMissingness):
    ###########################
    # RESPVAL gated variables #
    ###########################

    def _handle_respval_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by RESPVAL, which generally
        follow:

        If FIELD is blank and RESPVAL in (2,3), then FIELD should = 0
        """
        value = self.uds.get_value(field, int)
        respval = self.uds.get_value("respval", int)

        if value is None and respval in [2, 3]:
            return 0

        return None

    def _missingness_resphear(self) -> Optional[int]:
        """Handles missingness for RESPHEAR."""
        return self._handle_respval_gate("resphear")

    def _missingness_respdist(self) -> Optional[int]:
        """Handles missingness for RESPDIST."""
        return self._handle_respval_gate("respdist")

    def _missingness_respintr(self) -> Optional[int]:
        """Handles missingness for RESPINTR."""
        return self._handle_respval_gate("respintr")

    def _missingness_motrem(self) -> Optional[int]:
        """Handles missingness for MOTREM."""
        return self._handle_respval_gate("motrem")

    def _missingness_respdisn(self) -> Optional[int]:
        """Handles missingness for RESPDISN."""
        return self._handle_respval_gate("respdisn")

    def _missingness_respfatg(self) -> Optional[int]:
        """Handles missingness for RESPFATG."""
        return self._handle_respval_gate("respfatg")

    def _missingness_respemot(self) -> Optional[int]:
        """Handles missingness for RESPEMOT."""
        return self._handle_respval_gate("respemot")

    def _missingness_respasst(self) -> Optional[int]:
        """Handles missingness for RESPASST."""
        return self._handle_respval_gate("respasst")

    def _missingness_respoth(self) -> Optional[int]:
        """Handles missingness for RESPOTH."""
        return self._handle_respval_gate("respoth")

    ##############################
    # VERBALTEST gated variables #
    ##############################

    def _handle_verbaltest_gate(
        self, verbal_value: int, set_value: int
    ) -> Optional[int]:
        """Handles variables gated by VERBALTEST, which generally follows the
        below logic.

        If VERBALTEST = 1/2 then FIELD should = 88/888.
        """
        if self.uds.get_value("verbaltest", int) == verbal_value:
            return set_value

        return None

    def _missingness_rey1rec(self) -> Optional[int]:
        """Handles missingness for REY1REC."""
        return self._handle_verbaltest_gate(verbal_value=2, set_value=88)

    def _missingness_reydti(self) -> Optional[int]:
        """Handles missingness for REYDTI."""
        return self._handle_verbaltest_gate(verbal_value=2, set_value=88)

    def _missingness_reymethod(self) -> Optional[int]:
        """Handles missingness for REYMETHOD."""
        return self._handle_verbaltest_gate(verbal_value=2, set_value=88)

    def _missingness_cerad1rec(self) -> Optional[int]:
        """Handles missingness for CERAD1REC."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=88)

    def _missingness_cerad1read(self) -> Optional[int]:
        """Handles missingness for CERAD1READ."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=88)

    def _missingness_cerad1int(self) -> Optional[int]:
        """Handles missingness for CERAD1INT."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=888)

    def _missingness_cerad2rec(self) -> Optional[int]:
        """Handles missingness for CERAD2REC."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=88)

    def _missingness_cerad2read(self) -> Optional[int]:
        """Handles missingness for CERAD2READ."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=88)

    def _missingness_cerad2int(self) -> Optional[int]:
        """Handles missingness for CERAD2INT."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=888)

    def _missingness_cerad3rec(self) -> Optional[int]:
        """Handles missingness for CERAD3REC."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=88)

    def _missingness_cerad3read(self) -> Optional[int]:
        """Handles missingness for CERAD3READ."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=88)

    def _missingness_cerad3int(self) -> Optional[int]:
        """Handles missingness for CERAD3INT."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=888)

    def _missingness_ceraddti(self) -> Optional[int]:
        """Handles missingness for CERADDTI."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=88)

    def _missingness_ceradj6rec(self) -> Optional[int]:
        """Handles missingness for CERADJ6REC."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=88)

    def _missingness_ceradj6int(self) -> Optional[int]:
        """Handles missingness for CERADJ6INT."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=888)

    def _missingness_ceradj7yes(self) -> Optional[int]:
        """Handles missingness for CERADJ7YES."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=88)

    def _missingness_ceradj7no(self) -> Optional[int]:
        """Handles missingness for CERADJ7NO."""
        return self._handle_verbaltest_gate(verbal_value=1, set_value=88)

    ##########################################
    # Write-in variables that rely on a gate #
    ##########################################

    def _missingness_mocalanx(self) -> Optional[str]:
        """Handles missingness for MOCALANX."""
        return self.handle_gated_writein("mocalan", 3)

    def _missingness_npsylanx(self) -> Optional[str]:
        """Handles missingness for NPSYLANX."""
        return self.handle_gated_writein("npsylan", 3)

    def _missingness_respothx(self) -> Optional[str]:
        """Handles missingness for RESPOTHX."""
        return self.handle_gated_writein("respoth", 1)

    def _missingness_mmselanx(self) -> Optional[str]:
        """Handles missingness for MMSELANX."""
        return self.handle_gated_writein("mmselan", 3)

    #######################################################
    # REYXREC gated variables - cascades across variables #
    # Relies on both VERBALTEST and an earlier variable   #
    #######################################################

    def _handle_optional_gate(self, gate: str) -> Optional[int]:
        """Generically handle:

        If GATE is in 88 or 95-98, then FIELD should = GATE.
        """
        return self.handle_set_to_gate(gate, check_values=[88, 95, 96, 97, 98])

    def _handle_reyxrec_cascade(self, gate: str) -> Optional[int]:
        """Handle the REYXREC cascading rules, e.g:

        1. The VERBALTEST check (If VERBALTEST = 2 then FIELD should = 88)
        2. If GATE is 88 or 95-98 then FIELD should = GATE
        """
        result = self._handle_verbaltest_gate(verbal_value=2, set_value=888)
        if result is None:
            result = self._handle_optional_gate(gate)

        return result

    def _missingness_reydint(self) -> Optional[int]:
        """Handles missingness for REYDINT."""
        return self._handle_reyxrec_cascade("reydrec")

    def _missingness_reytcor(self) -> Optional[int]:
        """Handles missingness for REYTCOR."""
        return self._handle_reyxrec_cascade("reydrec")

    def _missingness_reyfpos(self) -> Optional[int]:
        """Handles missingness for REYFPOS."""
        return self._handle_reyxrec_cascade("reydrec")

    def _missingness_rey1int(self) -> Optional[int]:
        """Handles missingness for REY1INT."""
        return self._handle_reyxrec_cascade("rey1rec")

    def _missingness_rey2rec(self) -> Optional[int]:
        """Handles missingness for REY2REC."""
        return self._handle_reyxrec_cascade("rey1rec")

    def _missingness_rey2int(self) -> Optional[int]:
        """Handles missingness for REY2INT."""
        return self._handle_reyxrec_cascade("rey1rec")

    def _missingness_rey3rec(self) -> Optional[int]:
        """Handles missingness for REY3REC."""
        return self._handle_reyxrec_cascade("rey2rec")

    def _missingness_rey3int(self) -> Optional[int]:
        """Handles missingness for REY3INT."""
        return self._handle_reyxrec_cascade("rey2rec")

    def _missingness_rey4rec(self) -> Optional[int]:
        """Handles missingness for REY4REC."""
        return self._handle_reyxrec_cascade("rey3rec")

    def _missingness_rey4int(self) -> Optional[int]:
        """Handles missingness for REY4INT."""
        return self._handle_reyxrec_cascade("rey3rec")

    def _missingness_rey5rec(self) -> Optional[int]:
        """Handles missingness for REY5REC."""
        return self._handle_reyxrec_cascade("rey4rec")

    def _missingness_rey5int(self) -> Optional[int]:
        """Handles missingness for REY5INT."""
        return self._handle_reyxrec_cascade("rey4rec")

    def _missingness_reybrec(self) -> Optional[int]:
        """Handles missingness for REYBREC."""
        return self._handle_reyxrec_cascade("rey5rec")

    def _missingness_reybint(self) -> Optional[int]:
        """Handles missingness for REYBINT."""
        return self._handle_reyxrec_cascade("rey5rec")

    def _missingness_rey6rec(self) -> Optional[int]:
        """Handles missingness for REY6REC."""
        return self._handle_reyxrec_cascade("reybrec")

    def _missingness_rey6int(self) -> Optional[int]:
        """Handles missingness for REY6INT."""
        return self._handle_reyxrec_cascade("reybrec")

    ##########################
    # TRAILX gated variables #
    ##########################

    def _handle_trailx_gate(self, gate: str) -> Optional[int]:
        """Generically handle:

        If GATE is 995-998 then FIELD should = GATE.
        """
        return self.handle_set_to_gate(gate, check_values=[995, 996, 997, 998])

    def _missingness_trailarr(self) -> Optional[int]:
        """Handles missingness for TRAILARR."""
        return self._handle_trailx_gate("traila")

    def _missingness_trailali(self) -> Optional[int]:
        """Handles missingness for TRAILALI."""
        return self._handle_trailx_gate("traila")

    def _missingness_trailbrr(self) -> Optional[int]:
        """Handles missingness for TRAILBRR."""
        return self._handle_trailx_gate("trailb")

    def _missingness_trailbli(self) -> Optional[int]:
        """Handles missingness for TRAILBLI."""
        return self._handle_trailx_gate("trailb")

    ###########################
    # OTRAILX gated variables #
    ###########################

    def _handle_otrailx_gate(self, gate: str) -> Optional[int]:
        """Generically handle:

        If GATE is 888 or 995-998 then FIELD should = GATE.
        """
        return self.handle_set_to_gate(gate, check_values=[888, 995, 996, 997, 998])

    def _missingness_otrlarr(self) -> Optional[int]:
        """Handles missingness for OTRLARR."""
        return self._handle_otrailx_gate("otraila")

    def _missingness_otrlali(self) -> Optional[int]:
        """Handles missingness for OTRLALI."""
        return self._handle_otrailx_gate("otraila")

    def _missingness_otrlbrr(self) -> Optional[int]:
        """Handles missingness for OTRLBRR."""
        return self._handle_otrailx_gate("otrailb")

    def _missingness_otrlbli(self) -> Optional[int]:
        """Handles missingness for OTRLBLI."""
        return self._handle_otrailx_gate("otrailb")

    ################################
    # Non-optional gated variables #
    ################################

    def _handle_non_optional_gate(self, gate: str) -> Optional[int]:
        """Generically handle:

        If GATE is 95-98 then FIELD should = GATE.
        """
        return self.handle_set_to_gate(gate, check_values=[95, 96, 97, 98])

    def _missingness_minttotw(self) -> Optional[int]:
        """Handles missingness for MINTTOTW."""
        return self._handle_non_optional_gate("minttots")

    def _missingness_mintscng(self) -> Optional[int]:
        """Handles missingness for MINTSCNG."""
        return self._handle_non_optional_gate("minttots")

    def _missingness_mintscnc(self) -> Optional[int]:
        """Handles missingness for MINTSCNC."""
        return self._handle_non_optional_gate("minttots")

    def _missingness_mintpcng(self) -> Optional[int]:
        """Handles missingness for MINTPCNG."""
        return self._handle_non_optional_gate("minttots")

    def _missingness_mintpcnc(self) -> Optional[int]:
        """Handles missingness for MINTPCNC."""
        return self._handle_non_optional_gate("minttots")

    def _missingness_digbacls(self) -> Optional[int]:
        """Handles missingness for DIGBACLS."""
        return self._handle_non_optional_gate("digbacct")

    def _missingness_digforsl(self) -> Optional[int]:
        """Handles missingness for DIGFORSL."""
        return self._handle_non_optional_gate("digforct")

    def _missingness_crafturs(self) -> Optional[int]:
        """Handles missingness for CRAFTURS."""
        return self._handle_non_optional_gate("craftvrs")

    def _missingness_craftdre(self) -> Optional[int]:
        """Handles missingness for CRAFTDRE."""
        return self._handle_non_optional_gate("craftdvr")

    def _missingness_craftdti(self) -> Optional[int]:
        """Handles missingness for CRAFTDTI."""
        return self._handle_non_optional_gate("craftdvr")

    def _missingness_craftcue(self) -> Optional[int]:
        """Handles missingness for CRAFTCUE."""
        return self._handle_non_optional_gate("craftdvr")

    def _missingness_udsverfn(self) -> Optional[int]:
        """Handles missingness for UDSVERFN."""
        return self._handle_non_optional_gate("udsverfc")

    def _missingness_udsvernf(self) -> Optional[int]:
        """Handles missingness for UDSVERNF."""
        return self._handle_non_optional_gate("udsverfc")

    def _missingness_udsverlr(self) -> Optional[int]:
        """Handles missingness for UDSVERLR."""
        return self._handle_non_optional_gate("udsverlc")

    def _missingness_udsverln(self) -> Optional[int]:
        """Handles missingness for UDSVERLN."""
        return self._handle_non_optional_gate("udsverlc")

    def _missingness_udsvertn(self) -> Optional[int]:
        """Handles missingness for UDSVERTN."""
        return self._handle_non_optional_gate("udsverlc")

    def _missingness_udsverte(self) -> Optional[int]:
        """Handles missingness for UDSVERTE."""
        return self._handle_non_optional_gate("udsverlc")

    def _missingness_udsverti(self) -> Optional[int]:
        """Handles missingness for UDSVERTI."""
        return self._handle_non_optional_gate("udsverlc")
