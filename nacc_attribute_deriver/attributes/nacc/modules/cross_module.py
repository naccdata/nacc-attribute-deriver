"""Derived variables that rely on multiple modules."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.base_attribute import (
    SubjectDerivedAttribute,
)
from nacc_attribute_deriver.attributes.nacc.modules.uds.uds_attribute import (
    UDSAttribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_age,
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
        self.__uds = UDSAttribute(table)
        self.__subject_derived = SubjectDerivedAttribute(table)

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
        mds_deceased = self.is_int_value(
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
        if self.is_int_value(deceased, 1):
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
        mile_deceased = self.is_int_value(deceased, 1)

        # not reported as having died
        if not np_deceased and not mile_deceased:
            return 8

        # deceased but no NP data available
        if mile_deceased and not np_deceased:
            return 0

        # deceased with NP data available
        return 1
