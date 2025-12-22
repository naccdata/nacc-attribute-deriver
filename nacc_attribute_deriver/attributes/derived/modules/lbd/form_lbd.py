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

    ###################################################
    # Age attributes - aka those with a 777 prev code #
    ###################################################

    def __handle_age_attribute(self, field: str, prev_code: int = 777) -> Optional[int]:
        """Keep track of non-777s."""
        value = self.__lbd.get_value(field, int)
        if value == prev_code:
            return None

        return value

    #######
    # B1l #
    #######

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

    #######
    # B4l #
    #######

    def _create_lbdage(self) -> Optional[int]:
        """Captures LBDAGE."""
        return self.__handle_age_attribute("lbdage")

    def _create_lbdage2(self) -> Optional[int]:
        """Captures LBDAGE2."""
        return self.__handle_age_attribute("lbdage2")

    def _create_lbdelage(self) -> Optional[int]:
        """Captures LBDELAGE."""
        return self.__handle_age_attribute("lbdelage")

    def _create_lbhalage(self) -> Optional[int]:
        """Captures LBHALAGE."""
        return self.__handle_age_attribute("lbhalage")

    def _create_lbanxage(self) -> Optional[int]:
        """Captures LBANXAGE."""
        return self.__handle_age_attribute("lbanxage")

    def _create_lbapaage(self) -> Optional[int]:
        """Captures LBAPAAGE."""
        return self.__handle_age_attribute("lbapaage")

    #######
    # B9l #
    #######

    def _create_sccoagen(self) -> Optional[int]:
        """Captures SCCOAGEN."""
        return self.__handle_age_attribute("sccoagen")

    def _create_sccoaged(self) -> Optional[int]:
        """Captures SCCOAGED."""
        return self.__handle_age_attribute("sccoaged")
