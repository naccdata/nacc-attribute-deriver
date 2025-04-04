"""All neuropathology MQT derived variables.

Assumes NACC-derived variables are already set
"""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    DerivedNamespace,
)


class NeuropathologyAttributeCollection(AttributeCollection):
    """Class to collect genetic attributes."""

    def __init__(self, table):
        self.__derived = DerivedNamespace(table)

    def _create_visit_to_death_interval(self) -> int:
        """Mapped from NACCINT."""
        self.__derived.assert_required(["naccint"])
        return self.__derived.get_value("naccint")
