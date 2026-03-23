"""Handles the BDS form."""

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import InvalidFieldError


class BDSFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        self.__bds = FormNamespace(table=table, required=frozenset(["module"]))

        module = self.__bds.get_required("module", str)
        if module.upper() != "BDS":
            msg = f"Current file is not a BDS form: found {module}"
            raise InvalidFieldError(msg)

        self.__working = WorkingNamespace(table=table)

    def _create_bds_naccdage(self) -> int:
        """Creates BDS NACCDAGE - age at death.

        BDS forms are designed specifically to submit an NP form,
        so we always expect an NP form, which will always provide
        an age of death.

        If an NP form is not provided, just return 999.
        """
        age_at_death = self.__working.get_cross_sectional_value("np-death-age", int)
        if not age_at_death:
            return 999

        # enforce minimum of 18
        return max(18, age_at_death)
