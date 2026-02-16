"""Class to handle B1-specific missingness values.

Only in V3 and earlier.
"""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
    UNKNOWN_CODES,
)


class UDSFormB1Missingness(UDSMissingness):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table=table)

        # needed to get B1a variables
        self.__working = WorkingNamespace(table=table)
        self.__visitdate = self.uds.get_required("visitdate", str)

    def _missingness_height(self) -> float:
        """Handle missingness for HEIGHT. May need to add the decimal in legacy
        versions.

        Min 36 UDSv3+, max is 87.9, UDSv2 and earlier max is 96.0
        """
        height = self.uds.get_value("height", float)
        if height is None:
            return INFORMED_MISSINGNESS

        if height in [88, 88.8, 99, 99.9]:
            return 88.8

        heigdec = self.uds.get_value("heigdec", float)
        if heigdec is not None and heigdec != 0:
            height_with_dec = height + heigdec / 10
            if height != height_with_dec:
                height = height_with_dec

        return min(max(36.0, height), 87.9)

    #################################################
    # LEGACY 999 to 888 changes + range enforcement #
    #################################################

    def __handle_b1_ranges(
        self, field: str, minimum: int, maximum: int, from_b1a: bool = False
    ) -> int:
        """Handles the 999 to 888 change - see
        b1structrdd.sas. Also enforce min/max as needed.
        """
        value: int | None = None

        # if can come from separate b1a form, check that first
        if self.formver == 3 and from_b1a:
            value = self.__working.get_corresponding_longitudinal_value(
                self.__visitdate, field, int
            )

        if not value:
            value = self.generic_missingness(field, int)

        # Cannot be 999 in V4, so seems okay to not gate based
        # on version
        if value == 999:
            return 888

        if value not in UNKNOWN_CODES:
            # enforce specified range
            return min(max(minimum, value), maximum)

        return value

    def _missingness_weight(self) -> int:
        """Handles missingness for WEIGHT."""
        return self.__handle_b1_ranges("weight", 50, 400)

    def _missingness_bpsys(self) -> int:
        """Handles missingness for BPSYS."""
        return self.__handle_b1_ranges("bpsys", 70, 230)

    def _missingness_bpdias(self) -> int:
        """Handles missingness for BPDIAS."""
        return self.__handle_b1_ranges("bpdias", 30, 140)

    def _missingness_hrate(self) -> int:
        """Handles missingness for HRATE."""
        return self.__handle_b1_ranges("hrate", 33, 160)

    def _missingness_bpsysl(self) -> int:
        """Handles missingness for BPSYSL."""
        return self.__handle_b1_ranges("bpsysl", 70, 230, from_b1a=True)

    def _missingness_bpsysr(self) -> int:
        """Handles missingness for BPSYSR."""
        return self.__handle_b1_ranges("bpsysr", 70, 230, from_b1a=True)

    def _missingness_bpdiasl(self) -> int:
        """Handles missingness for BPDIASL."""
        return self.__handle_b1_ranges("bpdiasl", 30, 140, from_b1a=True)

    def _missingness_bpdiasr(self) -> int:
        """Handles missingness for BPDIASR."""
        return self.__handle_b1_ranges("bpdiasr", 30, 140, from_b1a=True)

    def _missingness_bpdevice(self) -> int:
        """Handles missingness for BPDEVICE."""
        if self.formver == 3:
            value = self.__working.get_corresponding_longitudinal_value(
                self.__visitdate, "bpdevice", int
            )
            if value is not None:
                return value

        return self.generic_missingness("bpdevice", int)

    ####################
    # LEGACY with gate #
    ####################

    def __handle_b1_with_gate(self, gate: str, field: str) -> int:
        """Handles B1 missingness with a gate."""
        gate_value = self.uds.get_value(gate, int)
        if gate_value == 0:
            return 8
        if gate_value == 9:
            return INFORMED_MISSINGNESS

        return self.generic_missingness(field, int)

    def _missingness_viswcorr(self) -> int:
        """Handles missingness for VISWCORR.

        Only in V3 and earlier - see b1structrdd.sas
        """
        return self.__handle_b1_with_gate("viscorr", "viswcorr")

    def _missingness_hearwaid(self) -> int:
        """Handles missingness for HEARWAID.

        Only in V3 and earlier - see b1structrdd.sas
        """
        return self.__handle_b1_with_gate("hearaid", "hearwaid")
