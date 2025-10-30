"""FamilyMemberHandler helper class, primarily for form A3.

Handles calculating cognitive status of a specific family member. This
is mainly required for:

NACCFAM
NACCMOM
NACCDAD
"""
from typing import ClassVar, List, Optional

from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS


class BaseFamilyMemberHandler:
    """Class to build and get family-specific attributes.

    KID/SIB attributes need an additional index.
    """

    ALLOWED_PREFIXES: frozenset[str] = frozenset(["mom", "dad", "sib", "kid"])

    def __init__(self, prefix: str, uds: UDSNamespace) -> None:
        """Initializer."""
        if prefix not in self.ALLOWED_PREFIXES:
            raise ValueError(f"Unrecognized A3 attribute prefix: {prefix}")

        self.__prefix = prefix
        self.__uds = uds

    @property
    def prefix(self) -> str:
        return self.__prefix

    @property
    def uds(self) -> UDSNamespace:
        return self.__uds

    @property
    def formver(self) -> int:
        return self.__uds.normalized_formver()

    def is_parent(self) -> bool:
        """Returns whether or not this prefix is a parent."""
        return self.__prefix in ["mom", "dad"]

    def get_bound(self) -> int:
        """Get the upper bound based on the number of sibs/kids reported."""
        assert not self.is_parent(), "Trying to get bound on parent attribute"
        result = self.__uds.get_value(f"{self.__prefix}s", int)
        if result is not None:
            return result + 1

        return 0

    def get_parent_attribute(self, postfix: str) -> Optional[int]:
        """Build and get attribute for mom/dad."""
        assert self.is_parent(), "Trying to get a parent attribute on a SIB/KID"
        return self.__uds.get_value(f"{self.__prefix}{postfix}", int)

    def get_sib_kid_attribute(self, postfix: str, index: int) -> Optional[int]:
        """Build and get the attribute for sib/kid."""
        assert not self.is_parent(), "Trying to get SIB/KID attribute on a parent"
        return self.__uds.get_value(f"{self.__prefix}{index}{postfix}", int)


class LegacyFamilyMemberHandler(BaseFamilyMemberHandler):
    """Handles legacy family logic (V3 and earlier)."""

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
        if uds.normalized_formver() > 3:
            raise AttributeDeriverError(
                "Cannot instantiate LegacyFamilyMemberHandler for UDS form version "
                + f"{uds.normalized_formver()} (required V1-V3)")

        super().__init__(prefix, uds)

    def _dem(self, index: Optional[int] = None) -> Optional[int]:
        """Get family member demented (V2 and earlier). Grabs:

        MOMDEM, DADDEM, SIB#DEM, KID#DEM
        """
        if index is not None:
            return self.get_sib_kid_attribute("dem", index)

        return self.get_parent_attribute("dem")

    def _neur(self, index: Optional[int] = None) -> Optional[int]:
        """Get family member neurological problem (V3 and later). Grabs:

        MOMNEUR, DADNEUR, SIB#NEU, KID#NEU
        """
        if index is not None:
            return self.get_sib_kid_attribute("neu", index)

        return self.get_parent_attribute("neur")

    def _prdx(self, index: Optional[int] = None) -> Optional[int]:
        """Get family member primary diagnosis (V3 and later).

        Grabs:
        MOMPRDX, DADPRDX, SIB#PDX, KID#PDX
        """
        if index is not None:
            return self.get_sib_kid_attribute("pdx", index)

        return self.get_parent_attribute("prdx")

    def has_data(self) -> bool:
        """Return whether or not there is the necessary data to make a decision
        to begin with.

        This helps determine whether a derived variable should return 9
        (unknown) vs 0 (no).
        """
        if self.is_parent():
            return any(x is not None for x in [self._dem(), self._neur(), self._prdx()])

        num_total = self.uds.get_value(f"{self.prefix}s", int)
        if num_total is None:
            return False
        elif num_total == 0:  # if 0, not expecting any data
            return True

        if self.formver == 1:
            return self.uds.get_value(f"{self.prefix}sdem", int) is not None

        for i in range(1, self.get_bound()):
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
            if self.formver >= 3:
                return self._neur() == 1 and self._prdx() in self.DXCODES

            # V1/V2, dem
            return self._dem() == 1

        # handle sibs/kids. return True if ANY have cognitive impairment
        # in V1, each sib/kid doesn't have their own DEM value, instead
        # stored in an overall SIBSDEM or KIDSDEM variable
        if self.formver == 1:
            num_dem = self.uds.get_value(f"{self.prefix}sdem", int)
            return num_dem is not None and num_dem > 0 and num_dem < 30

        # in V2+, each sib/kid does have specific dem/neur values
        # in V2, look for SIB#DEM and KID#DEM
        # in V3+, look for SIB#NEU/SIB#PDX and KID#NEU/KID#PDX
        for i in range(1, self.get_bound()):
            # V3+, neur/pdx
            if self.formver >= 3:
                if self._neur(i) == 1 and self._prdx(i) in self.DXCODES:
                    return True
            # V1/V2, dem
            elif self._dem(i) == 1:
                return True

        return False

    def cognitive_impairment_status(self) -> int:
        """Gets the cognitive impairment status for V3 and earlier.

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
            # return 9
            return 0

        if self.is_parent():
            if self.formver == 3:
                return 0 if self._neur() is not None else 9

            return 9 if self._dem() == 9 else 0

        # in V1, each sib/kid doesn't have their own DEM value, instead
        # stored in an overall SIBSDEM or KIDSDEM variable
        if self.formver == 1:
            num_dem = self.uds.get_value(f"{self.prefix}sdem", int)
            return 9 if num_dem == 99 else 0

        # check all the kids/sibs; per RDD, if ANY are Unknown they are ALL
        # coded as Unknown (9), so leave early
        for i in range(1, self.get_bound()):
            if self._dem(i) == 9 or self._neur(i) == 9:
                return 9

        return 0

    # def check_neur_is_8(self) -> bool:
    #     """TODO: This method was added to match SAS behavior but I do not think
    #     it's correct/makes sense, hence making it its own method for easy
    #     removal in the future.

    #     But in V3, it seems if all first-degree members are coded as
    #     XNEUR == 8 (N/A, no neurological problem or psychiatric condition)
    #     then NACCFAM = 9 (Unknown), instead of 0 (No). So keep track of if
    #     everything is 8.
    #     """
    #     if self.is_parent():
    #         return self._neur() == 8

    #     for i in range(1, self.get_bound()):
    #         if self._neur(i) != 8:
    #             return False

    #     return True


