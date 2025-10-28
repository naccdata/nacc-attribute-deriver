"""Class to handle C1/C2-specific missingness values."""

from typing import List, Optional

from .missingness_uds import UDSMissingness


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

        if value is None and respval in [2, 3]:
            return 0

        return None

    def _missingness_resphear(self) -> Optional[int]:
        """Handles missingness for RESPHEAR"""
        return self._handle_respval_gate("resphear")

    def _missingness_respdist(self) -> Optional[int]:
        """Handles missingness for RESPDIST"""
        return self._handle_respval_gate("respdist")

    def _missingness_respintr(self) -> Optional[int]:
        """Handles missingness for RESPINTR"""
        return self._handle_respval_gate("respintr")

    def _missingness_motrem(self) -> Optional[int]:
        """Handles missingness for MOTREM"""
        return self._handle_respval_gate("motrem")

    def _missingness_respdisn(self) -> Optional[int]:
        """Handles missingness for RESPDISN"""
        return self._handle_respval_gate("respdisn")

    def _missingness_respfatg(self) -> Optional[int]:
        """Handles missingness for RESPFATG"""
        return self._handle_respval_gate("respfatg")

    def _missingness_respemot(self) -> Optional[int]:
        """Handles missingness for RESPEMOT"""
        return self._handle_respval_gate("respemot")

    def _missingness_respasst(self) -> Optional[int]:
        """Handles missingness for RESPASST"""
        return self._handle_respval_gate("respasst")

    def _missingness_respoth(self) -> Optional[int]:
        """Handles missingness for RESPOTH"""
        return self._handle_respval_gate("respoth")

    ##############################
    # VERBALTEST gated variables #
    ##############################

    def _missingness_verbaltest_gate(self, default: int = 88) -> Optional[int]:
        """Handles variables gated by VERBALTEST, which generally
        follows the below logic.

        Since we don't need to check the field specifically
        for this, most rules except those that return 888 can
        directly call this method instead.

        If VERBALTEST = 2 then FIELD should = 88/888.
        """
        if self.uds.get_value("verbaltest", int) == 2:
            return default

        return None

    def _missingness_reybint(self) -> Optional[int]:
        """Handles missingness for REYBINT"""
        return self._missingness_verbaltest_gate("reybint", default=888)

    def _missingness_cerad1int(self) -> Optional[int]:
        """Handles missingness for CERAD1INT"""
        return self._missingness_verbaltest_gate("cerad1int", default=888)

    def _missingness_cerad2int(self) -> Optional[int]:
        """Handles missingness for CERAD2INT"""
        return self._missingness_verbaltest_gate("cerad2int", default=888)

    def _missingness_cerad3int(self) -> Optional[int]:
        """Handles missingness for CERAD3INT"""
        return self._missingness_verbaltest_gate("cerad3int", default=888)

    def _missingness_ceradj6int(self) -> Optional[int]:
        """Handles missingness for CERADJ6INT"""
        return self._missingness_verbaltest_gate("ceradj6int", default=888)

    ##########################################
    # Write-in variables that rely on a gate #
    ##########################################

    def _missingness_mocalanx(self) -> Optional[str]:
        """Handles missingness for MOCALANX"""
        return self.handle_gated_blank("mocalan", 3)

    def _missingness_npsylanx(self) -> Optional[str]:
        """Handles missingness for NPSYLANX"""
        return self.handle_gated_blank("npsylan", 3)

    def _missingness_respothx(self) -> Optional[str]:
        """Handles missingness for RESPOTHX"""
        return self.handle_gated_blank("respoth", 1)

    def _missingness_mmselanx(self) -> Optional[str]:
        """Handles missingness for MMSELANX"""
        return self.handle_gated_blank("mmselan", 3)

    ########################################
    # MINTTOTS and REYDREC gated variables #
    ########################################

    def _handle_set_to_gate(self, gate: str) -> Optional[int]:
        """Generically handle:

        If GATE is in 88 or 95-98, then FIELD should = GATE.
        """
        value = self.uds.get_value(gate, int)
        if value in [88, 95, 96, 97, 98]:
            return value

        return None

    def _missingness_minttots_gate(self) -> Optional[int]:
        """Handles variables gated by MINTTOTS, which generally
        follows the below logic.

        Since we don't need to check the field specifically
        for this, most rules except can directly call this method
        instead.

        If MINTTOTS is 88 or 95-98, then FIELD should = MINTTOTS
        """
        return self._handle_set_to_gate('minttots')

    def _missingness_reydrec_gate(self) -> Optional[int]:
        """Handles variables gated by REYDREC, which generally
        follows the below logic.

        Since we don't need to check the field specifically
        for this, most rules except can directly call this method
        instead.

        If REYDREC is 88 or 95-98, then FIELD should = REYDREC
        """
        return self._handle_set_to_gate('reydrec')

    ###########################
    # REYXREC gated variables #
    ###########################

    def _missingness_rey1int(self) -> Optional[int]:
        """Handles missingness for REY1INT"""
        return self._handle_set_to_gate("rey1rec")

    def _missingness_rey2int(self) -> Optional[int]:
        """Handles missingness for REY2INT"""
        return self._handle_set_to_gate("rey2rec")

    def _missingness_rey3int(self) -> Optional[int]:
        """Handles missingness for REY3INT"""
        return self._handle_set_to_gate("rey3rec")

    def _missingness_rey4int(self) -> Optional[int]:
        """Handles missingness for REY4INT"""
        return self._handle_set_to_gate("rey4rec")

    def _missingness_rey5int(self) -> Optional[int]:
        """Handles missingness for REY5INT"""
        return self._handle_set_to_gate("rey5rec")

    def _missingness_rey6int(self) -> Optional[int]:
        """Handles missingness for REY6INT"""
        return self._handle_set_to_gate("rey6rec")

    def _missingness_rey6int(self) -> Optional[int]:
        """Handles missingness for REY6INT"""
        return self._handle_set_to_gate("rey6rec")