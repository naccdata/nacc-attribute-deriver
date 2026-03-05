"""Handles the MDS form."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    approximate_date,
    calculate_age,
    date_from_form_date,
    make_date_from_parts,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError, InvalidFieldError


class MDSFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        self.__mds = FormNamespace(table=table, required=frozenset(["module"]))
        self.__subject_derived = SubjectDerivedNamespace(table=table)

        module = self.__mds.get_required("module", str)
        if module.upper() != "MDS":
            msg = f"Current file is not a MDS form: found {module}"
            raise InvalidFieldError(msg)

    def get_date(self) -> Optional[date]:
        return self.__mds.get_date()

    def _create_mds_death_date(self) -> Optional[str]:
        """MDS death date; can be unknown."""
        # not dead
        if self.__mds.get_value("vitalst", int) != 2:
            return None

        year = self.__mds.get_value("deathyr", int)  # can be 9999
        month = self.__mds.get_value("deathmo", int)  # can be 99
        day = self.__mds.get_value("deathday", int)  # can be 99

        return make_date_from_parts(year=year, month=month, day=day)

    def _create_mds_death_age(self) -> Optional[int]:
        """Make the MDS death age; 999 for unknown/can't be calculated."""
        # not dead
        if self.__mds.get_value("vitalst", int) != 2:
            return None

        # get death date; approximate if just the day is unknown
        death_date = approximate_date(self._create_mds_death_date())

        # make birth date
        year = self.__mds.get_value("birthyr", int)  # required
        month = self.__mds.get_value("birthmo", int)  # can be 99
        day = self.__mds.get_value("birthday", int)  # can be 99
        birthday = make_date_from_parts(year=year, month=month, day=day)

        # also approximate birthday if just the day is unknown
        birthday = approximate_date(birthday)

        # try to calculate age
        try:
            death_age = calculate_age(
                date1=date_from_form_date(birthday),
                date2=date_from_form_date(death_date),
            )
            return death_age
        except (TypeError, ValueError, AttributeDeriverError):
            pass

        # unknown/can't be calculated
        return 999

    def _create_mds_naccmdss(self) -> int:
        """Creates NACCMDSS - Subject's status in the Minimal Data Set
        (MDS) and Uniform Data Set (UDS)

        This is more cross-form, but we are setting it additively.

        1: In the UDS and MDS
        2: In MDS only
        3: In UDS only
        """
        status = self.__subject_derived.get_cross_sectional_value("naccmdss", int)

        # already known to be in MDS and/or UDS
        if status in [1, 2]:
            return status

        # UDS flagged, so update to 1
        if status == 3:
            return 1

        return 2

    def _create_mds_source(self) -> int:
        """Returns MDS source."""
        source = self.__mds.get_value("source", int)

        # 9 = Missing/Unknown, so use as default if missing
        return source if source is not None else 9

    def _create_mds_affiliate(self) -> bool:
        """Returns whether or not the participant is an affiliate.

        In MDS checks if source == 3
        """
        return self.__mds.get_value("source", int) == 3
