"""Handles the LBD form.

Currently just looks for existence.
"""

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import FormNamespace
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable


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
