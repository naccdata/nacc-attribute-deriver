"""Derived variables that come from the header variables."""

import datetime
from typing import Any, List, Optional

from nacc_attribute_deriver.attributes.base.namespace import (
    SubjectDerivedNamespace,
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.schema.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_days,
    datetime_from_form_date,
)

from .uds_attribute_collection import UDSAttributeCollection


class UDSHeaderAttributeCollection(UDSAttributeCollection):
    """Class to collect UDS header attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__working = WorkingDerivedNamespace(table=table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

    def get_current_visitdate(self) -> datetime.date:
        """Creates the current visit's date."""
        raw_visitdate = self.uds.get_required("visitdate", str)
        visitdate = datetime_from_form_date(raw_visitdate)

        if not visitdate:
            raise InvalidFieldError(f"Failed to parse visitdate: {raw_visitdate}")

        return visitdate.date()

    def _create_uds_visitdate(self) -> str:
        """Gets the visitdate - temporary derived variable."""
        return str(self.get_current_visitdate())

    def get_visitdates(self) -> List[datetime.date]:
        """Get all UDS visits.

        Adds the current UDS visit if not already there, but generally
        expects that to have been curated after that has already been
        set.
        """
        visitdates: list[Any] | None = self.__working.get_cross_sectional_value(
            "uds-visitdates", list
        )

        if not visitdates:
            visitdates = []

        current_visitdate = str(self.get_current_visitdate())
        if current_visitdate not in visitdates:
            visitdates.append(current_visitdate)
            visitdates.sort()

        # convert strings to dates
        result = [datetime_from_form_date(x) for x in visitdates]
        if any(x is None for x in result):
            raise InvalidFieldError("Invalid date found in uds-visitdates")

        return [x.date() for x in result]  # type: ignore

    def _create_naccavst(self) -> int:
        """Creates NACCAVST - total number of all UDS visits.

        This is also used for NACCVNUM, just under a different curation rule
        (cross-sectional vs longitudinal).
        """
        return len(self.get_visitdates())

    def _create_naccdays(self) -> Optional[int]:
        """Creates NACCDAYS - days from initial visit to most recent visit
        (max 5000).

        This is also used for NACCFDAYS, just under a different curation
        rule (cross-sectional vs longitudinal).
        """
        if self.uds.is_initial():
            return 0

        # while technically shouldn't happen, we do appear to have some
        # weird cases where there is not an initial packet in the system
        # return None in that case
        raw_initial = self.__working.get_cross_sectional_dated_value(
            "initial-uds-visit", str
        )
        initial_visitdate = datetime_from_form_date(raw_initial)
        if not initial_visitdate:
            return None

        current_visitdate = self.get_current_visitdate()
        num_days = calculate_days(initial_visitdate.date(), current_visitdate)
        if num_days is None:
            raise AttributeDeriverError(
                "Cannot calculate days between current and initial visit"
            )

        # TODO: RDD says max is 5000 but QAF doesn't seem to limit it
        # return min(num_days, 5000)
        return num_days

    def _create_naccnvst(self) -> int:
        """Creates NACCNVST - Total number of in-person UDS visits made."""
        total = self.__subject_derived.get_cross_sectional_value("naccnvst", int)
        if total is None:
            total = 0

        if self.uds.is_in_person():
            return total + 1

        return total

    def _create_uds_naccmdss(self) -> int:
        """Creates NACCMDSS - Subject's status in the Minimal Data Set
        (MDS) and Uniform Data Set (UDS)

        This is more cross-form, but we are setting it additively.
        """
        status = self.__subject_derived.get_cross_sectional_value("naccmdss", int)

        # already known to be in UDS and/or MDS
        if status in [1, 3]:
            return status

        # MDS flagged, so update to 1
        if status == 2:
            return 1

        return 3
