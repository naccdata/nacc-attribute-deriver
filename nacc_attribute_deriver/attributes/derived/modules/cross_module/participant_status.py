"""Data classes to track different participant statuses.

All status changes have two date values: the date
the status change actually happened, and the date of
the form that the status change was reported.

In general, we determine a participant's status based
on the latest thing that happened, which requres us
to compare dates. The complication comes when such dates
conflict or override each other, or have unknown parts
(e.g. 9999-99-99). We try to determine which date came
later based on the information we have, but if that is
not possible, we use the form date as a last resort.

Most status changes simply come from the MLST form. Deceased
is more complicated as it could also come from an NP or MDS
form. Additionally, for that status specifically, we also
want to track the AGE at which the participant died, so further
logic must be done to get that information.

Much of this logic also relies on working variables being set
correctly beforehand by other forms. Additionally, these working
variables MUST be set as a DateTaggedValue - that way, we get
both the status AND form dates. For some statuses, this
might be the same date.

See the following for more info:
    - attributes.derived.modules.mlst.form_mlst
    - attributes.derived.modules.np.form_np
    - attributes.derived.modules.md.form_mds
"""

import re

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Any, Optional

from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)

from nacc_attribute_deriver.utils.errors import AttributeDeriverError
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    date_from_form_date,
    parse_date_parts,
)

INVALID_DATES = {8888, 9999, 88, 99, None}


@dataclass
class ParticipantStatus(ABC):
    """Data class to represent a participant status."""

    # name of the status
    status: str

    # the actual date of the status change.
    # these can have unknown parts, so needs to be kept as a string
    status_date: str

    # date of the form the status change was reported in
    # MUST be set, so used as a tiebreaker if we cannot compare
    # otherwise
    form_date: date

    def __post_init__(self):
        """Ensure date is in YYYY-MM-DD format."""
        try:
            year, month, day = parse_date_parts(self.status_date)
            self.status_date = f"{year:4d}-{month:02d}-{day:02d}"
        except AttributeDeriverError:
            raise AttributeDeriverError(
                f"Participant status date {self.status} not in "
                + f"YYYY-MM-DD format: {self.status_date}"
            )

    def __eq__(self, other: "ParticipantStatus") -> bool:
        """Compare equality by if this status was done on the same day as the
        other status."""
        if not isinstance(other, ParticipantStatus):
            return False

        # if both can be converted to a date, compare like that
        try:
            this_date = date_from_form_date(self.status_date)
            other_date = date_from_form_date(other.status_date)

            if this_date is not None and other_date is not None:
                raise ValueError(this_date == other_date)
                return this_date == other_date
        except (TypeError, ValueError, AttributeDeriverError):
            pass

        # otherwise just compare the form dates; we don't want
        # to check equality on any unknowns
        return self.form_date == other.form_date

    def __lt__(self, other: "ParticipantStatus") -> bool:
        """Compare statuses by date of status."""
        if not isinstance(other, ParticipantStatus):
            return False

        # if both can be converted to a date, compare like that
        try:
            this_date = date_from_form_date(self.status_date)
            other_date = date_from_form_date(other.status_date)

            if this_date is not None and other_date is not None:
                return this_date < other_date
        except (TypeError, ValueError, AttributeDeriverError):
            pass

        # means at least one of the dates is in partial form
        # need to compare part by part. we are assuming values
        # are in YYYY-MM-DD format, so it also evaluates in order
        # of priority
        try:
            this_parts = (int(x) for x in self.status_date.split("-"))
            other_parts = (int(x) for x in other.status_date.split("-"))
            for this_part, other_part in zip(this_parts, other_parts):
                # break at the earliest part in priority that we can't compare
                if this_part in INVALID_DATES or other_part in INVALID_DATES:
                    break

                if this_part < other_part:
                    return True
                if this_part > other_part:
                    return False

                # if equal, go onto next part
        except (TypeError, ValueError) as e:
            raise AttributeDeriverError(f"Status date cannot be parsed: {e}") from e

        # unable to determine; use form's date by default, which HAS
        # to be defined
        return self.form_date < other.form_date

    @classmethod
    @abstractmethod
    def create_from_working_namespace(
        cls, working: WorkingNamespace
    ) -> Optional["ParticipantStatus"]:
        """Creates the given status using the table information.

        If information necessary to set the status is not present,
        returns None. This is effectively the same as saying the
        participant does NOT have that status (e.g. if there is no death
        date reported, that participant is not dead.)

        Args:
            working: The Working namespace; holds working variables carried
                over from curation of othe forms
        """
        pass


