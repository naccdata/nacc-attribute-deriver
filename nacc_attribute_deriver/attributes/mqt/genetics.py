"""All genetics MQT derived variables.

Assumes NACC-derived variables are already set
"""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    DerivedNamespace,
    RawNamespace,
)


class GeneticAttributeCollection(AttributeCollection):
    """Class to collect genetic attributes."""

    def __init__(self, table):
        self.__raw = RawNamespace(table)
        self.__derived = DerivedNamespace(table)

    def _create_apoe(self) -> int:
        """Mapped from NACCAPOE."""
        self.__derived.assert_required(["naccapoe"])
        return self.__derived.get_value("naccapoe")
