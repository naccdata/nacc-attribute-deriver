"""Handles the MILESTONE form.

Most of the NACC derived variable that use MILESTONE data are actually
cross-form and also need to be compared to UDS values. As such, most of
the _create functions here are meant to carry over values to later be
evaluated under the UDS scope under `CrossModuleAttributeCollection` in
`cross_module.py`
"""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
    SubjectDerivedNamespace,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import create_death_date
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)


class MilestoneAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__milestone = FormNamespace(table=table, required=frozenset(["module"]))
        self.__working = WorkingNamespace(table=table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

        self.__deceased = self.__milestone.get_value("deceased", int)

        module = self.__milestone.get_required("module", str)
        if module.upper() != "MLST":
            msg = f"Current file is not a MLST form: found {module}"
            raise InvalidFieldError(msg)

    def get_date(self) -> date:
        """Get the MLST date - needed to let RENURSE be dated."""
        visitdate = self.__milestone.get_date()
        if not visitdate:
            raise AttributeDeriverError("Cannot determine visitdate for MLST visit")

        return visitdate

    def _create_milestone_visitdates(self) -> str:
        """UDS needs to know if MLST exists - if this is called,
        return visitdate."""
        return str(self.get_date())

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

    def _create_milestone_discontinued(self) -> Optional[int]:
        """Determine if subject is discontinued.

        This is a working variable used to derive NACCACTV, which could be
        overrwritten by a subject rejoining the ADC at a later milestone
        form or having subsequent UDS visit, so needs to be checked
        in cross_module logic. Note if this function returns None,
        it will not update/override anything a previous MLST form set.

        Note we are not including minimal contact in this variable
        (unlike discontinued date) because NACCACTV needs to separate
        discontinued (generally) vs minimal contact, unlike the discontinued
        dates which sort of conflate the two. So this variable is
        really just letting NACCACTV know that the subject was explicitly
        marked as dicontinued.
        """
        rejoin = self.__milestone.get_value("rejoin", int)
        if rejoin is None:
            rejoin = self.__milestone.get_value("rejoined", int)

        if rejoin == 1:
            return 0

        return self.__milestone.get_value("discont", int)

    def _create_milestone_protocol(self) -> Optional[int]:
        """Return the milestone protocol.

        This is used in V2/V3.
        """
        return self.__milestone.get_value("protocol", int)

    def _create_milestone_udsactiv(self) -> Optional[int]:
        """Return the milestone udsactv.

        This is used in V1.
        """
        return self.__milestone.get_value("udsactiv", int)

    def get_discontinued_date_part(
        self, attribute: str, change_part: str, visit_part: str
    ) -> int:
        """Get subject discontinued date part. Either explicitly set as
        discontinued, or minimum contact/followed to autopsy.

        If active or rejoined, return 88 instead.

        If minimal contact (PROTOCOL = 2 or UDSACTIV = 3), then use
        CHANGEX or VISITX dates as discontinued date.
        """
        default = 88 if attribute != "discyr" else 8888

        if (
            self.__milestone.get_value("rejoin", int) == 1
            or self.__milestone.get_value("rejoined", int) == 1
        ):
            return default

        # either explicitly discontinued or minimum contact
        discont = self.__milestone.get_value("discont", int)
        protocol = self.__milestone.get_value("protocol", int)  # V2/V3
        udsactiv = self.__milestone.get_value("udsactiv", int)  # V1

        if discont == 1 or protocol == 2 or udsactiv in [3, 4]:
            for field in [attribute, change_part, visit_part]:
                disc_date = self.__milestone.get_value(field, int)
                if disc_date is not None:
                    return disc_date

        # check if already set; these are written to working since
        # they need to be compared against UDS visits later
        existing_value = self.__working.get_cross_sectional_value(
            f"milestone-{attribute}", int
        )
        if existing_value is not None:
            return existing_value

        return default

    def _create_milestone_discday(self) -> int:
        """Carry over DISCDAY (DISCDY in newer versions)

        - Day of discontinuation from annual follow-up.

        Used for NACCDSDY, but can potentially be overwritten by a later
        UDS visit - see
            cross_module._create_naccdsdy
        """
        # may be discday or discdy; see if discdy (V4) version exists,
        # otherwise default to discday
        field = "discdy"
        if self.__milestone.get_value(field, int) is None:
            field = "discday"

        result = self.get_discontinued_date_part(field, "changedy", "visitday")
        if result == 99:  # could be set to 99 by CHANGEDY
            return 88

        return result

    def _create_milestone_discmo(self) -> int:
        """Carry over DISCMO - Month of discontinuation from annual follow-up.

        Used for NACCDSMO, but can potentially be overwritten by a later
        UDS visit - see
            cross_module._create_naccdsmo
        """
        result = self.get_discontinued_date_part("discmo", "changemo", "visitmo")
        if result == 99:  # could be set to 99 by CHANGEMO
            return 88

        return result

    def _create_milestone_discyr(self) -> int:
        """Carry over DISCYR - Year of discontinuation from annual follow-up.

        Used for NACCDSYR, but can potentially be overwritten by a later
        UDS visit - see
            cross_module._create_naccdsyr
        """
        result = self.get_discontinued_date_part("discyr", "changeyr", "visityr")

        # in this case we do set a minimum of 2005 per RDD
        return max(2005, result)

    def get_nursing_home_date_part(self, attribute: str, derived_attribute: str) -> int:
        """Get subject moved to nursing home date part."""
        default = 88 if attribute != "nurseyr" else 8888

        result = self.__milestone.get_value(attribute, int)
        if result is not None:
            return result

        # check if already set; pulls directly from derived variables
        # since independent of other scopes (e.g. UDS)
        existing_value = self.__subject_derived.get_cross_sectional_value(
            derived_attribute, int
        )
        if existing_value is not None:
            return existing_value

        return default

    def _create_naccnrdy(self) -> int:
        """Creates NACCNRDY - Day permanently moved to nursing home."""
        return self.get_nursing_home_date_part("nursedy", "naccnrdy")

    def _create_naccnrmo(self) -> int:
        """Creates NACCNRMO - Month permanently moved to nursing home."""
        return self.get_nursing_home_date_part("nursemo", "naccnrmo")

    def _create_naccnryr(self) -> int:
        """Creates NACCNRYR - Year permanently moved to nursing home."""
        result = self.get_nursing_home_date_part("nurseyr", "naccnryr")

        # in this case we do set a minimum of 2002 per RDD
        return max(2002, result)

    def _create_milestone_renurse(self) -> Optional[int]:
        """Determine RENURSE (NURSEHOM in older versions), needs to be dated to
        compute NACCNURP.

        Note if this function returns None, it will not update/override
        anything a previous MLST form set.
        """
        renurse = self.__milestone.get_value("renurse", int)
        if renurse is None:
            renurse = self.__milestone.get_value("nursehom", int)

        # if RENURSE/NURSEHM both undefined, see if they set
        # NURSEDY, NURSEMO, NURSEYR
        if renurse is None:
            nurse_vars = [
                self.__milestone.get_value(x, int)
                for x in ["nursedy", "nursemo", "nurseyr"]
            ]
            if all(x is not None and x not in [88, 8888] for x in nurse_vars):
                return 1

        return renurse
