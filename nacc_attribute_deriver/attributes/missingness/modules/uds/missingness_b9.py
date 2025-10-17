"""Class to handle B9-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS

from .missingness_uds import UDSMissingness


class UDSFormB9Missingness(UDSMissingness):


    def _handle_b9_gate(self, gate: str, missingness_value: int) -> int:
        """Handles missingness values gated by the specified variable:

        If GATE = 0, then VAR must be MISSINGNESS_VALUE
        """
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        if self.uds.get_value(gate, int) == 0:
            return missing_value

        return None

    def _missingness_decclin_gate_0(self) -> int:
        """Handles missingness for the following variables,
        which must be 0 if DECCLIN is 0:


        DECCLOG, COGMEM, COROGI, COGJUDG, COGLANG, COGVIS, COGATTN,
        COGFLUC, COGOTHR, COGMODE, DECCLBE, BEAPATHY, BEDEP, BEANX,
        BEEUPH, BEIRRIT, BEAGIT, BEVHALL, BEVPATT, BEVWELL, BEAHALL,
        BEAHSIMP, BEAHCOMP, BEDEL, BEAGGRS, BEDISIN, BEPERCH, BEEMPATH,
        BEOBCOM, BEANGER, BESUBAB, BEREM, BEREMCONF, BEOTHR, BEMODE,
        DECCLMOT, MOGAIT, MOFALLS, MOSLOW, MOTREM, MOLIMB, MOFACE,
        MOSPEECH, MOMODE, MOMOPARK, MOMOALS
        """
        return self._handle_b9_gate("decclin", missing_value=0)

    def _missingness_decclin_gate_8(self) -> int:
        """Handles missingness for the following variables,
        which must be 8 if DECCLIN is 0

        COURSE, FRSTCHG
        """
        return self._handle_b9_gate("decclin", missing_value=8)
