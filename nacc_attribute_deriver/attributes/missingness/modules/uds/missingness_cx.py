"""Class to handle C1/C2 (V3 and earlier) and C2/C2T (V4) specific missingness
values.

It is arguably overkill to write a _missingness_ function for every
variable, when many could call a common rule instead (e.g. all MINTTOTS-
dependent variables could call the same rule) but due to the sheer
number of them and slight nuances I decided to be extremely explicit
here to make sure we aren't accidentally missing or duplicating any.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.utils.date import parse_unknown_dates


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

    def _missingness_npsylanx(self) -> Optional[str]:
        """Handles missingness for NPSYLANX."""
        # REGRESSION: if there was something there, legacy seems to
        # just keep it
        if self.formver < 4 and self.uds.get_value("npsylanx", str) is not None:
            return None

        result = self.handle_forbidden_gated_writein("npsylan", 3)
        if result is not None:
            return result

        return self.generic_missingness("npsylanx", str)

    def _missingness_mocalanx(self) -> Optional[str]:
        """Handles missingness for MOCALANX."""
        result = self.handle_forbidden_gated_writein("mocalan", 3)
        if result is not None:
            return result

        return self.generic_missingness("mocalanx", str)

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

    def _handle_reyxrec_cascade(
        self, gate: str, field: str, gate_mresult: Optional[int] = None
    ) -> Optional[int]:
        """Handle the REYXREC cascading rules, e.g:

        1. The VERBALTEST check (If VERBALTEST = 2 then FIELD should = 88)
        2. If GATE is 88 or 95-98 then FIELD should = GATE

        The FIELD = GATE effect may cascade through missingness, so also
        need to evaluate the missingness of the gate value,
        e.g. if REY1REC is 88, that sets the missingness of REY2REC to 88,
        which needs to set the missingness of REY3REC to 88, and so on until
        the end.

        However, since this is happening somewhat dynamically (e.g. not the raw
        form values), each variable needs to call the missingness of its gate
        (unless the gate itself does not rely on something), which ends up
        cascading in a somewhat recursive manner to store the final value
        in gate_mresult.
        """
        result = self._handle_verbaltest_gate(verbal_value=2, set_value=888)
        if result is not None:
            return result

        check_values = [88, 95, 96, 97, 98]
        result = self.handle_set_to_gate(gate, check_values=check_values)
        if result is not None:
            return result

        if gate_mresult is not None and gate_mresult in check_values:
            return gate_mresult

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
        return self._handle_reyxrec_cascade(
            "rey2rec", "rey3rec", gate_mresult=self._missingness_rey2rec()
        )

    def _missingness_rey3int(self) -> Optional[int]:
        """Handles missingness for REY3INT."""
        return self._handle_reyxrec_cascade(
            "rey2rec", "rey3int", gate_mresult=self._missingness_rey2rec()
        )

    def _missingness_rey4rec(self) -> Optional[int]:
        """Handles missingness for REY4REC."""
        return self._handle_reyxrec_cascade(
            "rey3rec", "rey4rec", gate_mresult=self._missingness_rey3rec()
        )

    def _missingness_rey4int(self) -> Optional[int]:
        """Handles missingness for REY4INT."""
        return self._handle_reyxrec_cascade(
            "rey3rec", "rey4int", gate_mresult=self._missingness_rey3rec()
        )

    def _missingness_rey5rec(self) -> Optional[int]:
        """Handles missingness for REY5REC."""
        return self._handle_reyxrec_cascade(
            "rey4rec", "rey5rec", gate_mresult=self._missingness_rey4rec()
        )

    def _missingness_rey5int(self) -> Optional[int]:
        """Handles missingness for REY5INT."""
        return self._handle_reyxrec_cascade(
            "rey4rec", "rey5int", gate_mresult=self._missingness_rey4rec()
        )

    def _missingness_reybrec(self) -> Optional[int]:
        """Handles missingness for REYBREC."""
        return self._handle_reyxrec_cascade(
            "rey5rec", "reybrec", gate_mresult=self._missingness_rey5rec()
        )

    def _missingness_reybint(self) -> Optional[int]:
        """Handles missingness for REYBINT."""
        return self._handle_reyxrec_cascade(
            "rey5rec", "reybint", gate_mresult=self._missingness_rey5rec()
        )

    def _missingness_rey6rec(self) -> Optional[int]:
        """Handles missingness for REY6REC."""
        return self._handle_reyxrec_cascade(
            "reybrec", "rey6rec", gate_mresult=self._missingness_reybrec()
        )

    def _missingness_rey6int(self) -> Optional[int]:
        """Handles missingness for REY6INT."""
        return self._handle_reyxrec_cascade(
            "reybrec", "rey6int", gate_mresult=self._missingness_reybrec()
        )

    ##########################
    # TRAILX gated variables #
    ##########################

    def _handle_trailx_gate(self, gate: str, field: str) -> Optional[int]:
        """Generically handle:

        For V4: If GATE is 995-998 then FIELD should = GATE.
        For V3 and earlier: see SAS code
        """
        check_values = [995, 996, 997, 998]
        result = self.handle_set_to_gate(gate, check_values=check_values)

        if result is not None:
            # REGRESSION:
            # older versions subtracted 900 to make it two digits
            if self.formver < 4 and result in check_values:
                return result - 900

            return result

        # REGRESSION: if V1/V2 and any of these variables were set to 88,
        # this would be recoded to -4. For v1 also returned -4 if it was None
        if self.formver < 3:
            value = self.uds.get_value(field, int)
            if value == 88 or (self.formver < 2 and value is None):
                return INFORMED_MISSINGNESS

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

    ###########################
    # OTRAILX gated variables #
    ###########################

    def _handle_otrailx_gate(self, gate: str, field: str) -> Optional[int]:
        """Generically handle:

        If GATE is 888 or 995-998 then FIELD should = GATE.
        """
        check_values = [888, 995, 996, 997, 998]
        result = self.handle_set_to_gate(gate, check_values=check_values)
        if result is not None:
            # REGRESSION:
            # older versions subtracted 800/900 to make it two digits
            if self.formver < 4 and result in check_values:
                if result == 888:
                    return result - 800
                return result - 900

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

    def _handle_non_optional_gate(
        self, gate: str, field: str, set_to_missingness: int = False
    ) -> Optional[int]:
        """Generically handle:

        If GATE is 95-98 then FIELD should = GATE.
        """
        check_values = [95, 96, 97, 98]

        # REGRESSION - most should set to gate, not informed missingness
        if set_to_missingness and self.uds.get_value(gate, int) in check_values:
            return INFORMED_MISSINGNESS

        result = self.handle_set_to_gate(gate, check_values=check_values)
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
        # REGRESSION: in legacy, we set it to -4 if the condition
        # passes, not the gate
        return self._handle_non_optional_gate(
            "craftdvr", "craftdti", set_to_missingness=self.formver < 4
        )

    def _missingness_craftcue(self) -> Optional[int]:
        """Handles missingness for CRAFTCUE."""
        # REGRESSION: in legacy, we set it to -4 if the condition
        # passes, not the gate
        return self._handle_non_optional_gate(
            "craftdvr", "craftcue", set_to_missingness=self.formver < 4
        )

    def _missingness_udsbenrs(self) -> Optional[int]:
        """Handles missingness for UDSBENRS."""
        # REGRESSION: in legacy, we set it to -4 if the condition
        # passes, not the gate. Not in V4 so always set to missingness
        return self._handle_non_optional_gate(
            "udsbentd", "udsbenrs", set_to_missingness=True
        )

    ############################
    # UDSVER-related variables #
    ############################

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

    """REGRESSION:
    The following cascade based on UDSVERTN, which is a similar situation
    to the REYXREC variables above but at a much smaller scale as it only
    really involves 3 variables.

    From SAS, the overall cascade is:

        UDSVERFC -> UDSVERFN, UDSVERNF, UDSVERTN
        UDSVERLC -> UDSVERLR, UDSVERLN, UDSVERTN
        UDSVERTN -> UDSVERTE, UDSVERTI 

    Note that UDSVERTN is the common factor, and may be set by
    UDSVERFC or UDSVERLC. This in turn effects what UDSVERTE and
    UDSVERTI are set to. As such, we need to check these first.

    Meanwhile, UDSVERFN, UDSVERNF, UDSVERLR, and UDSVERLN
    can just call the _handle_non_optional_gate directly, as they
    only have one non-cascading gate.
    """

    def _missingness_udsvertn(self) -> Optional[int]:
        """Handles missingness for UDSVERTN."""
        # REGRESSION: Checks UDSVERFC first, then UDSVERLC
        result = self._handle_non_optional_gate("udsverfc", "udsvertn")
        if result is None or result in [95, 96, 97, 98]:
            return result

        return self._handle_non_optional_gate("udsverlc", "udsvertn")

    def _missingness_udsverte(self) -> Optional[int]:
        """Handles missingness for UDSVERTE."""
        # REGRESSION
        udsvertn = self._missingness_udsvertn()
        if udsvertn is None:
            udsvertn = self.uds.get_value("udsvertn", int)

        if udsvertn in [95, 96, 97, 98]:
            return udsvertn

        return self._handle_non_optional_gate("udsverlc", "udsverte")

    def _missingness_udsverti(self) -> Optional[int]:
        """Handles missingness for UDSVERTI."""
        # REGRESSION
        udsvertn = self._missingness_udsvertn()
        if udsvertn is None:
            udsvertn = self.uds.get_value("udsvertn", int)

        if udsvertn in [95, 96, 97, 98]:
            return udsvertn

        return self._handle_non_optional_gate("udsverlc", "udsverti")

    ############################
    # LOGIPREV-gated variables #
    ############################

    # REGRESSION - should these be kept as logidate_c1?

    def __handle_logiprev_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by LOGIPREV."""
        logiprev = self.uds.get_value("logiprev", int)
        if logiprev is None or logiprev in [88, 99]:
            return INFORMED_MISSINGNESS

        # Looks liike LOGIMO, LOGIDAY, and LOGIYR are actually parsed
        # from logidate_c1
        value = self.uds.get_value(field, int)
        if value is None:
            logiyr, logimo, logiday = parse_unknown_dates(
                self.uds.get_value("logidate_c1", str)
            )
            if field == "logiyr":
                value = logiyr
            elif field == "logimo":
                value = logimo
            elif field == "logiday":
                value = logiday

        if (field == "logiyr") and (value is None or value == 9999):
            return 8888

        if (field != "logiyr") and (value is None or value == 99):
            return 88

        return None

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

    ############################
    # MOCACOMP-gated variables #
    ############################

    def _missingness_mocatots(self) -> Optional[int]:
        """Handles missingness for MOCATOTS."""
        if self.uds.get_value("mocacomp", int) == 0:
            return 88

        return self.generic_missingness("mocacomp", int)

    def __handle_mocacomp_gate(self, field: str) -> Optional[int]:
        """Handle variables gated by MOCACOMP.

        If MOCACOMP = 0, then FIELD = MOCAREAS
        """
        if self.uds.get_value("mocacomp", int) == 0:
            mocareas = self.uds.get_value("mocareas", int)
            return mocareas if mocareas is not None else INFORMED_MISSINGNESS

        return self.generic_missingness(field, int)

    def _missingness_mocatrai(self) -> Optional[int]:
        """Handles missingness for MOCATRAI."""
        return self.__handle_mocacomp_gate("mocatrai")

    def _missingness_mocacube(self) -> Optional[int]:
        """Handles missingness for MOCACUBE."""
        return self.__handle_mocacomp_gate("mocacube")

    def _missingness_mocacloc(self) -> Optional[int]:
        """Handles missingness for MOCACLOC."""
        return self.__handle_mocacomp_gate("mocacloc")

    def _missingness_mocaclon(self) -> Optional[int]:
        """Handles missingness for MOCACLON."""
        return self.__handle_mocacomp_gate("mocaclon")

    def _missingness_mocacloh(self) -> Optional[int]:
        """Handles missingness for MOCACLOH."""
        return self.__handle_mocacomp_gate("mocacloh")

    def _missingness_mocanami(self) -> Optional[int]:
        """Handles missingness for MOCANAMI."""
        return self.__handle_mocacomp_gate("mocanami")

    def _missingness_mocaregi(self) -> Optional[int]:
        """Handles missingness for MOCAREGI."""
        return self.__handle_mocacomp_gate("mocaregi")

    def _missingness_mocadigi(self) -> Optional[int]:
        """Handles missingness for MOCADIGI."""
        return self.__handle_mocacomp_gate("mocadigi")

    def _missingness_mocalett(self) -> Optional[int]:
        """Handles missingness for MOCALETT."""
        return self.__handle_mocacomp_gate("mocalett")

    def _missingness_mocaser7(self) -> Optional[int]:
        """Handles missingness for MOCASER7."""
        return self.__handle_mocacomp_gate("mocaser7")

    def _missingness_mocarepe(self) -> Optional[int]:
        """Handles missingness for MOCAREPE."""
        return self.__handle_mocacomp_gate("mocarepe")

    def _missingness_mocaflue(self) -> Optional[int]:
        """Handles missingness for MOCAFLUE."""
        return self.__handle_mocacomp_gate("mocaflue")

    def _missingness_mocaabst(self) -> Optional[int]:
        """Handles missingness for MOCAABST."""
        return self.__handle_mocacomp_gate("mocaabst")

    def _missingness_mocarecn(self) -> Optional[int]:
        """Handles missingness for MOCARECN."""
        return self.__handle_mocacomp_gate("mocarecn")

    def _missingness_mocarecc(self) -> Optional[int]:
        """Handles missingness for MOCARECC."""
        return self.__handle_mocacomp_gate("mocarecc")

    def _missingness_mocarecr(self) -> Optional[int]:
        """Handles missingness for MOCARECR."""
        return self.__handle_mocacomp_gate("mocarecr")

    def _missingness_mocaordt(self) -> Optional[int]:
        """Handles missingness for MOCAORDT."""
        return self.__handle_mocacomp_gate("mocaordt")

    def _missingness_mocaormo(self) -> Optional[int]:
        """Handles missingness for MOCAORMO."""
        return self.__handle_mocacomp_gate("mocaormo")

    def _missingness_mocaoryr(self) -> Optional[int]:
        """Handles missingness for MOCAORYR."""
        return self.__handle_mocacomp_gate("mocaoryr")

    def _missingness_mocaordy(self) -> Optional[int]:
        """Handles missingness for MOCAORDY."""
        return self.__handle_mocacomp_gate("mocaordy")

    def _missingness_mocaorpl(self) -> Optional[int]:
        """Handles missingness for MOCAORPL."""
        return self.__handle_mocacomp_gate("mocaorpl")

    def _missingness_mocaorct(self) -> Optional[int]:
        """Handles missingness for MOCAORCT."""
        return self.__handle_mocacomp_gate("mocaorct")

    #########
    # Other #
    #########

    def _missingness_memtime(self) -> Optional[int]:
        """Handles missingness for MEMTIME."""
        memtime = self.uds.get_value("memtime", int)
        memunits = self.uds.get_value("memunits", int)

        if (
            memtime in [88, 99]
            and memunits is not None
            and memunits >= 0
            and memunits <= 25
        ):
            return 99

        if (memtime in [88, 99] or memtime is None) and memunits in [95, 96, 97, 98]:
            return INFORMED_MISSINGNESS

        return self.generic_missingness("memtime", int)
