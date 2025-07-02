"""Derived variables from form A1: Participant Demographics.

From derive.sas and a1structrdd.sas
"""

from typing import Optional

from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    datetime_from_form_date,
)

from .helpers.generate_race import generate_race
from .uds_attribute_collection import UDSAttributeCollection


class UDSFormA1Attribute(UDSAttributeCollection):
    """Class to collect UDS A1 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

    def _create_naccage(self) -> int:
        """Creates NACCAGE (age) Generates DOB from BIRTHMO and BIRTHYR and
        compares to form date."""
        dob = self.uds.generate_uds_dob()
        visitdate = datetime_from_form_date(self.uds.get_required("visitdate", str))

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
        if not self.uds.is_initial():
            return None

        return self._create_naccage()

    def _create_nacclivs(self) -> int:
        """Creates NACCLIVS - living situation."""
        if self.formver >= 3:
            livsitua = self.uds.get_value("livsitua", int)
            if livsitua == 4:
                return 5
            if livsitua in [5, 6]:
                return 4
            if livsitua is None:
                return 9

            return livsitua

        livsit = self.uds.get_value("livsit", int)
        return livsit if livsit is not None else 9

    def _create_naccnihr(self) -> Optional[int]:
        """Creates NACCNIHR (race) if first form."""
        if not self.uds.is_initial():
            return None

        result = generate_race(
            race=self.uds.get_value("race", int),
            racex=self.uds.get_value("racex", str),
            racesec=self.uds.get_value("racesec", int),
            racesecx=self.uds.get_value("racesecx", str),
            raceter=self.uds.get_value("raceter", int),
            raceterx=self.uds.get_value("raceterx", str),
        )

        return result

    def _create_naccreas(self) -> Optional[int]:
        """Creates NACCREAS - primary reason for coming to ADC.

        Not collected at followup visits.
        """
        if not self.uds.is_initial():
            return None

        reason = self.uds.get_value("reason", int)
        if reason in [3, 4]:
            return 7

        return reason if reason is not None else 9

    def _create_naccrefr(self) -> Optional[int]:
        """Ceates NACCREFR - principle referral source.

        Not collected at followup visits.
        """
        if not self.uds.is_initial():
            return None

        if self.formver >= 3:
            refersc = self.uds.get_value("refersc", int)
            if refersc in [1, 2, 3]:
                return 1
            if refersc in [4, 5, 6]:
                return 2
            if refersc is None:
                return 9
            return refersc

        refer = self.uds.get_value("refer", int)
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
        source = self.uds.get_value("source", int)
        sourcenw = self.uds.get_value("sourcenw", int)

        return source == 4 or sourcenw == 2

    def _create_educ(self) -> Optional[int]:
        """UDS education level."""
        return self.uds.get_value("educ", int)

    def _create_prespart(self) -> Optional[int]:
        """Presumed participation.

        Used for NACCACTV.
        """
        return self.uds.get_value("prespart", int)
