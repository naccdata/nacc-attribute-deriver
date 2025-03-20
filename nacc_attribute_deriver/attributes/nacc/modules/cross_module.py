"""Derived variables that rely on multiple modules."""

from datetime import datetime
from typing import Any, Optional

from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    datetime_from_form_date,
)

from .uds.uds_attribute import UDSAttribute


class CrossModuleAttribute(UDSAttribute):
    """Class to collect cross-module attributes.

    Based from the UDS Attributes.
    """

    def __init__(
        self,
        table: SymbolTable,
        form_prefix: str = "file.info.forms.json.",
        np_prefix: str = "file.info.np.",
        mds_prefix: str = "file.info.mds.",
        mile_prefix: str = "file.info.milestone.",
    ) -> None:
        """Override initializer to set other module prefixes."""
        super().__init__(table, form_prefix)
        self.__np_prefix = np_prefix
        self.__mds_prefix = mds_prefix
        self.__mile_prefix = mile_prefix

    def get_np_value(self, key: str, default: Any = None) -> Any:
        """Get NP-specific value.

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
        """
        return self.get_value(key, default, prefix=self.__np_prefix)

    def get_mds_value(self, key: str, default: Any = None) -> Any:
        """Get MDS-specific value.

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
        """
        return self.get_value(key, default, prefix=self.__mds_prefix)

    def get_mile_value(self, key: str, default: Any = None) -> Any:
        """Get Milestone-specific value.

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
        """
        return self.get_value(key, default, prefix=self.__mile_prefix)

    def _determine_death_date(self) -> Optional[datetime]:
        """Determines the death status, and returns the death date if found.

        Checks the following forms in order:
            - NP
            - Milestone
            - MDS

        Returns:
            Death date if found, None otherwise
        """
        found = False
        dyr, dmo, ddy = None, None, None

        # NP form - all seem required but check on NPDAGE anyways
        if self.get_np_value("npdage") is not None:
            dyr = self.get_np_value("npdodyr")
            dmo = self.get_np_value("npdodmo")
            ddy = self.get_np_value("npdoddy")
            if dyr and dmo and ddy:
                found = True

        # Milestone form - DECEASED == 1 == Subject has died
        if not found and self.get_mile_value("deceased") in [1, "1"]:
            dyr = self.get_mile_value("deathyr")
            dmo = self.get_mile_value("deathmo")  # can be 99
            ddy = self.get_mile_value("deathdy")  # can be 99
            if dyr and dmo and ddy:
                found = True

        # MDS form - VITALST == 2 == Dead
        if not found and self.get_mds_value("vitalst") in [2, "2"]:
            dyr = self.get_mds_value("deathyr")  # can be 9999
            dmo = self.get_mds_value("deathmo")  # can be 99
            ddy = self.get_mds_value("deathday")  # can be 99
            if dyr and dmo and ddy:
                found = True

        if not found or dyr in ["9999", 9999]:
            return None

        # cast to ints and handle unknown dates
        try:
            dyr = int(dyr) if dyr else dyr
            dmo = int(dmo) if dmo else dmo
            ddy = int(ddy) if ddy else ddy

            if dyr and dyr != 9999:
                if not dmo or dmo > 12:
                    dmo = 7
                if not ddy or ddy > 31:
                    ddy = 1
        except (TypeError, ValueError):
            return None

        death_date = f"{dyr}-{dmo:02d}-{ddy:02d}"
        return datetime_from_form_date(death_date)

    def _create_naccdage(self) -> int:
        """From derive.sas and derivenew.sas."""
        # check that subject is deceased at all
        mds_deceased = self.get_mds_value("vitalst") in [2, "2"]
        if self._create_naccdied() == 0 and not mds_deceased:
            return 888

        # NP, grab from NPDAGE
        npdage = self.get_np_value("npdage")
        if npdage:
            return npdage

        # otherwise calculate from DOB/DOD
        birth_date = self.generate_uds_dob()
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
        if self.get_np_value("npdage") is not None or self.get_mile_value(
            "deceased"
        ) in [1, "1"]:
            return 1

        return 0

    def _create_naccautp(self) -> int:
        """Creates NACCAUTP - similar to NACCDIED but also
        needs to differentiate if an NP form was submitted
        or not.
        """
        np_deceased = self.get_np_value("npdage") is not None
        mile_deceased = self.get_mile_value("deceased") in [1, "1"]

        # not reported as having died
        if not np_deceased and not mile_deceased:
            return 8

        # deceased but no NP data available
        if mile_deceased and not np_deceased:
            return 0

        # deceased with NP data avaiable
        return 1
