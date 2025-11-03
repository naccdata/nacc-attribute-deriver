"""Class to handle B8-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)

from .missingness_uds import UDSMissingness


class UDSFormB8Missingness(UDSMissingness):
    ###########################
    # NORMNREXAM GATED VALUES #
    ###########################

    def _handle_normnrexam_gate(self, field: str) -> Optional[int]:
        """Handles missingness that relies solely on NORMNREXAM.

        If condition does not pass, return generic missingness.
        """
        if self.uds.get_value("normnrexam", int) == 0:
            return 0

        return self.generic_missingness(field)

    def _missingness_parksign(self) -> Optional[int]:
        """Handle missingness for PARKSIGN."""
        if self.formver < 3:
            return self._handle_normexam_gate("parksign")

        return self._handle_normnrexam_gate("parksign")

    def _missingness_othersign(self) -> Optional[int]:
        """Handle missingness for OTHERSIGN."""
        return self._handle_normnrexam_gate("othersign")

    def _missingness_gaitabn(self) -> Optional[int]:
        """Handle missingness for GAITABN."""
        return self._handle_normnrexam_gate("gaitabn")

    def _missingness_gaitfind(self) -> Optional[int]:
        """Handle missingness for GAITFIND.

        If condition does not pass, return generic missingness.
        """
        normnrexam = self.uds.get_value("normnrexam", int)
        gaitabn = self.uds.get_value("gaitabn", int)

        if normnrexam == 0 or gaitabn == 0:
            return 8

        return self.generic_missingness("gaitfind")

    ############################
    # B8-specific GATED VALUES #
    ############################

    def _handle_b8_missingness(self, gate: str, field: str) -> Optional[int]:
        """Handles B8 missingness that relies on NORMNREXAM and a GATE variable
        (PARKSIGN or OTHERSIGN), which follows:

        For V4:
            If NORMNREXAM=0 or GATE=0 then FIELD should = 0
            If GATE=8 then FIELD should =8
            Else return None (don't change)
        Else:
            -4

        If condition does not pass, return generic missingness.
        """
        normnrexam = self.uds.get_value("normnrexam", int)
        gate_value = self.uds.get_value(gate, int)

        if normnrexam == 0 or gate_value == 0:
            return 0

        if gate_value == 8:
            return 8

        return self.generic_missingness(field)

    def _missingness_slowingfm(self) -> Optional[int]:
        """Handles missingness for SLOWINGFM."""
        return self._handle_b8_missingness(gate="parksign", field="slowingfm")

    def _missingness_tremrest(self) -> Optional[int]:
        """Handles missingness for TREMREST."""
        return self._handle_b8_missingness(gate="parksign", field="tremrest")

    def _missingness_trempost(self) -> Optional[int]:
        """Handles missingness for TREMPOST."""
        return self._handle_b8_missingness(gate="parksign", field="trempost")

    def _missingness_tremkine(self) -> Optional[int]:
        """Handles missingness for TREMKINE."""
        return self._handle_b8_missingness(gate="parksign", field="tremkine")

    def _missingness_rigidarm(self) -> Optional[int]:
        """Handles missingness for RIGIDARM."""
        return self._handle_b8_missingness(gate="parksign", field="rigidarm")

    def _missingness_rigidleg(self) -> Optional[int]:
        """Handles missingness for RIGIDLEG."""
        return self._handle_b8_missingness(gate="parksign", field="rigidleg")

    def _missingness_dystarm(self) -> Optional[int]:
        """Handles missingness for DYSTARM."""
        return self._handle_b8_missingness(gate="parksign", field="dystarm")

    def _missingness_dystleg(self) -> Optional[int]:
        """Handles missingness for DYSTLEG."""
        return self._handle_b8_missingness(gate="parksign", field="dystleg")

    def _missingness_chorea(self) -> Optional[int]:
        """Handles missingness for CHOREA."""
        return self._handle_b8_missingness(gate="parksign", field="chorea")

    def _missingness_ampmotor(self) -> Optional[int]:
        """Handles missingness for AMPMOTOR."""
        return self._handle_b8_missingness(gate="parksign", field="ampmotor")

    def _missingness_axialrig(self) -> Optional[int]:
        """Handles missingness for AXIALRIG."""
        return self._handle_b8_missingness(gate="parksign", field="axialrig")

    def _missingness_postinst(self) -> Optional[int]:
        """Handles missingness for POSTINST."""
        if self.formver < 3:
            return self._handle_normexam_gate("postinst")

        return self._handle_b8_missingness(gate="parksign", field="postinst")

    def _missingness_masking(self) -> Optional[int]:
        """Handles missingness for MASKING."""
        return self._handle_b8_missingness(gate="parksign", field="masking")

    def _missingness_stooped(self) -> Optional[int]:
        """Handles missingness for STOOPED."""
        return self._handle_b8_missingness(gate="parksign", field="stooped")

    def _missingness_limbaprax(self) -> Optional[int]:
        """Handles missingness for LIMBAPRAX."""
        return self._handle_b8_missingness(gate="othersign", field="limbaprax")

    def _missingness_umndist(self) -> Optional[int]:
        """Handles missingness for UMNDIST."""
        return self._handle_b8_missingness(gate="othersign", field="umndist")

    def _missingness_lmndist(self) -> Optional[int]:
        """Handles missingness for LMNDIST."""
        return self._handle_b8_missingness(gate="othersign", field="lmndist")

    def _missingness_vfieldcut(self) -> Optional[int]:
        """Handles missingness for VFIELDCUT."""
        return self._handle_b8_missingness(gate="othersign", field="vfieldcut")

    def _missingness_limbatax(self) -> Optional[int]:
        """Handles missingness for LIMBATAX."""
        return self._handle_b8_missingness(gate="othersign", field="limbatax")

    def _missingness_myoclon(self) -> Optional[int]:
        """Handles missingness for MYOCLON."""
        return self._handle_b8_missingness(gate="othersign", field="myoclon")

    def _missingness_unisomato(self) -> Optional[int]:
        """Handles missingness for UNISOMATO."""
        return self._handle_b8_missingness(gate="othersign", field="unisomato")

    def _missingness_aphasia(self) -> Optional[int]:
        """Handles missingness for APHASIA."""
        return self._handle_b8_missingness(gate="othersign", field="aphasia")

    def _missingness_alienlimb(self) -> Optional[int]:
        """Handles missingness for ALIENLIMB."""
        return self._handle_b8_missingness(gate="othersign", field="alienlimb")

    def _missingness_hspatneg(self) -> Optional[int]:
        """Handles missingness for HSPATNEG."""
        return self._handle_b8_missingness(gate="othersign", field="hspatneg")

    def _missingness_pspoagno(self) -> Optional[int]:
        """Handles missingness for PSPOAGNO."""
        return self._handle_b8_missingness(gate="othersign", field="pspoagno")

    def _missingness_smtagno(self) -> Optional[int]:
        """Handles missingness for SMTAGNO."""
        return self._handle_b8_missingness(gate="othersign", field="smtagno")

    def _missingness_opticatax(self) -> Optional[int]:
        """Handles missingness for OPTICATAX."""
        return self._handle_b8_missingness(gate="othersign", field="opticatax")

    def _missingness_apraxgaze(self) -> Optional[int]:
        """Handles missingness for APRAXGAZE."""
        return self._handle_b8_missingness(gate="othersign", field="apraxgaze")

    def _missingness_vhgazepal(self) -> Optional[int]:
        """Handles missingness for VHGAZEPAL."""
        return self._handle_b8_missingness(gate="othersign", field="vhgazepal")

    def _missingness_dysarth(self) -> Optional[int]:
        """Handles missingness for DYSARTH."""
        return self._handle_b8_missingness(gate="othersign", field="dysarth")

    def _missingness_apraxsp(self) -> Optional[int]:
        """Handles missingness for APRAXSP."""
        if self.formver < 3:
            return self._handle_normexam_gate("apraxsp")

        return self._handle_b8_missingness(gate="othersign", field="apraxsp")

    #########################
    # NORMEXAM-gated values #
    #########################

    def _handle_normexam_gate(self, field: str) -> Optional[int]:
        """V3 and earlier only.

        Handles values gated by NORMEXAM.
        """
        if self.uds.get_value("normexam", int) in [0, 2]:
            return 0

        return self.generic_missingness("field")

    def _missingness_resttrl(self) -> Optional[int]:
        """Handles missingness for RESTTRL."""
        return self._handle_normexam_gate("resttrl")

    def _missingness_resttrr(self) -> Optional[int]:
        """Handles missingness for RESTTRR."""
        return self._handle_normexam_gate("resttrr")

    def _missingness_slowingl(self) -> Optional[int]:
        """Handles missingness for SLOWINGL."""
        return self._handle_normexam_gate("slowingl")

    def _missingness_slowingr(self) -> Optional[int]:
        """Handles missingness for SLOWINGR."""
        return self._handle_normexam_gate("slowingr")

    def _missingness_rigidl(self) -> Optional[int]:
        """Handles missingness for RIGIDL."""
        return self._handle_normexam_gate("rigidl")

    def _missingness_rigidr(self) -> Optional[int]:
        """Handles missingness for RIGIDR."""
        return self._handle_normexam_gate("rigidr")

    def _missingness_brady(self) -> Optional[int]:
        """Handles missingness for BRADY."""
        return self._handle_normexam_gate("brady")

    def _missingness_parkgait(self) -> Optional[int]:
        """Handles missingness for PARKGAIT."""
        return self._handle_normexam_gate("parkgait")

    def _missingness_cvdsigns(self) -> Optional[int]:
        """Handles missingness for CVDSIGNS."""
        return self._handle_normexam_gate("cvdsigns")

    def _missingness_cortdef(self) -> Optional[int]:
        """Handles missingness for CORTDEF."""
        return self._handle_normexam_gate("cortdef")

    def _missingness_sivdfind(self) -> Optional[int]:
        """Handles missingness for SIVDFIND."""
        return self._handle_normexam_gate("sivdfind")

    def _missingness_cvdmotl(self) -> Optional[int]:
        """Handles missingness for CVDMOTL."""
        return self._handle_normexam_gate("cvdmotl")

    def _missingness_cvdmotr(self) -> Optional[int]:
        """Handles missingness for CVDMOTR."""
        return self._handle_normexam_gate("cvdmotr")

    def _missingness_cortvisl(self) -> Optional[int]:
        """Handles missingness for CORTVISL."""
        return self._handle_normexam_gate("cortvisl")

    def _missingness_cortvisr(self) -> Optional[int]:
        """Handles missingness for CORTVISR."""
        return self._handle_normexam_gate("cortvisr")

    def _missingness_somatl(self) -> Optional[int]:
        """Handles missingness for SOMATL."""
        return self._handle_normexam_gate("somatl")

    def _missingness_somatr(self) -> Optional[int]:
        """Handles missingness for SOMATR."""
        return self._handle_normexam_gate("somatr")

    def _missingness_postcort(self) -> Optional[int]:
        """Handles missingness for POSTCORT."""
        return self._handle_normexam_gate("postcort")

    def _missingness_pspcbs(self) -> Optional[int]:
        """Handles missingness for PSPCBS."""
        return self._handle_normexam_gate("pspcbs")

    def _missingness_eyepsp(self) -> Optional[int]:
        """Handles missingness for EYEPSP."""
        return self._handle_normexam_gate("eyepsp")

    def _missingness_dyspsp(self) -> Optional[int]:
        """Handles missingness for DYSPSP."""
        return self._handle_normexam_gate("dyspsp")

    def _missingness_axialpsp(self) -> Optional[int]:
        """Handles missingness for AXIALPSP."""
        return self._handle_normexam_gate("axialpsp")

    def _missingness_gaitpsp(self) -> Optional[int]:
        """Handles missingness for GAITPSP."""
        return self._handle_normexam_gate("gaitpsp")

    def _missingness_apraxl(self) -> Optional[int]:
        """Handles missingness for APRAXL."""
        return self._handle_normexam_gate("apraxl")

    def _missingness_apraxr(self) -> Optional[int]:
        """Handles missingness for APRAXR."""
        return self._handle_normexam_gate("apraxr")

    def _missingness_cortsenl(self) -> Optional[int]:
        """Handles missingness for CORTSENL."""
        return self._handle_normexam_gate("cortsenl")

    def _missingness_cortsenr(self) -> Optional[int]:
        """Handles missingness for CORTSENR."""
        return self._handle_normexam_gate("cortsenr")

    def _missingness_ataxl(self) -> Optional[int]:
        """Handles missingness for ATAXL."""
        return self._handle_normexam_gate("ataxl")

    def _missingness_ataxr(self) -> Optional[int]:
        """Handles missingness for ATAXR."""
        return self._handle_normexam_gate("ataxr")

    def _missingness_alienlml(self) -> Optional[int]:
        """Handles missingness for ALIENLML."""
        return self._handle_normexam_gate("alienlml")

    def _missingness_alienlmr(self) -> Optional[int]:
        """Handles missingness for ALIENLMR."""
        return self._handle_normexam_gate("alienlmr")

    def _missingness_dystonl(self) -> Optional[int]:
        """Handles missingness for DYSTONL."""
        return self._handle_normexam_gate("dystonl")

    def _missingness_dystonr(self) -> Optional[int]:
        """Handles missingness for DYSTONR."""
        return self._handle_normexam_gate("dystonr")

    def _missingness_myocllt(self) -> Optional[int]:
        """Handles missingness for MYOCLLT."""
        return self._handle_normexam_gate("myocllt")

    def _missingness_myoclrt(self) -> Optional[int]:
        """Handles missingness for MYOCLRT."""
        return self._handle_normexam_gate("myoclrt")

    def _missingness_alsfind(self) -> Optional[int]:
        """Handles missingness for ALSFIND."""
        return self._handle_normexam_gate("alsfind")

    def _missingness_gaitnph(self) -> Optional[int]:
        """Handles missingness for GAITNPH."""
        return self._handle_normexam_gate("gaitnph")

    def _missingness_othneur(self) -> Optional[int]:
        """Handles missingness for OTHNEUR.

        V3 and earlier only. For some reason the SAS code separates this
        out (NORMEXAM only == 0 instead of 0 and 2 like the others).
        """
        if self.formver >= 4:
            return INFORMED_MISSINGNESS

        if self.uds.get_value("normexam", int) == 0:
            return 0

        return self.generic_missingness("othneur")

    #############
    # Write-ins #
    #############

    def _missingness_othneurx(self) -> Optional[str]:
        """Handles missingness for OTHNEURX."""
        return self.generic_writein("othneurx")

    # there is recode logic for PARKQ, CVDQ, and PSPQ but these do not
    # appear in the DED nor are they in the QAF, so can probably ignore?
    # they seem to be write-in values for something
