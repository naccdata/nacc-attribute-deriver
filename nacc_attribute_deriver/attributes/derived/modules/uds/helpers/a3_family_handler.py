"""Handles NACCFAM, NACCMOM, and NACCDAD logic."""

from abc import ABC, abstractmethod
from typing import ClassVar, Literal, List, Optional
from pydantic import BaseModel, ValidationError, field_validator

from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace,
)
from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError

PARENTS = Literal["mom", "dad"]
SIBKIDS = Literal["sib", "kid"]


class FamilyStatusRecord(BaseModel):
    """Keep a record of the family status at each visit. Will be used to update
    the working variable.

    Statuses can be:
        0: Has no cognitive impairment
        1: Has cognitive impairment
        9: Unknown (default)
    """

    mom_status: int
    dad_status: int
    sib_status: int
    kid_status: int

    @field_validator(
        "mom_status", "dad_status", "sib_status", "kid_status", mode="after"
    )
    @classmethod
    def status_valid(cls, value: int) -> int:
        """Ensure the status being set is valid."""
        if value not in [0, 1, 9, INFORMED_MISSINGNESS]:
            raise ValidationError(f"Unrecognized family member status: {value}")

        return value

    def family_status(self) -> int:
        """Return the status of the family."""
        statuses = [self.mom_status, self.dad_status, self.sib_status, self.kid_status]

        if any(x == 1 for x in statuses):
            return 1
        if all(x == 0 for x in statuses):
            return 0
        if all(x == INFORMED_MISSINGNESS for x in statuses):
            return INFORMED_MISSINGNESS

        return 9


class A3FamilyHandler(ABC):
    def __init__(self, uds: UDSNamespace, table: SymbolTable) -> None:
        self.uds = uds
        self.__working = WorkingNamespace(table=table)
        self.__record = self.make_family_record()

    def __return_working_value(self, attribute: str) -> int:
        """Return working value.

        If not defined, then set to 9 (unknown).
        """
        result = self.__working.get_cross_sectional_value(attribute, int)
        return result if result is not None else INFORMED_MISSINGNESS

    @property
    def record(self) -> FamilyStatusRecord:
        return self.__record

    @property
    def prev_mom(self) -> int:
        return self.__return_working_value("cognitive_status_mom")

    @property
    def prev_dad(self) -> int:
        return self.__return_working_value("cognitive_status_dad")

    @property
    def prev_sib(self) -> int:
        return self.__return_working_value("cognitive_status_sib")

    @property
    def prev_kid(self) -> int:
        return self.__return_working_value("cognitive_status_kid")

    @abstractmethod
    def make_family_record(self) -> FamilyStatusRecord:
        pass

    @abstractmethod
    def get_sibkid_group_statuses(self, prefix: SIBKIDS, num_group: int) -> List[int]:
        """Get the sib/kids statuses for all members.

        Args:
            prefix: The prefix; should be one of sib or kid
            num_group: number of members in the group to evaluate
        Returns:
            List of status results for each member in the group
        """

    def run_sibkid_status_logic(self, prefix: SIBKIDS, prev_value: int) -> int:
        """Run the SIBS/KIDS logic, which has a lot of the same scaffolding
        just slightly different inner logic.

        Args:
            prefix: The prefix; should be one of sib or kid
            prev_value: the previous status for this group
        Returns:
            the status for this group as of this visit
        """
        # get SIBS/KIDS variable
        num_group = self.uds.get_value(f"{prefix}s", int)

        # if no SIBS/KIDS, no possible cognitive status other than no
        if num_group == 0:
            return 0

        # if SIBS/KIDS is unknown, we need to loop through and check all variables
        if num_group in [77, 99]:
            return 20 if prefix == "sib" else 15

        # siblings or kids defined; need to iterate over and collect all attributes
        if num_group is not None and num_group > 0:
            group_statuses = self.get_sibkid_group_statuses(prefix, num_group)

            if any(x == 1 for x in group_statuses):
                return 1

            if all(x == 0 for x in group_statuses):
                return 0

            if prev_value in [0, 1]:
                return prev_value

            if any(x in [0, 9] for x in group_statuses):
                return 9

        if prev_value in [0, 1, 9]:
            return prev_value

        return INFORMED_MISSINGNESS


class A3FamilyHandlerPrevVisit(A3FamilyHandler):
    """Handles determining family status based off the previous visit, which
    basically just pulls forward the values."""

    def make_family_record(self) -> FamilyStatusRecord:
        return FamilyStatusRecord(
            mom_status=self.prev_mom,
            dad_status=self.prev_dad,
            sib_status=self.prev_sib,
            kid_status=self.prev_kid,
        )


