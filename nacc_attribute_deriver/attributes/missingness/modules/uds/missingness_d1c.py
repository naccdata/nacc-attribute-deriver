"""Class to handle D1c-specific missingness values.

D1c is optional (MODED1C = 0 means not completed). As with B6, the
informative missingness codes only apply when the form was completed;
otherwise all variables fall back to generic missingness (-4).

Write-in variables (DXOTHPLSMX, DXOTHCSFX, IMGRSOTHX, ASYNASSAYX,
ASYNANLYSX, CR1OTHX) stay blank, which generic missingness already does.
"""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness


class UDSFormD1cMissingness(UDSMissingness):
    @property
    def submitted(self) -> bool:
        """Check if the form was completed."""
        return self.uds.get_value("moded1c", int) == 1

    def _missingness_langd1c(self) -> int:
        """Handle missingness for LANGD1C."""
        return self.handle_optional_header_variables("lang", "d1c", [1, 2])

    def __handle_checkbox(self, gate: str, field: str) -> int:
        """Handles "select all that apply" checkboxes under a yes/no gate:

        If GATE = 0 and FIELD is blank, then FIELD = 8
        If GATE = 1 and FIELD is blank, then FIELD = 0
        """
        if self.submitted and self.uds.get_value(field, int) is None:
            gate_value = self.uds.get_value(gate, int)
            if gate_value == 0:
                return 8
            if gate_value == 1:
                return 0

        return self.generic_missingness(field, int)

    def __handle_unchecked_box(self, checkbox: str, field: str) -> int:
        """Handles the follow-up questions to a checkbox:

        If CHECKBOX is blank and FIELD is blank, then FIELD = 8
        """
        if (
            self.submitted
            and self.uds.get_value(checkbox, int) is None
            and self.uds.get_value(field, int) is None
        ):
            return 8

        return self.generic_missingness(field, int)

    def __handle_gate_no(self, gate: str, field: str) -> int:
        """Handles questions skipped by a yes/no gate:

        If GATE = 0 and FIELD is blank, then FIELD = 8
        """
        if (
            self.submitted
            and self.uds.get_value(gate, int) == 0
            and self.uds.get_value(field, int) is None
        ):
            return 8

        return self.generic_missingness(field, int)

    def __handle_imgrsinf_box(self, field: str) -> int:
        """Handles the Lacunar/Cortical boxes under IMGRSINF (Infarction on
        MRI):

        If INFORISCH = 0 and FIELD is blank, then FIELD = 8
        If INFORISCH = 1 and IMGRSINF is blank, then FIELD = 8
        If IMGRSINF = 1 and FIELD is blank, then FIELD = 0
        """
        if self.submitted and self.uds.get_value(field, int) is None:
            inforisch = self.uds.get_value("inforisch", int)
            imgrsinf = self.uds.get_value("imgrsinf", int)
            if inforisch == 0:
                return 8
            if imgrsinf == 1:
                return 0
            if inforisch == 1 and imgrsinf is None:
                return 8

        return self.generic_missingness(field, int)

    #########################################
    # Checkboxes gated by a yes/no question #
    #########################################

    def _missingness_dxptau217(self) -> int:
        """Handles missingness for DXPTAU217."""
        return self.__handle_checkbox("dxplsmabio", "dxptau217")

    def _missingness_dxpcpt217(self) -> int:
        """Handles missingness for DXPCPT217."""
        return self.__handle_checkbox("dxplsmabio", "dxpcpt217")

    def _missingness_dxothplsma(self) -> int:
        """Handles missingness for DXOTHPLSMA."""
        return self.__handle_checkbox("dxplsmabio", "dxothplsma")

    def _missingness_dxpt181ab(self) -> int:
        """Handles missingness for DXPT181AB."""
        return self.__handle_checkbox("dxcsfbio", "dxpt181ab")

    def _missingness_dxttabeta(self) -> int:
        """Handles missingness for DXTTABETA."""
        return self.__handle_checkbox("dxcsfbio", "dxttabeta")

    def _missingness_dxab42ab40(self) -> int:
        """Handles missingness for DXAB42AB40."""
        return self.__handle_checkbox("dxcsfbio", "dxab42ab40")

    def _missingness_dxothcsf(self) -> int:
        """Handles missingness for DXOTHCSF."""
        return self.__handle_checkbox("dxcsfbio", "dxothcsf")

    def _missingness_apetvis(self) -> int:
        """Handles missingness for APETVIS."""
        return self.__handle_checkbox("dxapet", "apetvis")

    def _missingness_apetquant(self) -> int:
        """Handles missingness for APETQUANT."""
        return self.__handle_checkbox("dxapet", "apetquant")

    def _missingness_tpetmtlvis(self) -> int:
        """Handles missingness for TPETMTLVIS."""
        return self.__handle_checkbox("dxtaupet", "tpetmtlvis")

    def _missingness_tpetmtlqnt(self) -> int:
        """Handles missingness for TPETMTLQNT."""
        return self.__handle_checkbox("dxtaupet", "tpetmtlqnt")

    def _missingness_tpetneovis(self) -> int:
        """Handles missingness for TPETNEOVIS."""
        return self.__handle_checkbox("dxtaupet", "tpetneovis")

    def _missingness_tpetneoqnt(self) -> int:
        """Handles missingness for TPETNEOQNT."""
        return self.__handle_checkbox("dxtaupet", "tpetneoqnt")

    def _missingness_imgrsinf(self) -> int:
        """Handles missingness for IMGRSINF."""
        return self.__handle_checkbox("inforisch", "imgrsinf")

    def _missingness_imgrsmicr(self) -> int:
        """Handles missingness for IMGRSMICR."""
        return self.__handle_checkbox("inforisch", "imgrsmicr")

    def _missingness_imgrswmh(self) -> int:
        """Handles missingness for IMGRSWMH."""
        return self.__handle_checkbox("inforisch", "imgrswmh")

    def _missingness_imgrsspsid(self) -> int:
        """Handles missingness for IMGRSSPSID."""
        return self.__handle_checkbox("inforisch", "imgrsspsid")

    def _missingness_imgrsoth(self) -> int:
        """Handles missingness for IMGRSOTH."""
        return self.__handle_checkbox("inforisch", "imgrsoth")

    def _missingness_cr1apet(self) -> int:
        """Handles missingness for CR1APET."""
        return self.__handle_checkbox("aacritmet", "cr1apet")

    def _missingness_cr1ptau217(self) -> int:
        """Handles missingness for CR1PTAU217."""
        return self.__handle_checkbox("aacritmet", "cr1ptau217")

    def _missingness_cr1pcpt217(self) -> int:
        """Handles missingness for CR1PCPT217."""
        return self.__handle_checkbox("aacritmet", "cr1pcpt217")

    def _missingness_cr1pt181ab(self) -> int:
        """Handles missingness for CR1PT181AB."""
        return self.__handle_checkbox("aacritmet", "cr1pt181ab")

    def _missingness_cr1ttabeta(self) -> int:
        """Handles missingness for CR1TTABETA."""
        return self.__handle_checkbox("aacritmet", "cr1ttabeta")

    def _missingness_c1ab42ab40(self) -> int:
        """Handles missingness for C1AB42AB40."""
        return self.__handle_checkbox("aacritmet", "c1ab42ab40")

    def _missingness_cr1oth(self) -> int:
        """Handles missingness for CR1OTH."""
        return self.__handle_checkbox("aacritmet", "cr1oth")

    #####################################
    # Follow-up questions to a checkbox #
    #####################################

    def _missingness_ptau217rs(self) -> int:
        """Handles missingness for PTAU217RS."""
        return self.__handle_unchecked_box("dxptau217", "ptau217rs")

    def _missingness_pt217anlys(self) -> int:
        """Handles missingness for PT217ANLYS."""
        return self.__handle_unchecked_box("dxptau217", "pt217anlys")

    def _missingness_pt217int(self) -> int:
        """Handles missingness for PT217INT."""
        return self.__handle_unchecked_box("dxptau217", "pt217int")

    def _missingness_pcpt217rs(self) -> int:
        """Handles missingness for PCPT217RS."""
        return self.__handle_unchecked_box("dxpcpt217", "pcpt217rs")

    def _missingness_pcpt217int(self) -> int:
        """Handles missingness for PCPT217INT."""
        return self.__handle_unchecked_box("dxpcpt217", "pcpt217int")

    def _missingness_othplsmars(self) -> int:
        """Handles missingness for OTHPLSMARS."""
        return self.__handle_unchecked_box("dxothplsma", "othplsmars")

    def _missingness_oplsmanlys(self) -> int:
        """Handles missingness for OPLSMANLYS."""
        return self.__handle_unchecked_box("dxothplsma", "oplsmanlys")

    def _missingness_oplsmaint(self) -> int:
        """Handles missingness for OPLSMAINT."""
        return self.__handle_unchecked_box("dxothplsma", "oplsmaint")

    def _missingness_pt181abrs(self) -> int:
        """Handles missingness for PT181ABRS."""
        return self.__handle_unchecked_box("dxpt181ab", "pt181abrs")

    def _missingness_pt181abays(self) -> int:
        """Handles missingness for PT181ABAYS."""
        return self.__handle_unchecked_box("dxpt181ab", "pt181abays")

    def _missingness_pt181abint(self) -> int:
        """Handles missingness for PT181ABINT."""
        return self.__handle_unchecked_box("dxpt181ab", "pt181abint")

    def _missingness_ttabetars(self) -> int:
        """Handles missingness for TTABETARS."""
        return self.__handle_unchecked_box("dxttabeta", "ttabetars")

    def _missingness_ttabetaint(self) -> int:
        """Handles missingness for TTABETAINT."""
        return self.__handle_unchecked_box("dxttabeta", "ttabetaint")

    def _missingness_ab42ab40rs(self) -> int:
        """Handles missingness for AB42AB40RS."""
        return self.__handle_unchecked_box("dxab42ab40", "ab42ab40rs")

    def _missingness_ab42ab40ay(self) -> int:
        """Handles missingness for AB42AB40AY."""
        return self.__handle_unchecked_box("dxab42ab40", "ab42ab40ay")

    def _missingness_ab42ab40it(self) -> int:
        """Handles missingness for AB42AB40IT."""
        return self.__handle_unchecked_box("dxab42ab40", "ab42ab40it")

    def _missingness_othcsfrs(self) -> int:
        """Handles missingness for OTHCSFRS."""
        return self.__handle_unchecked_box("dxothcsf", "othcsfrs")

    def _missingness_ocsfanlys(self) -> int:
        """Handles missingness for OCSFANLYS."""
        return self.__handle_unchecked_box("dxothcsf", "ocsfanlys")

    def _missingness_ocsfint(self) -> int:
        """Handles missingness for OCSFINT."""
        return self.__handle_unchecked_box("dxothcsf", "ocsfint")

    ######################################
    # Questions skipped by a yes/no gate #
    ######################################

    def _missingness_apetrs(self) -> int:
        """Handles missingness for APETRS."""
        return self.__handle_gate_no("dxapet", "apetrs")

    def _missingness_apetanlys(self) -> int:
        """Handles missingness for APETANLYS."""
        return self.__handle_gate_no("dxapet", "apetanlys")

    def _missingness_apetint(self) -> int:
        """Handles missingness for APETINT."""
        return self.__handle_gate_no("dxapet", "apetint")

    def _missingness_tpetmtlrs(self) -> int:
        """Handles missingness for TPETMTLRS."""
        return self.__handle_gate_no("dxtaupet", "tpetmtlrs")

    def _missingness_tpetmtlays(self) -> int:
        """Handles missingness for TPETMTLAYS."""
        return self.__handle_gate_no("dxtaupet", "tpetmtlays")

    def _missingness_tpetneors(self) -> int:
        """Handles missingness for TPETNEORS."""
        return self.__handle_gate_no("dxtaupet", "tpetneors")

    def _missingness_tpetneoays(self) -> int:
        """Handles missingness for TPETNEOAYS."""
        return self.__handle_gate_no("dxtaupet", "tpetneoays")

    def _missingness_dxtauptint(self) -> int:
        """Handles missingness for DXTAUPTINT."""
        return self.__handle_gate_no("dxtaupet", "dxtauptint")

    def _missingness_imgrsint(self) -> int:
        """Handles missingness for IMGRSINT."""
        return self.__handle_gate_no("inforisch", "imgrsint")

    def _missingness_asynrs(self) -> int:
        """Handles missingness for ASYNRS."""
        return self.__handle_gate_no("dxasyn", "asynrs")

    def _missingness_asynassay(self) -> int:
        """Handles missingness for ASYNASSAY."""
        return self.__handle_gate_no("dxasyn", "asynassay")

    def _missingness_asynint(self) -> int:
        """Handles missingness for ASYNINT."""
        return self.__handle_gate_no("dxasyn", "asynint")

    def _missingness_biostage(self) -> int:
        """Handles missingness for BIOSTAGE."""
        return self.__handle_gate_no("aacritmet", "biostage")

    def _missingness_clinstage(self) -> int:
        """Handles missingness for CLINSTAGE."""
        return self.__handle_gate_no("aacritmet", "clinstage")

    ##########################################
    # IMGRSINF (Infarction on MRI) sub-boxes #
    ##########################################

    def _missingness_imgrsinflc(self) -> int:
        """Handles missingness for IMGRSINFLC."""
        return self.__handle_imgrsinf_box("imgrsinflc")

    def _missingness_imgrsinfct(self) -> int:
        """Handles missingness for IMGRSINFCT."""
        return self.__handle_imgrsinf_box("imgrsinfct")
