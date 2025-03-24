from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.base_attribute import FormAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import create_death_date


class MDSFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        self.__mds = FormAttribute(table)

    def _create_mds_death_date(self) -> Optional[date]:
        if not self.is_int_value(self.__mds.get_value("vitalst"), 2):
            return None

        year = self.__mds.get_value("deathyr")  # can be 9999
        month = self.__mds.get_value("deathmo")  # can be 99
        day = self.__mds.get_value("deathday")  # can be 99

        return create_death_date(year=year, month=month, day=day)

    def _create_mds_vitalst(self) -> int:
        return self.__mds.get_value("vitalst")
