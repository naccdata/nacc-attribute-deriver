"""Class to handle D1a-specific missingness values."""

from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

from .helpers.d1_base import UDSFormD1Missingness
from .helpers.d1a_cogothx_helper import D1aCOGOTHXHelper


class UDSFormD1aMissingness(UDSFormD1Missingness):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table)

        # may need to be reordered, so pre-compute
        self.__cogothx_attributes = D1aCOGOTHXHelper(table)

    ###########################
    # NORMCOG-gated variables #
    ###########################

    def _missingness_scd(self) -> int:
        """Handles missingness for SCD."""
        scd = self.uds.get_value("scd", int)
        if scd is None and self.normcog == 0:
            return 8

        return self.generic_missingness("scd", int)

    def _missingness_predomsyn(self) -> int:
        """Handles missingness for PREDOMSYN."""
        predomsyn = self.uds.get_value("predomsyn", int)
        if predomsyn is None and self.normcog == 0:
            return 8

        return self.generic_missingness("predomsyn", int)

    def _missingness_majdepdx(self) -> int:
        """Handles missingness for MAJDEPDX."""
        return self.handle_normcog_gate("majdepdx")

    def _missingness_othdepdx(self) -> int:
        """Handles missingness for OTHDEPDX."""
        return self.handle_normcog_gate("othdepdx")

    def _missingness_ndevdis(self) -> int:
        """Handles missingness for NDEVDIS."""
        return self.handle_normcog_gate("ndevdis")

    def _missingness_tbidx(self) -> int:
        """Handles missingness for TBIDX."""
        return self.handle_normcog_gate("tbidx")

    def _missingness_postc19(self) -> int:
        """Handles missingness for POSTC19."""
        return self.handle_normcog_gate("postc19")

    def _missingness_apneadx(self) -> int:
        """Handles missingness for APNEADX."""
        return self.handle_normcog_gate("apneadx")

    def _missingness_othcogill(self) -> int:
        """Handles missingness for OTHCOGILL."""
        return self.handle_normcog_gate("othcogill")

    def _missingness_hyceph(self) -> int:
        """Handles missingness for HYCEPH."""
        return self.handle_normcog_gate("hyceph")

    def _missingness_epilep(self) -> int:
        """Handles missingness for EPILEP."""
        return self.handle_normcog_gate("epilep")

    def _missingness_neop(self) -> int:
        """Handles missingness for NEOP."""
        return self.handle_normcog_gate("neop")

    def _missingness_hiv(self) -> int:
        """Handles missingness for HIV."""
        return self.handle_normcog_gate("hiv")

    def _missingness_bipoldx(self) -> int:
        """Handles missingness for BIPOLDX."""
        return self.handle_normcog_gate("bipoldx")

    def _missingness_schizop(self) -> int:
        """Handles missingness for SCHIZOP."""
        return self.handle_normcog_gate("schizop")

    def _missingness_anxiet(self) -> int:
        """Handles missingness for ANXIET."""
        return self.handle_normcog_gate("anxiet")

    def _missingness_delir(self) -> int:
        """Handles missingness for DELIR."""
        return self.handle_normcog_gate("delir")

    def _missingness_ptsddx(self) -> int:
        """Handles missingness for PTSDDX."""
        return self.handle_normcog_gate("ptsddx")

    def _missingness_othpsy(self) -> int:
        """Handles missingness for OTHPSY."""
        return self.handle_normcog_gate("othpsy")

    def _missingness_alcdem(self) -> int:
        """Handles missingness for ALCDEM."""
        return self.handle_normcog_gate("alcdem")

    def _missingness_impsub(self) -> int:
        """Handles missingness for IMPSUB."""
        return self.handle_normcog_gate("impsub")

    def _missingness_meds(self) -> int:
        """Handles missingness for MEDS."""
        return self.handle_normcog_gate("meds")

    def _missingness_cogoth(self) -> int:
        """Handles missingness for COGOTH."""
        return self.__cogothx_attributes.get("cogoth", int)

    def _missingness_cogoth2(self) -> int:
        """Handles missingness for COGOTH2."""
        return self.__cogothx_attributes.get("cogoth2", int)

    def _missingness_cogoth3(self) -> int:
        """Handles missingness for COGOTH3."""
        return self.__cogothx_attributes.get("cogoth3", int)

    ########################################
    # NORMCOG and DEMENTED-gated variables #
    ########################################

    def __handle_normcog_demented_gate(self, field: str) -> int:
        """Handles NORMCOG and DEMENTED-gated variables, which follow:

        If NORMCOG = 0 and DEMENTED = 0 and FIELD is blank, then FIELD = 0
        """
        value = self.uds.get_value(field, int)
        if value is None:
            if self.normcog == 0 and self.demented == 0:
                return 0

            return INFORMED_MISSINGNESS

        return value

    def _missingness_mcicritcln(self) -> int:
        """Handles missingness for MCICRITCLN."""
        return self.__handle_normcog_demented_gate("mcicritcln")

    def _missingness_mcicritimp(self) -> int:
        """Handles missingness for MCICRITIMP."""
        return self.__handle_normcog_demented_gate("mcicritimp")

    def _missingness_mcicritfun(self) -> int:
        """Handles missingness for MCICRITFUN."""
        return self.__handle_normcog_demented_gate("mcicritfun")

    ##############################################
    # NORMCOG, DEMENTED, and MCI-gated variables #
    ##############################################

    def __handle_normcog_demented_mci_gate(self, field: str) -> int:
        """Handles NORMCOG DEMENTED, and MCI-gated variables, which follow:

        If NORMCOG = 0 and DEMENTED = 0 and MCI = 0 and FIELD is blank,
        then FIELD = 0
        """
        value = self.uds.get_value(field, int)
        if value is None:
            if self.normcog == 0 and self.demented == 0 and self.mci == 0:
                return 0

            return INFORMED_MISSINGNESS

        return value

    def _missingness_impnomcifu(self) -> int:
        """Handles missingness for IMPNOMCIFU."""
        return self.__handle_normcog_demented_mci_gate("impnomcifu")

    def _missingness_impnomcicg(self) -> int:
        """Handles missingness for IMPNOMCICG."""
        return self.__handle_normcog_demented_mci_gate("impnomcicg")

    def _missingness_impnomclcd(self) -> int:
        """Handles missingness for IMPNOMCLCD."""
        return self.__handle_normcog_demented_mci_gate("impnomclcd")

    def _missingness_impnomcio(self) -> int:
        """Handles missingness for IMPNOMCIO."""
        return self.__handle_normcog_demented_mci_gate("impnomcio")

    ####################################
    # Cognitive status-gated variables #
    ####################################

    def __handle_cognitive_status_gate(self, field: str) -> int:
        """Handles variables dependent on cognitive status:

        If (MCI = 1 or DEMENTED = 1) and FIELD is blank, then FIELD = 0
        If (NORMCOG = 1 or IMPNOMCI = 1) and FIELD is blank, then FIELD = 8
        """
        value = self.uds.get_value(field, int)
        if value is None:
            if self.mci == 1 or self.demented == 1:
                return 0
            if self.normcog == 1 or self.impnomci == 1:
                return 8

            return INFORMED_MISSINGNESS

        return value

    def _missingness_cdommem(self) -> int:
        """Handles missingness for CDOMMEM."""
        return self.__handle_cognitive_status_gate("cdommem")

    def _missingness_cdomlang(self) -> int:
        """Handles missingness for CDOMLANG."""
        return self.__handle_cognitive_status_gate("cdomlang")

    def _missingness_cdomattn(self) -> int:
        """Handles missingness for CDOMATTN."""
        return self.__handle_cognitive_status_gate("cdomattn")

    def _missingness_cdomexec(self) -> int:
        """Handles missingness for CDOMEXEC."""
        return self.__handle_cognitive_status_gate("cdomexec")

    def _missingness_cdomvisu(self) -> int:
        """Handles missingness for CDOMVISU."""
        return self.__handle_cognitive_status_gate("cdomvisu")

    def _missingness_cdombeh(self) -> int:
        """Handles missingness for CDOMBEH."""
        return self.__handle_cognitive_status_gate("cdombeh")

    def _missingness_cdomaprax(self) -> int:
        """Handles missingness for CDOMAPRAX."""
        return self.__handle_cognitive_status_gate("cdomaprax")

    #########################################
    # NORMCOG and PREDOMSYN-gated variables #
    #########################################

    def __handle_predomsyn_anxiet_gate(self, gate: str, field: str) -> int:
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

        return self.handle_normcog_gate(field)

    def _missingness_amndem(self) -> int:
        """Handles missingness for AMNDEM."""
        amndem = self.uds.get_value("amndem", int)
        if self.formver < 4 and self.demented == 0 and amndem is None:
            return 8

        return self.__handle_predomsyn_anxiet_gate("predomsyn", "amndem")

    def _missingness_pca(self) -> int:
        """Handles missingness for PCA."""
        pca = self.uds.get_value("pca", int)
        if self.formver < 4 and self.demented == 0 and pca is None:
            return 8

        return self.__handle_predomsyn_anxiet_gate("predomsyn", "pca")

    def _missingness_namndem(self) -> int:
        """Handles missingness for NAMNDEM."""
        if self.formver == 3 and (self.demented == 0 or self.normcog == 1):
            namndem = self.uds.get_value("namndem", int)
            if namndem is None or namndem == 0:
                return 8

        return self.__handle_predomsyn_anxiet_gate("predomsyn", "namndem")

    def _missingness_dyexecsyn(self) -> int:
        """Handles missingness for DYEXECSYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "dyexecsyn")

    def _missingness_pspsyn(self) -> int:
        """Handles missingness for PSPSYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "pspsyn")

    def _missingness_ctesyn(self) -> int:
        """Handles missingness for CTESYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "ctesyn")

    def _missingness_cbssyn(self) -> int:
        """Handles missingness for CBSSYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "cbssyn")

    def _missingness_msasyn(self) -> int:
        """Handles missingness for MSASYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "msasyn")

    def _missingness_othsyn(self) -> int:
        """Handles missingness for OTHSYN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "othsyn")

    def _missingness_syninfclin(self) -> int:
        """Handles missingness for SYNINFCLIN."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "syninfclin")

    def _missingness_syninfctst(self) -> int:
        """Handles missingness for SYNINFCTST."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "syninfctst")

    def _missingness_syninfbiom(self) -> int:
        """Handles missingness for SYNINFBIOM."""
        return self.__handle_predomsyn_anxiet_gate("predomsyn", "syninfbiom")

    def _missingness_genanx(self) -> int:
        """Handles missingness for GENANX."""
        return self.__handle_predomsyn_anxiet_gate("anxiet", "genanx")

    def _missingness_panicdisdx(self) -> int:
        """Handles missingness for PANICDISDX."""
        return self.__handle_predomsyn_anxiet_gate("anxiet", "panicdisdx")

    def _missingness_ocddx(self) -> int:
        """Handles missingness for OCDDX."""
        return self.__handle_predomsyn_anxiet_gate("anxiet", "ocddx")

    def _missingness_othanxd(self) -> int:
        """Handles missingness for OTHANXD."""
        return self.__handle_predomsyn_anxiet_gate("anxiet", "othanxd")

    #########################################
    # NORMCOG and GATE-gated variables #
    #########################################

    def _missingness_lbdsynt(self) -> int:
        """Handles missingness for LBDSYNT."""
        return self.handle_cognitive_impairment_gate("lbdsyn", "lbdsynt")

    def _missingness_pspsynt(self) -> int:
        """Handles missingness for PSPSYNT."""
        return self.handle_cognitive_impairment_gate("pspsyn", "pspsynt")

    def _missingness_msasynt(self) -> int:
        """Handles missingness for MSASYNT."""
        return self.handle_cognitive_impairment_gate("msasyn", "msasynt")

    def _missingness_majdepdif(self) -> int:
        """Handles missingness for MAJDEPDIF."""
        return self.handle_cognitive_impairment_gate("majdepdx", "majdepdif")

    def _missingness_othdepdif(self) -> int:
        """Handles missingness for OTHDEPDIF."""
        return self.handle_cognitive_impairment_gate("othdepdx", "othdepdif")

    def _missingness_ndevdisif(self) -> int:
        """Handles missingness for NDEVDISIF."""
        return self.handle_cognitive_impairment_gate("ndevdis", "ndevdisif")

    def _missingness_tbidxif(self) -> int:
        """Handles missingness for TBIDXIF."""
        return self.handle_cognitive_impairment_gate("tbidx", "tbidxif")

    def _missingness_postc19if(self) -> int:
        """Handles missingness for POSTC19IF."""
        return self.handle_cognitive_impairment_gate("postc19", "postc19if")

    def _missingness_apneadxif(self) -> int:
        """Handles missingness for APNEADXIF."""
        return self.handle_cognitive_impairment_gate("apneadx", "apneadxif")

    def _missingness_othcillif(self) -> int:
        """Handles missingness for OTHCILLIF."""
        return self.handle_cognitive_impairment_gate("othcogill", "othcillif")

    def _missingness_hycephif(self) -> int:
        """Handles missingness for HYCEPHIF."""
        return self.handle_cognitive_impairment_gate("hyceph", "hycephif")

    def _missingness_epilepif(self) -> int:
        """Handles missingness for EPILEPIF."""
        return self.handle_cognitive_impairment_gate("epilep", "epilepif")

    def _missingness_neopif(self) -> int:
        """Handles missingness for NEOPIF."""
        return self.handle_cognitive_impairment_gate("neop", "neopif")

    def _missingness_hivif(self) -> int:
        """Handles missingness for HIVIF."""
        return self.handle_cognitive_impairment_gate("hiv", "hivif")

    def _missingness_bipoldif(self) -> int:
        """Handles missingness for BIPOLDIF."""
        return self.handle_cognitive_impairment_gate("bipoldx", "bipoldif")

    def _missingness_schizoif(self) -> int:
        """Handles missingness for SCHIZOIF."""
        return self.handle_cognitive_impairment_gate("schizop", "schizoif")

    def _missingness_anxietif(self) -> int:
        """Handles missingness for ANXIETIF."""
        return self.handle_cognitive_impairment_gate("anxiet", "anxietif")

    def _missingness_delirif(self) -> int:
        """Handles missingness for DELIRIF."""
        return self.handle_cognitive_impairment_gate("delir", "delirif")

    def _missingness_ptsddxif(self) -> int:
        """Handles missingness for PTSDDXIF."""
        return self.handle_cognitive_impairment_gate("ptsddx", "ptsddxif")

    def _missingness_othpsyif(self) -> int:
        """Handles missingness for OTHPSYIF."""
        return self.handle_cognitive_impairment_gate("othpsy", "othpsyif")

    def _missingness_alcdemif(self) -> int:
        """Handles missingness for ALCDEMIF."""
        return self.handle_cognitive_impairment_gate("alcdem", "alcdemif")

    def _missingness_impsubif(self) -> int:
        """Handles missingness for IMPSUBIF."""
        return self.handle_cognitive_impairment_gate("impsub", "impsubif")

    def _missingness_medsif(self) -> int:
        """Handles missingness for MEDSIF."""
        return self.handle_cognitive_impairment_gate("meds", "medsif")

    def _missingness_cogothif(self) -> int:
        """Handles missingness for COGOTHIF."""
        return self.__cogothx_attributes.get("cogothif", int)

    def _missingness_cogoth2f(self) -> int:
        """Handles missingness for COGOTH2F."""
        return self.__cogothx_attributes.get("cogoth2f", int)

    def _missingness_cogoth3f(self) -> int:
        """Handles missingness for COGOTH3F."""
        return self.__cogothx_attributes.get("cogoth3f", int)

    ###################
    # Other variables #
    ###################

    def _missingness_scddxconf(self) -> int:
        """Handles missingness for SCDDXCONF."""
        result = self.generic_missingness("scddxconf", int)
        if result == INFORMED_MISSINGNESS:
            scd = self.uds.get_value("scd", int)
            if self.normcog == 0 and scd == 0:
                return 8

        return result

    def _missingness_mbi(self) -> int:
        """Handles missingness for MBI."""
        result = self.generic_missingness("mbi", int)
        if result == INFORMED_MISSINGNESS:
            if self.normcog == 1 or self.demented == 1:
                return 8

        return result

    def _missingness_neopstat(self) -> int:
        """Handles missingness for NEOPSTAT."""
        result = self.generic_missingness("neopstat", int)
        if result == INFORMED_MISSINGNESS:
            neop = self.uds.get_value("neop", int)
            if neop is None or neop == 0:
                return 8

        return result

    def _missingness_demented(self) -> int:
        """Handles missingness for DEMENTED."""
        if self.uds.get_value("normcog", int) == 1:
            return 0

        return self.generic_missingness("demented", int)

    def _missingness_impnomci(self) -> int:
        """Handles missingness for IMPNOMCI."""
        if self.impnomci is None or self.impnomci == 0:
            return 0

        return self.impnomci

    def _missingness_cogothx(self) -> str:
        """Handles missingness for COGOTHX."""
        return self.__cogothx_attributes.get("cogothx", str)

    def _missingness_cogoth2x(self) -> str:
        """Handles missingness for COGOTH2X."""
        return self.__cogothx_attributes.get("cogoth2x", str)

    def _missingness_cogoth3x(self) -> str:
        """Handles missingness for COGOTH3X."""
        return self.__cogothx_attributes.get("cogoth3x", str)
