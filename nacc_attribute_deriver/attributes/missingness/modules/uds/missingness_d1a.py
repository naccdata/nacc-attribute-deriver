"""Class to handle D1a-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

from .missingness_d1 import UDSFormD1Missingness


class UDSFormD1aMissingness(UDSFormD1Missingness):
    ###########################
    # NORMCOG-gated variables #
    ###########################

    def __handle_normcog_gate(
        self, field: str, ignore_normcog_0: bool = False
    ) -> Optional[int]:
        """Handles NORMCOG-gated variables, which follow:

        If NORMCOG = 1 and FIELD is blank, FIELD = 8
        """
        if self.uds.get_value(field, int) is None:
            if self.normcog == 1:
                return 8
            if not ignore_normcog_0 and self.normcog == 0:
                return 0

            return INFORMED_MISSINGNESS

        return None

    def _missingness_scd(self) -> Optional[int]:
        """Handles missingness for SCD."""
        return self.__handle_normcog_gate("scd", ignore_normcog_0=True)

    def _missingness_predomsyn(self) -> Optional[int]:
        """Handles missingness for PREDOMSYN."""
        return self.__handle_normcog_gate("predomsyn", ignore_normcog_0=True)

    def _missingness_majdepdx(self) -> Optional[int]:
        """Handles missingness for MAJDEPDX."""
        return self.__handle_normcog_gate("majdepdx")

    def _missingness_othdepdx(self) -> Optional[int]:
        """Handles missingness for OTHDEPDX."""
        return self.__handle_normcog_gate("othdepdx")

    def _missingness_ndevdis(self) -> Optional[int]:
        """Handles missingness for NDEVDIS."""
        return self.__handle_normcog_gate("ndevdis")

    def _missingness_tbidx(self) -> Optional[int]:
        """Handles missingness for TBIDX."""
        return self.__handle_normcog_gate("tbidx")

    def _missingness_postc19(self) -> Optional[int]:
        """Handles missingness for POSTC19."""
        return self.__handle_normcog_gate("postc19")

    def _missingness_apneadx(self) -> Optional[int]:
        """Handles missingness for APNEADX."""
        return self.__handle_normcog_gate("apneadx")

    def _missingness_othcogill(self) -> Optional[int]:
        """Handles missingness for OTHCOGILL."""
        return self.__handle_normcog_gate("othcogill")

    def _missingness_hyceph(self) -> Optional[int]:
        """Handles missingness for HYCEPH."""
        return self.__handle_normcog_gate("hyceph")

    def _missingness_epilep(self) -> Optional[int]:
        """Handles missingness for EPILEP."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_gate("epilep")

    def _missingness_neop(self) -> Optional[int]:
        """Handles missingness for NEOP."""
        return self.__handle_normcog_gate("neop")

    def _missingness_hiv(self) -> Optional[int]:
        """Handles missingness for HIV."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_gate("hiv")

    def _missingness_bipoldx(self) -> Optional[int]:
        """Handles missingness for BIPOLDX."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_gate("bipoldx")

    def _missingness_schizop(self) -> Optional[int]:
        """Handles missingness for SCHIZOP."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_gate("schizop")

    def _missingness_anxiet(self) -> Optional[int]:
        """Handles missingness for ANXIET."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_gate("anxiet")

    def _missingness_delir(self) -> Optional[int]:
        """Handles missingness for DELIR."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_gate("delir")

    def _missingness_ptsddx(self) -> Optional[int]:
        """Handles missingness for PTSDDX."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_gate("ptsddx")

    def _missingness_othpsy(self) -> Optional[int]:
        """Handles missingness for OTHPSY."""
        return self.__handle_normcog_gate("othpsy")

    def _missingness_alcdem(self) -> Optional[int]:
        """Handles missingness for ALCDEM."""
        return self.__handle_normcog_gate("alcdem")

    def _missingness_impsub(self) -> Optional[int]:
        """Handles missingness for IMPSUB."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_gate("impsub")

    def _missingness_meds(self) -> Optional[int]:
        """Handles missingness for MEDS."""
        return self.__handle_normcog_gate("meds")

    def _missingness_cogoth(self) -> Optional[int]:
        """Handles missingness for COGOTH."""
        return self.__handle_normcog_gate("cogoth")

    def _missingness_cogoth2(self) -> Optional[int]:
        """Handles missingness for COGOTH2."""
        return self.__handle_normcog_gate("cogoth2")

    def _missingness_cogoth3(self) -> Optional[int]:
        """Handles missingness for COGOTH3."""
        return self.__handle_normcog_gate("cogoth3")

    def _missingness_probad(self) -> Optional[int]:
        """Handles missingness for PROBAD."""
        return self.__handle_normcog_gate("probad")

    def _missingness_possad(self) -> Optional[int]:
        """Handles missingness for POSSAD."""
        return self.__handle_normcog_gate("possad")

    def _missingness_probadif(self) -> Optional[int]:
        """Handles missingness for PROBADIF."""
        return self.__handle_normcog_gate("probadif")

    def _missingness_possadif(self) -> Optional[int]:
        """Handles missingness for POSSADIF."""
        return self.__handle_normcog_gate("possadif")

    def _missingness_ftd(self) -> Optional[int]:
        """Handles missingness for FTD."""
        return self.__handle_normcog_gate("ftd")

    def _missingness_ftdif(self) -> Optional[int]:
        """Handles missingness for FTDIF."""
        return self.__handle_normcog_gate("ftdif")

    def _missingness_ppaph(self) -> Optional[int]:
        """Handles missingness for PPAPH."""
        return self.__handle_normcog_gate("ppaph")

    def _missingness_ppaphif(self) -> Optional[int]:
        """Handles missingness for PPAPHIF."""
        return self.__handle_normcog_gate("ppaphif")

    def _missingness_vasc(self) -> Optional[int]:
        """Handles missingness for VASC."""
        return self.__handle_normcog_gate("vasc")

    def _missingness_vascif(self) -> Optional[int]:
        """Handles missingness for VASCIF."""
        return self.__handle_normcog_gate("vascif")

    def _missingness_vascps(self) -> Optional[int]:
        """Handles missingness for VASCPS."""
        return self.__handle_normcog_gate("vascps")

    def _missingness_vascpsif(self) -> Optional[int]:
        """Handles missingness for VASCPSIF."""
        return self.__handle_normcog_gate("vascpsif")

    def _missingness_strokif(self) -> Optional[int]:
        """Handles missingness for STROKIF."""
        return self.__handle_normcog_gate("strokif")

    def _missingness_esstreif(self) -> Optional[int]:
        """Handles missingness for ESSTREIF."""
        return self.__handle_normcog_gate("esstreif")

    def _missingness_brninjif(self) -> Optional[int]:
        """Handles missingness for BRNINJIF."""
        return self.__handle_normcog_gate("brninjif")

    def _missingness_depif(self) -> Optional[int]:
        """Handles missingness for DEPIF."""
        return self.__handle_normcog_gate("depif")

    def _missingness_dysillif(self) -> Optional[int]:
        """Handles missingness for DYSILLIF."""
        return self.__handle_normcog_gate("dysillif")

    def _missingness_demunif(self) -> Optional[int]:
        """Handles missingness for DEMUNIF."""
        return self.__handle_normcog_gate("demunif")

    def _missingness_dysill(self) -> Optional[int]:
        """Handles missingness for DYSILL."""
        return self.__handle_normcog_gate("dysill")

    def _missingness_demun(self) -> Optional[int]:
        """Handles missingness for DEMUN."""
        return self.__handle_normcog_gate("demun")

    ########################################
    # NORMCOG and DEMENTED-gated variables #
    ########################################

    def __handle_normcog_demented_gate(self, field: str) -> Optional[int]:
        """Handles NORMCOG and DEMENTED-gated variables, which follow:

        If NORMCOG = 0 and DEMENTED = 0 and FIELD is blank, then FIELD = 0
        """
        if self.uds.get_value(field, int) is None:
            if self.normcog == 0 and self.demented == 0:
                return 0

            return INFORMED_MISSINGNESS

        return None

    def _missingness_mcicritcln(self) -> Optional[int]:
        """Handles missingness for MCICRITCLN."""
        return self.__handle_normcog_demented_gate("mcicritcln")

    def _missingness_mcicritimp(self) -> Optional[int]:
        """Handles missingness for MCICRITIMP."""
        return self.__handle_normcog_demented_gate("mcicritimp")

    def _missingness_mcicritfun(self) -> Optional[int]:
        """Handles missingness for MCICRITFUN."""
        return self.__handle_normcog_demented_gate("mcicritfun")

    ##############################################
    # NORMCOG, DEMENTED, and MCI-gated variables #
    ##############################################

    def __handle_normcog_demented_mci_gate(self, field: str) -> Optional[int]:
        """Handles NORMCOG DEMENTED, and MCI-gated variables, which follow:

        If NORMCOG = 0 and DEMENTED = 0 and MCI = 0 and FIELD is blank,
        then FIELD = 0
        """
        if self.uds.get_value(field, int) is None:
            if self.normcog == 0 and self.demented == 0 and self.mci == 0:
                return 0

            return INFORMED_MISSINGNESS

        return None

    def _missingness_impnomcifu(self) -> Optional[int]:
        """Handles missingness for IMPNOMCIFU."""
        return self.__handle_normcog_demented_mci_gate("impnomcifu")

    def _missingness_impnomcicg(self) -> Optional[int]:
        """Handles missingness for IMPNOMCICG."""
        return self.__handle_normcog_demented_mci_gate("impnomcicg")

    def _missingness_impnomclcd(self) -> Optional[int]:
        """Handles missingness for IMPNOMCLCD."""
        return self.__handle_normcog_demented_mci_gate("impnomclcd")

    def _missingness_impnomcio(self) -> Optional[int]:
        """Handles missingness for IMPNOMCIO."""
        return self.__handle_normcog_demented_mci_gate("impnomcio")

    ####################################
    # Cognitive status-gated variables #
    ####################################

    def __handle_cognitive_status_gate(self, field: str) -> Optional[int]:
        """Handles variables dependent on cognitive status:

        If (MCI = 1 or DEMENTED = 1) and FIELD is blank, then FIELD = 0
        If (NORMCOG = 1 or IMPNOMCI = 1) and FIELD is blank, then FIELD = 8
        """
        if self.uds.get_value(field, int) is None:
            if self.mci == 1 or self.demented == 1:
                return 0
            if self.normcog == 1 or self.impnomci == 1:
                return 8

            return INFORMED_MISSINGNESS

        return None

    def _missingness_cdommem(self) -> Optional[int]:
        """Handles missingness for CDOMMEM."""
        return self.__handle_cognitive_status_gate("cdommem")

    def _missingness_cdomlang(self) -> Optional[int]:
        """Handles missingness for CDOMLANG."""
        return self.__handle_cognitive_status_gate("cdomlang")

    def _missingness_cdomattn(self) -> Optional[int]:
        """Handles missingness for CDOMATTN."""
        return self.__handle_cognitive_status_gate("cdomattn")

    def _missingness_cdomexec(self) -> Optional[int]:
        """Handles missingness for CDOMEXEC."""
        return self.__handle_cognitive_status_gate("cdomexec")

    def _missingness_cdomvisu(self) -> Optional[int]:
        """Handles missingness for CDOMVISU."""
        return self.__handle_cognitive_status_gate("cdomvisu")

    def _missingness_cdombeh(self) -> Optional[int]:
        """Handles missingness for CDOMBEH."""
        return self.__handle_cognitive_status_gate("cdombeh")

    def _missingness_cdomaprax(self) -> Optional[int]:
        """Handles missingness for CDOMAPRAX."""
        return self.__handle_cognitive_status_gate("cdomaprax")

    #########################################
    # NORMCOG and PREDOMSYN-gated variables #
    #########################################

    def __handle_predomsyn_anxiet_gate(self, gate: str, field: str) -> Optional[int]:
        """Handles variables dependent on NORMCOG and GATE (PREDOMSYN or
        ANXIET):

        If NORMCOG=0 and GATE=1 and FIELD is blank, then FIELD should =0
        If NORMCOG=0 and GATE=0 and FIELD is blank, then FIELD should =7
        Else if NORMCOG=1 and FIELD is blank, then FIELD should =8
        """
        assert gate in ["predomsyn", "anxiet"]
        if self.normcog == 0 and self.uds.get_value(field, int) is None:
            gate_value = self.uds.get_value(gate, int)
            if gate_value == 1:
                return 0
            if gate_value == 0:
                return 7

        return self.__handle_normcog_gate(field)

    def _missingness_amndem(self) -> Optional[int]:
        """Handles missingness for AMNDEM."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_predomsyn_anxiet_gate("predomsyn", "amndem")

    def _missingness_pca(self) -> Optional[int]:
        """Handles missingness for PCA."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_predomsyn_anxiet_gate("predomsyn", "pca")

    def _missingness_namndem(self) -> Optional[int]:
        """Handles missingness for NAMNDEM."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_predomsyn_anxiet_gate("predomsyn", "namndem")

    def _missingness_dyexecsyn(self) -> Optional[int]:
        """Handles missingness for DYEXECSYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "dyexecsyn")

    def _missingness_pspsyn(self) -> Optional[int]:
        """Handles missingness for PSPSYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "pspsyn")

    def _missingness_ctesyn(self) -> Optional[int]:
        """Handles missingness for CTESYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "ctesyn")

    def _missingness_cbssyn(self) -> Optional[int]:
        """Handles missingness for CBSSYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "cbssyn")

    def _missingness_msasyn(self) -> Optional[int]:
        """Handles missingness for MSASYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "msasyn")

    def _missingness_othsyn(self) -> Optional[int]:
        """Handles missingness for OTHSYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "othsyn")

    def _missingness_syninfclin(self) -> Optional[int]:
        """Handles missingness for SYNINFCLIN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "syninfclin")

    def _missingness_syninfctst(self) -> Optional[int]:
        """Handles missingness for SYNINFCTST."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "syninfctst")

    def _missingness_syninfbiom(self) -> Optional[int]:
        """Handles missingness for SYNINFBIOM."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "syninfbiom")

    def _missingness_genanx(self) -> Optional[int]:
        """Handles missingness for GENANX."""
        return self.__handle_predomsyn_anxiet_gate("anxiet", "genanx")

    def _missingness_panicdisdx(self) -> Optional[int]:
        """Handles missingness for PANICDISDX."""
        return self.__handle_predomsyn_anxiet_gate("anxiet", "panicdisdx")

    def _missingness_ocddx(self) -> Optional[int]:
        """Handles missingness for OCDDX."""
        return self.__handle_predomsyn_anxiet_gate("anxiet", "ocddx")

    def _missingness_othanxd(self) -> Optional[int]:
        """Handles missingness for OTHANXD."""
        return self.__handle_predomsyn_anxiet_gate("anxiet", "othanxd")

    #########################################
    # NORMCOG and GATE-gated variables #
    #########################################

    def __handle_normcog_with_additional_gate(
        self, gate: str, field: str
    ) -> Optional[int]:
        """Handles variables dependent on NORMCOG and another gate:

        If NORMCOG = 0 and GATE is 0 or blank and FIELD is blank, FIELD = 7
        Else if NORMCOG = 1 and FIELD is blank, FIELD = 8
        """
        gate_value = self.uds.get_value(gate, int)
        value = self.uds.get_value(field, int)

        if (
            self.normcog == 0
            and (gate_value is None or gate_value == 0)
            and value is None
        ):
            return 7

        return self.__handle_normcog_gate(field)

    def _missingness_lbdsynt(self) -> Optional[int]:
        """Handles missingness for LBDSYNT."""
        return self.__handle_normcog_with_additional_gate("lbdsyn", "lbdsynt")

    def _missingness_pspsynt(self) -> Optional[int]:
        """Handles missingness for PSPSYNT."""
        return self.__handle_normcog_with_additional_gate("pspsyn", "pspsynt")

    def _missingness_msasynt(self) -> Optional[int]:
        """Handles missingness for MSASYNT."""
        return self.__handle_normcog_with_additional_gate("msasyn", "msasynt")

    def _missingness_majdepdif(self) -> Optional[int]:
        """Handles missingness for MAJDEPDIF."""
        return self.__handle_normcog_with_additional_gate("majdepdx", "majdepdif")

    def _missingness_othdepdif(self) -> Optional[int]:
        """Handles missingness for OTHDEPDIF."""
        return self.__handle_normcog_with_additional_gate("othdepdx", "othdepdif")

    def _missingness_ndevdisif(self) -> Optional[int]:
        """Handles missingness for NDEVDISIF."""
        return self.__handle_normcog_with_additional_gate("ndevdis", "ndevdisif")

    def _missingness_tbidxif(self) -> Optional[int]:
        """Handles missingness for TBIDXIF."""
        return self.__handle_normcog_with_additional_gate("tbidx", "tbidxif")

    def _missingness_postc19if(self) -> Optional[int]:
        """Handles missingness for POSTC19IF."""
        return self.__handle_normcog_with_additional_gate("postc19", "postc19if")

    def _missingness_apneadxif(self) -> Optional[int]:
        """Handles missingness for APNEADXIF."""
        return self.__handle_normcog_with_additional_gate("apneadx", "apneadxif")

    def _missingness_othcillif(self) -> Optional[int]:
        """Handles missingness for OTHCILLIF."""
        return self.__handle_normcog_with_additional_gate("othcogill", "othcillif")

    def _missingness_hycephif(self) -> Optional[int]:
        """Handles missingness for HYCEPHIF."""
        return self.__handle_normcog_with_additional_gate("hyceph", "hycephif")

    def _missingness_epilepif(self) -> Optional[int]:
        """Handles missingness for EPILEPIF."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_with_additional_gate("epilep", "epilepif")

    def _missingness_neopif(self) -> Optional[int]:
        """Handles missingness for NEOPIF."""
        return self.__handle_normcog_with_additional_gate("neop", "neopif")

    def _missingness_hivif(self) -> Optional[int]:
        """Handles missingness for HIVIF."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_with_additional_gate("hiv", "hivif")

    def _missingness_bipoldif(self) -> Optional[int]:
        """Handles missingness for BIPOLDIF."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_with_additional_gate("bipoldx", "bipoldif")

    def _missingness_schizoif(self) -> Optional[int]:
        """Handles missingness for SCHIZOIF."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_with_additional_gate("schizop", "schizoif")

    def _missingness_anxietif(self) -> Optional[int]:
        """Handles missingness for ANXIETIF."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_with_additional_gate("anxiet", "anxietif")

    def _missingness_delirif(self) -> Optional[int]:
        """Handles missingness for DELIRIF."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_with_additional_gate("delir", "delirif")

    def _missingness_ptsddxif(self) -> Optional[int]:
        """Handles missingness for PTSDDXIF."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_with_additional_gate("ptsddx", "ptsddxif")

    def _missingness_othpsyif(self) -> Optional[int]:
        """Handles missingness for OTHPSYIF."""
        return self.__handle_normcog_with_additional_gate("othpsy", "othpsyif")

    def _missingness_alcdemif(self) -> Optional[int]:
        """Handles missingness for ALCDEMIF."""
        return self.__handle_normcog_with_additional_gate("alcdem", "alcdemif")

    def _missingness_impsubif(self) -> Optional[int]:
        """Handles missingness for IMPSUBIF."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_normcog_with_additional_gate("impsub", "impsubif")

    def _missingness_medsif(self) -> Optional[int]:
        """Handles missingness for MEDSIF."""
        return self.__handle_normcog_with_additional_gate("meds", "medsif")

    def _missingness_cogothif(self) -> Optional[int]:
        """Handles missingness for COGOTHIF."""
        return self.__handle_normcog_with_additional_gate("cogoth", "cogothif")

    def _missingness_cogoth2f(self) -> Optional[int]:
        """Handles missingness for COGOTH2F."""
        return self.__handle_normcog_with_additional_gate("cogoth2", "cogoth2f")

    def _missingness_cogoth3f(self) -> Optional[int]:
        """Handles missingness for COGOTH3F."""
        return self.__handle_normcog_with_additional_gate("cogoth3", "cogoth3f")

    #######################
    # CVD-gated variables #
    #######################

    def __handle_cvd_gate(
        self, field: str, return_value: int, evaluate_prevstk: bool = False
    ) -> Optional[int]:
        """Handles variables gated by CVD."""
        if self.formver < 3:
            return INFORMED_MISSINGNESS

        cvd = self.uds.get_value("cvd", int)
        if cvd == 0:
            return return_value
        if evaluate_prevstk and cvd == 1:
            prevstk = self.uds.get_value("prevstk", int)
            if prevstk == 0:
                return return_value

        return self.generic_missingness(field)

    def _missingness_prevstk(self) -> Optional[int]:
        """Handles missingness for PREVSTK."""
        return self.__handle_cvd_gate("prevstk", 0)

    def _missingness_infwmh(self) -> Optional[int]:
        """Handles missingness for INFWMH."""
        return self.__handle_cvd_gate("infwmh", 9)

    def _missingness_infnetw(self) -> Optional[int]:
        """Handles missingness for INFNETW."""
        return self.__handle_cvd_gate("infnetw", 9)

    def _missingness_strokdec(self) -> Optional[int]:
        """Handles missingness for STROKDEC."""
        return self.__handle_cvd_gate("strokdec", 8, evaluate_prevstk=True)

    def _missingness_stkimag(self) -> Optional[int]:
        """Handles missingness for STKIMAG."""
        return self.__handle_cvd_gate("stkimag", 8, evaluate_prevstk=True)

    ###################
    # Other variables #
    ###################

    def _missingness_scddxconf(self) -> Optional[int]:
        """Handles missingness for SCDDXCONF."""
        if self.uds.get_value("scddxconf", int) is None:
            scd = self.uds.get_value("scd", int)
            if self.normcog == 1 and scd == 0:
                return 8

            return INFORMED_MISSINGNESS

        return None

    def _missingness_mbi(self) -> Optional[int]:
        """Handles missingness for MBI."""
        if self.uds.get_value("mbi", int) is None:
            if self.normcog == 1 or self.demented == 1:
                return 8

            return INFORMED_MISSINGNESS

        return None

    def _missingness_neopstat(self) -> Optional[int]:
        """Handles missingness for NEOPSTAT."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        neop = self.uds.get_value("neop", int)
        if self.uds.get_value("neopstat", int) is None:
            if neop is None or neop == 0:
                return 8

            return INFORMED_MISSINGNESS

        return None

    def _missingness_demented(self) -> Optional[int]:
        """Handles missingness for DEMENTED."""
        if self.uds.get_value("normcog", int) == 1:
            return 0

        return self.generic_missingness("demented")

    def _missingness_alcabuse(self) -> Optional[int]:
        """Handles missingness for ALCABUSE."""
        if self.uds.get_value("alcdem", int) == 0:
            return 8

        return self.generic_missingness("alcabuse")

    def _missingness_deptreat(self) -> Optional[int]:
        """Handles missingness for DEPTREAT."""
        if self.uds.get_value("dep", int) == 0:
            return 8

        return self.generic_missingness("deptreat")

    def _missingness_brnincte(self) -> Optional[int]:
        if self.uds.get_value("brninj", int) == 0:
            return 8

        return self.generic_missingness("brnincte")

    ######################
    # Write-in variables #
    ######################

    def _missingness_impnomciox(self) -> Optional[str]:
        """Handles missingness for IMPNOMCIOX."""
        return self.generic_writein("impnomciox")

    def _missingness_othsynx(self) -> Optional[str]:
        """Handles missingness for OTHSYNX."""
        return self.generic_writein("othsynx")

    def _missingness_othanxdx(self) -> Optional[str]:
        """Handles missingness for OTHANXDX."""
        return self.generic_writein("othanxdx")

    def _missingness_othcogillx(self) -> Optional[str]:
        """Handles missingness for OTHCOGILLX."""
        return self.generic_writein("othcogillx")

    def _missingness_othpsyx(self) -> Optional[str]:
        """Handles missingness for OTHPSYX."""
        return self.generic_writein("othpsyx")

    def _missingness_cogothx(self) -> Optional[str]:
        """Handles missingness for COGOTHX."""
        return self.generic_writein("cogothx")

    def _missingness_cogoth2x(self) -> Optional[str]:
        """Handles missingness for COGOTH2X."""
        return self.generic_writein("cogoth2x")

    def _missingness_cogoth3x(self) -> Optional[str]:
        """Handles missingness for COGOTH3X."""
        return self.generic_writein("cogoth3x")
