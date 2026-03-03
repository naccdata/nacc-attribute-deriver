"""Handles the MILESTONE form.

Most of the NACC derived variable that use MILESTONE data are actually
cross-module and also need to be compared to other modules. As such, most of
the _create functions here are meant to keep track of when certain statuses
or events occured, and carry both that + the date of the MLST visit it was
denoted in over for cross_module derivation.

See attributes.derived.modules.cross_module.participant_status to see how
these end up being handled to determine a participant's status.
"""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    make_date_from_parts,
    standardize_date,
)
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)


class MilestoneAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__mlst = FormNamespace(table=table, required=frozenset(["module"]))
        self.__working = WorkingNamespace(table=table)

        module = self.__mlst.get_required("module", str)
        if module.upper() != "MLST":
            msg = f"Current file is not a MLST form: found {module}"
            raise InvalidFieldError(msg)

    def get_date(self) -> Optional[date]:
        return self.__mlst.get_date()

    def get_mlst_date(self) -> str:
        """Get date of this MLST visit as a string."""
        visitdate = self.__mlst.get_date()
        if not visitdate:
            raise AttributeDeriverError("Cannot determine visitdate for MLST visit")

        result = standardize_date(str(visitdate))
        if not result:
            raise AttributeDeriverError(
                f"Cannot standardize MLST visitdate: {visitdate}"
            )

        return result

    def __create_status_date(
        self, year_field: str, month_field: str, day_field: str
    ) -> str:
        """Create the date the status changed.

        If cannot be determined, return the MLST visit date.
        """
        year = self.__mlst.get_value(year_field, int)
        month = self.__mlst.get_value(month_field, int)
        day = self.__mlst.get_value(day_field, int)

        # make date from parts; if it cannot be made, return MLST date
        status_date = make_date_from_parts(year=year, month=month, day=day)
        if not status_date:
            return self.get_mlst_date()

        return status_date

    def _create_milestone_discontinued_date(self) -> Optional[str]:
        """Check if subject is discontinued; if so, create the discontinued
        date."""
        # discontinued can be determined by DISCONT = 1 or, for V1
        # only, UDSACTIV = 4
        discont = self.__mlst.get_value("discont", int)
        udsactiv = self.__mlst.get_value("udsactiv", int)

        # not discontinued; return None
        if discont != 1 and udsactiv != 4:
            return None

        # DISCDY is DISCDAY in some forms, so check
        day_field = "discdy"
        if self.__mlst.get_value(day_field, int) is None:
            day_field = "discday"

        return self.__create_status_date("discyr", "discmo", day_field)

    def _create_milestone_death_date(self) -> Optional[str]:
        """Check if subject died; if so, create deceased date."""
        deceased = self.__mlst.get_value("deceased", int)

        # not dead
        if deceased != 1:
            return None

        return self.__create_status_date("deathyr", "deathmo", "deathdy")

    def _create_milesetone_renurse_date(self) -> Optional[str]:
        """Check if subject moved to a permenant nursing home; if so, create
        renurse date."""
        renurse = self.__mlst.get_value("renurse", int)
        if renurse is None:
            renurse = self.__mlst.get_value("nursehom", int)

        # no nursing home, return None
        if renurse != 1:
            return None

        return self.__create_status_date("nurseyr", "nursemo", "nursedy")

    def get_change_date(self) -> str:
        """Get the date of the status change. Used to denote when REJOIN or
        PROTOCOl was set.

        The CHANGEx variables are only available in V3. If not provided,
        default to the MLST visitdate.
        """
        return self.__create_status_date("changeyr", "changemo", "changedy")

    def _create_milestone_rejoined_date(self) -> Optional[str]:
        """Check if subject rejoined; if so, create the rejoined date."""
        # rejoined can only be determined by REJOIN/REJOINED = 1
        # on the MLST form
        rejoin = self.__mlst.get_value("rejoin", int)
        if rejoin is None:
            rejoin = self.__mlst.get_value("rejoined", int)

        # not rejoined, return None
        if rejoin != 1:
            return None

        return self.get_change_date()

    def _create_milestone_minimum_contact_date(self) -> Optional[str]:
        """Check if subject was set to minimum contact; based on
        PROTOCOL = 2 or UDSACTIV = 3."""
        protocol = self.__mlst.get_value("protocol", int)
        udsactiv = self.__mlst.get_value("udsactiv", int)

        # set to minimum contact, return change date
        if protocol == 2 or udsactiv == 3:
            return self.get_change_date()

        # not minimum contact, return None
        return None
