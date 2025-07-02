"""Handles the MILESTONE form."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import FormNamespace
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import create_death_date


class MilestoneAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__milestone = FormNamespace(table=table, required=frozenset(["module"]))
        self.__deceased = self.__milestone.get_value("deceased", int)

        module = self.__milestone.get_required("module", str)
        if module.upper() != "MLST":
            msg = f"Current file is not a MLST form: found {module}"
            raise InvalidFieldError(msg)

    def _create_milestone_death_date(self) -> Optional[date]:
        """Create milestone death date."""
        if self.__deceased != 1:
            return None

        year = self.__milestone.get_value("deathyr", int)
        month = self.__milestone.get_value("deathmo", int)  # can be 99
        day = self.__milestone.get_value("deathdy", int)  # can be 99

        # if month and day unknown, converted to YYYY/07/01 (SAS)
        return create_death_date(year=year, month=month, day=day)

    def _create_milestone_death_month(self) -> Optional[int]:
        """Milestone death month - can be 99."""
        if self.__deceased != 1:
            return None

        month = self.__milestone.get_value("deathmo", int)

        try:
            if month is not None:
                month = int(month)
        except (ValueError, TypeError) as e:
            raise InvalidFieldError("Milestone DEATHMO not an integer") from e

        return month if month is not None else 99

    def _create_milestone_deceased(self) -> Optional[int]:
        """Milestone DECEASED."""
        return self.__deceased

    def _create_milestone_discontinued(self) -> bool:
        """Determine if subject is discontinued.

        This is a cross-sectional variable that could potentially be
        overrwritten by a subject rejoining the ADC at a later milestone
        form.
        """
        if self.__milestone.get_value("rejoin", int) == 1:
            return False

        return self.__milestone.get_value("discont", int) == 1

    def _create_milestone_protocol(self) -> Optional[int]:
        """Return the mielstone protocol."""
        return self.__milestone.get_value("protocol", int)
