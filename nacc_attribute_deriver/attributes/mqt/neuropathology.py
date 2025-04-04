"""All neuropathology MQT derived variables.

Assumes NACC-derived variables are already set
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    DerivedNamespace,
)


class NeuropathologyAttributeCollection(AttributeCollection):
    """Class to collect genetic attributes."""

    def __init__(self, table):
        self.__derived = DerivedNamespace(table)

    def _create_np_visit_to_death_interval(self) -> int:
        """Mapped from NACCINT."""
        self.__derived.assert_required(["naccint"])
        return self.__derived.get_value("naccint")

    def _create_np_b_score(self) -> int:
        """Mapped from NACCBRAA."""
        self.__derived.assert_required(["naccbraa"])
        return self.__derived.get_value("naccbraa")

    def _create_np_c_score(self) -> int:
        """Mapped from NACCNEUR."""
        self.__derived.assert_required(["naccneur"])
        return self.__derived.get_value("naccneur")

    def _create_np_microinfarcts(self) -> int:
        """Mapped from NACCMICR."""
        self.__derived.assert_required(["naccmicr"])
        return self.__derived.get_value("naccmicr")

    def _create_np_hemorrhages_and_microbleeds(self) -> Optional[int]:
        """Mapped from NACCHEM."""
        self.__derived.assert_required(["nacchem"])
        return self.__derived.get_value("nacchem")

    def _create_np_arteriolosclerosis(self) -> Optional[int]:
        """Mapped from NACCARTE."""
        self.__derived.assert_required(["naccarte"])
        return self.__derived.get_value("naccarte")

    def _create_np_lewy_pathology(self) -> Optional[int]:
        """Mapped from NACCLEWY."""
        self.__derived.assert_required(["nacclewy"])
        return self.__derived.get_value("nacclewy")
