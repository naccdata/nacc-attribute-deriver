"""Handles the FTLD form.

Currently just looks for existence.
"""

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import FormNamespace
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable


class FTLDFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        self.__ftld = FormNamespace(table=table, required=frozenset(["module"]))

        module = self.__ftld.get_required("module", str)
        if module.upper() != "FTLD":
            msg = f"Current file is not a FTLD form: found {module}"
            raise InvalidFieldError(msg)

    def _create_naccftd(self) -> int:
        """Handles NACCFTD - if this is getting called at all,
        assumes FTLD form."""
        return 1
