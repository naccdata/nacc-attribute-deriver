"""Handles the LBD form.

Currently just looks for existence.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import FormNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import InvalidFieldError


class LBDFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        self.__lbd = FormNamespace(table=table, required=frozenset(["module"]))

        module = self.__lbd.get_required("module", str)
        if module.upper() != "LBD":
            msg = f"Current file is not a LBD form: found {module}"
            raise InvalidFieldError(msg)

    def _create_nacclbdm(self) -> int:
        """Handles NACCLBDM - if this is getting called at all,
        assumes LBD form."""
        return 1

    def __handle_age_attribute(self, field: str, prev_code: int = 777) -> Optional[int]:
        """REGRESSION: It looks like the LBD/FTLD QAF does not handle 777?
        Like it stays as 777. So exact behavior is undefined. For now, just
        keep track of non-777s."""
        value = self.__lbd.get_value(field, int)
        if value == prev_code:
            return None

        if prev_code == 777:
            return None

        return value

    def _create_lbpsyage(self) -> Optional[int]:
        """Captures LBPSYAGE."""
        return self.__handle_age_attribute("lbpsyage")

    def _create_lbsagerm(self) -> Optional[int]:
        """Captures LBSAGERM."""
        return self.__handle_age_attribute("lbsagerm")

    def _create_lbsagesm(self) -> Optional[int]:
        """Captures LBSAGESM."""
        return self.__handle_age_attribute("lbsagesm")

    def _create_lbsagegt(self) -> Optional[int]:
        """Captures LBSAGEGT."""
        return self.__handle_age_attribute("lbsagegt")

    def _create_lbsagefl(self) -> Optional[int]:
        """Captures LBSAGEFL."""
        return self.__handle_age_attribute("lbsagefl")

    def _create_lbsagetr(self) -> Optional[int]:
        """Captures LBSAGETR."""
        return self.__handle_age_attribute("lbsagetr")

    def _create_lbsagebr(self) -> Optional[int]:
        """Captures LBSAGEBR."""
        return self.__handle_age_attribute("lbsagebr")
