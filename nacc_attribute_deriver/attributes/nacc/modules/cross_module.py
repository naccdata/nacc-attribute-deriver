"""Derived variables that rely on multiple modules."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)

# from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    calculate_interval,
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
        self.__subject_derived = SubjectDerivedNamespace(table)

    def _determine_death_date(self) -> Optional[date]:
        """Determines the death status, and returns the death date if found.

        Checks the following forms in order:
            - NP
            - Milestone
            - MDS

        Returns:
            Death date if found, None otherwise
        """
        np_date = self.__subject_derived.get_value("np_death_date")
        death_date = datetime_from_form_date(np_date)
        if death_date:
            return death_date.date()

        milestone_date = self.__subject_derived.get_value("milestone_death_date")
        death_date = datetime_from_form_date(milestone_date)
        if death_date:
            return death_date.date()

        mds_date = self.__subject_derived.get_value("mds_death_date")
        death_date = datetime_from_form_date(mds_date)
        if death_date:
            return death_date.date()

        return None

    def _create_naccdage(self) -> int:
        """From derive.sas and derivenew.sas."""
        # check that subject is deceased at all
        mds_deceased = self.is_target_int(
            self.__subject_derived.get_value("mds_vital_status"), 2
        )
        if self._create_naccdied() == 0 and not mds_deceased:
            return 888

        # NP, grab from NPDAGE
        npdage = self.__subject_derived.get_value("np_death_age")
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
        death_age = self.__subject_derived.get_value("np_death_age")
        if death_age is not None:
            return 1

        deceased = self.__subject_derived.get_value("milestone_deceased")
        if self.is_target_int(deceased, 1):
            return 1

        return 0

    def _create_naccautp(self) -> int:
        """Creates NACCAUTP - similar to NACCDIED but also
        needs to differentiate if an NP form was submitted
        or not.
        """
        death_age = self.__subject_derived.get_value("np_death_age")
        deceased = self.__subject_derived.get_value("milestone_deceased")
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
        self.__subject_derived.assert_required(["uds-visitdates"])
        visitdates = self.__subject_derived.get_value("uds-visitdates")

        # a non-valid visitdate shouldn't be possible but handle just in case
        if not visitdates:
            return 999

        last_visit = datetime_from_form_date(sorted(list(visitdates))[-1])
        if not last_visit:
            return 999

        result = calculate_interval(last_visit.date(), deathdate)

        # handle negative
        return 999 if result is None or result < 0 else result

    # def _create_affiliate(self) -> bool:
    #     """Returns whether or not this is an affiliated participant.
    #     Looks for sourcenw != 1 in UDS or source != (1, 2, 3) in MDS.
    #     """
    #     if self.__uds.normalized_formver() in [1, 2]:
    #         source = self.__uds.get('source'):
    #         if source is not None:
    #             try:
    #                 return int(source) == 4
    #             except (TypeError, ValueError):
    #                 pass

    #     sourcenw = self.__uds.get('sourcenw')
    #     if sourcenw is not None:
    #         try:
    #             return int(sourcenw) == 2
    #         except (TypeError, ValueError):
    #             pass

    #     mds_source = self.__subject_derived.get_value("mds_source")
    #     if mds_source is not None:
    #         try:
    #             return int(source) not in [1, 2, 3]
    #         except (TypeError, ValueError):
    #             pass

    #     raise MissingRequiredError(
    #         "Cannot determine participant affiliated status")
