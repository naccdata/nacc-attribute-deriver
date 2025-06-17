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
        if self.__prefix == 'sib':
            return self.__uds.get_value('sibs', int, default=0)

        return self.__uds.get_value('kids', int, default=0)

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

    def has_data(self) -> bool:
        """Return whether or not there is data to make a decision to begin
        with."""
        if self.is_parent():
            return any(x is not None for x in [self._dem(), self._neur(), self._prdx()])

        for i in range(1, self.get_bound() + 1):
            if any(x is not None for x in [self._dem(i), self._neur(i), self._prdx(i)]):
                return True

        return False

    def has_cognitive_impairment(self) -> bool:
        """In SAS code, creates XDEM variables (MDEM, DDEM, SDEM, KDEM), used to
        specify if the family member has cognitive impairment.

        This is primarily done by checking xdem (< v3) and xneur (v3+)

        Returns:
            True if they do, False otherwise
        """
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

        return False

    def cognitive_impairment_status(self) -> int:  # noqa: C901
        """In SAS code, creates XNOT variables (MNOT, DNOT, SNOT, KNOT), used to
        specify that the family member does NOT have cognitive impairment.

        This ended up being written quite differently from the SAS code, but
        did start from it, so logic may still be a bit unintuitive.

        Returns:
            1. Has cognitive impairment
            0: No cognitive impairment, or code other than specified list
            9: Unknown
        """
        if self.has_cognitive_impairment():
            return 1

        # if no data to evaluate, return Unknown (9)
        if not self.has_data():
            return 9

        if self.is_parent():
            return 9 if self._neur() == 9 else 0

        # check all the kids/sibs; per RDD, if ANY are Unknown they are ALL
        # coded as Unknown (9), so leave early
        for i in range(1, self.get_bound() + 1):
            if self._neur(i) == 9:
                return 9

        return 0
