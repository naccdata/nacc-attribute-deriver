"""FamilyHandler helper class, primarily for form A3."""

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
        """Returns whether or not this prefix is a parent."""
        return self.__prefix in ["mom", "dad"]

    def get_bound(self) -> int:
        """Get the upper bound based on the number of sibs/kids reported."""
        assert not self.is_parent(), "Trying to get bound on parent attribute"
        return self.__uds.get_value(f"{self.__prefix}s", int, default=0)  # type: ignore

    def _get_parent_attribute(self, postfix: str) -> Optional[int]:
        """Build and get attribute for mom/dad."""
        assert self.is_parent(), "Trying to get a parent attribute on a SIB/KID"
        return self.__uds.get_value(f"{self.__prefix}{postfix}", int)

    def _get_sib_kid_attribute(self, postfix: str, index: int) -> Optional[int]:
        """Build and get the attribute for sib/kid."""
        assert not self.is_parent(), "Trying to get SIB/KID attribute on a parent"
        return self.__uds.get_value(f"{self.__prefix}{index}{postfix}", int)

    def _dem(self, index: Optional[int] = None) -> Optional[int]:
        """Get family member demented (V2 and earlier). Grabs:

        MOMDEM, DADDEM, SIB#DEM, KID#DEM
        """
        if index is not None:
            return self._get_sib_kid_attribute("dem", index)

        return self._get_parent_attribute("dem")

    def _neur(self, index: Optional[int] = None) -> Optional[int]:
        """Get family member neurological problem (V3 and later). Grabs:

        MOMNEUR, DADNEUR, SIB#NEU, KID#NEU
        """
        if index is not None:
            return self._get_sib_kid_attribute("neu", index)

        return self._get_parent_attribute("neur")

    def _prdx(self, index: Optional[int] = None) -> Optional[int]:
        """Get family member primary diagnosis (V3 and later).

        Grabs:
        MOMPRDX, DADPRDX, SIB#PDX, KID#PDX
        """
        if index is not None:
            return self._get_sib_kid_attribute("pdx", index)

        return self._get_parent_attribute("prdx")

    def has_data(self) -> bool:
        """Return whether or not there is the necessary data to make a decision
        to begin with.

        This helps determine whether a derived variable should return 9
        (unknown) vs 0 (no).
        """
        if self.is_parent():
            return any(x is not None for x in [self._dem(), self._neur(), self._prdx()])

        num_total = self.__uds.get_value(f"{self.__prefix}s", int)
        if num_total is None:
            return False
        elif num_total == 0:  # if 0, not expecting any data
            return True

        if self.__formver == 1:
            return self.__uds.get_value(f"{self.__prefix}sdem", int) is not None

        for i in range(1, self.get_bound() + 1):
            if any(x is not None for x in [self._dem(i), self._neur(i), self._prdx(i)]):
                return True

        return False

    def has_cognitive_impairment(self) -> bool:
        """In SAS code, creates XDEM variables (MDEM, DDEM, SDEM, KDEM), used
        to specify if the family member has cognitive impairment.

        This is primarily done by checking:
            V1/V2: xdem == 1
            V3+: xneur == 1 AND xprdx one of the primary diagnosis codes

        As far as derived variables are concerned, siblings/kids are only checked
        for NACCFAM (anyone in the family), so returns early if it holds true for
        any of them.

        Returns:
            True if they do, False otherwise
        """
        if self.is_parent():
            # V3+, neur/pdx
            if self.__formver >= 3:
                return self._neur() == 1 and self._prdx() in self.DXCODES

            # V1/V2, dem
            return self._dem() == 1

        # handle sibs/kids. return True if ANY have cognitive impairment
        # in V1, each sib/kid doesn't have their own DEM value, instead
        # stored in an overall SIBSDEM or KIDSDEM variable
        if self.__formver == 1:
            num_dem = self.__uds.get_value(f"{self.__prefix}sdem", int)
            return num_dem is not None and num_dem > 0 and num_dem < 30

        # in V2+, each sib/kid does have specific dem/neur values
        # in V2, look for SIB#DEM and KID#DEM
        # in V3+, look for SIB#NEU/SIB#PDX and KID#NEU/KID#PDX
        for i in range(1, self.get_bound() + 1):
            # V3+, neur/pdx
            if self.__formver >= 3:
                if self._neur(i) == 1 and self._prdx(i) in self.DXCODES:
                    return True
            # V1/V2, dem
            elif self._dem(i) == 1:
                return True

        return False

    def cognitive_impairment_status(self) -> int:
        """Gets the cognitive impairment status.

        In SAS, this was the XNOT variable code (MNOT, DNOT, SNOT, KNOT), but
        ended up being quite confusing, so was rewritten based on RDD
        specs and regression testing.

        Once we determine there is no cognitive impairment, we need
        to differentiate between an absolute no (0) vs an unknown (9).
        This is done by looking at whether or not the corresponding XDEM
        or XNEUR variable is 9.
            TODO: V3+ and V1/V2 behavior seem to intuitively be doing different
                things (e.g. when is 0 vs 9 returned), but coded to match
                regression tests/QAF. May want to look more into

        Returns:
            1. Has cognitive impairment
            0: No cognitive impairment, or code other than specified list
            9: Unknown
        """
        if self.has_cognitive_impairment():
            return 1

        # if no data to evaluate, return 0 (no cognitive impairment)
        if not self.has_data():
            #return 9
            return 0

        if self.is_parent():
            if self.__formver >= 3:
                return 0 if self._neur() is not None else 9

            return 9 if self._dem() == 9 else 0

        # in V1, each sib/kid doesn't have their own DEM value, instead
        # stored in an overall SIBSDEM or KIDSDEM variable
        if self.__formver == 1:
            num_dem = self.__uds.get_value(f"{self.__prefix}sdem", int)
            return 9 if num_dem == 99 else 0

        # check all the kids/sibs; per RDD, if ANY are Unknown they are ALL
        # coded as Unknown (9), so leave early
        for i in range(1, self.get_bound() + 1):
            if self._dem(i) == 9 or self._neur(i) == 9:
                return 9

        return 0
