"""Handles the CLS form."""

from typing import List, Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import FormNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import InvalidFieldError


class CLSFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        self.__cls = FormNamespace(
            table=table, required=frozenset(["formver", "module"])
        )

        module = self.__cls.get_required("module", str)
        if module.upper() != "CLS":
            msg = f"Current file is not a CLS form: found {module}"
            raise InvalidFieldError(msg)

    def calculate_proficiency(self, attributes: List[str]) -> Optional[float]:
        """Calculates proficiency given the list of attributes.

        Args:
            attributes: Attributes to add up - assumes all integers.
        Returns:
            The average, if all attributes are defined, rounded to the nearest
            0.1
        """
        all_fields = [self.__cls.get_value(x, int) for x in attributes]
        if any(x is None for x in all_fields):
            return None

        return round(sum(all_fields) / len(all_fields), 1)  # type: ignore

    def _create_naccengl(self) -> Optional[float]:
        """Creates NACCENGL - average English level."""
        return self.calculate_proficiency(
            ["aspkengl", "areaengl", "awriengl", "aundengl"]
        )

    def _create_naccspnl(self) -> Optional[float]:
        """Creates NACCSPNL - average Spanish level."""
        return self.calculate_proficiency(
            ["aspkspan", "areaspan", "awrispan", "aundspan"]
        )
