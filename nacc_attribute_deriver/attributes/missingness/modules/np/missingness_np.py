"""Class to handle NP form missingness values.

See derivenp.sas. There is a lot of recode logic but I think just using
general missingness resolves most of them since they boil down to "if
the variable doesn't exist in this version, set to -4".
"""

from typing import Optional, Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.symbol_table import SymbolTable


class NPMissingness(FormMissingnessCollection):
    """Class to handle NP missingness values."""

    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table, required=frozenset(["formver"]))
        self.formver = self.form.get_required("formver", int)

    def _missingness_np(self, field: str, attr_type: Type[T]) -> Optional[T]:
        """Defines general missingness for NP;

        -4 / 4.4 / blank if missing.
        """
        return self.generic_missingness(field, attr_type)

    ####################################
    # Form version-dependent variables #
    ####################################

    def _missingness_nppatho(self) -> Optional[int]:
        """Handles missingness for NPPATHO."""
        nppath = self.form.get_value("nppath", int)
        if self.formver in [10, 11] and nppath == 0:
            return 0

        return self.generic_missingness("nppatho", int)
