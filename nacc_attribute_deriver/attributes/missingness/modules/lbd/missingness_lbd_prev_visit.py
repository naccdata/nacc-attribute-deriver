"""Class to handle LBD 777 (provided at previous visit) values,
which are typically all ages.
"""

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class LBDFormPrevVisitMissingness(FormMissingnessCollection):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table=table)

        # to grab the last time a variable was ever set,
        # not necessarily previous form
        self.__working = WorkingNamespace(table=table)

    def __handle_lbd_age_prev_value(self, field: str) -> int:
        """Same situation as B9."""
        return self.handle_prev_visit(field, int, prev_code=777, working=self.__working)

    #######
    # B1l #
    #######

    def _missingness_lbpsyage(self) -> int:
        """Captures LBPSYAGE."""
        return self.__handle_lbd_age_prev_value("lbpsyage")

    def _missingness_lbsagerm(self) -> int:
        """Captures LBSAGERM."""
        return self.__handle_lbd_age_prev_value("lbsagerm")

    def _missingness_lbsagesm(self) -> int:
        """Captures LBSAGESM."""
        return self.__handle_lbd_age_prev_value("lbsagesm")

    def _missingness_lbsagegt(self) -> int:
        """Captures LBSAGEGT."""
        return self.__handle_lbd_age_prev_value("lbsagegt")

    def _missingness_lbsagefl(self) -> int:
        """Captures LBSAGEFL."""
        return self.__handle_lbd_age_prev_value("lbsagefl")

    def _missingness_lbsagetr(self) -> int:
        """Captures LBSAGETR."""
        return self.__handle_lbd_age_prev_value("lbsagetr")

    def _missingness_lbsagebr(self) -> int:
        """Captures LBSAGEBR."""
        return self.__handle_lbd_age_prev_value("lbsagebr")

    #######
    # B4l #
    #######

    def _missingness_lbdage(self) -> int:
        """Captures LBDAGE."""
        return self.__handle_lbd_age_prev_value("lbdage")

    def _missingness_lbdelage(self) -> int:
        """Captures LBDELAGE."""
        return self.__handle_lbd_age_prev_value("lbdelage")

    def _missingness_lbhalage(self) -> int:
        """Captures LBHALAGE."""
        return self.__handle_lbd_age_prev_value("lbhalage")

    def _missingness_lbanxage(self) -> int:
        """Captures LBANXAGE."""
        return self.__handle_lbd_age_prev_value("lbanxage")

    def _missingness_lbapaage(self) -> int:
        """Captures LBAPAAGE."""
        return self.__handle_lbd_age_prev_value("lbapaage")

    #######
    # B9l #
    #######

    def _missingness_sccoagen(self) -> int:
        """Captures SCCOAGEN."""
        return self.__handle_lbd_age_prev_value("sccoagen")

    def _missingness_sccoaged(self) -> int:
        """Captures SCCOAGED."""
        return self.__handle_lbd_age_prev_value("sccoaged")
