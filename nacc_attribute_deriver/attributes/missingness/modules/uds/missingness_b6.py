"""Class to handle B6-specific missingness values."""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness


class UDSFormB6Missingness(UDSMissingness):
    def _missingness_nogds(self) -> int:
        """Handle missingness for NOGDS."""
        nogds = self.uds.get_value("nogds", int)
        return nogds if nogds is not None else 0

    def __handle_nogds_gate(self, field: str) -> int:
        """Handles missingness for GDS vars."""
        nogds = self.uds.get_value("nogds", int)
        value = self.uds.get_value(field, int)

        if nogds == 1 or value is None:
            return 9

        return self.generic_missingness(field, int)

    def _missingness_satis(self) -> int:
        """Handles missingness for SATIS."""
        return self.__handle_nogds_gate("satis")

    def _missingness_dropact(self) -> int:
        """Handles missingness for DROPACT."""
        return self.__handle_nogds_gate("dropact")

    def _missingness_empty(self) -> int:
        """Handles missingness for EMPTY."""
        return self.__handle_nogds_gate("empty")

    def _missingness_bored(self) -> int:
        """Handles missingness for BORED."""
        return self.__handle_nogds_gate("bored")

    def _missingness_spirits(self) -> int:
        """Handles missingness for SPIRITS."""
        return self.__handle_nogds_gate("spirits")

    def _missingness_afraid(self) -> int:
        """Handles missingness for AFRAID."""
        return self.__handle_nogds_gate("afraid")

    def _missingness_happy(self) -> int:
        """Handles missingness for HAPPY."""
        return self.__handle_nogds_gate("happy")

    def _missingness_helpless(self) -> int:
        """Handles missingness for HELPLESS."""
        return self.__handle_nogds_gate("helpless")

    def _missingness_stayhome(self) -> int:
        """Handles missingness for STAYHOME."""
        return self.__handle_nogds_gate("stayhome")

    def _missingness_memprob(self) -> int:
        """Handles missingness for MEMPROB."""
        return self.__handle_nogds_gate("memprob")

    def _missingness_wondrful(self) -> int:
        """Handles missingness for WONDRFUL."""
        return self.__handle_nogds_gate("wondrful")

    def _missingness_wrthless(self) -> int:
        """Handles missingness for WRTHLESS."""
        return self.__handle_nogds_gate("wrthless")

    def _missingness_energy(self) -> int:
        """Handles missingness for ENERGY."""
        return self.__handle_nogds_gate("energy")

    def _missingness_hopeless(self) -> int:
        """Handles missingness for HOPELESS."""
        return self.__handle_nogds_gate("hopeless")

    def _missingness_better(self) -> int:
        """Handles missingness for BETTER."""
        return self.__handle_nogds_gate("better")
