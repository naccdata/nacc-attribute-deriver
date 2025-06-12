from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import FormNamespace
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import create_death_date


class MDSFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        self.__mds = FormNamespace(table=table, required=frozenset(["vitalst"]))

        self.__vitalst = self.__mds.get_required("vitalst", int)

    def _create_mds_death_date(self) -> Optional[date]:
        """MDS death date; can be unknown."""
        if self.__vitalst != 2:
            return None

        year = self.__mds.get_value("deathyr", int)  # can be 9999
        month = self.__mds.get_value("deathmo", int)  # can be 99
        day = self.__mds.get_value("deathday", int)  # can be 99

        return create_death_date(year=year, month=month, day=day)

    def _create_mds_death_month(self) -> Optional[int]:
        """MDS death month - can be 99."""
        if self.__vitalst != 2:
            return None

        month = self.__mds.get_value("deathmo", int)

        try:
            if month is not None:
                month = int(month)
        except (ValueError, TypeError) as e:
            raise InvalidFieldError("MDS DEATHMO not an integer") from e

        return month if month is not None else 99

    def _create_mds_vitalst(self) -> int:
        """MDS VITALST."""
        return self.__vitalst
