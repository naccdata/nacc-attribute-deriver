"""Derived variables that rely on multiple modules."""
from datetime import datetime
from typing import Any

from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import calculate_age

from .uds.uds_attribute import UDSAttribute


class CrossModuleAttribute(UDSAttribute):
    """Class to collect cross-module attributes.

    Based from the UDS Attributes.
    """

    def __init__(self,
                 table: SymbolTable,
                 form_prefix: str = 'file.info.forms.json.',
                 np_prefix: str = 'file.info.np.',
                 mds_prefix: str = 'file.info.mds.',
                 mile_prefix: str = 'file.info.milestone.') -> None:
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

    # death status
    def _determine_death_np(self):
        """Determines the death status given the NP form."""

    def _create_naccdage(self) -> int:
        """From derive.sas and derivenew.sas.

        Grabs data from NP -> MDS -> UDS forms. This might not be totally correct.

        Location:
            file.info.derived.naccdage
        Operation:
            update
        Type:
            cross-sectional
        Description:
            Age at death
        """
        # NP
        npdage = self.get_np_value('npdage')
        if npdage:
            return npdage

        dod = None

        # MDS
        if self.get_mds_value('deceased') == 1:
            dyr = self.get_mds_value('deathyr')
            dmo = self.get_mds_value('deathmo')
            ddy = self.get_mds_value('deathdy')
            dod = datetime(dyr, dmo, ddy)

        # UDS
        dob = self.generate_uds_dob()

        if not dod or not dob:
            return 999

        age = calculate_age(dob, dod)
        if not age:
            return 888

        return age

    def _create_naccdied(self) -> int:
        """Creates NACCDIED from NP and/or milestone form.
        Defaults to 0 for unknown.

        Location:
            file.info.derived.naccdied
        Operation:
            update
        Type:
            cross-sectional
        Description:
            Subject is known to be deceased
        """


