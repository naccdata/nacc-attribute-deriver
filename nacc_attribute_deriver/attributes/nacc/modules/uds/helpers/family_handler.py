"""FamilyHandler helper class, primarily for form A3.

Handles calculating cognitive status across an entire family. This is
mainly required for NACCFAM, which is significantly involved.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS

from .family_member_handler import (
    BaseFamilyMemberHandler,
    FamilyMemberHandler,
    LegacyFamilyMemberHandler,
)


class BaseFamiylHandler(ABC):
    """Handles cognitive status across an entire family."""

    def __init__(self,
                 uds: UDSNamespace,
                 prev_record: Optional[PreviousRecordNamespace] = None) -> None:
        """Initializer."""
        self.uds = uds
        self.prev_record = prev_record

        member_handler = FamilyMemberHandler
        if self.uds.normalized_formver() < 4:
            member_handler = LegacyFamilyMemberHandler

        self.__mom = member_handler("mom", uds)
        self.__dad = member_handler("dad", uds)
        self.__sibs = member_handler("sib", uds)
        self.__kids = member_handler("kid", uds)

        self.__all_members = [
            self.__mom,
            self.__dad,
            self.__sibs,
            self.__kids,
        ]

    @property
    def mom(self) -> BaseFamilyMemberHandler:
        return self.__mom

    @property
    def dad(self) -> BaseFamilyMemberHandler:
        return self.__dad

    @property
    def sibs(self) -> BaseFamilyMemberHandler:
        return self.__sibs

    @property
    def kids(self) -> BaseFamilyMemberHandler:
        return self.__kids

    @property
    def all_members(self) -> List[BaseFamilyMemberHandler]:
        return self.__all_members

    @abstractmethod
    def determine_naccparent(self,
                             member: BaseFamilyMemberHandler,
                             known_value: int) -> int:
        """Determines NACCMOM and NACCDAD.

        Args:
            member: the family member (mom or dad)
            known_value: the known derived value (value of NACCMOM or NACCDAD
                based on the curation thus far)
        """
        pass

    @abstractmethod
    def determine_naccfam(self, known_value: int) -> int:
        """Determines NACCFAM.

        Args:
            knwon_value: The known derived value (value of NACCFAM based on
                the curation thus far)
        """
        pass



class LegacyFamilyHandler(BaseFamiylHandler):
    """Handles cognitive status across an entire family for V1-V3."""

    def __init__(self,
                 uds: UDSNamespace,
                 prev_record: Optional[PreviousRecordNamespace] = None) -> None:
        """Initializer."""
        if uds.normalized_formver() > 3:
            raise AttributeDeriverError(
                "Cannot instantiate LegacyFamilyHandler for UDS form version "
                + f"{uds.normalized_formver()} (required V1-V3)")

        super().__init__(uds, prev_record)

    def determine_naccparent(self,
                             member: BaseFamiylHandler,
                             known_value: int,) -> int:
        """Determine NACCPARENT (NACCMOM or NACCDAD).

        TODO: currently doesn't use prev record since it's based off the legacy
            SAS code, but probably should - would likely help with the confusion
        """
        # if reported 1 at any visit, stays as 1
        if known_value == 1:
            return 1

        # if no data, per RDD: "Known cognitive impairment history
        # reported at any visit supersedes all visits with missing codes"
        # and
        # "Those with submitted Form A3 who are missing necessary data are
        # coded as Unknown (9)", which known_value might be by default
        if not member.has_data():
            return known_value

        # otherwise, check cognitive impairment status
        return member.cognitive_impairment_status()

    def determine_naccfam(self, known_value: int) -> int:
        """Determine V1-V3 NACCFAM."""
        # If known value is already 1, stays at 1
        if known_value == 1:
            return 1

        # if all have no data, then fallback to known value
        if all(not member.has_data() for member in self.all_members):
            return known_value

        # if V3 and all 8, return 9
        # TODO - I really don't think this is the correct behavior;
        # see comments under check_neur_is_8
        # if self.formver >= 3:
        #     all_8s = [member.check_neur_is_8() for member in self.all_members]
        #     if all(all_8s):
        #         return 9

        # get cognitive status for each family member
        family_status = [
            member.cognitive_impairment_status() for member in self.all_members
        ]
        if any(status == 1 for status in family_status):
            return 1

        # from RDD: "Those who are missing data on all first-degree
        # family members are coded as Unknown (9). If some first-degree
        # family members are coded as No and some are coded as Unknown,
        # then they are all coded as Unknown (9)"
        return 9 if any(status == 9 for status in family_status) else 0


class FamilyHandler(BaseFamiylHandler):
    """Handles cognitive status across an entire family for V4+."""

    def __init__(self,
                 uds: UDSNamespace,
                 prev_record: Optional[PreviousRecordNamespace] = None) -> None:
        """Initializer."""
        if uds.normalized_formver() < 4:
            raise AttributeDeriverError(
                "Cannot instantiate FamilyHandler for UDS form version "
                + f"{uds.normalized_formver()} (required V4+)")

        super().__init__(uds, prev_record)

    def determine_naccparent(self,
                             member: BaseFamiylHandler,
                             known_value: int) -> int:
        """Determine NACCPARENT (NACCMOM or NACCDAD)."""
        # if reported 1 at any visit, stays as 1
        if known_value == 1:
            return 1

        result = member.determine_etpr_status(prev_record=self.prev_record)
        if result in [INFORMED_MISSINGNESS, 9] and known_value in [0, 1]:
            return known_value

        return result

    def __determine_parent_status(self) -> int:
        """Determine the parent status by looking at MOMETPR and DADETPR.

        This  looks at the same code determine_etpr_status() that is
        used to determine NACCMOM and NACCDAD, and resolves the two.
        """
        mometpr = self.mom.determine_etpr_status()
        dadetpr = self.dad.determine_etpr_status()
        parents = None

        if mometpr == 1 or dadetpr == 1:
            return 1
        if mometpr == 0 and dadetpr == 0:
            return 0

        return INFORMED_MISSINGNESS

    def __determine_sibs_kids_status(self, member: FamilyMemberHandler):
        """Determine the SIBS/KIDS status.

        Checks the ETPR status for all relevant sibs/kids, and resolves
        the results across all of them.
        """
        results = []

        for i in range(1, member.get_bound()):
            results.append(member.determine_etpr_status(
                index=i, prev_record=self.prev_record))

        if all(x is None for x in results):
            return INFORMED_MISSINGNESS

        if any(x == 1 for x in results):
            return 1

        if all(x == 0 for x in results):
            return 0

        return 9

    def determine_naccfam(self, known_value: int) -> int:
        """Determine NACCFAM for V4+."""
        # If known value is already 1, stays at 1
        if known_value == 1:
            return 1

        family_status = [
            self.__determine_parent_status(),
            self.__determine_sibs_kids_status(self.__sibs),
            self.__determine_sibs_kids_status(self.__kids)
        ]

        if all(x == -4 for x in family_status):
            return INFORMED_MISSINGNESS

        if any(x == 1 for x in family_status):
            return 1

        if all(x == 0 for x in family_status):
            return 0

        return 9
