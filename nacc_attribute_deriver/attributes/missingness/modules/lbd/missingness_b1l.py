"""Class to handle LBD B1l missingness values.

Mainly done for the 777 (provided at previous visit) values.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class LBDFormB1lMissingness(FormMissingnessCollection):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table=table)

        # to grab the last time a variable was ever set,
        # not necessarily previous form
        self.__working = WorkingNamespace(table=table)

    def __handle_lbd_age_prev_value(self, field: str) -> int:
        """Same situation as B9."""
        return self.handle_prev_visit(field, int, prev_code=777, working=self.__working)

    def _missingness_lbpsyage(self) -> Optional[int]:
        """Captures LBPSYAGE."""
        return self.__handle_lbd_age_prev_value("lbpsyage")

    def _missingness_lbsagerm(self) -> Optional[int]:
        """Captures LBSAGERM."""
        return self.__handle_lbd_age_prev_value("lbsagerm")

    def _missingness_lbsagesm(self) -> Optional[int]:
        """Captures LBSAGESM."""
        return self.__handle_lbd_age_prev_value("lbsagesm")

    def _missingness_lbsagegt(self) -> Optional[int]:
        """Captures LBSAGEGT."""
        return self.__handle_lbd_age_prev_value("lbsagegt")

    def _missingness_lbsagefl(self) -> Optional[int]:
        """Captures LBSAGEFL."""
        return self.__handle_lbd_age_prev_value("lbsagefl")

    def _missingness_lbsagetr(self) -> Optional[int]:
        """Captures LBSAGETR."""
        return self.__handle_lbd_age_prev_value("lbsagetr")

    def _missingness_lbsagebr(self) -> Optional[int]:
        """Captures LBSAGEBR."""
        return self.__handle_lbd_age_prev_value("lbsagebr")
