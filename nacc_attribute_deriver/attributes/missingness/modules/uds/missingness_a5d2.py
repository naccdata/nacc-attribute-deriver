"""Class to handle A5D2-specific missingness values.

Some of these variables have recode logic defined in the legacy SAS
code, so there are some version differences.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.namespace.namespace import (
    DerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)

from .missingness_uds import UDSMissingness


class UDSFormA5D2Missingness(UDSMissingness):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table=table)

        # needed for variables gated by NACCTBI
        self.__derived = DerivedNamespace(table=table)

    def __handle_a5d2_gate(
        self,
        gate: str,
        field: str,
        no_return_value: int = 8,
        unknown_return_value: int = 9,
        carry_forward: bool = False,
        skip_gate_on_legacy: bool = True,
    ) -> Optional[int]:
        """Handle generic A5D2 when there is both a gate and potentially a
        carryforward (777) situation:

        If GATE == 0, return NO_RETURN_VALUE
            (value to return when the answer is 0 = No, generally 888)
        If GATE == 9, return UNKNOWN_RETURN_VALUE
            (value to return when anwer is 9 = Unknown, generally 999)

        If carry forward, handle carry forward case (if 777, carry forward
        from previous visit), else generic missingness.

        If GATE = 0, then FIELD should be 8
        If GATE = 9, then FIELD should be 9
        Else generic missingness
        """
        if self.formver >= 4 or not skip_gate_on_legacy:
            gate_value = self.uds.get_value(gate, int)
            if gate_value == 0:
                return no_return_value
            if gate_value == 9:
                return unknown_return_value

        if carry_forward:
            return self.handle_prev_visit(field, int, prev_code=777)

        return self.generic_missingness(field, int)

    def handle_a5d2_carry_forward(
        self,
        gate: str,
        field: str,
        no_return_value: int = 888,
        unknown_return_value: int = 999,
        skip_gate_on_legacy: bool = False,
    ) -> Optional[int]:
        """Handle generic A5D2 gate with carry forward."""
        return self.__handle_a5d2_gate(
            gate,
            field,
            no_return_value=no_return_value,
            unknown_return_value=unknown_return_value,
            carry_forward=True,
            skip_gate_on_legacy=skip_gate_on_legacy,
        )

    def _missingness_smokyrs(self) -> Optional[int]:
        """Handles missingness for SMOKYRS."""
        # works a little different in legacy
        # TODO - should this be updated to the V4 version?
        # the original logic doesn't make much sense
        if self.formver < 4:
            smokyrs = self.uds.get_value("smokyrs", int)
            tobac100 = self.uds.get_value("tobac100", int)

            if (smokyrs is None or smokyrs in [88, 99]) and tobac100 == 0:
                return 0

            if smokyrs is None and tobac100 == 9:
                return 88

            return self.generic_missingness("smokyrs", int)

        return self.handle_a5d2_carry_forward(
            "tobac100",
            "smokyrs",
            no_return_value=88,
            unknown_return_value=99,
        )

    ########################
    # GATED CARRY FORWARDS #
    ########################

    def _missingness_quitsmok(self) -> Optional[int]:
        """Handles missingness for QUITSMOK."""
        return self.handle_a5d2_carry_forward(
            "tobac100", "quitsmok", skip_gate_on_legacy=False
        )

    def _missingness_hrtattage(self) -> Optional[int]:
        """Handles missingness for HRTATTAGE."""
        return self.handle_a5d2_carry_forward("hrtattack", "hrtattage")

    def _missingness_cardarrage(self) -> Optional[int]:
        """Handles missingness for CARDARRAGE."""
        return self.handle_a5d2_carry_forward("cardarrest", "cardarrage")

    def _missingness_bypassage(self) -> Optional[int]:
        """Handles missingness for BYPASSAGE."""
        return self.handle_a5d2_carry_forward("cvbypass", "bypassage")

    def _missingness_pacdefage(self) -> Optional[int]:
        """Handles missingness for PACDEFAGE."""
        return self.handle_a5d2_carry_forward("cvpacdef", "pacdefage")

    def _missingness_valveage(self) -> Optional[int]:
        """Handles missingness for VALVEAGE."""
        return self.handle_a5d2_carry_forward("cvhvalve", "valveage")

    def _missingness_strokage(self) -> Optional[int]:
        """Handles missingness for STROKAGE."""
        return self.handle_a5d2_carry_forward("cbstroke", "strokage")

    def _missingness_tiaage(self) -> Optional[int]:
        """Handles missingness for TIAAGE."""
        return self.handle_a5d2_carry_forward("cbtia", "tiaage")

    def _missingness_pdage(self) -> Optional[int]:
        """Handles missingness for PDAGE."""
        return self.handle_a5d2_carry_forward("pd", "pdage")

    def _missingness_pdothrage(self) -> Optional[int]:
        """Handles missingness for PDOTHRAGE."""
        return self.handle_a5d2_carry_forward("pdothr", "pdothrage")

    def _missingness_seizage(self) -> Optional[int]:
        """Handles missingness for SEIZAGE."""
        return self.handle_a5d2_carry_forward("seizures", "seizage")

    def _missingness_impyears(self) -> Optional[int]:
        """Handles missingness for IMPYEARS."""
        return self.handle_a5d2_carry_forward("headimp", "impyears")

    def _missingness_firsttbi(self) -> Optional[int]:
        """Handles missingness for FIRSTTBI."""
        return self.handle_a5d2_carry_forward("headinjury", "firsttbi")

    def _missingness_lasttbi(self) -> Optional[int]:
        """Handles missingness for LASTTBI."""
        return self.handle_a5d2_carry_forward("headinjury", "lasttbi")

    def _missingness_diabage(self) -> Optional[int]:
        """Handles missingness for DIABAGE."""
        return self.handle_a5d2_carry_forward("diabetes", "diabage")

    def _missingness_hypertage(self) -> Optional[int]:
        """Handles missingness for HYPERTAGE."""
        return self.handle_a5d2_carry_forward("hyperten", "hypertage")

    def _missingness_hyperchage(self) -> Optional[int]:
        """Handles missingness for HYPERCHAGE."""
        return self.handle_a5d2_carry_forward("hypercho", "hyperchage")

    def _missingness_cancerage(self) -> Optional[int]:
        """Handles missingness for CANCERAGE."""
        return self.handle_a5d2_carry_forward("canceractv", "cancerage")

    def _missingness_kidneyage(self) -> Optional[int]:
        """Handles missingness for KIDNEYAGE."""
        return self.handle_a5d2_carry_forward("kidney", "kidneyage")

    def _missingness_liverage(self) -> Optional[int]:
        """Handles missingness for LIVERAGE."""
        return self.handle_a5d2_carry_forward("liver", "liverage")

    def _missingness_pvdage(self) -> Optional[int]:
        """Handles missingness for PVDAGE."""
        return self.handle_a5d2_carry_forward("pvd", "pvdage")

    def _missingness_hivage(self) -> Optional[int]:
        """Handles missingness for HIVAGE."""
        return self.handle_a5d2_carry_forward("hivdiag", "hivage")

    #################
    # GENERIC GATES #
    #################

    def _missingness_packsper(self) -> Optional[int]:
        """Handles missingness for PACKSPER."""
        # works a little different in legacy
        # TODO - should this be updated to the V4 version?
        if self.formver < 4:
            packsper = self.uds.get_value("packsper", int)
            tobac100 = self.uds.get_value("tobac100", int)

            # smokyr's own missingness gets used in the following
            # logic, so use/call that directly. better way to clean
            # this up?
            missingness_smokyrs = self._missingness_smokyrs()  # type: ignore
            current_smokyrs = self.uds.get_value("smokyrs", int)

            # we care about if SMOKYRS is 0 through being explicitly
            # set or through a missingness result
            resolved_smokyrs = missingness_smokyrs == 0 or current_smokyrs == 0

            if tobac100 == 0 and resolved_smokyrs:
                return 0

            if packsper is None or packsper in [8, 9]:  # noqa: SIM102
                if tobac100 in [0, 8, 9] or resolved_smokyrs:
                    return 8

            # Fall back to V4 case

        return self.__handle_a5d2_gate("tobac100", "packsper")

    def _missingness_tobac30(self) -> Optional[int]:
        """Handles missingness for TOBAC30."""
        return self.__handle_a5d2_gate("tobac100", "tobac30")

    def _missingness_alcdrinks(self) -> Optional[int]:
        """Handles missingness for ALCDRINKS."""
        return self.__handle_a5d2_gate("alcfreqyr", "alcdrinks")

    def _missingness_alcbinge(self) -> Optional[int]:
        """Handles missingness for ALCBINGE."""
        return self.__handle_a5d2_gate("alcfreqyr", "alcbinge")

    def _missingness_hrtattmult(self) -> Optional[int]:
        """Handles missingness for HRTATTMULT."""
        return self.__handle_a5d2_gate("hrtattack", "hrtattmult")

    def _missingness_strokstat(self) -> Optional[int]:
        """Handles missingness for STROKSTAT."""
        return self.__handle_a5d2_gate("cbstroke", "strokstat")

    def _missingness_covidhosp(self) -> Optional[int]:
        """Handles missingness for COVIDHOSP."""
        return self.__handle_a5d2_gate("covid19", "covidhosp")

    def _missingness_generalanx(self) -> Optional[int]:
        """Handles missingness for GENERALANX."""
        return self.__handle_a5d2_gate("anxiety", "generalanx")

    def _missingness_panicdis(self) -> Optional[int]:
        """Handles missingness for PANICDIS."""
        return self.__handle_a5d2_gate("anxiety", "panicdis")

    def _missingness_othanxdis(self) -> Optional[int]:
        """Handles missingness for OTHANXDIS."""
        return self.__handle_a5d2_gate("anxiety", "othanxdis")

    def _missingness_angiocp(self) -> Optional[int]:
        """Handles missingness for ANGIOCP."""
        return self.__handle_a5d2_gate("cbstroke", "angiocp")

    def _missingness_strokmul(self) -> Optional[int]:
        """Handles missingness for STROKMUL."""
        return self.__handle_a5d2_gate(
            "cbstroke", "strokmul", skip_gate_on_legacy=False
        )

    def _missingness_ocd(self) -> Optional[int]:
        """Handles missingness for OCD."""
        return self.__handle_a5d2_gate("anxiety", "ocd")

    def _missingness_tiamult(self) -> Optional[int]:
        """Handles missingness for TIAMULT."""
        return self.__handle_a5d2_gate("cbtia", "tiamult", skip_gate_on_legacy=False)

    # the following have unique logic from V3 and earlier so
    # brought over from SAS recode logic

    def _missingness_diabtype(self) -> Optional[int]:
        """Handles missingness for DIABTYPE."""
        diabetes = self.uds.get_value("diabetes", int)
        if self.formver < 3 and diabetes in [1, 2]:
            return 9
        if self.formver < 4 and diabetes in [0, 9]:
            return 8

        return self.__handle_a5d2_gate("diabetes", "diabtype")

    def _missingness_alcfreq(self) -> Optional[int]:
        """Only V3.

        Handles missingness for ALCFREQ.
        """
        return self.__handle_a5d2_gate(
            "alcoccas",
            "alcfreq",
            no_return_value=8,
            unknown_return_value=INFORMED_MISSINGNESS,
            skip_gate_on_legacy=False,
        )

    def _missingness_hattmult(self) -> Optional[int]:
        """Handles missingness for HATTMULT.

        Only V3.
        """
        return self.__handle_a5d2_gate(
            "cvhatt",
            "hattmult",
            no_return_value=8,
            unknown_return_value=INFORMED_MISSINGNESS,
            skip_gate_on_legacy=False,
        )

    def _missingness_hattyear(self) -> Optional[int]:
        """Handles missingness for HATTYEAR.

        Only V3
        """
        return self.__handle_a5d2_gate(
            "cvhatt",
            "hattyear",
            no_return_value=8888,
            unknown_return_value=INFORMED_MISSINGNESS,
            skip_gate_on_legacy=False,
        )

    #############################
    # CARRY FORWARD ONLY VALUES #
    #############################

    def _missingness_nomensage(self) -> Optional[int]:
        """Handles missingness for NOMENSAGE."""
        return self.handle_prev_visit("nomensage", int, prev_code=777)

    def _missingness_hrtyears(self) -> Optional[int]:
        """Handles missingness for HRTYEARS."""
        return self.handle_prev_visit("hrtyears", int, prev_code=777)

    def _missingness_hrtstrtage(self) -> Optional[int]:
        """Handles missingness for HRTSTRTAGE."""
        return self.handle_prev_visit("hrtstrtage", int, prev_code=777)

    def _missingness_hrtendage(self) -> Optional[int]:
        """Handles missingness for HRTENDAGE."""
        return self.handle_prev_visit("hrtendage", int, prev_code=777)

    def _missingness_bcpillsyr(self) -> Optional[int]:
        """Handles missingness for BCPILLSYR."""
        return self.handle_prev_visit("bcpillsyr", int, prev_code=777)

    def _missingness_bcstartage(self) -> Optional[int]:
        """Handles missingness for BCSTARTAGE."""
        return self.handle_prev_visit("bcstartage", int, prev_code=777)

    def _missingness_bcendage(self) -> Optional[int]:
        """Handles missingness for BCENDAGE."""
        return self.handle_prev_visit("bcendage", int, prev_code=777)

    ########################
    # HEADIMP GATED VALUES #
    ########################

    def __handle_headimp_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by HEADIMP, which follow:

        If HEADIMP = 1 and FIELD is blank, FIELD should = 0
        """
        headimp = self.uds.get_value("headimp", int)
        value = self.uds.get_value(field, int)

        if value is None:
            if headimp == 1:
                return 0
            return INFORMED_MISSINGNESS

        return None

    def _missingness_impamfoot(self) -> Optional[int]:
        """Handles missingness for IMPAMFOOT."""
        return self.__handle_headimp_gate("impamfoot")

    def _missingness_impsoccer(self) -> Optional[int]:
        """Handles missingness for IMPSOCCER."""
        return self.__handle_headimp_gate("impsoccer")

    def _missingness_imphockey(self) -> Optional[int]:
        """Handles missingness for IMPHOCKEY."""
        return self.__handle_headimp_gate("imphockey")

    def _missingness_impboxing(self) -> Optional[int]:
        """Handles missingness for IMPBOXING."""
        return self.__handle_headimp_gate("impboxing")

    def _missingness_impsport(self) -> Optional[int]:
        """Handles missingness for IMPSPORT."""
        return self.__handle_headimp_gate("impsport")

    def _missingness_impipv(self) -> Optional[int]:
        """Handles missingness for IMPIPV."""
        return self.__handle_headimp_gate("impipv")

    def _missingness_impmilit(self) -> Optional[int]:
        """Handles missingness for IMPMILIT."""
        return self.__handle_headimp_gate("impmilit")

    def _missingness_impassault(self) -> Optional[int]:
        """Handles missingness for IMPASSAULT."""
        return self.__handle_headimp_gate("impassault")

    def _missingness_impother(self) -> Optional[int]:
        """Handles missingness for IMPOTHER."""
        return self.__handle_headimp_gate("impother")

    #########################
    # DIABETES GATED VALUES #
    #########################

    def __handle_diabetes_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by DIABETES, which follow:

        If DIABETES = 1 or 2 and FIELD is blank, FIELD should = 0
        """
        diabetes = self.uds.get_value("diabetes", int)
        value = self.uds.get_value(field, int)

        if value is None:
            if diabetes in [1, 2]:
                return 0
            return INFORMED_MISSINGNESS

        return None

    def _missingness_diabins(self) -> Optional[int]:
        """Handles missingness for DIABINS."""
        return self.__handle_diabetes_gate("diabins")

    def _missingness_diabmeds(self) -> Optional[int]:
        """Handles missingness for DIABMEDS."""
        return self.__handle_diabetes_gate("diabmeds")

    def _missingness_diabglp1(self) -> Optional[int]:
        """Handles missingness for DIABGLP1."""
        return self.__handle_diabetes_gate("diabglp1")

    def _missingness_diabrecact(self) -> Optional[int]:
        """Handles missingness for DIABRECACT."""
        return self.__handle_diabetes_gate("diabrecact")

    def _missingness_diabdiet(self) -> Optional[int]:
        """Handles missingness for DIABDIET."""
        return self.__handle_diabetes_gate("diabdiet")

    ##########################
    # ARTHRITIS GATED VALUES #
    ##########################

    def __handle_arthritis_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by ARTHRITIS (V4) or ARTHRIT (V3 and
        earlier), which follow:

        If ARTHRITIS = 1 or 2 and FIELD is blank, FIELD should = 0
        If ARTHRITIS is 0 or 9 and FIELD is blank, then FIELD should = 8

        OR

        If ARTHRIT = 0 and FIELD is blank, FIELD should = 0
        If ARTHRIT = 9 and FIELD is blank, then FIELD should = 8
        """
        gate = "arthrit" if self.formver < 4 else "arthritis"
        gate_value = self.uds.get_value(gate, int)
        value = self.uds.get_value(field, int)

        if value is None:
            if self.formver < 4:
                if gate_value == 0:
                    return 0
                if gate_value == 9:
                    return 8
            else:
                if gate_value in [1, 2]:
                    return 0
                if gate_value in [0, 9]:
                    return 8

            return INFORMED_MISSINGNESS

        return None

    def _missingness_arthupex(self) -> Optional[int]:
        """Handles missingness for ARTHUPEX."""
        return self.__handle_arthritis_gate("arthupex")

    def _missingness_arthloex(self) -> Optional[int]:
        """Handles missingness for ARTHLOEX."""
        return self.__handle_arthritis_gate("arthloex")

    def _missingness_arthspin(self) -> Optional[int]:
        """Handles missingness for ARTHSPIN."""
        return self.__handle_arthritis_gate("arthspin")

    def _missingness_arthunk(self) -> Optional[int]:
        """Handles missingness for ARTHUNK."""
        return self.__handle_arthritis_gate("arthunk")

    def _missingness_arthtype(self) -> Optional[int]:
        """Handles missingness for ARTHTYPE."""
        arthrit = self.uds.get_value("arthrit", int)
        arthtype = self.uds.get_value("arthtype", int)

        if arthtype is None:
            if arthrit in [0, 9]:
                return 8

            return INFORMED_MISSINGNESS

        return None

    ######################
    # APNEA GATED VALUES #
    ######################

    def __handle_apnea_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by APNEA, which follow:

        If APNEA = 0 or 2, FIELD should = 8
        If APNEA = 9, FIELD should = 9
        """
        apnea = self.uds.get_value("apnea", int)
        if apnea in [0, 2]:
            return 8
        if apnea == 9:
            return 9

        return self.generic_missingness(field, int)

    def _missingness_cpap(self) -> Optional[int]:
        """Handles missingness for CPAP."""
        return self.__handle_apnea_gate("cpap")

    def _missingness_apneaoral(self) -> Optional[int]:
        """Handles missingness for APNEAORAL."""
        return self.__handle_apnea_gate("apneaoral")

    ###########################
    # CANCERACTV GATED VALUES #
    ###########################

    def __handle_canceractv_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by CANCERACTV, which follow:

        If CANCERACTV = 1 or 2 and FIELD is blank, FIELD should = 0
        """
        canceractv = self.uds.get_value("canceractv", int)
        value = self.uds.get_value(field, int)

        if value is None:
            if canceractv in [1, 2]:
                return 0
            return INFORMED_MISSINGNESS

        return None

    def _missingness_cancerprim(self) -> Optional[int]:
        """Handles missingness for CANCERPRIM."""
        return self.__handle_canceractv_gate("cancerprim")

    def _missingness_cancermeta(self) -> Optional[int]:
        """Handles missingness for CANCERMETA."""
        return self.__handle_canceractv_gate("cancermeta")

    def _missingness_cancerunk(self) -> Optional[int]:
        """Handles missingness for CANCERUNK."""
        return self.__handle_canceractv_gate("cancerunk")

    def _missingness_cancblood(self) -> Optional[int]:
        """Handles missingness for CANCBLOOD."""
        return self.__handle_canceractv_gate("cancblood")

    def _missingness_cancbreast(self) -> Optional[int]:
        """Handles missingness for CANCBREAST."""
        return self.__handle_canceractv_gate("cancbreast")

    def _missingness_canccolon(self) -> Optional[int]:
        """Handles missingness for CANCCOLON."""
        return self.__handle_canceractv_gate("canccolon")

    def _missingness_canclung(self) -> Optional[int]:
        """Handles missingness for CANCLUNG."""
        return self.__handle_canceractv_gate("canclung")

    def _missingness_cancprost(self) -> Optional[int]:
        """Handles missingness for CANCPROST."""
        return self.__handle_canceractv_gate("cancprost")

    def _missingness_cancother(self) -> Optional[int]:
        """Handles missingness for CANCOTHER."""
        return self.__handle_canceractv_gate("cancother")

    def _missingness_cancrad(self) -> Optional[int]:
        """Handles missingness for CANCRAD."""
        return self.__handle_canceractv_gate("cancrad")

    def _missingness_cancresect(self) -> Optional[int]:
        """Handles missingness for CANCRESECT."""
        return self.__handle_canceractv_gate("cancresect")

    def _missingness_cancimmuno(self) -> Optional[int]:
        """Handles missingness for CANCIMMUNO."""
        return self.__handle_canceractv_gate("cancimmuno")

    def _missingness_cancbone(self) -> Optional[int]:
        """Handles missingness for CANCBONE."""
        return self.__handle_canceractv_gate("cancbone")

    def _missingness_cancchemo(self) -> Optional[int]:
        """Handles missingness for CANCCHEMO."""
        return self.__handle_canceractv_gate("cancchemo")

    def _missingness_canchorm(self) -> Optional[int]:
        """Handles missingness for CANCHORM."""
        return self.__handle_canceractv_gate("canchorm")

    def _missingness_canctroth(self) -> Optional[int]:
        """Handles missingness for CANCTROTH."""
        return self.__handle_canceractv_gate("canctroth")

    ###########################
    # CANCERMETA GATED VALUES #
    ###########################

    def __handle_cancermeta_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by CANCERMETA, which follow:

        If CANCERMETA = 1 and FIELD is blank, FIELD should = 0
        """
        cancermeta = self.uds.get_value("cancermeta", int)
        value = self.uds.get_value(field, int)

        if value is None:
            if cancermeta == 1:
                return 0
            return INFORMED_MISSINGNESS

        return None

    def _missingness_cancmetbr(self) -> Optional[int]:
        """Handles missingness for CANCMETBR."""
        return self.__handle_cancermeta_gate("cancmetbr")

    def _missingness_cancmetoth(self) -> Optional[int]:
        """Handles missingness for CANCMETOTH."""
        return self.__handle_cancermeta_gate("cancmetoth")

    ##########################
    # NOMENSAGE GATED VALUES #
    ##########################

    def __handle_nomensage_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by NOMENSAGE, which follow:

        If NOMENSAGE is between 10 and 70 and FIELD is blank, then FIELD should = 0
        """
        nomensage = self.uds.get_value("nomensage", int)
        value = self.uds.get_value(field, int)

        if value is None and nomensage is not None:  # noqa: SIM102
            if nomensage >= 10 and nomensage <= 70:
                return 0

        return self.generic_missingness(field, int)

    def _missingness_nomensnat(self) -> Optional[int]:
        """Handles missingness for NOMENSNAT."""
        return self.__handle_nomensage_gate("nomensnat")

    def _missingness_nomenshyst(self) -> Optional[int]:
        """Handles missingness for NOMENSHYST."""
        return self.__handle_nomensage_gate("nomenshyst")

    def _missingness_nomenssurg(self) -> Optional[int]:
        """Handles missingness for NOMENSSURG."""
        return self.__handle_nomensage_gate("nomenssurg")

    def _missingness_nomenschem(self) -> Optional[int]:
        """Handles missingness for NOMENSCHEM."""
        return self.__handle_nomensage_gate("nomenschem")

    def _missingness_nomensrad(self) -> Optional[int]:
        """Handles missingness for NOMENSRAD."""
        return self.__handle_nomensage_gate("nomensrad")

    def _missingness_nomenshorm(self) -> Optional[int]:
        """Handles missingness for NOMENSHORM."""
        return self.__handle_nomensage_gate("nomenshorm")

    def _missingness_nomensestr(self) -> Optional[int]:
        """Handles missingness for NOMENSESTR."""
        return self.__handle_nomensage_gate("nomensestr")

    def _missingness_nomensunk(self) -> Optional[int]:
        """Handles missingness for NOMENSUNK."""
        return self.__handle_nomensage_gate("nomensunk")

    def _missingness_nomensoth(self) -> Optional[int]:
        """Handles missingness for NOMENSOTH."""
        return self.__handle_nomensage_gate("nomensoth")

    ########################
    # NACCTBI-GATED VALUES #
    ########################

    def __handle_nacctbi_gated_values(self, field: str) -> Optional[int]:
        """V3 only. Handles values gated by TBI logic and actually looks at the
        derived variable NACCTBI.

        Since this is derived before missingness, assumes it can find it
        under file.info.derived.nacctbi
        """
        value = self.uds.get_value(field, int)
        if value is None:
            nacctbi = self.__derived.get_value("nacctbi", int)
            if nacctbi == 0:
                return 0
            if nacctbi == 9:
                return INFORMED_MISSINGNESS

        return self.generic_missingness(field, int)

    def _missingness_tbibrief(self) -> Optional[int]:
        """Handles missingness for TBIBRIEF."""
        return self.__handle_nacctbi_gated_values("tbibrief")

    def _missingness_tbiexten(self) -> Optional[int]:
        """Handles missingness for TBIEXTEN."""
        return self.__handle_nacctbi_gated_values("tbiexten")

    def _missingness_tbiwolos(self) -> Optional[int]:
        """Handles missingness for TBIWOLOS."""
        return self.__handle_nacctbi_gated_values("tbiwolos")

    def _missingness_tbiyear(self) -> Optional[int]:
        """Handles missingness for TBIYEAR."""
        tbiyear = self.uds.get_value("tbiyear", int)
        nacctbi = self.__derived.get_value("nacctbi", int)

        if tbiyear is None and nacctbi in [0, 9]:
            return 8888

        return self.generic_missingness("tbiyear", int)

    #########
    # OTHER #
    #########

    def _missingness_carotidage(self) -> Optional[int]:
        """Handles missingness for CAROTIDAGE."""
        cbstroke = self.uds.get_value("cbstroke", int)
        angiocp = self.uds.get_value("angiocp", int)
        if cbstroke == 0 or angiocp == 0:
            return 888
        if cbstroke == 9 or angiocp == 9:
            return 999

        return self.handle_prev_visit("carotidage", int, prev_code=777)

    def _missingness_seiznum(self) -> Optional[int]:
        """Handles missingness for SEIZNUM."""
        seizures = self.uds.get_value("seizures", int)
        if seizures in [0, 2]:
            return 8
        if seizures == 9:
            return 9

        return self.generic_missingness("seiznum", int)

    def _missingness_deprtreat(self) -> Optional[int]:
        """Handles missingness for DEPRTREAT."""
        majordep = self.uds.get_value("majordep", int)
        otherdep = self.uds.get_value("otherdep", int)

        if majordep in [0, 2, 9] or otherdep in [0, 2, 9]:
            return 8

        return self.generic_missingness("deprtreat", int)

    def _missingness_pdyr(self) -> Optional[int]:
        """Handles missingness for PDYR.

        From V3 and earlier SAS recode logic
        """
        if self.uds.get_value("pd", int) in [0, 9]:
            return 8888

        return self.generic_missingness("pdyr", int)

    def _missingness_pdothryr(self) -> Optional[int]:
        """Handles missingness for PDOTHRYR.

        From V3 and earlier SAS recode logic
        """
        if self.uds.get_value("pdothr", int) in [0, 9]:
            return 8888

        return self.generic_missingness("pdothryr", int)

    ###################
    # OTHER - WRITEIN #
    ###################

    def _missingness_impotherx(self) -> Optional[str]:
        """Handles missingness for IMPOTHERX."""
        return self.handle_gated_writein("impother", "impotherx", [0])

    def _missingness_cancotherx(self) -> Optional[str]:
        """Handles missingness for CANCOTHERX."""
        return self.handle_gated_writein("cancother", "cancotherx", [0])

    def _missingness_canctrothx(self) -> Optional[str]:
        """Handles missingness for CANCTROTHX."""
        return self.handle_gated_writein("canctroth", "canctrothx", [0])

    def _missingness_othcondx(self) -> Optional[str]:
        """Handles missingness for OTHCONDX."""
        return self.handle_gated_writein("othercond", "othcondx", [0, 9])

    def _missingness_othanxdisx(self) -> Optional[str]:
        """Handles missingness for OTHANXDISX."""
        return self.handle_gated_writein("othanxdis", "othanxdisx", [0, 9])

    def _missingness_nomensothx(self) -> Optional[str]:
        """Handles missingness for NOMENSOTHX."""
        return self.handle_gated_writein("nomensoth", "nomensothx", [0])

    def _missingness_cvothrx(self) -> Optional[str]:
        """Handles missingness for CVOTHRX."""
        return self.handle_gated_writein("cvothr", "cvothrx", [0, 9])

    def _missingness_arthtypx(self) -> Optional[str]:
        """Handles missingness for ARTHTYPX."""
        return self.handle_gated_writein("arthrothr", "arthtypx", [0])

    def _missingness_othsleex(self) -> Optional[str]:
        """Handles missingness for OTHSLEEX."""
        return self.handle_gated_writein("othsleep", "othsleex", [0, 9])

    def _missingness_psycdisx(self) -> Optional[str]:
        """Handles missingness for PSYCDISX."""
        return self.handle_gated_writein("psycdis", "psycdisx", [0, 9])

    ############################
    # Legacy D2-only variables #
    ############################

    def __handle_arth_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by ARTH."""
        arth = self.uds.get_value("arth", int)
        if arth is None or arth == 0:
            return 8

        return self.generic_missingness(field, int)

    def _missingness_artype(self) -> Optional[int]:
        """Handles missingness for ARTYPE."""
        return self.__handle_arth_gate("artype")

    def _missingness_artupex(self) -> Optional[int]:
        """Handles missingness for ARTUPEX."""
        return self.__handle_arth_gate("artupex")

    def _missingness_artloex(self) -> Optional[int]:
        """Handles missingness for ARTLOEX."""
        return self.__handle_arth_gate("artloex")

    def _missingness_artspin(self) -> Optional[int]:
        """Handles missingness for ARTSPIN."""
        return self.__handle_arth_gate("artspin")

    def _missingness_artunkn(self) -> Optional[int]:
        """Handles missingness for ARTUNKN."""
        return self.__handle_arth_gate("artunkn")
