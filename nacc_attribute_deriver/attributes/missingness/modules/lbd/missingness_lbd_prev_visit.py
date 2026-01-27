"""Class to handle LBD 777 (provided at previous visit) values, which are
typically all ages."""

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
    UNKNOWN_CODES,
)


class LBDFormPrevVisitMissingness(FormMissingnessCollection):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table=table)

        # to grab the last time a variable was ever set,
        # not necessarily previous form
        self.__working = WorkingNamespace(table=table)

    def __handle_lbd_age_prev_value(
        self, field: str, minimum: int, maximum: int
    ) -> int:
        """Same situation as B9; also enforce ranges."""
        result = self.handle_prev_visit(
            field, int, prev_code=777, default=999, working=self.__working
        )

        if result not in UNKNOWN_CODES:
            return min(max(minimum, result), maximum)

        return result

    #######
    # B1l #
    #######

    def _missingness_lbpsyage(self) -> int:
        """Captures LBPSYAGE."""
        return self.__handle_lbd_age_prev_value("lbpsyage", 15, 110)

    def _missingness_lbsagerm(self) -> int:
        """Captures LBSAGERM."""
        return self.__handle_lbd_age_prev_value("lbsagerm", 15, 110)

    def _missingness_lbsagesm(self) -> int:
        """Captures LBSAGESM."""
        return self.__handle_lbd_age_prev_value("lbsagesm", 15, 110)

    def _missingness_lbsagegt(self) -> int:
        """Captures LBSAGEGT."""
        return self.__handle_lbd_age_prev_value("lbsagegt", 9, 110)

    def _missingness_lbsagefl(self) -> int:
        """Captures LBSAGEFL."""
        return self.__handle_lbd_age_prev_value("lbsagefl", 9, 110)

    def _missingness_lbsagetr(self) -> int:
        """Captures LBSAGETR."""
        return self.__handle_lbd_age_prev_value("lbsagetr", 9, 110)

    def _missingness_lbsagebr(self) -> int:
        """Captures LBSAGEBR."""
        return self.__handle_lbd_age_prev_value("lbsagebr", 9, 110)

    def _missingness_lbspsym(self) -> int:
        """Captures LBSPSYM."""
        result = self.handle_prev_visit(
            "lbspsym", int, prev_code=0, working=self.__working
        )
        return result if result != 0 else INFORMED_MISSINGNESS

    #######
    # B4l #
    #######

    def _missingness_lbdage(self) -> int:
        """Captures LBDAGE."""
        return self.__handle_lbd_age_prev_value("lbdage", 15, 110)

    def _missingness_lbdage2(self) -> int:
        """Captures LBDAGE2."""
        return self.__handle_lbd_age_prev_value("lbdage2", 15, 110)

    def _missingness_lbdelage(self) -> int:
        """Captures LBDELAGE."""
        return self.__handle_lbd_age_prev_value("lbdelage", 15, 110)

    def _missingness_lbhalage(self) -> int:
        """Captures LBHALAGE."""
        return self.__handle_lbd_age_prev_value("lbhalage", 15, 110)

    def _missingness_lbanxage(self) -> int:
        """Captures LBANXAGE."""
        return self.__handle_lbd_age_prev_value("lbanxage", 15, 110)

    def _missingness_lbapaage(self) -> int:
        """Captures LBAPAAGE."""
        return self.__handle_lbd_age_prev_value("lbapaage", 15, 110)

    #######
    # B9l #
    #######

    def _missingness_sccoagen(self) -> int:
        """Captures SCCOAGEN."""
        return self.__handle_lbd_age_prev_value("sccoagen", 15, 110)

    def _missingness_sccoaged(self) -> int:
        """Captures SCCOAGED."""
        return self.__handle_lbd_age_prev_value("sccoaged", 15, 110)

    def _missingness_sccofrst(self) -> int:
        """Captures SCCOFRST."""
        result = self.handle_prev_visit(
            "sccofrst", int, prev_code=0, working=self.__working
        )
        return result if result != 0 else INFORMED_MISSINGNESS
