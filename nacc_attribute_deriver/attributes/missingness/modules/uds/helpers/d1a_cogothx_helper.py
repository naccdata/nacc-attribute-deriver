"""Handles COGOTH reordering in form D1a.

See end of d1structrdd.sas for original reordering code. Essentially,
we may need to move groups of variables up, for example:

If COGOTH1 = 0, COGOTH2 = 0, but COGOTH3 = 1, then after missingness,
COGOTH1 = 1, COGOTH2 = 0, COGOTH3 = 0 (COGOTH3 moved to COGOTH1)

Since these are grouped, these variables cannot be done on a per-variable
basis the way attributes are usually handled, and will always force-resolve.
This helper does this on instantiation instead, and the missingness rules
will pull directly from the results.
"""

from typing import Optional, Type

from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    T,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.utils.errors import AttributeDeriverError

from .d1_base import UDSFormD1Missingness


class D1aCOGOTHXHelper(UDSFormD1Missingness):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table)

        # apply missingness first
        self.__attributes = {
            "cogoth": self.handle_normcog_gate("cogoth"),
            "cogoth2": self.handle_normcog_gate("cogoth2"),
            "cogoth3": self.handle_normcog_gate("cogoth3"),
            "cogothif": self.handle_normcog_with_other_gate("cogoth", "cogothif"),
            "cogoth2f": self.handle_normcog_with_other_gate("cogoth2", "cogoth2f"),
            "cogoth3f": self.handle_normcog_with_other_gate("cogoth3", "cogoth3f"),
            "cogothx": self.generic_missingness("cogothx", str),
            "cogoth2x": self.generic_missingness("cogoth2x", str),
            "cogoth3x": self.generic_missingness("cogoth3x", str),
        }

        # REGRESSION - some explicitly set to -4 if formverd1 == 1.0
        if self.uds.get_value("formverd1", float) == 1.0:
            self.__attributes.update(
                {
                    x: INFORMED_MISSINGNESS
                    for x in ["cogoth2", "cogoth2f", "cogoth3", "cogoth3f"]
                    if self.uds.get_value(x, int) is None
                }
            )

        # resolve as needed - missingness may be None
        # due to value already existing
        for key, value in self.__attributes.items():
            if value is None:
                if key.endswith("x"):
                    self.__attributes[key] = self.uds.get_value(key, str)
                else:
                    self.__attributes[key] = self.uds.get_value(key, int)

        self.__reorder()

    def get(self, field: str, attr_type: Type[T]) -> T:
        """Get the resolved value."""
        if field not in self.__attributes:
            raise AttributeDeriverError(f"Unknown COGOTHX field: {field}")

        result = self.__attributes[field]
        if not isinstance(result, attr_type):
            raise AttributeDeriverError(f"Type mismatch on resolved {field}")

        return result

    def __reorder(self) -> None:
        """May need to move COGOTHX variables up; for example,

        if COGOTH1 = 0, COGOTH2 = 0, but COGOTH3 = 1,
        then after missingness,
        COGOTH1 = 1, COGOTH2 = 0, COGOTH3 = 0
        (COGOTH3 moved to COGOTH1)
        """
        attributes = self.__attributes
        if attributes["cogoth"] == 0:
            if attributes["cogoth2"] == 1:
                attributes.update(
                    {
                        "cogoth": attributes["cogoth2"],
                        "cogothif": attributes["cogoth2f"],
                        "cogothx": attributes["cogoth2x"],
                        "cogoth2": attributes["cogoth"],
                        "cogoth2f": attributes["cogothif"],
                        "cogoth2x": attributes["cogothx"],
                    }
                )

            if attributes["cogoth3"] == 1:
                attributes.update(
                    {
                        "cogoth": attributes["cogoth3"],
                        "cogothif": attributes["cogoth3f"],
                        "cogothx": attributes["cogoth3x"],
                        "cogoth3": attributes["cogoth"],
                        "cogoth3f": attributes["cogothif"],
                        "cogoth3x": attributes["cogothx"],
                    }
                )
        if attributes["cogoth3"] == 1 and attributes["cogoth2"] != 1:
            attributes.update(
                {
                    "cogoth2": attributes["cogoth3"],
                    "cogoth2f": attributes["cogoth3f"],
                    "cogoth2x": attributes["cogoth3x"],
                    "cogoth3": attributes["cogoth2"],
                    "cogoth3f": attributes["cogoth2f"],
                    "cogoth3x": attributes["cogoth2x"],
                }
            )

        # REGRESSION: In v1, COGOTH2F and COGOTH3F really should be -4
        # but it seems the following normcog recode logic is applied anyways
        # and overrides it, so manually handle the V1 case here
        if self.formver == 1:
            default = 8 if self.normcog == 1 else INFORMED_MISSINGNESS
            attributes.update({"cogoth2f": default, "cogoth3f": default})
