"""FamilyHandler helper class, primarily for form A3.

Handles calculating cognitive status across an entire family, namely

NACCMOM
NACCDAD
NACCFAM

NOTE: In older versions (V3 and earlier), it was originally intended that
if any of these variables were set to 1, it always stayed as 1. The behavior
of when it was 9 (unknown) on the other hand was a lot messier and seemed
inconsistent between versions.

GOING FORWARD, for V4 AND with changes to legacy code, we have decided that it
can switch between a 0 and a 1 (so always following the newest entry, especially
if the previous one was a mistake), but a 9 cannot "override" a 0 or 1 if it
already exists. While this will cause different output regarding older data in
the QAFs, enforcing this across all versions should hopefully help stabalize
the previous inconsistencies.
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


    def determine_single_status(self, status: int, known_value: int) -> int:
        """See note at top. Determines status for a single member. Only
        override if derived status is 0 or 1, or known value is not already a 0 or 1.
        """
        if (status in [0, 1]) or (known_value not in [0, 1]):
            return status

        # means known_value is 0 or 1, so return that instead
        return known_value

    def determine_group_status(self, all_statuses: List[int], known_value: int) -> int:
        """See note at top. Determines status across an entire group. Only
        override if derived status is 0 or 1, or known value is not already a 0 or 1.
        """
        if any(x == 1 for x in all_statuses):
            return 1

        if all(x == 0 for x in all_statuses):
            return 0

        status = 9
        if all(x == -4 for x in all_statuses):
            status = INFORMED_MISSINGNESS

        return self.determine_single_status(status, known_value)


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
                             known_value: int) -> int:
        """Determine V1-V3 NACCPARENT (NACCMOM or NACCDAD).

        TODO: currently doesn't use prev record since it's based off the legacy
            SAS code, but probably should - would likely help with the confusion
        """
        # if no data, fallback to known value
        if not member.has_data():
            return known_value

        # otherwise, check cognitive impairment status
        status = member.cognitive_impairment_status()
        return self.determine_single_status(status, known_value)

    def determine_naccfam(self, known_value: int) -> int:
        """Determine V1-V3 NACCFAM."""

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
        return self.determine_group_status(family_status, known_value)


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

        status = member.determine_etpr_status(prev_record=self.prev_record)
        return self.determine_single_status(status, known_value)

    def __determine_parent_status(self) -> int:
        """Determine the parent status by looking at MOMETPR and DADETPR.
        """
        mometpr = self.mom.determine_etpr_status()
        dadetpr = self.dad.determine_etpr_status()
        return self.determine_group_status([mometpr, dadetpr], known_value)

    def __determine_sibs_kids_status(self, member: FamilyMemberHandler):
        """Determine the SIBS/KIDS status.

        Checks the ETPR status for all relevant sibs/kids, and resolves
        the results across all of them.
        """
        group_status = [
            member.determine_etpr_status(index=i, prev_record=self.prev_record)
            for i in range(1, member.get_bound())
        ]

        self.determine_group_status(group_status, known_value=None)

    def determine_naccfam(self, known_value: int) -> int:
        """Determine NACCFAM for V4+."""
        family_status = [
            self.__determine_parent_status(),
            self.__determine_sibs_kids_status(self.__sibs),
            self.__determine_sibs_kids_status(self.__kids)
        ]

        return self.determine_group_status(family_status, known_value)
