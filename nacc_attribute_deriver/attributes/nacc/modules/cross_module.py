"""Derived variables that rely on multiple modules."""
from datetime import datetime
from typing import Any

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

    def __init__(self,
                 table: SymbolTable,
                 form_prefix: str = 'file.info.forms.json.',
                 np_prefix: str = 'np.info.forms.json.',
                 mds_prefix: str = 'mds.info.forms.json.') -> None:
        """Override initializer to set other module prefixdes."""
        super().__init__(table, form_prefix)
        self.__np_prefix = np_prefix
        self.__mds_prefix = mds_prefix

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
        dod = None
        # NP
        npdage = self.get_np_value('npdage')
        if npdage:
            dod = datetime_from_form_date(npdage)

        # milestone
        if not dod and self.get_mds_value('deceased') == 1:
            dyr = self.get_mds_value('deathyr')
            dmo = self.get_mds_value('deathmo')
            ddy = self.get_mds_value('deathdy')
            dod = datetime(dyr, dmo, ddy)

        # UDS
        # looks like looking at UDS is just for NACCINT?
        dob = self.generate_uds_dob()

        if not dod or not dob:
            return 999

        age = calculate_age(dob, dod)
        if not age:
            return 888

        return age
