"""Derived variables from form B1: Physical.

Form B1 is optional, so may not have been submitted.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormB1Attribute(AttributeCollection):
    """Class to collect UDS B1 attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)
        self.__formver = self.__uds.get_normalized_formver()
        self.__submitted = self.__uds.get_value("b1sub", int) == 1

    def get_height(self) -> Optional[float]:
        """Get height; may need to add decimal.

        Min 36
        UDSv3+, max is 87.9, UDSv2 and earlier max is 96.0
        """
        height = self.__uds.get_value('height', float)

        if (height is None or
            height == 99 or
            (self.__formver == 3 and height == 88)):
            return None

        heigdec = self.__uds.get_value('heigdec', float)
        if heigdec is not None and heigdec != 0:
            height += (heigdec / 10)

        return None if height < 36 else height

    def get_weight(self) -> Optional[int]:
        """Get weight; min 50, max 400"""
        weight = self.__uds.get_value('weight', int)
        if weight is None or weight < 50 or weight > 400:
            return None

        return weight

    def _create_naccbmi(self) -> Optional[float]:
        """Creates NACCBMI (body max index)."""
        if not self.__submitted:
            return None

        height = self.get_height()
        weight = self.get_weight()

        if height is not None and weight is not None:
            naccbmi = (weight * 703) / (height * height)
            return round(naccbmi, 1)

        return 888.8
