"""Derived variables that rely on multiple modules."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    calculate_months,
    datetime_from_form_date,
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
        death_date = datetime_from_form_date(np_date)
        if death_date:
            return death_date.date()

        milestone_date = self.__working.get_cross_sectional_value(
            "milestone-death-date", str
        )
        death_date = datetime_from_form_date(milestone_date)
        if death_date:
            return death_date.date()

        mds_date = self.__working.get_cross_sectional_value("mds-death-date", str)
        death_date = datetime_from_form_date(mds_date)
        if death_date:
            return death_date.date()

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

        last_visit = datetime_from_form_date(sorted(list(visitdates))[-1])
        if not last_visit:
            return 999

        result = calculate_months(last_visit.date(), deathdate)

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
        death_date = datetime_from_form_date(np_date)
        if death_date:
            return death_date.date().month

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
