"""Derived variables that rely on multiple modules."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    calculate_months,
    date_came_after,
    date_came_after_sparse,
    date_from_form_date,
)
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
)


class CrossModuleAttributeCollection(AttributeCollection):
    """Class to collect cross-module attributes.

    Based from the UDS Attributes.
    """

    def __init__(
        self,
        table: SymbolTable,
    ) -> None:
        """Override initializer to set other module prefixes."""
        self.__uds = UDSNamespace(table)
        self.__working = WorkingDerivedNamespace(
            table=table, required=frozenset(["cross-sectional.uds-visitdates"])
        )
        self.__subject_derived = SubjectDerivedNamespace(table=table)

    def _determine_death_date(self) -> Optional[date]:
        """Determines the death status, and returns the death date if found.

        Checks the following forms in order:
            - NP
            - Milestone
            - MDS

        Returns:
            Death date if found, None otherwise
        """
        np_date = self.__working.get_cross_sectional_value("np-death-date", str)
        death_date = date_from_form_date(np_date)
        if death_date:
            return death_date

        milestone_date = self.__working.get_cross_sectional_value(
            "milestone-death-date", str
        )
        death_date = date_from_form_date(milestone_date)
        if death_date:
            return death_date

        mds_date = self.__working.get_cross_sectional_value("mds-death-date", str)
        death_date = date_from_form_date(mds_date)
        if death_date:
            return death_date

        return None

    def _create_naccdage(self) -> int:
        """From derive.sas and derivenew.sas."""
        # check that subject is deceased at all
        mds_deceased = self.is_target_int(
            self.__working.get_cross_sectional_value("mds-vital-status", int), 2
        )
        if self._create_naccdied() == 0 and not mds_deceased:
            return 888

        # NP, grab from NPDAGE
        npdage = self.__working.get_cross_sectional_value("np-death-age", int)
        if npdage:
            return npdage

        # otherwise calculate from DOB/DOD
        birth_date = self.__uds.generate_uds_dob()
        death_date = self._determine_death_date()

        if not birth_date or not death_date:
            return 999

        age = calculate_age(birth_date, death_date)
        if not age:
            return 999

        return age

    def _create_naccdied(self) -> int:
        """Creates NACCDIED - determined if death
        has been reported by NP or Milestone form.
        """
        death_age = self.__working.get_cross_sectional_value("np-death-age", int)
        if death_age is not None:
            return 1

        deceased = self.__working.get_cross_sectional_value("milestone-deceased", int)
        if self.is_target_int(deceased, 1):
            return 1

        return 0

    def _create_naccautp(self) -> int:
        """Creates NACCAUTP - similar to NACCDIED but also
        needs to differentiate if an NP form was submitted
        or not.
        """
        death_age = self.__working.get_cross_sectional_value("np-death-age", int)
        deceased = self.__working.get_cross_sectional_value("milestone-deceased", int)
        np_deceased = death_age is not None
        mile_deceased = self.is_target_int(deceased, 1)

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
        deathdate = self._determine_death_date()

        # not dead
        if naccdied != 1:
            return 888

        # died but no/unknown death age
        if naccdied == 1 and not deathdate:
            return 999

        # compare to last UDS visit
        visitdates = self.__working.get_cross_sectional_value("uds-visitdates", list)

        # a non-valid visitdate shouldn't be possible but handle just in case
        if not visitdates:
            return 999

        last_visit = date_from_form_date(sorted(list(visitdates))[-1])
        if not last_visit:
            return 999

        result = calculate_months(last_visit, deathdate)

        # handle negative
        return 999 if result is None or result < 0 else result

    # Tried to use all things described in the rdd-np. Many seemed not
    # in the SAS code. Not sure if the MDS "vitalst" is passed through or not.
    def _create_naccmod(self) -> int:
        """Create the NACCMOD variable.

        Month of death. In Milestone and MDS, the month can be unknown
        (99) so need to inspect directly.
        """
        # check vital status
        naccdied = self._create_naccdied()
        if not naccdied:
            return 88

        # NP will always have a known month
        np_date = self.__working.get_cross_sectional_value("np-death-date", str)
        death_date = date_from_form_date(np_date)
        if death_date:
            return death_date.month

        # Milestone month may be 99
        milestone_mo = self.__working.get_cross_sectional_value(
            "milestone-death-month", int
        )
        if milestone_mo is not None and milestone_mo != 99:
            return milestone_mo

        # MDS death month may be 99
        mds_mo = self.__working.get_cross_sectional_value("mds-death-month", int)
        if mds_mo is not None and mds_mo != 99:
            return mds_mo

        return 99

    # SAS seemingly sparse for this. Another one with potential MDS.
    def _create_naccyod(self) -> int:
        """Create the NACCYOD variable.

        Year of death.
        """
        # year always defined if death date exists, even for MDS
        deathdate = self._determine_death_date()

        # Explicitly states in rdd-np that this shouldn't precede 1970.
        # Previously not mentioned in SAS code.
        if deathdate:
            return deathdate.year if (deathdate.year >= 1970) else 9999

        if self._create_naccdied() == 1:
            return 9999

        return 8888

    def uds_came_after(self, target_date: date | None) -> bool:
        """Compares UDS and given target dates.

        Returns:
            True: If UDS > target date
            False: If UDS <= target_date
        """
        uds_date = self.__uds.get_date()
        if not uds_date:
            raise AttributeDeriverError(
                "Cannot determine UDS date to compare to MLST form"
            )

        return date_came_after(uds_date, target_date)

    def _create_naccactv(self) -> int:
        """Creates NACCACTV - Follow-up status at the Alzheimer's
        Disease Center (ADC)

        Codes:
            0: If subject receives no followup contact (dead, discontinued,
                or enrolled as initial visit only)
                8: Returns 8 specifically if enrolled as initial visit only.
                    NACCACTVS casts this back to 0, NACCNOVS returns it as 8
            1: If subject is under annual followup and expected to make more
                Includes discontinued subjects who have since rejoined
                - This seems to also include subject who have not explicitly
                    been stated to have rejoined (via MLST form) BUT have
                    UDS visits after the date of the discontinued MLST form
            2: Minimal contact with ADC but still enrolled
        """
        # if dead, return 0
        if self._create_naccdied() == 1:
            return 0

        # if milestone marked subject as discontinued, and is the latest form,
        # return 0. if there were UDS visits after discontinuation was marked,
        # return 1
        mlst_discontinued = self.__working.get_cross_sectional_dated_value(
            "milestone-discontinued.latest", int
        )
        if mlst_discontinued and mlst_discontinued.value == 1:
            if self.uds_came_after(mlst_discontinued.date):
                return 1

            return 0

        # if UDS A1 prespart == 1 (initial evaluation only), return 0
        if self.__uds.get_value("prespart", int) == 1:
            return 0

        # 5 used for affiliates in SAS/R code
        if self.__subject_derived.get_cross_sectional_value("affiliate", bool):
            return 5

        # check milestone protocol
        protocol = self.__working.get_cross_sectional_value("milestone-protocol", int)

        # if protocol == 1 or 3, annual followup expected
        if protocol in [1, 3]:
            return 1
        # protocol == 2 is minimal contact
        if protocol == 2:
            return 2

        # protocol == 1 or 3, or just using 1 by default since this is an UDS
        # visit and we didn't hit any of the above non-active conditions
        # This also handles the case where they had prespart == 1 at initial
        # visits but then continued to have followup visits
        return 1

    def _create_naccnovs(self) -> int:
        """Creates NACCNOVS - No longer followed annually in person or by
        telephone. This is ultimately just checking the same things
        NACCACTV is and reinterprets results.
        """
        # if UDS is the latest one, check UDS prespart == 1 to return 8,
        # otherwise purely based on MLST
        mlsts = self.__working.get_cross_sectional_value("milestone-visitdates", list)
        if mlsts:
            most_recent_mlst = date_from_form_date(mlsts[-1])
            if (
                self.uds_came_after(most_recent_mlst)
                and self.__uds.get_value("prespart", int) == 1
            ):
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
            By default always 0
            Can only change (become 1) through an MLST form indicating PERMANENT move
            to a nursing home (RENURSE == 1)
                This can become a 0 if a later UDS has
                residenc != 4,9 (primary residence is nursing home or unknown)

                This can also become 0 if a subsequent MLST form EXPLICITLY sets
                RENURSE == 0 in a later MLST form
        """
        # get most recent MLST value of renurse
        renurse_record = self.__working.get_cross_sectional_dated_value(
            "milestone-renurse.latest", int
        )

        # if MLST value (RENURSE) is NOT 1, return 0
        if not renurse_record or renurse_record.value != 1:
            return 0

        # after this point assume renurse_record.value == 1
        # if a later UDS visit has residenc != null,4,9 then return 0
        if self.uds_came_after(renurse_record.date):
            residenc = self.__uds.get_value("residenc", int)
            if residenc is not None and residenc in [4, 9]:
                return 0

        # since MLST set RENURSE == 1 and UDS did not override, return 1
        return 1

    def determine_discontinued_date(self, attribute: str, default: int) -> int:
        """Determine the discontinued date part; compare to UDS/NP.

        If UDS form came AFTER MLST, return the default (even if MLST
        said discontinued.
        """
        discyr = self.__working.get_cross_sectional_value(
            "milestone-discyr.latest.value", int
        )
        discmo = self.__working.get_cross_sectional_value(
            "milestone-discmo.latest.value", int
        )
        discday = self.__working.get_cross_sectional_value(
            "milestone-discday.latest.value", int
        )

        uds_date = self.__uds.get_date()

        if not uds_date:
            raise AttributeDeriverError(
                "Cannot determine UDS date to compare to MLST form"
            )

        # if UDS came after MLST, return default
        if date_came_after_sparse(uds_date, discyr, discmo, discday):
            return default

        # MLST is the latest; return whatever MLST set
        disc_date = self.__working.get_cross_sectional_value(attribute, int)
        return disc_date if disc_date is not None else default

    def _create_naccdsdy(self) -> int:
        """Creates NACCDSDY - Day of discontinuation from annual follow-up."""
        return self.determine_discontinued_date("milestone-discday.latest.value", 88)

    def _create_naccdsmo(self) -> int:
        """Creates NACCDSMO - Month of discontinuation from annual follow-up."""
        return self.determine_discontinued_date("milestone-discmo.latest.value", 88)

    def _create_naccdsyr(self) -> int:
        """Creates NACCDSYR - Year of discontinuation from annual follow-up."""
        return self.determine_discontinued_date("milestone-discyr.latest.value", 8888)
