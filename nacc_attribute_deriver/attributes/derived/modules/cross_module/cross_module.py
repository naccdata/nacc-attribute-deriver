"""Derived variables that rely on multiple modules/forms.

This belongs to the cross_module scope and is intended to run last on
global data. As such, it does not rely on a specific form, but instead
information stored in subject.info, usually typically
subject.info.working.cross-sectional

Looks generally at UDS, NP, MLST, and MDS
"""

from datetime import date
from typing import Optional, Type

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
    T,
    WorkingNamespace,
)
from nacc_attribute_deriver.schema.rule_types import DateTaggedValue
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import UNKNOWN_CODES
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    calculate_months,
    date_came_after,
    date_came_after_sparse,
    date_from_form_date,
)


class CrossModuleAttributeCollection(AttributeCollection):
    """Class to collect cross-module attributes."""

    def __init__(self, table: SymbolTable) -> None:
        """Initializer."""
        self.__subject_derived = SubjectDerivedNamespace(table=table)
        self.__working = WorkingNamespace(table=table)

        # if the center is inactive, will override variables like
        # NACCACTV and NACCNOVS; assume True by default
        self.__active_center = table.get("_active_center", True)

    def __working_value(self, attribute: str, attribute_type: Type[T]) -> Optional[T]:
        """Grab cross-sectional working value."""
        return self.__working.get_cross_sectional_value(attribute, attribute_type)

    def __latest_working_value(
        self, attribute: str, attribute_type: Type[T]
    ) -> Optional[DateTaggedValue[T]]:
        """Grab latest cross-sectional working value."""
        return self.__working.get_cross_sectional_dated_value(attribute, attribute_type)

    def __determine_death_date(self) -> Optional[date]:
        """Determines the death status, and returns the death date if found.

        Checks the following forms in order:
            - NP
            - Milestone
            - MDS

        Returns:
            Death date if found, None otherwise
        """
        for field in ["np-death-date", "milestone-death-date", "mds-death-date"]:
            death_date = date_from_form_date(self.__working_value(field, str))
            if death_date:
                return death_date

        return None

    def __get_latest_visitdate(self, attribute: str) -> Optional[date]:
        """Get the latest UDS visitdate, if UDS visits exist."""
        visitdates = self.__working_value(attribute, list)
        if not visitdates:
            return None

        sorted_visitdates = sorted(list(visitdates))
        return date_from_form_date(sorted_visitdates[-1])

    def __determine_prespart(self) -> int:
        """Generally, PRESPART = 1 means initial visit only. However,
        if they ended up having more UDS visits, that means they are
        effectively ignoring/changing that and the participant is
        actually active, so override the value of PRESPART.

        Returns:
            1: If PRESPART == 1 and only the initial visit exists
            0: If PRESPART != 1 or multiple UDS visits (indicating follow-ups)
        """
        prespart = self.__working_value("prespart", int)
        if prespart == 1:
            # check if they really only had an initial visit by looking at
            # number of uds visits
            uds_visitdates = self.__working_value("uds-visitdates", list)
            if uds_visitdates and len(uds_visitdates) > 1:
                return 0

        return prespart if prespart is not None else 0

    ########################
    # NP DERIVED VARIABLES #
    ########################

    def _create_naccdage(self) -> int:
        """Creates NACCDAGE: Age at death.

        Pulls from NP, MLST, and UDS.
        """
        # check that subject is deceased at all
        mds_vital_status = self.__working_value("mds-vital-status", int)
        if self._create_naccdied() == 0 and mds_vital_status != 2:
            return 888

        # NP, grab from NPDAGE
        npdage = self.__working_value("np-death-age", int)
        if npdage:
            return npdage

        # otherwise calculate from DOB/DOD
        birth_date = date_from_form_date(self.__working_value("uds-date-of-birth", str))
        death_date = self.__determine_death_date()

        if not birth_date or not death_date:
            return 999

        age = calculate_age(birth_date, death_date)
        if not age:
            return 999

        return age

    def _create_naccautp(self) -> int:
        """Creates NACCAUTP - similar to NACCDIED but also
        needs to differentiate if an NP form was submitted
        or not.
        """
        death_age = self.__working_value("np-death-age", int)
        deceased = self.__working_value("milestone-deceased", int)
        np_deceased = death_age is not None
        mile_deceased = deceased == 1

        # not reported as having died
        if not np_deceased and not mile_deceased:
            return 8

        # deceased but no NP data available
        if mile_deceased and not np_deceased:
            return 0

        # deceased with NP data available
        return 1

    def _create_naccint(self) -> int:
        """Creates NACCINT, which is time interval (months) between last visit
        (UDS) and death (NP/Milestone).

        Uses NACCDIED and death date calculate.
        """
        naccdied = self._create_naccdied()
        deathdate = self.__determine_death_date()

        # not dead
        if naccdied != 1:
            return 888

        # died but no/unknown death age
        if naccdied == 1 and not deathdate:
            return 999

        # compare to last UDS visit
        last_visit = self.__get_latest_visitdate("uds-visitdates")
        if not last_visit:
            return 999

        result = calculate_months(last_visit, deathdate)

        # limit 0 - 100
        if result is None or result in UNKNOWN_CODES:
            return 999

        return min(result, 100)

    # Tried to use all things described in the rdd-np. Many seemed not
    # in the SAS code. Not sure if the MDS "vitalst" is passed through or not.
    def _create_naccmod(self) -> int:
        """Create the NACCMOD variable.

        Month of death. In Milestone and MDS, the month can be unknown
        (99) so need to inspect directly.

        REGRESSION: RDD only mentions NP/MLST. Ignore MDS?
        """
        # check vital status
        if not self._create_naccdied():
            return 88

        # NP will always have a known month
        np_date = self.__working_value("np-death-date", str)
        death_date = date_from_form_date(np_date)
        if death_date:
            return death_date.month

        # Milestone month may be 99
        milestone_mo = self.__working_value("milestone-death-month", int)
        if milestone_mo is not None and milestone_mo != 99:
            return milestone_mo

        # MDS death month may be 99
        # mds_mo = self.__working_value("mds-death-month", int)
        # if mds_mo is not None and mds_mo != 99:
        #     return mds_mo

        # if no MOD but a YOD is available, set MOD to 7
        if self._create_naccyod() not in [8888, 9999]:
            return 7

        return 99

    # SAS seemingly sparse for this. Another one with potential MDS.
    def _create_naccyod(self) -> int:
        """Create the NACCYOD variable.

        Year of death.

        REGRESSION: RDD only mentions NP/MLST. Ignore MDS?
        """
        # check vital status
        if not self._create_naccdied():
            return 8888

        # year always defined if death date exists
        # note MDS will not trigger the NACCDIED case
        deathdate = self.__determine_death_date()

        # Explicitly states in rdd-np that this shouldn't precede 1970.
        # Previously not mentioned in SAS code.
        if deathdate:
            return deathdate.year if (deathdate.year >= 1970) else 9999

        return 9999

    def uds_came_after(self, target_date: date | None) -> bool:
        """Compares UDS and given target dates.

        Returns:
            True: If UDS > target date
            False: If UDS <= target_date
        """
        uds_date = self.__get_latest_visitdate("uds-visitdates")
        if not uds_date:
            # may not be an UDS participant (e.g. MDS/BDS)
            return False

        return date_came_after(uds_date, target_date)

    ###############################
    # MILESTONE DERIVED VARIABLES #
    ###############################

    def _create_naccdied(self) -> int:
        """Creates NACCDIED - determined if death
        has been reported by NP or Milestone form.
        """
        death_age = self.__working_value("np-death-age", int)
        if death_age is not None:
            return 1

        deceased = self.__working_value("milestone-deceased", int)
        if deceased == 1:
            return 1

        return 0

    def _create_naccactv(self) -> int:
        """Creates NACCACTV - Follow-up status at the Alzheimer's
        Disease Center (ADC)

        Codes:
            0: If subject receives no followup contact (dead, discontinued,
                or enrolled as initial visit only)
            1: If subject is under annual followup and expected to make more
                Includes discontinued subjects who have since rejoined
                - This seems to also include subject who have not explicitly
                    been stated to have rejoined (via MLST form) BUT have
                    UDS visits after the date of the discontinued MLST form
            2: Minimal contact with ADC but still enrolled
            5: Affiliate
        """
        # it not an active center or dead (from NP/MLST), return 0
        if not self.__active_center or self._create_naccdied() == 1:
            return 0

        # if milestone marked subject as discontinued, and is the latest form,
        # return 0. if there were UDS visits after discontinuation was marked,
        # basically treat as NOT discontinued and pass through
        mlst_discontinued = self.__latest_working_value("milestone-discontinued", int)
        if mlst_discontinued and mlst_discontinued.value == 1:  # noqa: SIM102
            if not self.uds_came_after(mlst_discontinued.date):
                return 0

        # if UDS A1 prespart == 1 (initial evaluation only), return 0
        if self.__determine_prespart() == 1:
            return 0

        # 5 used for affiliates in SAS/R code
        if self.__subject_derived.get_value("affiliate", bool):
            return 5

        # check milestone protocol/udsactiv
        protocol = self.__working_value("milestone-protocol", int)
        udsactiv = self.__working_value("milestone-udsactiv", int)

        # inactive
        if udsactiv == 4:
            return 0

        # annual followup expected
        if protocol in [1, 3] or udsactiv in [1, 2]:
            return 1
        # minimal contact
        if protocol == 2 or udsactiv == 3:
            return 2

        # protocol == 1 or 3, or just active
        return 1

    def _create_naccnovs(self) -> int:
        """Creates NACCNOVS - No longer followed annually in person or by
        telephone. This is ultimately just checking the same things
        NACCACTV is and reinterprets results.
        """
        # if not an active center, always return 1
        if not self.__active_center:
            return 1

        # if UDS is the latest one, check UDS prespart == 1 to return 8,
        # otherwise purely based on MLST
        recent_mlst = self.__get_latest_visitdate("milestone-visitdates")
        if recent_mlst:
            prespart = self.__determine_prespart()
            if self.uds_came_after(recent_mlst) and prespart == 1:
                return 8

        naccactv = self._create_naccactv()
        if naccactv == 1:
            return 0
        if naccactv in [0, 2]:
            return 1

        # only other case is 8 (initial visit only) which we return as-is
        return naccactv

    def _create_naccnurp(self) -> int:
        """Creates NACCNURP - Permanently moved to a nursing home.

        Looks at both Milestone and Form A1.

        NOTE: After discussion with RT, this is the agreed-upon behavior:
            By default always 0 (did not permenantly move to nursing home)
            Can only change (become 1) through an MLST form indicating PERMANENT move
            to a nursing home (RENURSE == 1)
                This can become a 0 if a later UDS has
                residenc != 4,9 (primary residence is nursing home or unknown)

                This can also become 0 if a subsequent MLST form EXPLICITLY sets
                RENURSE == 0 in a later MLST form
        """
        # get most recent MLST value of renurse
        renurse_record = self.__latest_working_value("milestone-renurse", int)

        # if MLST value (RENURSE/NURSEHOM) != 1, return 0
        if not renurse_record or renurse_record.value != 1:
            return 0

        # after this point assume renurse_record.value == 1
        # if a later UDS visit has residenc != null,4,9 then return 0
        if self.uds_came_after(renurse_record.date):
            residenc = self.__working_value("residenc", int)
            if residenc is not None and residenc in [4, 9]:
                return 0

        # since MLST set RENURSE == 1 and UDS did not override, return 1
        return 1

    def determine_discontinued_date(self, attribute: str, default: int) -> int:
        """Determine the discontinued date part; compare to UDS/NP.

        If UDS form came AFTER MLST, return the default (even if MLST
        said discontinued.
        """
        discyr = self.__working_value("milestone-discyr", int)
        discmo = self.__working_value("milestone-discmo", int)
        discday = self.__working_value("milestone-discday", int)
        uds_date = self.__get_latest_visitdate("uds-visitdates")

        # if UDS came after MLST, return default
        if date_came_after_sparse(uds_date, discyr, discmo, discday):
            return default

        # MLST is the latest (or only form, which technically isn't possible);
        # return whatever MLST set
        disc_date = self.__working_value(attribute, int)
        return disc_date if disc_date is not None else default

    def _create_naccdsdy(self) -> int:
        """Creates NACCDSDY - Day of discontinuation from annual follow-up."""
        return self.determine_discontinued_date("milestone-discday", 88)

    def _create_naccdsmo(self) -> int:
        """Creates NACCDSMO - Month of discontinuation from annual follow-up."""
        return self.determine_discontinued_date("milestone-discmo", 88)

    def _create_naccdsyr(self) -> int:
        """Creates NACCDSYR - Year of discontinuation from annual follow-up."""
        return self.determine_discontinued_date("milestone-discyr", 8888)

    def _create_nacccore(self) -> int:
        """Creates NACCCORE - Clinical core participant."""
        # cannot just check affiliate mainly because of mds_source possibly being 9
        mds_source = self.__working_value("mds-source", int)
        uds_source = self.__working_value("uds-source", int)
        uds_sourcenw = self.__working_value("uds-sourcenw", int)

        # UDS participant
        if uds_source != 4 and uds_sourcenw != 2 and mds_source is None:
            return 1

        # MDS participant
        if mds_source not in [3, 9] and uds_source is None and uds_sourcenw is None:
            return 1

        # use overall affiliate status as a fallback
        affiliate = self.__subject_derived.get_value("affiliate", bool)
        return 1 if not affiliate else 0
