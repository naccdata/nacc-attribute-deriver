"""Helper methods for NP derived variables."""

from typing import Optional

from nacc_attribute_deriver.attributes.base.namespace import (
    FormNamespace,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError


class NPMapper:
    """Class to define static mapping functions."""

    def __init__(self, np: FormNamespace):
        """Initializer; assumes np is correct form."""
        self.__np = np
        self.formver = self.__np.get_required("formver", int)

    def map_gross(self, new: int | None) -> Optional[int]:
        npgross = self.__np.get_value("npgross", int)
        if npgross == 2:
            return 0
        if npgross == 9:
            return 9

        return new

    def map_sub4(self, old: int | None) -> int:
        if old in [1, 2, 3, 4]:
            return 4 - old
        if old == 5:
            return 8

        return 9

    def map_v9(self, old: int | None) -> int:
        if old == 1:
            return 1
        if old == 2:
            return 0
        if old == 3:
            return 8

        return 9

    def map_vasc(self, new: int | None) -> Optional[int]:
        npgross = self.__np.get_value("npgross", int)
        npvasc = self.__np.get_value("npvasc", int)
        if npgross == 2 or npvasc == 2:
            return 0
        if npgross == 9 or npvasc == 9:
            return 9
        if npvasc == 3:
            return 8

        return new

    def map_sub1(self, old: int | None):
        if old in [1, 2, 3, 4]:
            return old - 1
        if old == 5:
            return 8

        return 9

    def map_lewy(self) -> int:
        nplewy = self.__np.get_value("nplewy", int)
        if nplewy == 6:
            return 8
        if nplewy == 5:
            return 0
        if nplewy is not None:
            return nplewy

        return 9

    def map_v10(self, old: int | None, gateway: int | None) -> Optional[int]:
        if old is not None:
            return old

        if gateway in [8, 9]:
            return gateway
        if gateway == 0:
            return None

        return 9

    def map_comb2(self, old1: int | None, old2: int | None) -> int:
        """Combine two variables to create new one."""
        if old1 == 1 or old2 == 1:
            return 1
        if old1 == 2 or old2 == 2:
            return 0
        if old1 == 3 or old2 == 3:
            return 8

        return 9

    def banked_v9(self, old: int | None) -> Optional[int]:
        """Banked specimens."""
        if self.formver > 9:
            raise AttributeDeriverError("banked_v9 not valid for formver > 9")

        # -4 case in SAS, treat as None in new system
        if self.formver in [1, 7] and old is None:
            return None

        if old in [0, 2]:
            return 0
        if old == 1:
            return 1

        return 9
