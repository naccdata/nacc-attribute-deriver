"""CSF-specific derived variables."""

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    RawNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class CSFAttributeCollection(AttributeCollection):
    """Class to collect historical NCRAD APOE attributes."""

    def __init__(self, table: SymbolTable) -> None:
        """Override initializer to set prefix to NCRAD-specific data."""
        self.__csf = RawNamespace(table)

    def __concentration_within_range(
        self, field: str, min_value: float, max_value: float
    ) -> int:
        """Returns whether the given concentration field is within the
        specified range."""
        value = self.__csf.get_value(field, float)
        if not value:
            return 0

        if value >= min_value and value <= max_value:
            return 1

        return 0

    def _create_naccacsf(self) -> int:
        """Creates NACCACSF: One or more measures of Abeta1-42 reported."""
        return self.__concentration_within_range("csfabeta", 1, 3200)

    def _create_naccpcsf(self) -> int:
        """Creates NACCPCSF: One or more measures of P-tau181P reported."""
        return self.__concentration_within_range("csfptau", 1, 500)

    def _create_nacctcsf(self) -> int:
        """Creates NACCTCSF: One or more measures of T-tau reported."""
        return self.__concentration_within_range("csfttau", 1, 2500)
