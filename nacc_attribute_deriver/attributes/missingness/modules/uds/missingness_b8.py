"""Class to handle B8-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS

from .missingness_uds import UDSMissingness


class UDSFormB8Missingness(UDSMissingness):
    def _handle_normnrexam_gate(self) -> Optional[int]:
        """Handles missingness that relies solely on NORMNREXAM."""
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        if self.uds.get_value("normnrexam", int) == 0:
            return 0

        return None

    def _missingness_parksign(self) -> Optional[int]:
        """Handle missingness for PARKSIGN."""
        return self._handle_normnrexam_gate()

    def _missingness_othersign(self) -> Optional[int]:
        """Handle missingness for OTHERSIGN."""
        return self._handle_normnrexam_gate()

    def _missingness_gaitabn(self) -> Optional[int]:
        """Handle missingness for GAITABN."""
        return self._handle_normnrexam_gate()

    def _missingness_gaitfind(self) -> Optional[int]:
        """Handle missingness for GAITFIND."""
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        normnrexam = self.uds.get_value("normnrexam", int)
        gaitabn = self.uds.get_value("gaitabn", int)

        if normnrexam == 0 or gaitabn == 0:
            return 8

        return None

    def _handle_b8_missingness(self, gate: str) -> Optional[int]:
        """Handles B8 missingness that relies on NORMNREXAM and a GATE variable
        (PARKSIGN or OTHERSIGN), which follows:

        For V4:
            If NORMNREXAM=0 or GATE=0 then FIELD should = 0
            If GATE=8 then FIELD should =8
            Else return None (don't change)
        Else:
            -4
        """
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        normnrexam = self.uds.get_value("normnrexam", int)
        gate_value = self.uds.get_value(gate, int)

        if normnrexam == 0 or gate_value == 0:
            return 0

        if gate_value == 8:
            return 8

        return None

    def _missingness_slowingfm(self) -> Optional[int]:
        """Handles missingness for SLOWINGFM."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_tremrest(self) -> Optional[int]:
        """Handles missingness for TREMREST."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_trempost(self) -> Optional[int]:
        """Handles missingness for TREMPOST."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_tremkine(self) -> Optional[int]:
        """Handles missingness for TREMKINE."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_rigidarm(self) -> Optional[int]:
        """Handles missingness for RIGIDARM."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_rigidleg(self) -> Optional[int]:
        """Handles missingness for RIGIDLEG."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_dystarm(self) -> Optional[int]:
        """Handles missingness for DYSTARM."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_dystleg(self) -> Optional[int]:
        """Handles missingness for DYSTLEG."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_chorea(self) -> Optional[int]:
        """Handles missingness for CHOREA."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_ampmotor(self) -> Optional[int]:
        """Handles missingness for AMPMOTOR."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_axialrig(self) -> Optional[int]:
        """Handles missingness for AXIALRIG."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_postinst(self) -> Optional[int]:
        """Handles missingness for POSTINST."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_masking(self) -> Optional[int]:
        """Handles missingness for MASKING."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_stooped(self) -> Optional[int]:
        """Handles missingness for STOOPED."""
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_limbaprax(self) -> Optional[int]:
        """Handles missingness for LIMBAPRAX."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_umndist(self) -> Optional[int]:
        """Handles missingness for UMNDIST."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_lmndist(self) -> Optional[int]:
        """Handles missingness for LMNDIST."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_vfieldcut(self) -> Optional[int]:
        """Handles missingness for VFIELDCUT."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_limbatax(self) -> Optional[int]:
        """Handles missingness for LIMBATAX."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_myoclon(self) -> Optional[int]:
        """Handles missingness for MYOCLON."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_unisomato(self) -> Optional[int]:
        """Handles missingness for UNISOMATO."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_aphasia(self) -> Optional[int]:
        """Handles missingness for APHASIA."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_alienlimb(self) -> Optional[int]:
        """Handles missingness for ALIENLIMB."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_hspatneg(self) -> Optional[int]:
        """Handles missingness for HSPATNEG."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_pspoagno(self) -> Optional[int]:
        """Handles missingness for PSPOAGNO."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_smtagno(self) -> Optional[int]:
        """Handles missingness for SMTAGNO."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_opticatax(self) -> Optional[int]:
        """Handles missingness for OPTICATAX."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_apraxgaze(self) -> Optional[int]:
        """Handles missingness for APRAXGAZE."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_vhgazepal(self) -> Optional[int]:
        """Handles missingness for VHGAZEPAL."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_dysarth(self) -> Optional[int]:
        """Handles missingness for DYSARTH."""
        return self._handle_b8_missingness(gate="othersign")

    def _missingness_apraxsp(self) -> Optional[int]:
        """Handles missingness for APRAXSP."""
        return self._handle_b8_missingness(gate="othersign")
