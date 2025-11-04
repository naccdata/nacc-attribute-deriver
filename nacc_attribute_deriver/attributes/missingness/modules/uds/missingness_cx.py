"""Class to handle C1/C2 (V3 and earlier) and C2/C2T (V4) specific missingness
values.

It is arguably overkill to write a _missingness_ function for every
variable, when many could call a common rule instead (e.g. all MINTTOTS-
dependent variables could call the same rule) but due to the sheer
number of them and slight nuances I decided to be extremely explicit
here to make sure we aren't accidentally missing or duplicating any.
"""

from typing import Optional

from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

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

        if value is None:
            if respval in [2, 3]:
                return 0

            return INFORMED_MISSINGNESS

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
        result = self.handle_forbidden_gated_writein("mocalan", 3)
        if result is not None:
            return result

        return self.generic_missingness("mocalanx", str)

    def _missingness_npsylanx(self) -> Optional[str]:
        """Handles missingness for NPSYLANX."""
        result = self.handle_forbidden_gated_writein("npsylan", 3)
        if result is not None:
            return result

        return self.generic_missingness("npsylanx", str)

    def _missingness_respothx(self) -> Optional[str]:
        """Handles missingness for RESPOTHX."""
        result = self.handle_forbidden_gated_writein("respoth", 1)
        if result is not None:
            return result

        return self.generic_missingness("respothx", str)

    def _missingness_mmselanx(self) -> Optional[str]:
        """Handles missingness for MMSELANX."""
        result = self.handle_forbidden_gated_writein("mmselan", 3)
        if result is not None:
            return result

        return self.generic_missingness("mmselanx", str)

    #######################################################
    # REYXREC gated variables - cascades across variables #
    # Relies on both VERBALTEST and an earlier variable   #
    #######################################################

    def _handle_reyxrec_cascade(self, gate: str, field: str) -> Optional[int]:
        """Handle the REYXREC cascading rules, e.g:

        1. The VERBALTEST check (If VERBALTEST = 2 then FIELD should = 88)
        2. If GATE is 88 or 95-98 then FIELD should = GATE
        """
        result = self._handle_verbaltest_gate(verbal_value=2, set_value=888)
        if result is not None:
            return result

        result = self.handle_set_to_gate(gate, check_values=[88, 95, 96, 97, 98])
        if result is not None:
            return result

        return self.generic_missingness(field, int)

    def _missingness_reydint(self) -> Optional[int]:
        """Handles missingness for REYDINT."""
        return self._handle_reyxrec_cascade("reydrec", "reydint")

    def _missingness_reytcor(self) -> Optional[int]:
        """Handles missingness for REYTCOR."""
        return self._handle_reyxrec_cascade("reydrec", "reytcor")

    def _missingness_reyfpos(self) -> Optional[int]:
        """Handles missingness for REYFPOS."""
        return self._handle_reyxrec_cascade("reydrec", "reyfpos")

    def _missingness_rey1int(self) -> Optional[int]:
        """Handles missingness for REY1INT."""
        return self._handle_reyxrec_cascade("rey1rec", "rey1int")

    def _missingness_rey2rec(self) -> Optional[int]:
        """Handles missingness for REY2REC."""
        return self._handle_reyxrec_cascade("rey1rec", "rey2rec")

    def _missingness_rey2int(self) -> Optional[int]:
        """Handles missingness for REY2INT."""
        return self._handle_reyxrec_cascade("rey1rec", "rey2int")

    def _missingness_rey3rec(self) -> Optional[int]:
        """Handles missingness for REY3REC."""
        return self._handle_reyxrec_cascade("rey2rec", "rey3rec")

    def _missingness_rey3int(self) -> Optional[int]:
        """Handles missingness for REY3INT."""
        return self._handle_reyxrec_cascade("rey2rec", "rey3int")

    def _missingness_rey4rec(self) -> Optional[int]:
        """Handles missingness for REY4REC."""
        return self._handle_reyxrec_cascade("rey3rec", "rey4rec")

    def _missingness_rey4int(self) -> Optional[int]:
        """Handles missingness for REY4INT."""
        return self._handle_reyxrec_cascade("rey3rec", "rey4int")

    def _missingness_rey5rec(self) -> Optional[int]:
        """Handles missingness for REY5REC."""
        return self._handle_reyxrec_cascade("rey4rec", "rey5rec")

    def _missingness_rey5int(self) -> Optional[int]:
        """Handles missingness for REY5INT."""
        return self._handle_reyxrec_cascade("rey4rec", "rey5int")

    def _missingness_reybrec(self) -> Optional[int]:
        """Handles missingness for REYBREC."""
        return self._handle_reyxrec_cascade("rey5rec", "reybrec")

    def _missingness_reybint(self) -> Optional[int]:
        """Handles missingness for REYBINT."""
        return self._handle_reyxrec_cascade("rey5rec", "reybint")

    def _missingness_rey6rec(self) -> Optional[int]:
        """Handles missingness for REY6REC."""
        return self._handle_reyxrec_cascade("reybrec", "rey6rec")

    def _missingness_rey6int(self) -> Optional[int]:
        """Handles missingness for REY6INT."""
        return self._handle_reyxrec_cascade("reybrec", "rey6int")

    ##########################
    # TRAILX gated variables #
    ##########################

    def _handle_trailx_gate(self, gate: str, field: str) -> Optional[int]:
        """Generically handle:

        For V4: If GATE is 995-998 then FIELD should = GATE.
        For V3 and earlier: see SAS code
        """
        # if self.uds.get_value(gate, int) == 999:
        #     return 99

        # if self.formver < 3:
        #     value = self.uds.get_value(field, int)
        #     if value is None or value == 88:
        #         return INFORMED_MISSINGNESS

        result = self.handle_set_to_gate(gate, check_values=[995, 996, 997, 998])
        if result is not None:
            return result

        return self.generic_missingness(field, int)

    def _missingness_trailarr(self) -> Optional[int]:
        """Handles missingness for TRAILARR."""
        return self._handle_trailx_gate("traila", "trailarr")

    def _missingness_trailali(self) -> Optional[int]:
        """Handles missingness for TRAILALI."""
        return self._handle_trailx_gate("traila", "trailali")

    def _missingness_trailbrr(self) -> Optional[int]:
        """Handles missingness for TRAILBRR."""
        return self._handle_trailx_gate("trailb", "trailbrr")

    def _missingness_trailbli(self) -> Optional[int]:
        """Handles missingness for TRAILBLI."""
        return self._handle_trailx_gate("trailb", "trailbli")

    # def _missingness_traila(self) -> Optional[int]:
    #     """Handles missingness for TRAILA."""
    #     if self.uds.get_value("traila", int) is None:
    #         return 999

    #     return None

    # def _missingness_trailb(self) -> Optional[int]:
    #     """Handles missingness for TRAILB."""
    #     if self.uds.get_value("trailb", int) is None:
    #         return 999

    #     return None

    ###########################
    # OTRAILX gated variables #
    ###########################

    def _handle_otrailx_gate(self, gate: str, field: str) -> Optional[int]:
        """Generically handle:

        If GATE is 888 or 995-998 then FIELD should = GATE.
        """
        result = self.handle_set_to_gate(gate, check_values=[888, 995, 996, 997, 998])
        if result is not None:
            return result

        return self.generic_missingness(field, int)

    def _missingness_otrlarr(self) -> Optional[int]:
        """Handles missingness for OTRLARR."""
        return self._handle_otrailx_gate("otraila", "otrlarr")

    def _missingness_otrlali(self) -> Optional[int]:
        """Handles missingness for OTRLALI."""
        return self._handle_otrailx_gate("otraila", "otrlali")

    def _missingness_otrlbrr(self) -> Optional[int]:
        """Handles missingness for OTRLBRR."""
        return self._handle_otrailx_gate("otrailb", "otrlbrr")

    def _missingness_otrlbli(self) -> Optional[int]:
        """Handles missingness for OTRLBLI."""
        return self._handle_otrailx_gate("otrailb", "otrlbli")

    ################################
    # Non-optional gated variables #
    ################################

    def _handle_non_optional_gate(self, gate: str, field: str) -> Optional[int]:
        """Generically handle:

        If GATE is 95-98 then FIELD should = GATE.
        """
        result = self.handle_set_to_gate(gate, check_values=[95, 96, 97, 98])
        if result is not None:
            return result

        return self.generic_missingness(field, int)

    def _missingness_minttotw(self) -> Optional[int]:
        """Handles missingness for MINTTOTW."""
        return self._handle_non_optional_gate("minttots", "minttotw")

    def _missingness_mintscng(self) -> Optional[int]:
        """Handles missingness for MINTSCNG."""
        return self._handle_non_optional_gate("minttots", "mintscng")

    def _missingness_mintscnc(self) -> Optional[int]:
        """Handles missingness for MINTSCNC."""
        return self._handle_non_optional_gate("minttots", "mintscnc")

    def _missingness_mintpcng(self) -> Optional[int]:
        """Handles missingness for MINTPCNG."""
        return self._handle_non_optional_gate("minttots", "mintpcng")

    def _missingness_mintpcnc(self) -> Optional[int]:
        """Handles missingness for MINTPCNC."""
        return self._handle_non_optional_gate("minttots", "mintpcnc")

    def _missingness_digbacls(self) -> Optional[int]:
        """Handles missingness for DIGBACLS."""
        return self._handle_non_optional_gate("digbacct", "digbacls")

    def _missingness_digforsl(self) -> Optional[int]:
        """Handles missingness for DIGFORSL."""
        return self._handle_non_optional_gate("digforct", "digforsl")

    def _missingness_crafturs(self) -> Optional[int]:
        """Handles missingness for CRAFTURS."""
        return self._handle_non_optional_gate("craftvrs", "crafturs")

    def _missingness_craftdre(self) -> Optional[int]:
        """Handles missingness for CRAFTDRE."""
        return self._handle_non_optional_gate("craftdvr", "craftdre")

    def _missingness_craftdti(self) -> Optional[int]:
        """Handles missingness for CRAFTDTI."""
        return self._handle_non_optional_gate("craftdvr", "craftdti")

    def _missingness_craftcue(self) -> Optional[int]:
        """Handles missingness for CRAFTCUE."""
        return self._handle_non_optional_gate("craftdvr", "craftcue")

    def _missingness_udsverfn(self) -> Optional[int]:
        """Handles missingness for UDSVERFN."""
        return self._handle_non_optional_gate("udsverfc", "udsverfn")

    def _missingness_udsvernf(self) -> Optional[int]:
        """Handles missingness for UDSVERNF."""
        return self._handle_non_optional_gate("udsverfc", "udsvernf")

    def _missingness_udsverlr(self) -> Optional[int]:
        """Handles missingness for UDSVERLR."""
        return self._handle_non_optional_gate("udsverlc", "udsverlr")

    def _missingness_udsverln(self) -> Optional[int]:
        """Handles missingness for UDSVERLN."""
        return self._handle_non_optional_gate("udsverlc", "udsverln")

    def _missingness_udsvertn(self) -> Optional[int]:
        """Handles missingness for UDSVERTN."""
        return self._handle_non_optional_gate("udsverlc", "udsvertn")

    def _missingness_udsverte(self) -> Optional[int]:
        """Handles missingness for UDSVERTE."""
        return self._handle_non_optional_gate("udsverlc", "udsverte")

    def _missingness_udsverti(self) -> Optional[int]:
        """Handles missingness for UDSVERTI."""
        return self._handle_non_optional_gate("udsverlc", "udsverti")

    ############################
    # LOGIPREV-gated variables #
    ############################

    def __handle_logiprev_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by LOGIPREV."""
        logiprev = self.uds.get_value("logiprev", int)
        if logiprev is None or logiprev in [88, 99]:
            return INFORMED_MISSINGNESS

        return self.generic_missingness(field, int)

    def _missingness_logiprev(self) -> Optional[int]:
        """Handles missingness for LOGIPREV."""
        return self.__handle_logiprev_gate("logiprev")

    def _missingness_logimo(self) -> Optional[int]:
        """Handles missingness for LOGIMO."""
        return self.__handle_logiprev_gate("logimo")

    def _missingness_logiday(self) -> Optional[int]:
        """Handles missingness for LOGIDAY."""
        return self.__handle_logiprev_gate("logiday")

    def _missingness_logiyr(self) -> Optional[int]:
        """Handles missingness for LOGIYR."""
        return self.__handle_logiprev_gate("logiyr")
