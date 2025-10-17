"""Class to handle B8-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS

from .missingness_uds import UDSMissingness


class UDSFormB8Missingness(UDSMissingness):
    def _missingness_normnrexam_gate(self) -> Optional[int]:
        """Handles missingness that relies solely on NORMNREXAM:

        PARKSIGN, OTHERSIGN, and GAITABN.
        """
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        if self.uds.get_value("normnrexam", int) == 0:
            return 0

        return None

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

    def _missingness_parksign_gate(self) -> Optional[int]:
        """Handles missingness for B8 variables that are gated
        by PARKSIGN:

        SLOWINGFM, TREMREST, TREMPOST, TREMKINE, RIGIDARM,
        RIGIDLEG, DYSTARM, DYSTLEG, CHOREA, AMPMOTOR, AXIALRIG,
        POSTINST, MASKING, STOOPED
        """
        return self._handle_b8_missingness(gate="parksign")

    def _missingness_othersign_gate(self) -> Optional[int]:
        """Handles missingness for B8 variables that are gated
        by OTHERSIGN:

        LIMBAPRAX, UMNDIST, LMNDIST, VFIELDCUT, LIMBATAX,
        MYOCLON, UNISOMATO, APHASIA, ALIENLIMB, HSPATNEG,
        PSPOAGNO, SMTAGNO, OPTICATAX, APRAXGAZE, VHGAZEPAL,
        DYSARTH, APRAXSP
        """
        return self._handle_b8_missingness(gate="othersign")
