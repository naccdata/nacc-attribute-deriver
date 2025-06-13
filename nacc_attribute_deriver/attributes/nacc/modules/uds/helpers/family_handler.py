"""FamilyHandler helper class, primarily for form A3.

This logic is quite confusing - need to test thoroughly.
"""

from typing import ClassVar, List, Optional

from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)


class FamilyHandler:
    """Class to build and get family-specific attributes.

    KID/SIB attributes need an additional index.
    """

    ALLOWED_PREFIXES: frozenset[str] = frozenset(["mom", "dad", "sib", "kid"])

    DXCODES: ClassVar[List[int]] = [
        40,
        41,
        42,
        43,
        44,
        50,
        70,
        80,
        100,
        110,
        120,
        130,
        131,
        132,
        133,
        140,
        150,
        170,
        230,
        240,
        260,
        310,
        320,
        400,
        410,
        420,
        421,
        422,
        430,
        431,
        433,
        434,
        435,
        436,
        439,
        440,
        450,
        490,
        999,
    ]

    def __init__(self, prefix: str, uds: UDSNamespace) -> None:
        """Initializer."""
        if prefix not in self.ALLOWED_PREFIXES:
            raise ValueError(f"Unrecognized A3 attribute prefix: {prefix}")

        self.__prefix = prefix
        self.__uds = uds
        self.__formver = self.__uds.normalized_formver()

    def is_parent(self) -> bool:
        return self.__prefix in ["mom", "dad"]

    def get_bound(self) -> int:
        assert not self.is_parent(), "Parent attributes cannot have ranges"
        return 20 if self.__prefix == "sib" else 15

    def _get_parent_attribute(self, postfix: str) -> Optional[int]:
        """Build and get attribute for mom/dad."""
        assert self.is_parent(), "Must specify index on mom/dad attribute"
        return self.__uds.get_value(f"{self.__prefix}{postfix}", int)

    def _get_sib_kid_attribute(self, postfix: str, index: int) -> Optional[int]:
        """Build and get the attribute for sib/kid."""
        assert not self.is_parent(), "Cannot specify index on a sib/kid attribute"

        return self.__uds.get_value(f"{self.__prefix}{index}{postfix}", int)

    def _dem(self, index: Optional[int] = None) -> Optional[int]:
        """Get family member demented (V2 and earlier)."""
        if index is not None:
            return self._get_sib_kid_attribute("dem", index)

        return self._get_parent_attribute("dem")

    def _neur(self, index: Optional[int] = None) -> Optional[int]:
        """Get family member neurological problem (V3 and later)."""
        if index is not None:
            return self._get_sib_kid_attribute("neu", index)

        return self._get_parent_attribute("neur")

    def _prdx(self, index: Optional[int] = None) -> Optional[int]:
        """Get family member primary diagnosis (V3 and later)."""
        if index is not None:
            return self._get_sib_kid_attribute("pdx", index)

        return self._get_parent_attribute("prdx")

    def xdem(self) -> bool:
        """Creates XDEM variables (MDEM, DDEM, SDEM, KDEM), used to compute
        other derived variables, which specifies if the family member is
        demented."""
        if self.is_parent():
            if self._dem() == 1 or (self._neur() == 1 and self._prdx() in self.DXCODES):
                return True
        else:
            for i in range(1, self.get_bound() + 1):
                if self._dem(i) == 1 or (
                    self._neur(i) == 1 and self._prdx(i) in self.DXCODES
                ):
                    return True

            # number of sibs/kids demented specified in V1, so also check
            # if we still have not determined XDEM. leave early if 9 is found
            if self.__formver == 1:
                num_dem = self.__uds.get_value(f"{self.__prefix}sdem", int)
                if num_dem is not None and num_dem > 0 and num_dem < 30:
                    return True
            elif self.__formver == 2:
                for i in range(1, self.get_bound() + 1):
                    dem_i = self._dem(i)
                    if dem_i == 1:
                        return True
                    # in SAS code this was tangled with XNOT, and if
                    # dem_i == 9 then loop would set it and break early, but I
                    # feel that doesn't make sense for XDEM? comment out
                    # for now, if it fails a bunch of regression tests
                    # then put back in
                    # elif dem_i == 9:
                    #     break

        return False

    def xnot(self) -> bool:  # noqa: C901
        """Creates XNOT variables (MNOT, DNOT, SNOT, KNOT), used to compute
        other derived variables, which specifies if the family member does NOT
        have cognitive impairment.

        If unknown (9) it seems the SAS code returns 0/False early to signifiy
        they might have cognitive impairment.
        """
        if self.__formver == 3:
            if self.is_parent():
                prdx = self._prdx()
                if self._neur() in [2, 3, 4, 5] or (prdx and prdx not in self.DXCODES):
                    return True
            else:
                result = False
                for i in range(1, self.get_bound() + 1):
                    prdx = self._prdx(i)
                    if (
                        self._neur(i) in [2, 3, 4, 5, 8]
                        or prdx and prdx not in self.DXCODES
                    ):
                        result = True
                    elif self._neur(i) == 9:
                        return False

                return result

            return False

        # assuming formver < 3 after this

        if self.is_parent():
            return self._dem() == 0

        # assuming sibs/kids after this point
        # if 0 siblings/kids, return 1; SAS code continues and theoretically
        # could get overwritten by formver-specific code but shouldn't in practice
        # so should be fine to leave early? because if there are no sibs/kids
        # the other variables can never be set
        num_total = self.__uds.get_value(f"{self.__prefix}s", int)
        if num_total == 0:
            return True
        if num_total is None:
            num_total = 0

        # number of sibs/kids demented specified in V1, so also check
        if self.__formver == 1:
            num_dem = self.__uds.get_value(f"{self.__prefix}sdem", int)
            if num_dem == 0:
                return True
            elif num_total > 0 and num_total < 30 and num_dem != 0:
                return False

        elif self.__formver == 2:
            result = False
            for i in range(1, self.get_bound() + 1):
                dem_i = self._dem(i)
                if dem_i == 9:
                    return False
                elif dem_i == 0:
                    result = True

            return result

        return False
