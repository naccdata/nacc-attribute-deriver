from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import FormNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import create_death_date


class MilestoneAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__milestone = FormNamespace(table)

    def _create_milestone_death_date(self) -> Optional[date]:
        if not self.is_int_value(self.__milestone.get_value("deceased"), 1):
            return None

        year = self.__milestone.get_value("deathyr")
        month = self.__milestone.get_value("deathmo")  # can be 99
        day = self.__milestone.get_value("deathdy")  # can be 99

        return create_death_date(year=year, month=month, day=day)

    def _create_milestone_deceased(self) -> Optional[int]:
        return self.__milestone.get_value("deceased")
