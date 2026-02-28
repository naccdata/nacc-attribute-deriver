"""Handles NACCFAM logic for V1 and V2.

Largely just based on *DEM variables.
"""

class FamilyStatusRecord(BaseModel):
    """Keep a record of the family status at each visit. Will
    be used to update the working variable.

    Statuses can be:
        0: Has no cognitive impairment
        1: Has cognitive impairment
        9: Unknown (default)
    """

    mom_status: int
    dad_status: int
    sib_status: int
    kid_status: int

    @field_validator('mom_status', 'dad_status', 'sib_status', 'kid_status', mode='after')
    @classmethod
    def status_valid(cls, value: int) -> int:
        """Ensure the status being set is valid."""
        if value not in [0, 1, 9]:
            raise ValidationError(f"Unrecognized family member status: {value}")

        return value

    def family_status(self) -> int:
        """Return the status of the family."""
        statuses = [self.mom_status, self.dad_status, self.sib_status, self.kid_status]

        if any(x == 1 for x in statuses):
            return 1
        if all(x == 0 for x in statuses):
            return 0

        return 9


class A3FamilyHandler:

    def __init__(
        self, uds: UDSNamespace, working: WorkingNamespace
    ) -> None:
        self.uds = uds
        self.working = working
        self.family_record = self.make_family_record()

    @property
    def prev_mom(self) -> int:
        return self.working.get_cross_sectional_value("cognitive_status_mom")

    @property
    def prev_dad(self) -> int:
        return self.working.get_cross_sectional_value("cognitive_status_dad")

    @property
    def prev_sib(self) -> int:
        return self.working.get_cross_sectional_value("cognitive_status_sib")

    @property
    def prev_kid(self) -> int:
        return self.working.get_cross_sectional_value("cognitive_status_kid")

    @abstractmethod
    def make_family_record(self) -> FamilyStatusRecord:
        pass


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
            sib_status=self.__determine_sibkid_status("sibs", "sibsdem", self.prev_sib),
            kid_status=self.__determine_sibkid_status("kids", "kidsdem", self.prev_kid),
        )

    def __determine_parent_status(self, field: str, prev_demented: int) -> int:
        """Determine the parent member's status
        """
        demented = self.uds.get_value(field, int)

        # definitively set if 0 or 1
        if demented in [0, 1]:
            return dem_value

        # at this point it's 9 or blank. see if the previous
        # family record set it
        if prev_demented in [0, 1]:
            return prev_demented

        # default to 9 (unknown)
        return 9

    def __determine_sibkid_status(self, group: str, field: str, prev_demented: int) -> int:
        """Determine the sib or kid status.
        """
        num_group = self.uds.get_value(group, int)

        # if no SIBS/KIDS, no possible cognitive status other than no
        if num_group == 0:
            return 0

        # at least one sib/kid, check if demented explicitly reported
        # we also let 99 through in this case since it doesn't effect calculations
        if num_group is not None and num_group > 0:
            demented = self.uds.get_value(field, int)
            if demented is not None:
                # definitely a 0 (88 is N/A which usually means no sibs/kids)
                if demented in [0, 88]:
                    return 0

                # means at least one sibs/kids is demented, definitely a 1
                if demented != 99 and demented > 0:
                    return 1

        # at this point we don't know, so check if the previous record
        # set it to something, and if it did, return that
        if prev_demented in [0, 1]:
            return prev_demented

        # otherwise set to 9 for unknown
        return 9


class A3FamilyHandlerV2(A3FamilyHandler):
    """Handles determining family status for V2 forms."""

    def make_family_record(self) -> FamilyStatusRecord:
        return FamilyStatusRecord(
            mom_status=self.__determine_parent_status("momdem", self.prev_mom),
            dad_status=self.__determine_parent_status("daddem", self.prev_dad),
            sib_status=self.__determine_sibkid_status("sibs", "sib", self.prev_sib),
            kid_status=self.__determine_sibkid_status("kids", "kid", self.prev_kid),
        )

    def __determine_parent_status(self, field: str, prev_demented: int) -> int:
        """Determine the parent member's status. This is done the same way
        as V1, but keeping explicitly separate just to not cross wires for now.
        """
        demented = self.uds.get_value(field, int)

        # definitively set if 0 or 1
        if demented in [0, 1]:
            return dem_value

        # at this point it's 9 or blank. see if the previous
        # family record set it
        if prev_demented in [0, 1]:
            return prev_demented

        # default to 9 (unknown)
        return 9

    def __determine_sibkid_status(self, group: str, prefix: str, prev_demented: int) -> int:
        """Determine the sib or kid status.

        Unlike V1, we now need to loop over the total possible number of
        sibs/kids instead of just looking at SIBSDEM and KIDSDEM.
        """
        # get SIBS/KIDS
        num_group = self.uds.get_value(group)

        # if no SIBS/KIDS, no possible cognitive status other than no
        if num_group == 0:
            return 0

        # if SIBS/KIDS is unknown, we need to loop through and check all dem variables
        if num_group == 99:
            num_group = 20 if group == "sibs" else 15

        # siblings or kids defined; need to iterate over and collect all attributes
        if num_group is not None and num_group > 0:
            all_group_statuses = []
            for i in range(num_group + 1):
                all_group_statuses.append(
                    self.uds.get_value(f"{prefix}{i}dem", int)
                )

            if any(x == 1 for x in all_group_statuses):
                return 1

            if all(x == 0 for x in all_group_statuses):
                return 0

        # otherwise, at this point we don't know, so check if the previous record
        # set it to something, and if it did, return that
        if prev_demented in [0, 1]:
            return prev_demented

        # otherwise set to 9 for unknown
        return 9
