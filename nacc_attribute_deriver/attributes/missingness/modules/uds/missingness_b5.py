"""Class to handle B5-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)

from .missingness_uds import UDSMissingness


class UDSFormB5Missingness(UDSMissingness):
    def _missingness_npiqinfx(self) -> Optional[str]:
        """Handle missingness for NPIQINFX."""
        return self.handle_forbidden_gated_writein("npiqinf", 3)

    ###############
    # XSEV values #
    ###############

    def __handle_xsev_gate(self, gate: str, field: str) -> Optional[int]:
        """Handle B5 gates, which follow:

        If GATE == 0, then FIELD = 8
        If GATE == 9 then FIELD = -4
        """
        gate_value = self.uds.get_value(gate, int)
        if gate_value == 0:
            return 8
        if gate_value == 9:
            return INFORMED_MISSINGNESS

        return self.generic_missingness(field)

    def _missingness_delsev(self) -> Optional[int]:
        """Handles missingness for DELSEV."""
        return self.__handle_xsev_gate("del", "delsev")

    def _missingness_hallsev(self) -> Optional[int]:
        """Handles missingness for HALLSEV."""
        return self.__handle_xsev_gate("hall", "hallsev")

    def _missingness_agitsev(self) -> Optional[int]:
        """Handles missingness for AGITSEV."""
        return self.__handle_xsev_gate("agit", "agitsev")

    def _missingness_depdsev(self) -> Optional[int]:
        """Handles missingness for DEPDSEV."""
        return self.__handle_xsev_gate("depd", "depdsev")

    def _missingness_anxsev(self) -> Optional[int]:
        """Handles missingness for ANXSEV."""
        return self.__handle_xsev_gate("anx", "anxsev")

    def _missingness_elatsev(self) -> Optional[int]:
        """Handles missingness for ELATSEV."""
        return self.__handle_xsev_gate("elat", "elatsev")

    def _missingness_apasev(self) -> Optional[int]:
        """Handles missingness for APASEV."""
        return self.__handle_xsev_gate("apa", "apasev")

    def _missingness_disnsev(self) -> Optional[int]:
        """Handles missingness for DISNSEV."""
        return self.__handle_xsev_gate("disn", "disnsev")

    def _missingness_irrsev(self) -> Optional[int]:
        """Handles missingness for IRRSEV."""
        return self.__handle_xsev_gate("irr", "irrsev")

    def _missingness_motsev(self) -> Optional[int]:
        """Handles missingness for MOTSEV."""
        return self.__handle_xsev_gate("mot", "motsev")

    def _missingness_nitesev(self) -> Optional[int]:
        """Handles missingness for NITESEV."""
        return self.__handle_xsev_gate("nite", "nitesev")

    def _missingness_appsev(self) -> Optional[int]:
        """Handles missingness for APPSEV."""
        return self.__handle_xsev_gate("app", "appsev")
