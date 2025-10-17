"""Class to handle B9-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS

from .missingness_uds import UDSMissingness


class UDSFormB9Missingness(UDSMissingness):
    def _handle_b9_gate(self, gate: str, field: str, missingness_value: int) -> int:
        """Handles missingness values gated by the specified variable:

        If GATE = 0, then VAR must be MISSINGNESS_VALUE

        If condition does not apply, return generic missingness.
        """
        if self.uds.get_value(gate, int) == 0:
            return missing_value

        return self.generic_missingness(field)

    def _missingness_decclog(self) -> Optional[int]:
        """Handles missingness for DECCLOG"""
        return self._handle_b9_gate("decclin", field="decclog", missingness_value=0)

    def _missingness_cogmem(self) -> Optional[int]:
        """Handles missingness for COGMEM"""
        return self._handle_b9_gate("decclin", field="cogmem", missingness_value=0)

    def _missingness_corogi(self) -> Optional[int]:
        """Handles missingness for COROGI"""
        return self._handle_b9_gate("decclin", field="corogi", missingness_value=0)

    def _missingness_cogjudg(self) -> Optional[int]:
        """Handles missingness for COGJUDG"""
        return self._handle_b9_gate("decclin", field="cogjudg", missingness_value=0)

    def _missingness_coglang(self) -> Optional[int]:
        """Handles missingness for COGLANG"""
        return self._handle_b9_gate("decclin", field="coglang", missingness_value=0)

    def _missingness_cogvis(self) -> Optional[int]:
        """Handles missingness for COGVIS"""
        return self._handle_b9_gate("decclin", field="cogvis", missingness_value=0)

    def _missingness_cogattn(self) -> Optional[int]:
        """Handles missingness for COGATTN"""
        return self._handle_b9_gate("decclin", field="cogattn", missingness_value=0)

    def _missingness_cogfluc(self) -> Optional[int]:
        """Handles missingness for COGFLUC"""
        return self._handle_b9_gate("decclin", field="cogfluc", missingness_value=0)

    def _missingness_cogothr(self) -> Optional[int]:
        """Handles missingness for COGOTHR"""
        return self._handle_b9_gate("decclin", field="cogothr", missingness_value=0)

    def _missingness_cogmode(self) -> Optional[int]:
        """Handles missingness for COGMODE"""
        return self._handle_b9_gate("decclin", field="cogmode", missingness_value=0)

    def _missingness_decclbe(self) -> Optional[int]:
        """Handles missingness for DECCLBE"""
        return self._handle_b9_gate("decclin", field="decclbe", missingness_value=0)

    def _missingness_beapathy(self) -> Optional[int]:
        """Handles missingness for BEAPATHY"""
        return self._handle_b9_gate("decclin", field="beapathy", missingness_value=0)

    def _missingness_bedep(self) -> Optional[int]:
        """Handles missingness for BEDEP"""
        return self._handle_b9_gate("decclin", field="bedep", missingness_value=0)

    def _missingness_beanx(self) -> Optional[int]:
        """Handles missingness for BEANX"""
        return self._handle_b9_gate("decclin", field="beanx", missingness_value=0)

    def _missingness_beeuph(self) -> Optional[int]:
        """Handles missingness for BEEUPH"""
        return self._handle_b9_gate("decclin", field="beeuph", missingness_value=0)

    def _missingness_beirrit(self) -> Optional[int]:
        """Handles missingness for BEIRRIT"""
        return self._handle_b9_gate("decclin", field="beirrit", missingness_value=0)

    def _missingness_beagit(self) -> Optional[int]:
        """Handles missingness for BEAGIT"""
        return self._handle_b9_gate("decclin", field="beagit", missingness_value=0)

    def _missingness_bevhall(self) -> Optional[int]:
        """Handles missingness for BEVHALL"""
        return self._handle_b9_gate("decclin", field="bevhall", missingness_value=0)

    def _missingness_bevpatt(self) -> Optional[int]:
        """Handles missingness for BEVPATT"""
        return self._handle_b9_gate("decclin", field="bevpatt", missingness_value=0)

    def _missingness_bevwell(self) -> Optional[int]:
        """Handles missingness for BEVWELL"""
        return self._handle_b9_gate("decclin", field="bevwell", missingness_value=0)

    def _missingness_beahall(self) -> Optional[int]:
        """Handles missingness for BEAHALL"""
        return self._handle_b9_gate("decclin", field="beahall", missingness_value=0)

    def _missingness_beahsimp(self) -> Optional[int]:
        """Handles missingness for BEAHSIMP"""
        return self._handle_b9_gate("decclin", field="beahsimp", missingness_value=0)

    def _missingness_beahcomp(self) -> Optional[int]:
        """Handles missingness for BEAHCOMP"""
        return self._handle_b9_gate("decclin", field="beahcomp", missingness_value=0)

    def _missingness_bedel(self) -> Optional[int]:
        """Handles missingness for BEDEL"""
        return self._handle_b9_gate("decclin", field="bedel", missingness_value=0)

    def _missingness_beaggrs(self) -> Optional[int]:
        """Handles missingness for BEAGGRS"""
        return self._handle_b9_gate("decclin", field="beaggrs", missingness_value=0)

    def _missingness_bedisin(self) -> Optional[int]:
        """Handles missingness for BEDISIN"""
        return self._handle_b9_gate("decclin", field="bedisin", missingness_value=0)

    def _missingness_beperch(self) -> Optional[int]:
        """Handles missingness for BEPERCH"""
        return self._handle_b9_gate("decclin", field="beperch", missingness_value=0)

    def _missingness_beempath(self) -> Optional[int]:
        """Handles missingness for BEEMPATH"""
        return self._handle_b9_gate("decclin", field="beempath", missingness_value=0)

    def _missingness_beobcom(self) -> Optional[int]:
        """Handles missingness for BEOBCOM"""
        return self._handle_b9_gate("decclin", field="beobcom", missingness_value=0)

    def _missingness_beanger(self) -> Optional[int]:
        """Handles missingness for BEANGER"""
        return self._handle_b9_gate("decclin", field="beanger", missingness_value=0)

    def _missingness_besubab(self) -> Optional[int]:
        """Handles missingness for BESUBAB"""
        return self._handle_b9_gate("decclin", field="besubab", missingness_value=0)

    def _missingness_berem(self) -> Optional[int]:
        """Handles missingness for BEREM"""
        return self._handle_b9_gate("decclin", field="berem", missingness_value=0)

    def _missingness_beremconf(self) -> Optional[int]:
        """Handles missingness for BEREMCONF"""
        return self._handle_b9_gate("decclin", field="beremconf", missingness_value=0)

    def _missingness_beothr(self) -> Optional[int]:
        """Handles missingness for BEOTHR"""
        return self._handle_b9_gate("decclin", field="beothr", missingness_value=0)

    def _missingness_bemode(self) -> Optional[int]:
        """Handles missingness for BEMODE"""
        return self._handle_b9_gate("decclin", field="bemode", missingness_value=0)

    def _missingness_decclmot(self) -> Optional[int]:
        """Handles missingness for DECCLMOT"""
        return self._handle_b9_gate("decclin", field="decclmot", missingness_value=0)

    def _missingness_mogait(self) -> Optional[int]:
        """Handles missingness for MOGAIT"""
        return self._handle_b9_gate("decclin", field="mogait", missingness_value=0)

    def _missingness_mofalls(self) -> Optional[int]:
        """Handles missingness for MOFALLS"""
        return self._handle_b9_gate("decclin", field="mofalls", missingness_value=0)

    def _missingness_moslow(self) -> Optional[int]:
        """Handles missingness for MOSLOW"""
        return self._handle_b9_gate("decclin", field="moslow", missingness_value=0)

    def _missingness_motrem(self) -> Optional[int]:
        """Handles missingness for MOTREM"""
        return self._handle_b9_gate("decclin", field="motrem", missingness_value=0)

    def _missingness_molimb(self) -> Optional[int]:
        """Handles missingness for MOLIMB"""
        return self._handle_b9_gate("decclin", field="molimb", missingness_value=0)

    def _missingness_moface(self) -> Optional[int]:
        """Handles missingness for MOFACE"""
        return self._handle_b9_gate("decclin", field="moface", missingness_value=0)

    def _missingness_mospeech(self) -> Optional[int]:
        """Handles missingness for MOSPEECH"""
        return self._handle_b9_gate("decclin", field="mospeech", missingness_value=0)

    def _missingness_momode(self) -> Optional[int]:
        """Handles missingness for MOMODE"""
        return self._handle_b9_gate("decclin", field="momode", missingness_value=0)

    def _missingness_momopark(self) -> Optional[int]:
        """Handles missingness for MOMOPARK"""
        return self._handle_b9_gate("decclin", field="momopark", missingness_value=0)

    def _missingness_momoals(self) -> Optional[int]:
        """Handles missingness for MOMOALS"""
        return self._handle_b9_gate("decclin", field="momoals", missingness_value=0)

    def _missingness_course(self) -> Optional[int]:
        """Handles missingness for COURSE"""
        return self._handle_b9_gate("decclin", field="course", missingness_value=8)

    def _missingness_frstchg(self) -> Optional[int]:
        """Handles missingness for FRSTCHG"""
        return self._handle_b9_gate("decclin", field="frstchg", missingness_value=8)

    def _missingness_cogmem(self) -> Optional[int]:
        """Handles missingness for COGMEM"""
        return self._handle_b9_gate("decclog", field="cogmem", missingness_value=0)

    def _missingness_corogi(self) -> Optional[int]:
        """Handles missingness for COROGI"""
        return self._handle_b9_gate("decclog", field="corogi", missingness_value=0)

    def _missingness_cogjudg(self) -> Optional[int]:
        """Handles missingness for COGJUDG"""
        return self._handle_b9_gate("decclog", field="cogjudg", missingness_value=0)

    def _missingness_coglang(self) -> Optional[int]:
        """Handles missingness for COGLANG"""
        return self._handle_b9_gate("decclog", field="coglang", missingness_value=0)

    def _missingness_cogvis(self) -> Optional[int]:
        """Handles missingness for COGVIS"""
        return self._handle_b9_gate("decclog", field="cogvis", missingness_value=0)

    def _missingness_cogattn(self) -> Optional[int]:
        """Handles missingness for COGATTN"""
        return self._handle_b9_gate("decclog", field="cogattn", missingness_value=0)

    def _missingness_cogfluc(self) -> Optional[int]:
        """Handles missingness for COGFLUC"""
        return self._handle_b9_gate("decclog", field="cogfluc", missingness_value=0)

    def _missingness_cogothr(self) -> Optional[int]:
        """Handles missingness for COGOTHR"""
        return self._handle_b9_gate("decclog", field="cogothr", missingness_value=0)

    def _missingness_cogmode(self) -> Optional[int]:
        """Handles missingness for COGMODE"""
        return self._handle_b9_gate("decclog", field="cogmode", missingness_value=0)

    def _missingness_beapathy(self) -> Optional[int]:
        """Handles missingness for BEAPATHY"""
        return self._handle_b9_gate("decclbe", field="beapathy", missingness_value=0)

    def _missingness_bedep(self) -> Optional[int]:
        """Handles missingness for BEDEP"""
        return self._handle_b9_gate("decclbe", field="bedep", missingness_value=0)

    def _missingness_beanx(self) -> Optional[int]:
        """Handles missingness for BEANX"""
        return self._handle_b9_gate("decclbe", field="beanx", missingness_value=0)

    def _missingness_beeuph(self) -> Optional[int]:
        """Handles missingness for BEEUPH"""
        return self._handle_b9_gate("decclbe", field="beeuph", missingness_value=0)

    def _missingness_beirrit(self) -> Optional[int]:
        """Handles missingness for BEIRRIT"""
        return self._handle_b9_gate("decclbe", field="beirrit", missingness_value=0)

    def _missingness_beagit(self) -> Optional[int]:
        """Handles missingness for BEAGIT"""
        return self._handle_b9_gate("decclbe", field="beagit", missingness_value=0)

    def _missingness_bevhall(self) -> Optional[int]:
        """Handles missingness for BEVHALL"""
        return self._handle_b9_gate("decclbe", field="bevhall", missingness_value=0)

    def _missingness_bevpatt(self) -> Optional[int]:
        """Handles missingness for BEVPATT"""
        return self._handle_b9_gate("decclbe", field="bevpatt", missingness_value=0)

    def _missingness_bevwell(self) -> Optional[int]:
        """Handles missingness for BEVWELL"""
        return self._handle_b9_gate("decclbe", field="bevwell", missingness_value=0)

    def _missingness_beahall(self) -> Optional[int]:
        """Handles missingness for BEAHALL"""
        return self._handle_b9_gate("decclbe", field="beahall", missingness_value=0)

    def _missingness_beahsimp(self) -> Optional[int]:
        """Handles missingness for BEAHSIMP"""
        return self._handle_b9_gate("decclbe", field="beahsimp", missingness_value=0)

    def _missingness_beahcomp(self) -> Optional[int]:
        """Handles missingness for BEAHCOMP"""
        return self._handle_b9_gate("decclbe", field="beahcomp", missingness_value=0)

    def _missingness_bedel(self) -> Optional[int]:
        """Handles missingness for BEDEL"""
        return self._handle_b9_gate("decclbe", field="bedel", missingness_value=0)

    def _missingness_beaggrs(self) -> Optional[int]:
        """Handles missingness for BEAGGRS"""
        return self._handle_b9_gate("decclbe", field="beaggrs", missingness_value=0)

    def _missingness_bedisin(self) -> Optional[int]:
        """Handles missingness for BEDISIN"""
        return self._handle_b9_gate("decclbe", field="bedisin", missingness_value=0)

    def _missingness_beperch(self) -> Optional[int]:
        """Handles missingness for BEPERCH"""
        return self._handle_b9_gate("decclbe", field="beperch", missingness_value=0)

    def _missingness_beempath(self) -> Optional[int]:
        """Handles missingness for BEEMPATH"""
        return self._handle_b9_gate("decclbe", field="beempath", missingness_value=0)

    def _missingness_beobcom(self) -> Optional[int]:
        """Handles missingness for BEOBCOM"""
        return self._handle_b9_gate("decclbe", field="beobcom", missingness_value=0)

    def _missingness_beanger(self) -> Optional[int]:
        """Handles missingness for BEANGER"""
        return self._handle_b9_gate("decclbe", field="beanger", missingness_value=0)

    def _missingness_besubab(self) -> Optional[int]:
        """Handles missingness for BESUBAB"""
        return self._handle_b9_gate("decclbe", field="besubab", missingness_value=0)

    def _missingness_alcuse(self) -> Optional[int]:
        """Handles missingness for ALCUSE"""
        return self._handle_b9_gate("decclbe", field="alcuse", missingness_value=0)

    def _missingness_seduse(self) -> Optional[int]:
        """Handles missingness for SEDUSE"""
        return self._handle_b9_gate("decclbe", field="seduse", missingness_value=0)

    def _missingness_opiateuse(self) -> Optional[int]:
        """Handles missingness for OPIATEUSE"""
        return self._handle_b9_gate("decclbe", field="opiateuse", missingness_value=0)

    def _missingness_cocaineuse(self) -> Optional[int]:
        """Handles missingness for COCAINEUSE"""
        return self._handle_b9_gate("decclbe", field="cocaineuse", missingness_value=0)

    def _missingness_cannabuse(self) -> Optional[int]:
        """Handles missingness for CANNABUSE"""
        return self._handle_b9_gate("decclbe", field="cannabuse", missingness_value=0)

    def _missingness_othsubuse(self) -> Optional[int]:
        """Handles missingness for OTHSUBUSE"""
        return self._handle_b9_gate("decclbe", field="othsubuse", missingness_value=0)

    def _missingness_berem(self) -> Optional[int]:
        """Handles missingness for BEREM"""
        return self._handle_b9_gate("decclbe", field="berem", missingness_value=0)

    def _missingness_beremconf(self) -> Optional[int]:
        """Handles missingness for BEREMCONF"""
        return self._handle_b9_gate("decclbe", field="beremconf", missingness_value=0)

    def _missingness_beothr(self) -> Optional[int]:
        """Handles missingness for BEOTHR"""
        return self._handle_b9_gate("decclbe", field="beothr", missingness_value=0)

    def _missingness_bemode(self) -> Optional[int]:
        """Handles missingness for BEMODE"""
        return self._handle_b9_gate("decclbe", field="bemode", missingness_value=0)

    def _missingness_mogait(self) -> Optional[int]:
        """Handles missingness for MOGAIT"""
        return self._handle_b9_gate("decclmot", field="mogait", missingness_value=0)

    def _missingness_mofalls(self) -> Optional[int]:
        """Handles missingness for MOFALLS"""
        return self._handle_b9_gate("decclmot", field="mofalls", missingness_value=0)

    def _missingness_moslow(self) -> Optional[int]:
        """Handles missingness for MOSLOW"""
        return self._handle_b9_gate("decclmot", field="moslow", missingness_value=0)

    def _missingness_motrem(self) -> Optional[int]:
        """Handles missingness for MOTREM"""
        return self._handle_b9_gate("decclmot", field="motrem", missingness_value=0)

    def _missingness_molimb(self) -> Optional[int]:
        """Handles missingness for MOLIMB"""
        return self._handle_b9_gate("decclmot", field="molimb", missingness_value=0)

    def _missingness_moface(self) -> Optional[int]:
        """Handles missingness for MOFACE"""
        return self._handle_b9_gate("decclmot", field="moface", missingness_value=0)

    def _missingness_mospeech(self) -> Optional[int]:
        """Handles missingness for MOSPEECH"""
        return self._handle_b9_gate("decclmot", field="mospeech", missingness_value=0)

    def _missingness_momode(self) -> Optional[int]:
        """Handles missingness for MOMODE"""
        return self._handle_b9_gate("decclmot", field="momode", missingness_value=0)

    def _missingness_momopark(self) -> Optional[int]:
        """Handles missingness for MOMOPARK"""
        return self._handle_b9_gate("decclmot", field="momopark", missingness_value=0)

    def _missingness_momoals(self) -> Optional[int]:
        """Handles missingness for MOMOALS"""
        return self._handle_b9_gate("decclmot", field="momoals", missingness_value=0)