@dataclass(eq=False)
class DeceasedStatus(ParticipantStatus):
    age_at_death: int
    has_np: bool

    @classmethod
    def create_from_working_namespace(
        cls, working: WorkingNamespace
    ) -> Optional["DeceasedStatus"]:
        """Determine if the participant ever died, and grab its corresponding
        latest date. A subject's death can be reported in several ways, in the
        following order of priority:

        1. An NP form has been provided
            - This also sets the has_np flag
        2. Marked as DECEASED on a MLST form
        3. Marked as DECEASED on an MDS form

        Additionally, for this status we want to keep track of the age of
        death as well and whether or not they have an NP form.

        1. If reported on an NP form, use that date.
        2. Otherwise, try to compute from the UDS birth date
        3. If an MDS death age was reported, use that
            - Technically if a participant died at MDS, they cannot be
                a UDS participant either, so we don't necessarily have to
                track this because the derived variables are calculated for
                UDS participants only. But doing it for completeness, and
                just in case it somehow does happen anyways.
        4. If we cannot determine the age at death, set to 999
        """
        death_date = None
        has_np = False

        for source in ["np-death-date", "milestone-death-date", "mds-death-date"]:
            death_date = working.get_cross_sectional_dated_value(source, str)
            if death_date:
                if source == "np-death-date":
                    has_np = True

                break

        # if no death date reported, not dead
        if not death_date:
            return None

        # otherwise, also determine the death age. evaluate in the order
        # as described above. set to None if it cannot be determined
        # 1. check if NP set it first
        age_at_death = working.get_cross_sectional_value("np-death-age", int)

        # NP MUST report the age at death; if not, we have a problem
        if has_np and not age_at_death:
            raise AttributeDeriverError("Missing NP death age when NP death reported")

        # 2. calculate from UDS visit (includes if MDS was set but they
        # have an UDS visit somehow; prioritize UDS birth date over what
        # was set in MDS). can only be calculated if the death date is a
        # full death date (no unknown parts)
        if not age_at_death:
            try:
                death_date_parsed = date_from_form_date(death_date.value)
                birth_date = date_from_form_date(
                    working.get_cross_sectional_value("uds-date-of-birth", str)
                )
                age_at_death = calculate_age(birth_date, death_date_parsed)
            except AttributeDeriverError:
                pass

        # 3. Try to pull from MDS. This should only ever be set by an
        # MDS-only participant, as every UDS visit is expected to have a
        # birth date provided
        if not age_at_death:
            age_at_death = working.get_cross_sectional_value("mds-death-age", int)

        # set deceased status
        return DeceasedStatus(
            status="deceased",
            status_date=death_date.value,
            form_date=death_date.date,
            age_at_death=age_at_death if age_at_death is not None else 999,
            has_np=has_np,
        )


@dataclass(eq=False)
class DiscontinuedStatus(ParticipantStatus):
    @classmethod
    def create_from_working_namespace(
        cls, working: WorkingNamespace
    ) -> Optional["DiscontinuedStatus"]:
        """Determine if the participant ever discontinued, and grab its
        corresponding latest date. A subject is denoted as discontinued if they
        are explicitly marked as discontinued on a MLST form.

        See form_mlst._create_milestone_discontinued_date for how we
        keep track of this.
        """
        discontinued_date = working.get_cross_sectional_dated_value(
            "milestone-discontinued-date", str
        )

        # if no discontinued date set, means not discontinued. return None
        if not discontinued_date:
            return None

        return DiscontinuedStatus(
            status="discontinued",
            status_date=discontinued_date.value,
            form_date=discontinued_date.date,
        )


@dataclass(eq=False)
class MinimumContactStatus(ParticipantStatus):
    @classmethod
    def create_from_working_namespace(
        cls, working: WorkingNamespace
    ) -> Optional["MinimumContactStatus"]:
        """Determine if the participant was set to minimum contact, and grab
        its corresponding latest date. A subject is denoted as minimum contact
        if they explicitly set PROTOCOL/UDSACTIV as such on the MLST form.

        See form_mlst._create_milestone_minimum_contact_date for how we
        keep track of this.
        """
        minimum_contact_date = working.get_cross_sectional_dated_value(
            "milestone-minimum-contact-date", str
        )

        # if no minimum contact date set, means not minimum contact. return None
        if not minimum_contact_date:
            return None

        return MinimumContactStatus(
            status="minimum_contact",
            status_date=minimum_contact_date.value,
            form_date=minimum_contact_date.date,
        )


