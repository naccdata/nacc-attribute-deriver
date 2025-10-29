"""FamilyHandler helper class, primarily for form A3.

Handles calculating cognitive status across an entire family. This is
mainly required for NACCFAM, which is significantly involved.
"""
from abc import ABC, abstractmethod
from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)

from .helpers.family_member_handler import (
    BaseFamilyMemberHandler,
    FamilyMemberHandler,
    LegacyFamilyMemberHandler,
)


class BaseFamiylHandler(ABC):
    """Handles cognitive status across an entire family."""

    def __init__(self, uds: UDSNamespace) -> None:
        """Initializer."""
        self.uds = uds

        member_handler = FamilyMemberHandler
        if self.uds.normalized_formver() < 4:
            member_handler = LegacyFamilyMemberHandler

        self.__mom = member_handler("mom", self.uds)
        self.__dad = member_handler("dad", self.uds)
        self.__sibs = member_handler("sib", self.uds)
        self.__kids = member_handler("kid", self.uds)

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

    @abstractmethod
    def determine_naccfam(self, known_value: int) -> int:
        """Determines NACCFAM."""
        pass


class LegacyFamilyHandler(BaseFamiylHandler):
    """Handles cognitive status across an entire family for V1-V3."""

    def __init__(self, uds: UDSNamespace) -> None:
        """Initializer."""
        if uds.normalized_formver() > 3:
            raise AttributeDeriverError(
                "Cannot instantiate LegacyFamilyHandler for UDS form version "
                + f"{uds.normalized_formver()} (required V1-V3)")

        super().__init__(uds)

    def determine_naccfam(self, known_value: int) -> int:
        """Determine V1-V3 NACCFAM."""
        # If known value is already 1, stays at 1
        if known_value == 1:
            return 1

        # if all have no data, then fallback to known value
        if all(not member.has_data() for member in self.__family):
            return known_value

        # if V3 and all 8, return 9
        # TODO - I really don't think this is the correct behavior;
        # see comments under check_neur_is_8
        # if self.formver >= 3:
        #     all_8s = [member.check_neur_is_8() for member in self.__family]
        #     if all(all_8s):
        #         return 9

        # get cognitive status for each family member
        family_status = [
            member.cognitive_impairment_status() for member in self.__family
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

    def __init__(self, uds: UDSNamespace) -> None:
        """Initializer."""
        if uds.normalized_formver() < 4:
            raise AttributeDeriverError(
                "Cannot instantiate FamilyHandler for UDS form version "
                + f"{uds.normalized_formver()} (required V4+)")

        super().__init__(uds)

    def determine_naccfam(self, known_value: int = 1) -> int:
        """Determine NACCFAM for V4+."""
        # If known value is already 1, stays at 1
        if known_value == 1:
            return 1

        