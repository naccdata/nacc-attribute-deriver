"""Handles the DS form.

Currently just looks for existence.
"""

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import FormNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import InvalidFieldError


class DSFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        self.__ds = FormNamespace(table=table, required=frozenset(["module"]))

        module = self.__ds.get_required("module", str)
        if module.upper() != "DS":
            msg = f"Current file is not a DS form: found {module}"
            raise InvalidFieldError(msg)

    def _create_naccds(self) -> int:
        """Handles NACCDS - if this is getting called at all, assumes DS
        form."""
        return 1
