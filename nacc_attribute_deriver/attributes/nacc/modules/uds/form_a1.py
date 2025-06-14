"""Derived variables from form A1: Participant Demographics."""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    datetime_from_form_date,
)

from .helpers.generate_race import generate_race


class UDSFormA1Attribute(AttributeCollection):
    """Class to collect UDS A1 attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

    def _create_naccage(self) -> int:
        """Creates NACCAGE (age) Generates DOB from BIRTHMO and BIRTHYR and
        compares to form date."""
        dob = self.__uds.generate_uds_dob()
        visitdate = datetime_from_form_date(self.__uds.get_required("visitdate", str))

        if not dob or not visitdate:
            raise AttributeDeriverError(
                "Missing one of DOB or visitdate to calculate naccage"
            )

        age = calculate_age(dob, visitdate.date())
        if age is None:
            raise AttributeDeriverError("Unable to calculate naccage")

        return age

    def _create_naccageb(self) -> Optional[int]:
        """Creates NACCAGEB (age at initial visit)."""
        if not self.__uds.is_initial():
            return None

        return self._create_naccage()

    def _create_nacclivs(self) -> int:
        """Creates NACCLIVS - living situation."""
        formver = self.__uds.normalized_formver()
        if formver >= 3:
            livsitua = self.__uds.get_value("livsitua", int)
            if livsitua == 4:
                return 5
            if livsitua in [5, 6]:
                return 4
            if livsitua is None:
                return 9

            return livsitua

        maristat = self.__uds.get_value("maristat", int)
        if maristat == 8:
            return 9

        livsit = self.__uds.get_value("livsit", int)
        return livsit if livsit is not None else 9

    def _create_naccnihr(self) -> Optional[int]:
        """Creates NACCNIHR (race) if first form."""
        if not self.__uds.is_initial():
            return None

        result = generate_race(
            race=self.__uds.get_value("race", int),
            racex=self.__uds.get_value("racex", str),
            racesec=self.__uds.get_value("racesec", int),
            racesecx=self.__uds.get_value("racesecx", str),
            raceter=self.__uds.get_value("raceter", int),
            raceterx=self.__uds.get_value("raceterx", str),
        )

        return result

    def _create_naccreas(self) -> Optional[int]:
        """Creates NACCREAS - primary reason for coming to ADC.

        Not collected at followup visits.
        """
        if not self.__uds.is_initial():
            return None

        reason = self.__uds.get_value("reason", int)
        if reason in [3, 4]:
            return 7

        return reason if reason is not None else 9

    def _create_naccrefr(self) -> Optional[int]:
        """Ceates NACCREFR - principle referral source.

        Not collected at followup visits.
        """
        if not self.__uds.is_initial():
            return None

        formver = self.__uds.normalized_formver()
        if formver >= 3:
            refersc = self.__uds.get_value("refersc", int)
            if refersc in [1, 2, 3]:
                return 1
            if refersc in [4, 5, 6]:
                return 2
            if refersc is None:
                return 9
            return refersc

        refer = self.__uds.get_value("refer", int)
        if refer == 5:
            return 2
        if refer in [3, 4, 6, 7]:
            return 8
        if refer is None:
            return 9

        return refer

    def _create_affiliate(self) -> bool:
        """Returns whether or not the participant is an affiliate.

        There are some nuances, but for now just check for source == 4
        or sourcenw == 2 (non-ADC).
        """
        # check if affiliate status already determined
        # TODO - right now treating like cross-sectional, but should this change
        # to non-affiliate if a later form defines it as such?
        affiliate = self.__subject_derived.get_value("affiliate", bool)
        if affiliate:
            return True

        # check source == 4 or sourcenw == 2
        source = self.__uds.get_value("source", int)
        sourcenw = self.__uds.get_value("sourcenw", int)

        return source == 4 or sourcenw == 2