class FamilyMemberHandler(BaseFamilyMemberHandler):
    """Handles current family logic (V4+)."""

    VALID_ETPR_VALUES: ClassVar[List[str]] = [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
    ]

    def __init__(self, prefix: str, uds: UDSNamespace) -> None:
        """Initializer."""
        if uds.normalized_formver() < 4:
            raise AttributeDeriverError(
                "Cannot instantiate FamilyMemberHandler for UDS form version "
                + f"{uds.normalized_formver()} (required V4+)")

        super().__init__(prefix, uds)

    def __etpr_status(self, value: str) -> Optional[int]:
        """Determine the ETPR status
        missingness values.

            If None/blank -> -4
            If 01-12 -> 1
            If 00 -> 0
        """
        if value is None or value == INFORMED_MISSINGNESS:
            return INFORMED_MISSINGNESS

        if value in self.VALID_ETPR_VALUES:
            return 1

        if value == '00':
            return 0

        # 66 should be handled before calling this method
        if value == '66':
            raise AttributeDeriverError(
                "Internal logic error: 66 should be handled for ETPR beforehand")

        return 9

    def determine_etpr_status(self,
                              index: int = None,
                              prev_record: Optional[PreviousRecordNamespace] = None) -> Optional[int]:
        """Determines the ETPR status for a family member in V4, with the
        following logic:

        IVP:
            If MEMBER_ETPR is blank, STATUS = -4
            If MEMBER_ETPR in 01-12, STATUS = 1
            If MEMBER_ETPR is 00, STATUS = 0

        FVP:
            If NWINFPAR/NWINFSIB = 0, then STATUS = STATUS[prev_vis]
            If NWINFPAR/NWINFSIB = 1 and (STATUS[prev_vis] = 1 and MEMBER_ETPR == 66)
                or MEMBER_ETPR in 01-12, then STATUS = 1
            If NWINFPAR/NWINFSIB = 1 and (STATUS[prev_vis] = 0 and MEMBER_ETPR == 66)
                or MEMBER_ETPR is 00, STATUS = 0

        Else if all above cannot be evaluated, STATUS = 9 (unknown).

        Longitudinally, the overall logic is:
            If NWINFO is 0 or ETPR == 66 (both cases only possible in FVP),
                get the status from the previous visit
            Else get the status of MEMBER_ETPR
        """
        # index is indicitive of if we're looking at a kid/sib
        if not self.is_parent() and not index:
            raise AttributeDeriverError("Need index to check SIB/KID ETPR")
        else:
            index = ""

        field = f"{self.prefix}{index}etpr"
        etpr = self.uds.get_value(field, str)
        prev_etpr = None
        if prev_record:
            prev_etpr = prev_record.get_value(field, str)

        if self.is_parent():
            nwinfo = self.uds.get_value("nwinfpar", int)
        elif self.prefix == 'sib':
            nwinfo = self.uds.get_value("nwinfsib", int)
        else:
            nwinfo = self.uds.get_value("nwinfkid", int)

        if nwinfo == 0 or etpr == '66':
            return self.__etpr_status(prev_etpr)

        return self.__etpr_status(etpr)