@dataclass(eq=False)
class InitialVisitOnlyStatus(ParticipantStatus):
    @classmethod
    def create_from_working_namespace(
        cls, working: WorkingNamespace
    ) -> Optional["InitialVisitOnlyStatus"]:
        """Determine if the participant was set to initial visit only, and grab its
        corresponding latest date. A subject is denoted as initial visit if
        they submit a single IVP UDS visit with PRESPART = 1 (V3 and earlier).

        This is a rather weak status that gets overriden if there is ANY new
        data from the participant, and is also not available in V4.
        """
        prespart = working.get_cross_sectional_dated_value("prespart", int)

        # not set to initial visit only, return None
        if prespart is None or prespart.value != 1:
            return None

        # check if they really only had an initial visit by looking at
        # number of uds visits; if they did, the original prespart designation
        # is voided
        uds_visitdates = working.get_cross_sectional_value("uds-visitdates", list)
        if uds_visitdates and len(uds_visitdates) > 1:
            return None

        # check the sole UDS visitdate is the same as the one that defined
        # the prespart variable; if not, we have a problem
        uds_visit = date_from_form_date(uds_visitdates[0]) if uds_visitdates else None
        if not uds_visit:
            raise AttributeDeriverError(
                f"Cannot find associated UDS visit for prespart with date: {prespart.date}"
            )

        if uds_visit != prespart.date:
            raise AttributeDeriverError(
                f"PRESPART set date does not match known UDS visit: PRESPART associated with {prespart.date} while UDS visit is {uds_visit}"
            )

        return MinimumContactStatus(
            status="initial_visit_only",
            status_date=str(
                prespart.date
            ),  # status date is same as form date for this one
            form_date=prespart.date,
        )


@dataclass(eq=False)
class RejoinedStatus(ParticipantStatus):
    @classmethod
    def create_from_working_namespace(
        cls, working: WorkingNamespace
    ) -> Optional["RejoinedStatus"]:
        """Determine if the participant ever rejoined, and grab its
        corresponding latest date. A subject is denoted as rejoined if they are
        explicitly marked as rejoined on a MLST form. Note this is different
        from an "implicit" rejoin via a later UDS Visit; see UDSAfterMLSTStatus
        for that.

        See form_mlst._create_milestone_rejoined_date for how we keep
        track of this.
        """
        rejoined_date = working.get_cross_sectional_dated_value(
            "milestone-rejoined-date", str
        )

        # if no rejoined date set, means not rejoined. return None
        if not rejoined_date:
            return None

        return RejoinedStatus(
            status="rejoined",
            status_date=rejoined_date.value,
            form_date=rejoined_date.date,
        )


@dataclass(eq=False)
class LatestUDSVisit(ParticipantStatus):
    @classmethod
    def __get_latest_visitdate(
        cls, working: WorkingNamespace, attribute: str
    ) -> Optional[date]:
        """Get the latest visitdate, if visits exist.

        Returns:
            The latest visitdate, if found, None otherwise
        """
        visitdates = working.get_cross_sectional_value(attribute, list)
        if not visitdates:
            return None

        sorted_visitdates = sorted(list(visitdates))
        return date_from_form_date(sorted_visitdates[-1])

    @classmethod
    def create_from_working_namespace(
        cls, working: WorkingNamespace
    ) -> Optional["UDSAfterMLSTStatus"]:
        """Get the participant's latest UDS visit.

        If this came after some status change, it can override/reset it.
        """
        latest_uds = cls.__get_latest_visitdate(working, "uds-visitdates")

        # no UDS visits; return None
        if not latest_uds:
            return None

        return LatestUDSVisit(
            status="latest_uds_visit", status_date=str(latest_uds), form_date=latest_uds
        )


@dataclass(eq=False)
class NursingHomeStatus(ParticipantStatus):
    @classmethod
    def create_from_working_namespace(
        cls, working: WorkingNamespace
    ) -> Optional["UDSAfterMLSTStatus"]:
        """Get when the participant permenantly moved to a nursing home.

        This status does not interact with other statuses, but instead
        looks at the latest RESIDENC value from the UDS A1 form that was
        set. RESIDENC can override/nullify this status if it is anything
        other than 4 (nursing home) or 9 (unknown) AND came after the
        day RENURSE from MLST was set. That being said, RESIDENC can
        never set this variable, only nullify it.
        """
        nursing_home_date = working.get_cross_sectional_dated_value(
            "milestone-renurse-date", str
        )

        # if no nursing date set from MLSTs, return None
        if not nursing_home_date:
            return None

        residenc = working.get_cross_sectional_dated_value("residenc", int)

        # if RESIDENC nullifies, return None
        if residenc and residenc.value not in [4, 9]:
            return None

        return NursingHomeStatus(
            status="nursing_home",
            status_date=nursing_home_date.value,
            form_date=nursing_home_date.date,
        )
