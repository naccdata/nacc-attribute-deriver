"""Derived variables that rely on multiple modules/forms.

This belongs to the cross_module scope and is intended to run last on
global data. As such, it does not rely on a specific form, but instead
information stored in subject.info, usually typically
subject.info.working.cross-sectional

Looks generally at UDS, NP, MLST, and MDS
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_months,
    date_from_form_date,
    parse_date_parts,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError

from .participant_status import ParticipantStatus
from .participant_status_handler import ParticipantStatusHandler


class CrossModuleAttributeCollection(AttributeCollection):
    """Class to collect cross-module attributes."""

    def __init__(self, table: SymbolTable) -> None:
        """Initializer."""
        self.__subject_derived = SubjectDerivedNamespace(table=table)
        self.__working = WorkingNamespace(table=table)

        # participant handler to keep track of the participant's statuses
        self.__participant = ParticipantStatusHandler(self.__working)

        # if the center is inactive, will override variables like
        # NACCACTV and NACCNOVS; assume True by default
        self.__active_center = table.get("_active_center", True)

    ########################
    # NP DERIVED VARIABLES #
    ########################

    def _create_naccdage(self) -> int:
        """Creates NACCDAGE: Age at death."""
        deceased = self.__participant.deceased()
        return 888 if not deceased else deceased.age_at_death

    def _create_naccautp(self) -> int:
        """Creates NACCAUTP - Neuropathology data from an autopsy available"""
        deceased = self.__participant.deceased()

        # not dead
        if not deceased:
            return 8

        return 1 if deceased.has_np else 0

    def _create_naccint(self) -> int:
        """Creates NACCINT, which is time interval (months) between last visit
        (UDS) and death (NP/Milestone, technically MDS as well but a subject
        that died at MDS shouldn't be an UDS participant)."""
        deceased = self.__participant.deceased()
        latest_uds_visit = self.__participant.latest_uds_visit()

        # not dead
        if not deceased:
            return 888
        if not latest_uds_visit:
            return 999

        # if death date has unknown parts, infer ONLY if the day is missing
        # by setting it to 15 (middle of the month). otherwise, just return 999
        death_date = deceased.status_date
        if "99" in death_date or "88" in death_date:
            year, month, day = parse_date_parts(death_date)
            if year not in [8888, 9999] and month not in [88, 99] and day in [88, 99]:
                death_date = f"{year}-{month}-15"
            else:
                return 999

        # otherwise, we're assuming the death date is known, try to calculate
        # from the latest UDS date (which should also be known)
        result = None
        try:  # noqa: SIM105
            result = calculate_months(
                date_from_form_date(latest_uds_visit.status_date),
                date_from_form_date(death_date),
            )
        except (TypeError, ValueError, AttributeDeriverError):
            pass

        return result if result is not None else 999

    def _create_naccmod(self) -> int:
        """Create the NACCMOD - Month of death"""
        deceased = self.__participant.deceased()

        # not dead
        if not deceased:
            return 88

        # parse out the death month
        _, month, _ = parse_date_parts(deceased.status_date)
        if month and month >= 1 and month < 12:
            return month

        return 99

    def _create_naccyod(self) -> int:
        """Create the NACCYOD - Year of death"""
        deceased = self.__participant.deceased()

        # not dead
        if not deceased:
            return 8888

        # parse out the death year
        year, _, _ = parse_date_parts(deceased.status_date)
        return 9999 if year is None else year

    ###############################
    # MILESTONE DERIVED VARIABLES #
    ###############################

    def _create_naccdied(self) -> int:
        """Creates NACCDIED - subject is known to be deceased."""
        return 1 if self.__participant.deceased() else 0

    def _create_naccactv(self) -> int:
        """Creates NACCACTV - Follow-up status at the Alzheimer's
        Disease Center (ADC)

        Codes:
            0: If subject receives no followup contact (dead, discontinued,
                or enrolled as initial visit only)
            1: If subject is under annual followup and expected to make more
                Includes discontinued subjects who have since rejoined
                - This also includes subject who have not explicitly
                    been stated to have rejoined (via MLST form) BUT have
                    UDS visits after the date of the discontinued MLST form
            2: Minimal contact with ADC but still enrolled
            5: Affiliate
        """
        # it not an active center, return 0
        if not self.__active_center:
            return 0

        # if an affiliate, return 5 (not in RDD and won't go in QAF
        # but just used to differentiate)
        if self.__subject_derived.get_value("affiliate", bool):
            return 5

        # if dead, discontinued, or initial visit only, return 0
        if (
            self.__participant.deceased()
            or self.__participant.discontinued()
            or self.__participant.initial_visit_only()
        ):
            return 0

        # if minimal contact, return 2
        if self.__participant.minimum_contact():
            return 2

        # otherwise presumed active
        return 1

    def _create_naccnovs(self) -> int:
        """Creates NACCNOVS - No longer followed annually in person or by
        telephone.
        """
        # it not an active center, return 1
        if not self.__active_center:
            return 1

        # if initial visit only, return 8
        if self.__participant.initial_visit_only():
            return 8

        # if dead, discontinued, or minimum contact only, return 1
        if (
            self.__participant.deceased()
            or self.__participant.discontinued()
            or self.__participant.minimum_contact()
        ):
            return 1

        # otherwise presumed active
        return 1

    def _create_naccnurp(self) -> int:
        """Creates NACCNURP - Permanently moved to a nursing home."""
        return 1 if self.__participant.nursing_home() else 0

    def _create_naccnrdy(self) -> int:
        """Creates NACCNRDY - Day permanently moved to nursing home."""
        nursing_home = self.__participant.nursing_home()

        # has not permenantly moved to a nursing home
        if not nursing_home:
            return 88

        # parse out the nursing home month
        _, _, day = parse_date_parts(nursing_home.status_date)
        return 99 if day is None else day

    def _create_naccnrmo(self) -> int:
        """Creates NACCNRMO - Month permanently moved to nursing home."""
        nursing_home = self.__participant.nursing_home()

        # has not permenantly moved to a nursing home
        if not nursing_home:
            return 88

        # parse out the nursing home month
        _, month, _ = parse_date_parts(nursing_home.status_date)
        return 99 if month is None else month

    def _create_naccnryr(self) -> int:
        """Creates NACCNRYR - Year permanently moved to nursing home."""
        nursing_home = self.__participant.nursing_home()

        # has not permenantly moved to a nursing home
        if not nursing_home:
            return 8888

        # parse out the nursing home year
        year, _, _ = parse_date_parts(nursing_home.status_date)
        return 9999 if year is None else year

    def __determine_status_for_discontinuation(self) -> Optional[ParticipantStatus]:
        """Determine which status to use for the discontinuation dates.

        Both discontinuation and minimum protocol status can set the
        discontinuation date.
        """
        discontinued = self.__participant.discontinued()
        minimum_contact = self.__participant.minimum_contact()

        # if both, figure out which one came later and use that; if they're the
        # same day it doesn't really matter (in terms of dates),
        # so prioritize discontinued
        if discontinued and minimum_contact:
            if minimum_contact < discontinued or minimum_contact == discontinued:
                return discontinued

            return minimum_contact

        if discontinued:
            return discontinued
        if minimum_contact:
            return minimum_contact

        return None

    def _create_naccdsdy(self) -> int:
        """Creates NACCDSDY - Day of discontinuation from annual follow-up.

        Discontinued date can also be set by minimum protocol status.
        """
        status = self.__determine_status_for_discontinuation()
        if not status:
            return 88

        # parse out the discontinued day
        _, _, day = parse_date_parts(status.status_date)
        return 99 if day is None else day

    def _create_naccdsmo(self) -> int:
        """Creates NACCDSMO - Month of discontinuation from annual follow-up.

        Discontinued date can also be set by minimum protocol status.
        """
        status = self.__determine_status_for_discontinuation()
        if not status:
            return 88

        # parse out the discontinued month
        _, month, _ = parse_date_parts(status.status_date)
        return 99 if month is None else month

    def _create_naccdsyr(self) -> int:
        """Creates NACCDSYR - Year of discontinuation from annual follow-up.

        Discontinued date can also be set by minimum protocol status.
        """
        status = self.__determine_status_for_discontinuation()
        if not status:
            return 8888

        # parse out the discontinued year
        year, _, _ = parse_date_parts(status.status_date)
        return 9999 if year is None else year

    def _create_nacccore(self) -> int:
        """Creates NACCCORE - Clinical core participant."""
        # cannot just check affiliate mainly because of mds_source possibly being 9
        mds_source = self.__working.get_cross_sectional_value("mds-source", int)
        uds_source = self.__working.get_cross_sectional_value("uds-source", int)
        uds_sourcenw = self.__working.get_cross_sectional_value("uds-sourcenw", int)

        # UDS participant
        if uds_source != 4 and uds_sourcenw != 2 and mds_source is None:
            return 1

        # MDS participant
        if mds_source not in [3, 9] and uds_source is None and uds_sourcenw is None:
            return 1

        # use overall affiliate status as a fallback
        affiliate = self.__subject_derived.get_value("affiliate", bool)
        return 1 if not affiliate else 0