class A3FamilyHandlerV1(A3FamilyHandler):
    """Handles determining family status for V1 forms."""

    def make_family_record(self) -> FamilyStatusRecord:
        return FamilyStatusRecord(
            mom_status=self.__determine_parent_status("momdem", self.prev_mom),
            dad_status=self.__determine_parent_status("daddem", self.prev_dad),
            sib_status=self.__determine_sibkid_status("sib", self.prev_sib),
            kid_status=self.__determine_sibkid_status("kid", self.prev_kid),
        )

    def __determine_parent_status(self, field: str, prev_value: int) -> int:
        """Determine the parent member's status."""
        # only check if parent changed
        if not self.uds.is_initial() and self.uds.get_value("parchg", int) != 1:
            return prev_value

        demented = self.uds.get_value(field, int)

        # definitively set if 0 or 1
        if demented in [0, 1]:
            return demented

        # at this point it's 9 or blank or pulling from the
        # previous value, so just return what is already set
        return prev_value

    def __determine_sibkid_status(self, prefix: SIBKIDS, prev_value: int) -> int:
        """Determine the sib or kid status."""
        # if no change, return previous value
        if not self.uds.is_initial() and self.uds.get_value(f"{prefix}chg", int) != 1:
            return prev_value

        return self.run_sibkid_status_logic(prefix, prev_value)

    def get_sibkid_group_statuses(self, prefix: SIBKIDS, num_group: int) -> List[int]:
        """Get the sib/kids statuses for all members.

        For V1, it's actually in one variable, so we ignore num_group
        and just return a list of size 1 with the determined status from
        this variable.
        """
        demented = self.uds.get_value(f"{prefix}sdem", int)
        if demented is not None:
            # definitely a 0 (88 is N/A which usually means no sibs/kids
            # but check anyways)
            if demented in [0, 88]:
                return [0]

            # means at least one sibs/kids is demented, definitely a 1
            if demented > 0 and demented not in [88, 99]:
                return [1]

            if demented == 99:
                return [9]

        return [INFORMED_MISSINGNESS]


class A3FamilyHandlerV2(A3FamilyHandler):
    """Handles determining family status for V2 forms."""

    def make_family_record(self) -> FamilyStatusRecord:
        return FamilyStatusRecord(
            mom_status=self.__determine_parent_status("momdem", self.prev_mom),
            dad_status=self.__determine_parent_status("daddem", self.prev_dad),
            sib_status=self.__determine_sibkid_status("sib", self.prev_sib),
            kid_status=self.__determine_sibkid_status("kid", self.prev_kid),
        )

    def __determine_parent_status(self, field: str, prev_value: int) -> int:
        """Determine the parent member's status.

        Same as V1, except swapped meaning of PARCHG.
        """
        # only check if parent changed
        if not self.uds.is_initial() and self.uds.get_value("parchg", int) != 0:
            return prev_value

        demented = self.uds.get_value(field, int)

        # definitively set if 0 or 1
        if demented in [0, 1]:
            return demented

        # at this point it's 9 or blank or pulling from the
        # previous value, so just return what is already set
        return prev_value

    def __determine_sibkid_status(self, prefix: SIBKIDS, prev_value: int) -> int:
        """Determine the sib or kid status."""
        # if no change, return previous value
        if not self.uds.is_initial() and self.uds.get_value(f"{prefix}chg", int) != 0:
            return prev_value

        return self.run_sibkid_status_logic(prefix, prev_value)

    def get_sibkid_group_statuses(self, prefix: SIBKIDS, num_group: int) -> List[int]:
        """Get the sib/kids statuses for all members.

        Unlike V1, we now need to loop over the total possible number of
        sibs/kids instead of just looking at SIBSDEM and KIDSDEM.
        """
        group_statuses = []
        for i in range(num_group + 1):
            demented = self.uds.get_value(f"{prefix}{i}dem", int)
            group_statuses.append(
                demented if demented is not None else INFORMED_MISSINGNESS
            )

        return group_statuses


