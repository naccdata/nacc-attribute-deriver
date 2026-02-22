"""Class to handle A5D2-specific missingness values.

Some of these variables have recode logic defined in the legacy SAS
code, so there are some version differences.
"""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.attributes.namespace.namespace import (
    DerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)


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
    ) -> int:
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
    ) -> int:
        """Handle generic A5D2 gate with carry forward."""
        return self.__handle_a5d2_gate(
            gate,
            field,
            no_return_value=no_return_value,
            unknown_return_value=unknown_return_value,
            carry_forward=True,
        )

    def _missingness_smokyrs(self) -> int:
        """Handles missingness for SMOKYRS."""
        return self.handle_a5d2_carry_forward(
            "tobac100",
            "smokyrs",
            no_return_value=88,
            unknown_return_value=99,
        )

    ########################
    # GATED CARRY FORWARDS #
    ########################

    def _missingness_quitsmok(self) -> int:
        """Handles missingness for QUITSMOK."""
        return self.handle_a5d2_carry_forward("tobac100", "quitsmok")

    def _missingness_hrtattage(self) -> int:
        """Handles missingness for HRTATTAGE."""
        return self.handle_a5d2_carry_forward("hrtattack", "hrtattage")

    def _missingness_cardarrage(self) -> int:
        """Handles missingness for CARDARRAGE."""
        return self.handle_a5d2_carry_forward("cardarrest", "cardarrage")

    def _missingness_bypassage(self) -> int:
        """Handles missingness for BYPASSAGE."""
        return self.handle_a5d2_carry_forward("cvbypass", "bypassage")

    def _missingness_pacdefage(self) -> int:
        """Handles missingness for PACDEFAGE."""
        return self.handle_a5d2_carry_forward("cvpacdef", "pacdefage")

    def _missingness_valveage(self) -> int:
        """Handles missingness for VALVEAGE."""
        return self.handle_a5d2_carry_forward("cvhvalve", "valveage")

    def _missingness_strokage(self) -> int:
        """Handles missingness for STROKAGE."""
        return self.handle_a5d2_carry_forward("cbstroke", "strokage")

    def _missingness_tiaage(self) -> int:
        """Handles missingness for TIAAGE."""
        return self.handle_a5d2_carry_forward("cbtia", "tiaage")

    def _missingness_pdage(self) -> int:
        """Handles missingness for PDAGE."""
        return self.handle_a5d2_carry_forward("pd", "pdage")

    def _missingness_pdothrage(self) -> int:
        """Handles missingness for PDOTHRAGE."""
        return self.handle_a5d2_carry_forward("pdothr", "pdothrage")

    def _missingness_seizage(self) -> int:
        """Handles missingness for SEIZAGE."""
        return self.handle_a5d2_carry_forward("seizures", "seizage")

    def _missingness_impyears(self) -> int:
        """Handles missingness for IMPYEARS."""
        return self.handle_a5d2_carry_forward("headimp", "impyears")

    def _missingness_firsttbi(self) -> int:
        """Handles missingness for FIRSTTBI."""
        return self.handle_a5d2_carry_forward("headinjury", "firsttbi")

    def _missingness_lasttbi(self) -> int:
        """Handles missingness for LASTTBI."""
        return self.handle_a5d2_carry_forward("headinjury", "lasttbi")

    def _missingness_diabage(self) -> int:
        """Handles missingness for DIABAGE."""
        return self.handle_a5d2_carry_forward("diabetes", "diabage")

    def _missingness_hypertage(self) -> int:
        """Handles missingness for HYPERTAGE."""
        return self.handle_a5d2_carry_forward("hyperten", "hypertage")

    def _missingness_hyperchage(self) -> int:
        """Handles missingness for HYPERCHAGE."""
        return self.handle_a5d2_carry_forward("hypercho", "hyperchage")

    def _missingness_cancerage(self) -> int:
        """Handles missingness for CANCERAGE."""
        return self.handle_a5d2_carry_forward("canceractv", "cancerage")

    def _missingness_kidneyage(self) -> int:
        """Handles missingness for KIDNEYAGE."""
        return self.handle_a5d2_carry_forward("kidney", "kidneyage")

    def _missingness_liverage(self) -> int:
        """Handles missingness for LIVERAGE."""
        return self.handle_a5d2_carry_forward("liver", "liverage")

    def _missingness_pvdage(self) -> int:
        """Handles missingness for PVDAGE."""
        return self.handle_a5d2_carry_forward("pvd", "pvdage")

    def _missingness_hivage(self) -> int:
        """Handles missingness for HIVAGE."""
        return self.handle_a5d2_carry_forward("hivdiag", "hivage")

    #################
    # GENERIC GATES #
    #################

    def _missingness_packsper(self) -> int:
        """Handles missingness for PACKSPER."""
        return self.__handle_a5d2_gate("tobac100", "packsper")

    def _missingness_tobac30(self) -> int:
        """Handles missingness for TOBAC30."""
        return self.__handle_a5d2_gate("tobac100", "tobac30")

    def _missingness_alcdrinks(self) -> int:
        """Handles missingness for ALCDRINKS."""
        return self.__handle_a5d2_gate("alcfreqyr", "alcdrinks")

    def _missingness_alcbinge(self) -> int:
        """Handles missingness for ALCBINGE."""
        return self.__handle_a5d2_gate("alcfreqyr", "alcbinge")

    def _missingness_hrtattmult(self) -> int:
        """Handles missingness for HRTATTMULT."""
        return self.__handle_a5d2_gate("hrtattack", "hrtattmult")

    def _missingness_strokstat(self) -> int:
        """Handles missingness for STROKSTAT."""
        return self.__handle_a5d2_gate("cbstroke", "strokstat")

    def _missingness_covidhosp(self) -> int:
        """Handles missingness for COVIDHOSP."""
        return self.__handle_a5d2_gate("covid19", "covidhosp")

    def _missingness_generalanx(self) -> int:
        """Handles missingness for GENERALANX."""
        return self.__handle_a5d2_gate("anxiety", "generalanx")

    def _missingness_panicdis(self) -> int:
        """Handles missingness for PANICDIS."""
        return self.__handle_a5d2_gate("anxiety", "panicdis")

    def _missingness_othanxdis(self) -> int:
        """Handles missingness for OTHANXDIS."""
        return self.__handle_a5d2_gate("anxiety", "othanxdis")

    def _missingness_angiocp(self) -> int:
        """Handles missingness for ANGIOCP."""
        return self.__handle_a5d2_gate("cbstroke", "angiocp")

    def _missingness_strokmul(self) -> int:
        """Handles missingness for STROKMUL."""
        return self.__handle_a5d2_gate("cbstroke", "strokmul")

    def _missingness_ocd(self) -> int:
        """Handles missingness for OCD."""
        return self.__handle_a5d2_gate("anxiety", "ocd")

    def _missingness_tiamult(self) -> int:
        """Handles missingness for TIAMULT."""
        return self.__handle_a5d2_gate("cbtia", "tiamult")

    # the following have unique logic from V3 and earlier so
    # brought over from SAS recode logic

    def _missingness_diabtype(self) -> int:
        """Handles missingness for DIABTYPE."""
        diabetes = self.uds.get_value("diabetes", int)
        formvera5 = self.uds.get_value("formvera5", float)
        if not formvera5:
            formvera5 = self.formver

        if formvera5 < 3:
            return INFORMED_MISSINGNESS

        if formvera5 < 4 and diabetes in [0, 9]:
            return 8

        return self.__handle_a5d2_gate("diabetes", "diabtype")

    def _missingness_alcfreq(self) -> int:
        """Only V3.

        Handles missingness for ALCFREQ.
        """
        return self.__handle_a5d2_gate(
            "alcoccas",
            "alcfreq",
            no_return_value=8,
            unknown_return_value=INFORMED_MISSINGNESS,
        )

    def _missingness_hattmult(self) -> int:
        """Handles missingness for HATTMULT.

        Only V3.
        """
        return self.__handle_a5d2_gate(
            "cvhatt",
            "hattmult",
            no_return_value=8,
            unknown_return_value=INFORMED_MISSINGNESS,
        )

    def _missingness_hattyear(self) -> int:
        """Handles missingness for HATTYEAR.

        Only V3
        """
        return self.__handle_a5d2_gate(
            "cvhatt",
            "hattyear",
            no_return_value=8888,
            unknown_return_value=INFORMED_MISSINGNESS,
        )

    #############################
    # CARRY FORWARD ONLY VALUES #
    #############################

    def __adjust_carry_forward_digits(
        self, field: str, adjust_88: bool = False, adjust_99: bool = False
    ) -> int:
        """In the 2025 Febuary release, 88 and 99 were adjusted to 888 and 999
        for the following variables, but some packets with the old values had
        already been accepted. So need to adjust here.

        Need to fine-tune between 88/99 since some have allowed ranges
        that go past 88.
        """
        result = self.handle_prev_visit(field, int, prev_code=777)
        if adjust_88 and result == 88:
            return 888
        if adjust_99 and result == 99:
            return 999

        return result

    def _missingness_nomensage(self) -> int:
        """Handles missingness for NOMENSAGE."""
        return self.__adjust_carry_forward_digits(
            "nomensage", adjust_88=True, adjust_99=True
        )

    def _missingness_hrtyears(self) -> int:
        """Handles missingness for HRTYEARS.

        0-90 or 999.
        """
        return self.__adjust_carry_forward_digits("hrtyears", adjust_99=True)

    def _missingness_hrtstrtage(self) -> int:
        """Handles missingness for HRTSTRTAGE. 10-110 or 999.

        NOTE: because the new range went over 88/99s, we can't
        easily detect old values. let go through for now.
        """
        return self.__adjust_carry_forward_digits("hrtstrtage")

    def _missingness_hrtendage(self) -> int:
        """Handles missingness for HRTENDAGE. 10-110 or 888 or 999.

        NOTE: because the new range went over 88/99s, we can't
        easily detect old values. let go through for now.
        """
        return self.__adjust_carry_forward_digits("hrtendage")

    def _missingness_bcpillsyr(self) -> int:
        """Handles missingness for BCPILLSYR."""
        return self.__adjust_carry_forward_digits("bcpillsyr", adjust_99=True)

    def _missingness_bcstartage(self) -> int:
        """Handles missingness for BCSTARTAGE."""
        return self.__adjust_carry_forward_digits("bcstartage", adjust_99=True)

    def _missingness_bcendage(self) -> int:
        """Handles missingness for BCENDAGE."""
        return self.__adjust_carry_forward_digits(
            "bcendage", adjust_88=True, adjust_99=True
        )

    def _missingness_menarche(self) -> int:
        """Handles missingness for MENARCHE.

        Has no carry-forward so adjust directly.
        """
        value = self.uds.get_value("menarche", int)
        if value == 88:
            return 888

        if value == 99:
            return 999

        return self.generic_missingness("menarche", int)

    ########################
    # HEADIMP GATED VALUES #
    ########################

    def __handle_headimp_gate(self, field: str) -> int:
        """Handles variables gated by HEADIMP, which follow:

        If HEADIMP = 1 and FIELD is blank, FIELD should = 0
        """
        headimp = self.uds.get_value("headimp", int)
        value = self.uds.get_value(field, int)

        if value is None:
            if headimp == 1:
                return 0
            return INFORMED_MISSINGNESS

        return value

    def _missingness_impamfoot(self) -> int:
        """Handles missingness for IMPAMFOOT."""
        return self.__handle_headimp_gate("impamfoot")

    def _missingness_impsoccer(self) -> int:
        """Handles missingness for IMPSOCCER."""
        return self.__handle_headimp_gate("impsoccer")

    def _missingness_imphockey(self) -> int:
        """Handles missingness for IMPHOCKEY."""
        return self.__handle_headimp_gate("imphockey")

    def _missingness_impboxing(self) -> int:
        """Handles missingness for IMPBOXING."""
        return self.__handle_headimp_gate("impboxing")

    def _missingness_impsport(self) -> int:
        """Handles missingness for IMPSPORT."""
        return self.__handle_headimp_gate("impsport")

    def _missingness_impipv(self) -> int:
        """Handles missingness for IMPIPV."""
        return self.__handle_headimp_gate("impipv")

    def _missingness_impmilit(self) -> int:
        """Handles missingness for IMPMILIT."""
        return self.__handle_headimp_gate("impmilit")

    def _missingness_impassault(self) -> int:
        """Handles missingness for IMPASSAULT."""
        return self.__handle_headimp_gate("impassault")

    def _missingness_impother(self) -> int:
        """Handles missingness for IMPOTHER."""
        return self.__handle_headimp_gate("impother")

    #########################
    # DIABETES GATED VALUES #
    #########################

    def __handle_diabetes_gate(self, field: str) -> int:
        """Handles variables gated by DIABETES, which follow:

        If DIABETES = 1 or 2 and FIELD is blank, FIELD should = 0
        """
        diabetes = self.uds.get_value("diabetes", int)
        value = self.uds.get_value(field, int)

        if value is None:
            if diabetes in [1, 2]:
                return 0
            return INFORMED_MISSINGNESS

        return value

    def _missingness_diabins(self) -> int:
        """Handles missingness for DIABINS."""
        return self.__handle_diabetes_gate("diabins")

    def _missingness_diabmeds(self) -> int:
        """Handles missingness for DIABMEDS."""
        return self.__handle_diabetes_gate("diabmeds")

    def _missingness_diabglp1(self) -> int:
        """Handles missingness for DIABGLP1."""
        return self.__handle_diabetes_gate("diabglp1")

    def _missingness_diabrecact(self) -> int:
        """Handles missingness for DIABRECACT."""
        return self.__handle_diabetes_gate("diabrecact")

    def _missingness_diabdiet(self) -> int:
        """Handles missingness for DIABDIET."""
        return self.__handle_diabetes_gate("diabdiet")

    ##########################
    # ARTHRITIS GATED VALUES #
    ##########################

    def __handle_arthritis_gate(self, field: str) -> int:
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

        return value

    def _missingness_arthupex(self) -> int:
        """Handles missingness for ARTHUPEX."""
        return self.__handle_arthritis_gate("arthupex")

    def _missingness_arthloex(self) -> int:
        """Handles missingness for ARTHLOEX."""
        return self.__handle_arthritis_gate("arthloex")

    def _missingness_arthspin(self) -> int:
        """Handles missingness for ARTHSPIN."""
        return self.__handle_arthritis_gate("arthspin")

    def _missingness_arthunk(self) -> int:
        """Handles missingness for ARTHUNK."""
        return self.__handle_arthritis_gate("arthunk")

    def _missingness_arthtype(self) -> int:
        """Handles missingness for ARTHTYPE."""
        arthrit = self.uds.get_value("arthrit", int)
        arthtype = self.uds.get_value("arthtype", int)

        if arthtype is None:
            if arthrit in [0, 9]:
                return 8

            return INFORMED_MISSINGNESS

        return arthtype

    ######################
    # APNEA GATED VALUES #
    ######################

    def __handle_apnea_gate(self, field: str) -> int:
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

    def _missingness_cpap(self) -> int:
        """Handles missingness for CPAP."""
        return self.__handle_apnea_gate("cpap")

    def _missingness_apneaoral(self) -> int:
        """Handles missingness for APNEAORAL."""
        return self.__handle_apnea_gate("apneaoral")

    ###########################
    # CANCERACTV GATED VALUES #
    ###########################

    def __handle_canceractv_gate(self, field: str) -> int:
        """Handles variables gated by CANCERACTV, which follow:

        If CANCERACTV = 1 or 2 and FIELD is blank, FIELD should = 0
        """
        canceractv = self.uds.get_value("canceractv", int)
        value = self.uds.get_value(field, int)

        if value is None:
            if canceractv in [1, 2]:
                return 0
            return INFORMED_MISSINGNESS

        return value

    def _missingness_cancerprim(self) -> int:
        """Handles missingness for CANCERPRIM."""
        return self.__handle_canceractv_gate("cancerprim")

    def _missingness_cancermeta(self) -> int:
        """Handles missingness for CANCERMETA."""
        return self.__handle_canceractv_gate("cancermeta")

    def _missingness_cancerunk(self) -> int:
        """Handles missingness for CANCERUNK."""
        return self.__handle_canceractv_gate("cancerunk")

    def _missingness_cancblood(self) -> int:
        """Handles missingness for CANCBLOOD."""
        return self.__handle_canceractv_gate("cancblood")

    def _missingness_cancbreast(self) -> int:
        """Handles missingness for CANCBREAST."""
        return self.__handle_canceractv_gate("cancbreast")

    def _missingness_canccolon(self) -> int:
        """Handles missingness for CANCCOLON."""
        return self.__handle_canceractv_gate("canccolon")

    def _missingness_canclung(self) -> int:
        """Handles missingness for CANCLUNG."""
        return self.__handle_canceractv_gate("canclung")

    def _missingness_cancprost(self) -> int:
        """Handles missingness for CANCPROST."""
        return self.__handle_canceractv_gate("cancprost")

    def _missingness_cancother(self) -> int:
        """Handles missingness for CANCOTHER."""
        return self.__handle_canceractv_gate("cancother")

    def _missingness_cancrad(self) -> int:
        """Handles missingness for CANCRAD."""
        return self.__handle_canceractv_gate("cancrad")

    def _missingness_cancresect(self) -> int:
        """Handles missingness for CANCRESECT."""
        return self.__handle_canceractv_gate("cancresect")

    def _missingness_cancimmuno(self) -> int:
        """Handles missingness for CANCIMMUNO."""
        return self.__handle_canceractv_gate("cancimmuno")

    def _missingness_cancbone(self) -> int:
        """Handles missingness for CANCBONE."""
        return self.__handle_canceractv_gate("cancbone")

    def _missingness_cancchemo(self) -> int:
        """Handles missingness for CANCCHEMO."""
        return self.__handle_canceractv_gate("cancchemo")

    def _missingness_canchorm(self) -> int:
        """Handles missingness for CANCHORM."""
        return self.__handle_canceractv_gate("canchorm")

    def _missingness_canctroth(self) -> int:
        """Handles missingness for CANCTROTH."""
        return self.__handle_canceractv_gate("canctroth")

    ###########################
    # CANCERMETA GATED VALUES #
    ###########################

    def __handle_cancermeta_gate(self, field: str) -> int:
        """Handles variables gated by CANCERMETA, which follow:

        If CANCERMETA = 1 and FIELD is blank, FIELD should = 0
        """
        cancermeta = self.uds.get_value("cancermeta", int)
        value = self.uds.get_value(field, int)

        if value is None:
            if cancermeta == 1:
                return 0
            return INFORMED_MISSINGNESS

        return value

    def _missingness_cancmetbr(self) -> int:
        """Handles missingness for CANCMETBR."""
        return self.__handle_cancermeta_gate("cancmetbr")

    def _missingness_cancmetoth(self) -> int:
        """Handles missingness for CANCMETOTH."""
        return self.__handle_cancermeta_gate("cancmetoth")

    ##########################
    # NOMENSAGE GATED VALUES #
    ##########################

    def __handle_nomensage_gate(self, field: str) -> int:
        """Handles variables gated by NOMENSAGE, which follow:

        If NOMENSAGE is between 10 and 70 and FIELD is blank, then FIELD should = 0
        """
        nomensage = self.uds.get_value("nomensage", int)
        value = self.uds.get_value(field, int)

        if value is None and nomensage is not None:  # noqa: SIM102
            if nomensage >= 10 and nomensage <= 70:
                return 0

        return self.generic_missingness(field, int)

    def _missingness_nomensnat(self) -> int:
        """Handles missingness for NOMENSNAT."""
        return self.__handle_nomensage_gate("nomensnat")

    def _missingness_nomenshyst(self) -> int:
        """Handles missingness for NOMENSHYST."""
        return self.__handle_nomensage_gate("nomenshyst")

    def _missingness_nomenssurg(self) -> int:
        """Handles missingness for NOMENSSURG."""
        return self.__handle_nomensage_gate("nomenssurg")

    def _missingness_nomenschem(self) -> int:
        """Handles missingness for NOMENSCHEM."""
        return self.__handle_nomensage_gate("nomenschem")

    def _missingness_nomensrad(self) -> int:
        """Handles missingness for NOMENSRAD."""
        return self.__handle_nomensage_gate("nomensrad")

    def _missingness_nomenshorm(self) -> int:
        """Handles missingness for NOMENSHORM."""
        return self.__handle_nomensage_gate("nomenshorm")

    def _missingness_nomensestr(self) -> int:
        """Handles missingness for NOMENSESTR."""
        return self.__handle_nomensage_gate("nomensestr")

    def _missingness_nomensunk(self) -> int:
        """Handles missingness for NOMENSUNK."""
        return self.__handle_nomensage_gate("nomensunk")

    def _missingness_nomensoth(self) -> int:
        """Handles missingness for NOMENSOTH."""
        return self.__handle_nomensage_gate("nomensoth")

    ########################
    # NACCTBI-GATED VALUES #
    ########################

    def __handle_nacctbi_gated_values(self, field: str) -> int:
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

    def _missingness_tbibrief(self) -> int:
        """Handles missingness for TBIBRIEF."""
        return self.__handle_nacctbi_gated_values("tbibrief")

    def _missingness_tbiexten(self) -> int:
        """Handles missingness for TBIEXTEN."""
        return self.__handle_nacctbi_gated_values("tbiexten")

    def _missingness_tbiwolos(self) -> int:
        """Handles missingness for TBIWOLOS."""
        return self.__handle_nacctbi_gated_values("tbiwolos")

    def _missingness_tbiyear(self) -> int:
        """Handles missingness for TBIYEAR."""
        tbiyear = self.uds.get_value("tbiyear", int)
        nacctbi = self.__derived.get_value("nacctbi", int)

        if tbiyear is None and nacctbi in [0, 9]:
            return 8888

        return self.generic_missingness("tbiyear", int)

    #########
    # OTHER #
    #########

    def _missingness_carotidage(self) -> int:
        """Handles missingness for CAROTIDAGE."""
        cbstroke = self.uds.get_value("cbstroke", int)
        angiocp = self.uds.get_value("angiocp", int)
        if cbstroke == 0 or angiocp == 0:
            return 888
        if cbstroke == 9 or angiocp == 9:
            return 999

        return self.handle_prev_visit("carotidage", int, prev_code=777)

    def _missingness_seiznum(self) -> int:
        """Handles missingness for SEIZNUM."""
        seizures = self.uds.get_value("seizures", int)
        if seizures in [0, 2]:
            return 8
        if seizures == 9:
            return 9

        return self.generic_missingness("seiznum", int)

    def _missingness_deprtreat(self) -> int:
        """Handles missingness for DEPRTREAT."""
        majordep = self.uds.get_value("majordep", int)
        otherdep = self.uds.get_value("otherdep", int)

        if majordep in [0, 2, 9] or otherdep in [0, 2, 9]:
            return 8

        return self.generic_missingness("deprtreat", int)

    def _missingness_pdyr(self) -> int:
        """Handles missingness for PDYR.

        From V3 and earlier SAS recode logic
        """
        if self.uds.get_value("pd", int) in [0, 9]:
            return 8888

        return self.generic_missingness("pdyr", int)

    def _missingness_pdothryr(self) -> int:
        """Handles missingness for PDOTHRYR.

        From V3 and earlier SAS recode logic
        """
        if self.uds.get_value("pdothr", int) in [0, 9]:
            return 8888

        return self.generic_missingness("pdothryr", int)

    ###################
    # OTHER - WRITEIN #
    ###################

    def _missingness_impotherx(self) -> str:
        """Handles missingness for IMPOTHERX."""
        return self.handle_gated_writein("impother", "impotherx", [0])

    def _missingness_cancotherx(self) -> str:
        """Handles missingness for CANCOTHERX."""
        return self.handle_gated_writein("cancother", "cancotherx", [0])

    def _missingness_canctrothx(self) -> str:
        """Handles missingness for CANCTROTHX."""
        return self.handle_gated_writein("canctroth", "canctrothx", [0])

    def _missingness_othcondx(self) -> str:
        """Handles missingness for OTHCONDX."""
        return self.handle_gated_writein("othercond", "othcondx", [0, 9])

    def _missingness_othanxdisx(self) -> str:
        """Handles missingness for OTHANXDISX."""
        return self.handle_gated_writein("othanxdis", "othanxdisx", [0, 9])

    def _missingness_nomensothx(self) -> str:
        """Handles missingness for NOMENSOTHX."""
        return self.handle_gated_writein("nomensoth", "nomensothx", [0])

    def _missingness_cvothrx(self) -> str:
        """Handles missingness for CVOTHRX."""
        return self.handle_gated_writein("cvothr", "cvothrx", [0, 9])

    def _missingness_arthtypx(self) -> str:
        """Handles missingness for ARTHTYPX."""
        return self.handle_gated_writein("arthrothr", "arthtypx", [0])

    def _missingness_othsleex(self) -> str:
        """Handles missingness for OTHSLEEX."""
        return self.handle_gated_writein("othsleep", "othsleex", [0, 9])

    def _missingness_psycdisx(self) -> str:
        """Handles missingness for PSYCDISX."""
        return self.handle_gated_writein("psycdis", "psycdisx", [0, 9])

    ############################
    # Legacy D2-only variables #
    ############################

    def __handle_arth_gate(self, field: str) -> int:
        """Handles variables gated by ARTH."""
        value = self.uds.get_value(field, int)

        if value is None or value == 0:
            # if ARTH is 0 (no) return 8 (not assessed)
            arth = self.uds.get_value("arth", int)
            if arth == 0:
                return 8

            # if ARTH = 8/blank (Not assessed)
            # return -4
            value = self.uds.get_value(field, int)
            if arth is None or arth == 8:
                return INFORMED_MISSINGNESS

            # if ARTH = 1, fallback to generic
            # missingness

        return self.generic_missingness(field, int)

    def _missingness_artype(self) -> int:
        """Handles missingness for ARTYPE."""
        return self.__handle_arth_gate("artype")

    def _missingness_artupex(self) -> int:
        """Handles missingness for ARTUPEX."""
        return self.__handle_arth_gate("artupex")

    def _missingness_artloex(self) -> int:
        """Handles missingness for ARTLOEX."""
        return self.__handle_arth_gate("artloex")

    def _missingness_artspin(self) -> int:
        """Handles missingness for ARTSPIN."""
        return self.__handle_arth_gate("artspin")

    def _missingness_artunkn(self) -> int:
        """Handles missingness for ARTUNKN."""
        return self.__handle_arth_gate("artunkn")
