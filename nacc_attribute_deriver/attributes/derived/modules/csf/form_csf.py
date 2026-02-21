"""CSF-specific derived variables."""

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import InvalidFieldError


class CSFAttributeCollection(AttributeCollection):
    """Class to collect historical NCRAD APOE attributes."""

    def __init__(self, table: SymbolTable) -> None:
        """Override initializer to set prefix to NCRAD-specific data."""
        self.__csf = FormNamespace(table=table, required=frozenset(["module"]))

        # need to check if set by another form
        self.__subject_derived = SubjectDerivedNamespace(table=table)

        module = self.__csf.get_required("module", str)
        if module.upper() != "CSF":
            msg = f"Current file is not a CSF form: found {module}"
            raise InvalidFieldError(msg)

    def __check_concentration(self, field: str, derived_field: str) -> int:
        """Returns 1 if concentration is vavlid, 0 otherwise.

        REGRESSION: this used to check within a specific range, but it is
            not guaranteed the user enters a value within that range.
            Missingness logic will enforce the actual values, so for the
            derived variables just check that it's there and not < 1.
        """
        # if already set to 1, return that
        if self.__subject_derived.get_cross_sectional_value(derived_field, int) == 1:
            return 1

        value = self.__csf.get_value(field, float)
        if value is None or value < 1:
            return 0

        return 1

    def _create_naccacsf(self) -> int:
        """Creates NACCACSF: One or more measures of Abeta1-42 reported."""
        return self.__check_concentration("csfabeta", "naccacsf")

    def _create_naccpcsf(self) -> int:
        """Creates NACCPCSF: One or more measures of P-tau181P reported."""
        return self.__check_concentration("csfptau", "naccpcsf")

    def _create_nacctcsf(self) -> int:
        """Creates NACCTCSF: One or more measures of T-tau reported."""
        return self.__check_concentration("csfttau", "nacctcsf")