class A3FamilyHandlerV3(A3FamilyHandler):
    """Handles determining family status for V3 forms.

    This version relies on two variables for each member:
        - MOMNEUR, DADNEUR, SIBxNEU, KIDxNEU: if set to 1, has a primary neurological problem
        - MOMPRDX, DADPRDX, SIBPxDX, KIDxPDX: the diagnosis code, must match below list

    Both must be true for the member's status to = 1.
    """

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
    ]

    def make_family_record(self) -> FamilyStatusRecord:
        return FamilyStatusRecord(
            mom_status=self.__determine_parent_status("mom", self.prev_mom),
            dad_status=self.__determine_parent_status("dad", self.prev_dad),
            sib_status=self.__determine_sibkid_status("sib", self.prev_sib),
            kid_status=self.__determine_sibkid_status("kid", self.prev_kid),
        )

    def __neur_and_prdx_status(
        self, neur_field: str, prdx_field: str, prev_value: Optional[int] = None
    ) -> int:
        """Determine if the member has cognitive impairment. Does the following
        logic:

        - If *NEUR = 1
            - If *PRDX in DXCODES, return 1
            - If *PRDX is set but is NOT 999 and NOT in DXCODES, return 0
        - If *NEUR is 2, 3, 4, 5, or 8, return 0
        - If prev_value was 0 or 1, return that
        - If *NEUR = 1 and *PRDX = 999, return 9
        - If *NEUR = 9, return 9
        - If prev_value was set, return that
        - Default to -4, since no data has been provided
        """
        neur_value = self.uds.get_value(neur_field, int)
        if neur_value == 1:
            prdx_value = self.uds.get_value(prdx_field, int)
            if prdx_value in self.DXCODES:
                return 1
            if (
                prdx_value is not None
                and prdx_value != 999
                and prdx_value not in self.DXCODES
            ):
                return 0

        if neur_value in [2, 3, 4, 5, 8]:
            return 0

        if prev_value in [0, 1]:
            return prev_value

        if neur_value == 1 and (prdx_value == 999 or prdx_value is None):
            return 9

        if neur_value == 9:
            return 9

        if prev_value in [0, 1, 9]:
            return prev_value

        return INFORMED_MISSINGNESS

    def __determine_parent_status(self, prefix: PARENTS, prev_value: int) -> int:
        """Determine the parent member's status."""
        if not self.uds.is_initial() and self.uds.get_value("nwinfpar", int) != 1:
            return prev_value

        return self.__neur_and_prdx_status(f"{prefix}neur", f"{prefix}prdx", prev_value)

    def __determine_sibkid_status(self, prefix: SIBKIDS, prev_value: int) -> int:
        """Determine the sib or kid status."""
        # if no change, return previous value
        if not self.uds.is_initial() and self.uds.get_value(f"nwinf{prefix}", int) != 1:
            return prev_value

        return self.run_sibkid_status_logic(prefix, prev_value)

    def get_sibkid_group_statuses(self, prefix: SIBKIDS, num_group: int) -> List[int]:
        """Get the sib/kids statuses for all members."""
        group_statuses = []
        for i in range(1, num_group + 1):
            group_statuses.append(
                self.__neur_and_prdx_status(f"{prefix}{i}neu", f"{prefix}{i}pdx", None)
            )

        return group_statuses


class A3FamilyHandlerV4(A3FamilyHandler):
    """Handles determining family status for V4 forms."""

    def __init__(self, uds: UDSNamespace, table: SymbolTable) -> None:
        # define prev namespace
        self.__prev_record = PreviousRecordNamespace(table=table)

        super().__init__(uds=uds, table=table)

    def make_family_record(self) -> FamilyStatusRecord:
        return FamilyStatusRecord(
            mom_status=self.__determine_parent_status("mometpr", self.prev_mom),
            dad_status=self.__determine_parent_status("dadetpr", self.prev_dad),
            sib_status=self.__determine_sibkid_status("sib", self.prev_sib),
            kid_status=self.__determine_sibkid_status("kid", self.prev_kid),
        )

    def __etpr_status(self, field: str, prev_value: Optional[int]) -> int:
        """Get the member's ETPR status. They're technically string values, but
        here we treat them as ints.

        Note prev_etpr is different from prev_value.
            - prev_etpr is what ETPR specifically was set in the previous visit,
                and in the context of this function will simply replace a 66
            - prev_value is the actual status value (0, 1, or 9) that was
                set in the previous visit
        """
        etpr = self.uds.get_value(field, int)

        # if etpr = 66, need to pull value from previous visit
        if etpr == 66:
            prev_etpr = self.__prev_record.get_resolved_value(field, int)

            # because of error checks and missingness this absolutely must be
            # defined. if it is not we have some other problem
            if prev_etpr is None:
                raise AttributeDeriverError(
                    f"{field} = 66 but previous {field} value not defined"
                )

            etpr = prev_etpr

        if etpr is not None and etpr >= 1 and etpr <= 12:
            return 1

        if etpr == 0:
            return 0

        if prev_value in [0, 1]:
            return prev_value

        if etpr == 99:
            return 9

        if prev_value in [0, 1, 9]:
            return prev_value

        return INFORMED_MISSINGNESS

    def __determine_parent_status(self, field: str, prev_value: int) -> int:
        """Determine the parent member's status."""
        if not self.uds.is_initial() and self.uds.get_value("nwinfpar", int) != 1:
            return prev_value

        return self.__etpr_status(field, prev_value)

    def __determine_sibkid_status(self, prefix: SIBKIDS, prev_value: int) -> int:
        """Determine the sib or kid status."""
        # if no change, return previous value
        if not self.uds.is_initial() and self.uds.get_value(f"nwinf{prefix}", int) != 1:
            return prev_value

        return self.run_sibkid_status_logic(prefix, prev_value)

    def get_sibkid_group_statuses(self, prefix: SIBKIDS, num_group: int) -> List[int]:
        """Get the sib/kids statuses for all members."""
        group_statuses = []
        for i in range(1, num_group + 1):
            group_statuses.append(self.__etpr_status(f"{prefix}{i}etpr", None))

        return group_statuses
