"""Handles the MILESTONE form."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    FormNamespace,
    SubjectDerivedNamespace,
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.schema.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import create_death_date


class MilestoneAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__milestone = FormNamespace(table=table, required=frozenset(["module"]))
        self.__working = WorkingDerivedNamespace(table=table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

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

    def get_discontinued_date_part(self, attribute: str, frmdate: str) -> int:
        """Get subject discontinued date part.

        If active or rejoined, return 88 instead.
        """
        default = 88 if attribute != "discyr" else 8888

        if self.__milestone.get_value("rejoin", int) == 1:
            return default

        if self.__milestone.get_value("discont", int) == 1:
            result = self.__milestone.get_value(attribute, int)
            if result is not None:
                return result

        # if minimal contact, return the form's date
        if self.__milestone.get_value("protocol", int) == 2:
            result = self.__milestone.get_value(frmdate, int)
            if result is not None:
                return result

        # check if already set
        existing_value = self.__subject_derived.get_cross_sectional_value(
            attribute, int
        )
        if existing_value is not None:
            return existing_value

        return default

    def _create_naccdsdy(self) -> int:
        """Creates NACCDSDY - Day of discontinuation from annual follow-up."""
        return self.get_discontinued_date_part("discday", "visitday")

    def _create_naccdsmo(self) -> int:
        """Creates NACCDSMO - Month of discontinuation from annual follow-up."""
        return self.get_discontinued_date_part("discmo", "visitmo")

    def _create_naccdsyr(self) -> int:
        """Creates NACCDSYR - Year of discontinuation from annual follow-up."""
        result = self.get_discontinued_date_part("discyr", "visityr")

        # in this case we do set a minimum of 2005 per RDD
        return max(2005, result)

    def get_nursing_home_date_part(self, attribute: str) -> int:
        """Get subject moved to nursing home date part."""
        default = 88 if attribute != "nurseyr" else 8888

        # TODO - there are some forms where renurse is not
        # defined but the attribute is - technically not supposed
        # to happen but for sake of consistency don't check for now?
        # if self.__milestone.get_value("renurse", int) != 1:
        #     return default

        result = self.__milestone.get_value(attribute, int)
        if result is not None:
            return result

        return default

    def _create_naccnrdy(self) -> int:
        """Creates NACCNRDY - Day permanently moved to nursing home."""
        return self.get_nursing_home_date_part("nursedy")

    def _create_naccnrmo(self) -> int:
        """Creates NACCNRMO - Month permanently moved to nursing home."""
        return self.get_nursing_home_date_part("nursemo")

    def _create_naccnryr(self) -> int:
        """Creates NACCNRYR - Year permanently moved to nursing home."""
        result = self.get_nursing_home_date_part("nurseyr")

        # in this case we do set a minimum of 2002 per RDD
        return max(2002, result)

    def _create_milestone_renurse(self) -> int:
        """Carryover RENURSE, needs to be longitudinally dated to compute
        NACCNURP.

        Use -4 for Nones so this is forcefully carried over.
        """
        result = self.__milestone.get_value("renurse", int)
        return result if result is not None else -4

    def get_date(self) -> date:
        """Get the MLST date - needed to let RENURSE be dated."""
        visitdate = self.__milestone.get_date()
        if not visitdate:
            raise AttributeDeriverError("Cannot determine visitdate for MLST visit")

        return visitdate
