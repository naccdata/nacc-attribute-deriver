"""Handles the participant's overall status.

Keeps track of all possible statuses. A REJOIN or UDS VISIT
status may override other statuses by happening later than them;
if so, this handler effectively pretends the status was not set.

If a status change happens at the same date as a REJOIN or UDS VISIT,
we prioritize the other status change (one way to think of it is they
completed the UDS visit and then decided to discontinue at the visit).
"""

from typing import Any, Optional

from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)

from .participant_status import (
    DeceasedStatus,
    DiscontinuedStatus,
    InitialVisitOnlyStatus,
    LatestUDSVisit,
    MinimumContactStatus,
    NursingHomeStatus,
    ParticipantStatus,
    RejoinedStatus,
)


class ParticipantStatusHandler:
    def __init__(self, working: WorkingNamespace) -> None:
        """Initializer."""
        # possible statuses. if none of these are set, the participant
        # is presumed active
        self.__deceased = DeceasedStatus.create_from_working_namespace(working)
        self.__discontinued = DiscontinuedStatus.create_from_working_namespace(working)
        self.__minimum_contact = MinimumContactStatus.create_from_working_namespace(
            working
        )
        self.__initial_visit_only = (
            InitialVisitOnlyStatus.create_from_working_namespace(working)
        )

        # states that can unset the above statuses, as they also make the
        # participant active
        self.__rejoined = RejoinedStatus.create_from_working_namespace(working)
        self.__latest_uds = LatestUDSVisit.create_from_working_namespace(working)

        # other statuses that don't interact with the above
        self.__nursing_home = NursingHomeStatus.create_from_working_namespace(working)

    def __determine_status_override(
        self,
        status: Optional[ParticipantStatus],
    ) -> Optional[Any]:
        """Determine if the status is valid, e.g. it is the latest and nothing
        invalidates it.

        A status can be invalidated if either a) they rejoined AFTER
        this status' date or b) they had a UDS visit AFTER this status'
        date.

        Args:
            status: The status to determine if whether should be overidden or not
        Returns:
            The status if it is still valid, None otherwise
        """
        # if status is not set, return None
        if not status:
            return None

        # if status is set, but a UDS visit or REJOIN came after, it has
        # effectively been unset; return None
        for state in [self.__latest_uds, self.__rejoined]:
            if state is not None and state > status:
                return None

        # otherwise, the status is the latest and valid, return
        return status

    def deceased(self) -> Optional[DeceasedStatus]:
        """Return if the participant is deceased."""
        return self.__determine_status_override(self.__deceased)

    def discontinued(self) -> Optional[DiscontinuedStatus]:
        """Return if the participant is discontinued."""
        return self.__determine_status_override(self.__discontinued)

    def minimum_contact(self) -> Optional[MinimumContactStatus]:
        """Return if the participant is minimum contact."""
        return self.__determine_status_override(self.__minimum_contact)

    def initial_visit_only(self) -> Optional[InitialVisitOnlyStatus]:
        """Return if the participant is initial visit only.

        Immediately overridden if ANYTHING else is set. So we just check
        for existence of other states.
        """
        if not self.__initial_visit_only:
            return None

        all_statuses = [
            self.__deceased,
            self.__discontinued,
            self.__minimum_contact,
            self.__rejoined,
            # note latest_uds is ignored here since InitialVisitOnlyStatus
            # already validates that there is only one UDS visit and
            # it corresponds to when PRESPART was set
        ]
        if any(x is not None for x in all_statuses):
            return None

        return self.__initial_visit_only

    def rejoined(self) -> Optional[RejoinedStatus]:
        """Return the rejoined status."""
        return self.__rejoined

    def latest_uds_visit(self) -> Optional[LatestUDSVisit]:
        """Return the latest UDS visit for the participant."""
        return self.__latest_uds

    def nursing_home(self) -> Optional[NursingHomeStatus]:
        """Return the latest nursing home status.

        This already check if a RESIDENC value overrode it, so just
        return as-is.
        """
        return self.__nursing_home
