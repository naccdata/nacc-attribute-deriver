"""Class to handle A4a-specific missingness values.

# TODO: STILL IN PROGRESS, WAITING RT FEEDBACK
"""

from typing import Any, List, Optional

from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

from .missingness_uds import UDSMissingness


class UDSFormA4aMissingness(UDSMissingness):
    def _handle_fvp_gate(self, gate: str, field: str) -> Optional[int]:
        """Handle FVP gated by NEWTREAT and NEWADEVENT.

        If NEWTREAT = 0 or 9, all subsequent variables Q.2a1a-3b3a
            should be autofilled to prior visit
        If NEWADEVENT = 0 or 9, all  subsequent variables Q.3b1-3b3a
            should be autofilled to prior visit
        """
        if self.uds.get_value(gate, int) in [0, 9]:
            return 0

        return self.generic_missingness(field)

    def _handle_a4a_missingness(  # noqa: C901
        self, fvp_gates: List[str], field: str, writein: bool = False
    ) -> Optional[Any]:
        """Handle A4a missingness, which is generally:

        For V4:
        If IVP and VAR is blank then VAR should = 0

        If FVP, check gates from fvp_gates argument, can be any one of the following:
            If NEWTREAT = 0 or 9, all subsequent variables Q.2a1a-3b3a
                should be autofilled to prior visit
            If NEWADEVENT = 0 or 9, all subsequent variables Q.3b1-3b3a
                should be autofilled to prior visit
            If TRTBIOMARK = 0 then VAR should = 8; if TRTBIOMARK = 9 then VAR should = 9
            If ADVEVENT = 0 then VAR should = 8; if ADVEVENT = 9 then VAR should = 9
            If NEWADEVENT=0 then VAR should =8; If NEWADEVENT=9 then VAR should =9

        Else default missingness (-4)
        """
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        if not self.uds.is_initial():
            for gate in fvp_gates:
                gate_value = self.uds.get_value(gate, int)

                if gate in ["newtreat", "newadevent"]:
                    if gate_value in [0, 9] and self.prev_record:
                        return self.prev_record.get_resolved_value(
                            field, attr_type=str if writein else int
                        )

                elif gate in ["trtbiomark", "advevent"]:
                    if gate_value == 0:
                        return 8
                    if gate_value == 9:
                        return 9

        if writein:
            return self.generic_writein(field)

        result = self.uds.get_value(field, int)
        if result is not None:
            return None

        return 0

    def _missingness_targetab1(self) -> Optional[int]:
        """Handles missingness for TARGETAB1."""
        return self._handle_a4a_missingness(["newtreat"], "targetab1")

    def _missingness_targettau1(self) -> Optional[int]:
        """Handles missingness for TARGETTAU1."""
        return self._handle_a4a_missingness(["newtreat"], "targettau1")

    def _missingness_targetinf1(self) -> Optional[int]:
        """Handles missingness for TARGETINF1."""
        return self._handle_a4a_missingness(["newtreat"], "targetinf1")

    def _missingness_targetsyn1(self) -> Optional[int]:
        """Handles missingness for TARGETSYN1."""
        return self._handle_a4a_missingness(["newtreat"], "targetsyn1")

    def _missingness_targetoth1(self) -> Optional[int]:
        """Handles missingness for TARGETOTH1."""
        return self._handle_a4a_missingness(["newtreat"], "targetoth1")

    def _missingness_targetotx1(self) -> Optional[str]:
        """Handles missingness for TARGETOTX1."""
        return self._handle_a4a_missingness(["newtreat"], "targetotx1", writein=True)

    def _missingness_trttrial1(self) -> Optional[str]:
        """Handles missingness for TRTTRIAL1."""
        return self._handle_a4a_missingness(["newtreat"], "trttrial1", writein=True)

    def _missingness_nctnum1(self) -> Optional[int]:
        """Handles missingness for NCTNUM1."""
        return self._handle_a4a_missingness(["newtreat"], "nctnum1", writein=True)

    def _missingness_targetab2(self) -> Optional[int]:
        """Handles missingness for TARGETAB2."""
        return self._handle_a4a_missingness(["newtreat"], "targetab2")

    def _missingness_targettau2(self) -> Optional[int]:
        """Handles missingness for TARGETTAU2."""
        return self._handle_a4a_missingness(["newtreat"], "targettau2")

    def _missingness_targetinf2(self) -> Optional[int]:
        """Handles missingness for TARGETINF2."""
        return self._handle_a4a_missingness(["newtreat"], "targetinf2")

    def _missingness_targetsyn2(self) -> Optional[int]:
        """Handles missingness for TARGETSYN2."""
        return self._handle_a4a_missingness(["newtreat"], "targetsyn2")

    def _missingness_targetoth2(self) -> Optional[int]:
        """Handles missingness for TARGETOTH2."""
        return self._handle_a4a_missingness(["newtreat"], "targetoth2")

    def _missingness_targetotx2(self) -> Optional[int]:
        """Handles missingness for TARGETOTX2."""
        return self._handle_a4a_missingness(["newtreat"], "targetotx2", writein=True)

    def _missingness_trttrial2(self) -> Optional[int]:
        """Handles missingness for TRTTRIAL2."""
        return self._handle_a4a_missingness(["newtreat"], "trttrial2", writein=True)

    def _missingness_nctnum2(self) -> Optional[int]:
        """Handles missingness for NCTNUM2."""
        return self._handle_a4a_missingness(["newtreat"], "nctnum2", writein=True)

    def _missingness_targetab3(self) -> Optional[int]:
        """Handles missingness for TARGETAB3."""
        return self._handle_a4a_missingness(["newtreat"], "targetab3")

    def _missingness_targettau3(self) -> Optional[int]:
        """Handles missingness for TARGETTAU3."""
        return self._handle_a4a_missingness(["newtreat"], "targettau3")

    def _missingness_targetinf3(self) -> Optional[int]:
        """Handles missingness for TARGETINF3."""
        return self._handle_a4a_missingness(["newtreat"], "targetinf3")

    def _missingness_targetsyn3(self) -> Optional[int]:
        """Handles missingness for TARGETSYN3."""
        return self._handle_a4a_missingness(["newtreat"], "targetsyn3")

    def _missingness_targetoth3(self) -> Optional[int]:
        """Handles missingness for TARGETOTH3."""
        return self._handle_a4a_missingness(["newtreat"], "targetoth3")

    def _missingness_targetotx3(self) -> Optional[int]:
        """Handles missingness for TARGETOTX3."""
        return self._handle_a4a_missingness(["newtreat"], "targetotx3", writein=True)

    def _missingness_trttrial3(self) -> Optional[int]:
        """Handles missingness for TRTTRIAL3."""
        return self._handle_a4a_missingness(["newtreat"], "trttrial3", writein=True)

    def _missingness_nctnum3(self) -> Optional[int]:
        """Handles missingness for NCTNUM3."""
        return self._handle_a4a_missingness(["newtreat"], "nctnum3", writein=True)

    def _missingness_targetab4(self) -> Optional[int]:
        """Handles missingness for TARGETAB4."""
        return self._handle_a4a_missingness(["newtreat"], "targetab4")

    def _missingness_targettau4(self) -> Optional[int]:
        """Handles missingness for TARGETTAU4."""
        return self._handle_a4a_missingness(["newtreat"], "targettau4")

    def _missingness_targetinf4(self) -> Optional[int]:
        """Handles missingness for TARGETINF4."""
        return self._handle_a4a_missingness(["newtreat"], "targetinf4")

    def _missingness_targetsyn4(self) -> Optional[int]:
        """Handles missingness for TARGETSYN4."""
        return self._handle_a4a_missingness(["newtreat"], "targetsyn4")

    def _missingness_targetoth4(self) -> Optional[int]:
        """Handles missingness for TARGETOTH4."""
        return self._handle_a4a_missingness(["newtreat"], "targetoth4")

    def _missingness_targetotx4(self) -> Optional[int]:
        """Handles missingness for TARGETOTX4."""
        return self._handle_a4a_missingness(["newtreat"], "targetotx4", writein=True)

    def _missingness_trttrial4(self) -> Optional[int]:
        """Handles missingness for TRTTRIAL4."""
        return self._handle_a4a_missingness(["newtreat"], "trttrial4", writein=True)

    def _missingness_nctnum4(self) -> Optional[int]:
        """Handles missingness for NCTNUM4."""
        return self._handle_a4a_missingness(["newtreat"], "nctnum4", writein=True)

    def _missingness_targetab5(self) -> Optional[int]:
        """Handles missingness for TARGETAB5."""
        return self._handle_a4a_missingness(["newtreat"], "targetab5")

    def _missingness_targettau5(self) -> Optional[int]:
        """Handles missingness for TARGETTAU5."""
        return self._handle_a4a_missingness(["newtreat"], "targettau5")

    def _missingness_targetinf5(self) -> Optional[int]:
        """Handles missingness for TARGETINF5."""
        return self._handle_a4a_missingness(["newtreat"], "targetinf5")

    def _missingness_targetsyn5(self) -> Optional[int]:
        """Handles missingness for TARGETSYN5."""
        return self._handle_a4a_missingness(["newtreat"], "targetsyn5")

    def _missingness_targetoth5(self) -> Optional[int]:
        """Handles missingness for TARGETOTH5."""
        return self._handle_a4a_missingness(["newtreat"], "targetoth5")

    def _missingness_targetotx5(self) -> Optional[int]:
        """Handles missingness for TARGETOTX5."""
        return self._handle_a4a_missingness(["newtreat"], "targetotx5", writein=True)

    def _missingness_trttrial5(self) -> Optional[int]:
        """Handles missingness for TRTTRIAL5."""
        return self._handle_a4a_missingness(["newtreat"], "trttrial5", writein=True)

    def _missingness_nctnum5(self) -> Optional[int]:
        """Handles missingness for NCTNUM5."""
        return self._handle_a4a_missingness(["newtreat"], "nctnum5", writein=True)

    def _missingness_targetab6(self) -> Optional[int]:
        """Handles missingness for TARGETAB6."""
        return self._handle_a4a_missingness(["newtreat"], "targetab6")

    def _missingness_targettau6(self) -> Optional[int]:
        """Handles missingness for TARGETTAU6."""
        return self._handle_a4a_missingness(["newtreat"], "targettau6")

    def _missingness_targetinf6(self) -> Optional[int]:
        """Handles missingness for TARGETINF6."""
        return self._handle_a4a_missingness(["newtreat"], "targetinf6")

    def _missingness_targetsyn6(self) -> Optional[int]:
        """Handles missingness for TARGETSYN6."""
        return self._handle_a4a_missingness(["newtreat"], "targetsyn6")

    def _missingness_targetoth6(self) -> Optional[int]:
        """Handles missingness for TARGETOTH6."""
        return self._handle_a4a_missingness(["newtreat"], "targetoth6")

    def _missingness_targetotx6(self) -> Optional[int]:
        """Handles missingness for TARGETOTX6."""
        return self._handle_a4a_missingness(["newtreat"], "targetotx6", writein=True)

    def _missingness_trttrial6(self) -> Optional[int]:
        """Handles missingness for TRTTRIAL6."""
        return self._handle_a4a_missingness(["newtreat"], "trttrial6", writein=True)

    def _missingness_nctnum6(self) -> Optional[int]:
        """Handles missingness for NCTNUM6."""
        return self._handle_a4a_missingness(["newtreat"], "nctnum6", writein=True)

    def _missingness_targetab7(self) -> Optional[int]:
        """Handles missingness for TARGETAB7."""
        return self._handle_a4a_missingness(["newtreat"], "targetab7")

    def _missingness_targettau7(self) -> Optional[int]:
        """Handles missingness for TARGETTAU7."""
        return self._handle_a4a_missingness(["newtreat"], "targettau7")

    def _missingness_targetinf7(self) -> Optional[int]:
        """Handles missingness for TARGETINF7."""
        return self._handle_a4a_missingness(["newtreat"], "targetinf7")

    def _missingness_targetsyn7(self) -> Optional[int]:
        """Handles missingness for TARGETSYN7."""
        return self._handle_a4a_missingness(["newtreat"], "targetsyn7")

    def _missingness_targetoth7(self) -> Optional[int]:
        """Handles missingness for TARGETOTH7."""
        return self._handle_a4a_missingness(["newtreat"], "targetoth7")

    def _missingness_targetotx7(self) -> Optional[int]:
        """Handles missingness for TARGETOTX7."""
        return self._handle_a4a_missingness(["newtreat"], "targetotx7", writein=True)

    def _missingness_trttrial7(self) -> Optional[int]:
        """Handles missingness for TRTTRIAL7."""
        return self._handle_a4a_missingness(["newtreat"], "trttrial7", writein=True)

    def _missingness_nctnum7(self) -> Optional[int]:
        """Handles missingness for NCTNUM7."""
        return self._handle_a4a_missingness(["newtreat"], "nctnum7", writein=True)

    def _missingness_targetab8(self) -> Optional[int]:
        """Handles missingness for TARGETAB8."""
        return self._handle_a4a_missingness(["newtreat"], "targetab8")

    def _missingness_targettau8(self) -> Optional[int]:
        """Handles missingness for TARGETTAU8."""
        return self._handle_a4a_missingness(["newtreat"], "targettau8")

    def _missingness_targetinf8(self) -> Optional[int]:
        """Handles missingness for TARGETINF8."""
        return self._handle_a4a_missingness(["newtreat"], "targetinf8")

    def _missingness_targetsyn8(self) -> Optional[int]:
        """Handles missingness for TARGETSYN8."""
        return self._handle_a4a_missingness(["newtreat"], "targetsyn8")

    def _missingness_targetoth8(self) -> Optional[int]:
        """Handles missingness for TARGETOTH8."""
        return self._handle_a4a_missingness(["newtreat"], "targetoth8")

    def _missingness_targetotx8(self) -> Optional[int]:
        """Handles missingness for TARGETOTX8."""
        return self._handle_a4a_missingness(["newtreat"], "targetotx8", writein=True)

    def _missingness_trttrial8(self) -> Optional[int]:
        """Handles missingness for TRTTRIAL8."""
        return self._handle_a4a_missingness(["newtreat"], "trttrial8", writein=True)

    def _missingness_nctnum8(self) -> Optional[int]:
        """Handles missingness for NCTNUM8."""
        return self._handle_a4a_missingness(["newtreat"], "nctnum8", writein=True)

    def _missingness_ariae(self) -> Optional[int]:
        """Handles missingness for ARIAE."""
        return self._handle_a4a_missingness(
            ["newtreat", "newadevent", "trtbiomark"], "ariae"
        )

    def _missingness_ariah(self) -> Optional[int]:
        """Handles missingness for ARIAH."""
        return self._handle_a4a_missingness(
            ["newtreat", "newadevent", "trtbiomark"], "ariah"
        )

    def _missingness_adverseoth(self) -> Optional[int]:
        """Handles missingness for ADVERSEOTH."""
        return self._handle_a4a_missingness(
            ["newtreat", "newadevent", "trtbiomark"], "adverseoth"
        )

    def _missingness_adverseotx(self) -> Optional[str]:
        """Handles missingness for ADVERSEOTX."""
        return self._handle_a4a_missingness(
            ["newtreat", "newadevent", "trtbiomark"], "adverseotx", writein=True
        )
