"""Derived variables from form A1: Participant Demographics.

From derive.sas and a1structrdd.sas
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_BLANK
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    date_from_form_date,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError

from .helpers.generate_race import generate_race_v3, generate_race_v4


class UDSFormA1Attribute(UDSAttributeCollection):
    """Class to collect UDS A1 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

    def _create_naccage(self) -> int:
        """Creates NACCAGE (age) Generates DOB from BIRTHMO and BIRTHYR and
        compares to form date."""
        dob = self.uds.generate_uds_dob()
        visitdate = date_from_form_date(self.uds.get_required("visitdate", str))

        if not dob or not visitdate:
            raise AttributeDeriverError(
                "Missing one of DOB or visitdate to calculate naccage"
            )

        age = calculate_age(dob, visitdate)
        if age is None:
            raise AttributeDeriverError("Unable to calculate naccage")

        return age

    def _create_naccageb(self) -> Optional[int]:
        """Creates NACCAGEB (age at initial visit)."""
        # also ignore I4s
        if not self.uds.is_initial() or self.uds.is_i4():
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
        """Creates NACCNIHR (race).

        Source variables only provided in IVP.
        """
        if not self.uds.is_initial():
            return None

        if self.formver < 4:
            return generate_race_v3(
                race=self.uds.get_value("race", int),
                racex=self.uds.get_value("racex", str),
                racesec=self.uds.get_value("racesec", int),
                racesecx=self.uds.get_value("racesecx", str),
                raceter=self.uds.get_value("raceter", int),
                raceterx=self.uds.get_value("raceterx", str),
            )

        return generate_race_v4(
            racewhite=self.uds.get_value("racewhite", int),
            raceblack=self.uds.get_value("raceblack", int),
            raceaian=self.uds.get_value("raceaian", int),
            racenhpi=self.uds.get_value("racenhpi", int),
            raceasian=self.uds.get_value("raceasian", int),
            racemena=self.uds.get_value("racemena", int),
            raceunkn=self.uds.get_value("raceunkn", int),
        )

    def _create_naccreas(self) -> Optional[int]:
        """Creates NACCREAS - primary reason for coming to ADC.

        Not collected at followup visits.
        REMOVED IN V4
        """
        if self.formver >= 4 or not self.uds.is_initial():
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

    def _create_naccsex(self) -> Optional[int]:
        """Creates NACCSEX - participant's sex.

        Source variables only provided in IVP.
        """
        if not self.uds.is_initial():
            return None

        if self.formver < 4:
            sex = self.uds.get_value("sex", int)
        else:
            sex = self.uds.get_value("birthsex", int)

        if sex is None:
            raise AttributeDeriverError(
                "Unable to derive NACCSEX, missing sex/birthsex"
            )

        return sex

    def _create_nacclang(self) -> Optional[int]:
        """Creates NACCLANG - primary language.

        Source variables only provided in IVP.
        """
        if not self.uds.is_initial():
            return None

        if self.formver < 4:
            # need to do some transformation/mapping
            # primlang -> nacclang
            primlang_mappings = {1: 1, 2: 2, 3: 3, 4: 3, 5: 4, 6: 5, 8: 8, 9: 9}

            primlang = self.uds.get_value("primlang", int)
            if primlang not in primlang_mappings:
                raise AttributeDeriverError(
                    "Unable to derive NACCLANG (V3 and earlier):"
                    + f"unsupported primlang value: {primlang}"
                )

            return primlang_mappings[primlang]

        predomlan = self.uds.get_value("predomlan", int)
        if predomlan is None:
            raise AttributeDeriverError(
                "Unable to derive NACCLANG (V4): missing PREDOMLAN"
            )

        return predomlan

    def _create_nacclangx(self) -> Optional[str]:
        """Creates NACCLANGX - Primary language, other - specify.

        Source variables only provided in IVP. Can be blank.
        """
        if not self.uds.is_initial():
            return None

        if self.formver < 4:
            result = self.uds.get_value("primlangx", str)
        else:
            result = self.uds.get_value("predomlanx", str)

        return result if result is not None else INFORMED_BLANK

    def _create_nacchisp(self) -> Optional[int]:
        """Creates NACCHISP - Hispanic/Latino ethnicity

        Source variables only provided in IVP.
        """
        if not self.uds.is_initial():
            return None

        if self.formver < 4:
            hispanic = self.uds.get_value("hispanic", int)
            if hispanic is None:
                raise AttributeDeriverError(
                    "Unable to derive NACCHISP (V3 and earlier): missing HISPANIC)"
                )
            return hispanic

        ethispanic = self.uds.get_value("ethispanic", int)
        if ethispanic == 1:
            return 1
        if not ethispanic:
            raceunkn = self.uds.get_value("raceunkn", int)
            if raceunkn is None:
                return 0
            if raceunkn == 1:
                return 9

        raise AttributeDeriverError(
            "Unable to derive NACCHISP (V4) from ETHISPANIC and RACEUNKN"
        )

    def _create_naccedulvl(self) -> Optional[int]:  # noqa: C901
        """Creates NACCEDULVL - Highest achieved level of education.

        Source variables only provided in IVP.
        """
        if not self.uds.is_initial():
            return None

        if self.formver < 4:
            # educ is not provided in FVP, so may need to resolve from previous record
            educ = self.uds.get_value("educ", int)
            if educ is None:
                raise AttributeDeriverError(
                    "Unable to derive NACCEDULVL (V3 and earlier): " + "missing EDUC"
                )

            if educ < 12:
                return 1
            if educ == 12:
                return 2
            if educ > 12 and educ < 16:
                return 3
            if educ >= 16 and educ < 18:
                return 4
            if educ >= 18 and educ < 20:
                return 5
            if educ >= 20 and educ <= 36:
                return 6
            if educ == 99:
                return 9

            raise AttributeDeriverError(
                "Unable to derive NACCEDULVL (V3 and earlier):"
                + f"unhandled EDUC value: {educ}"
            )

        # lvleduc is not provided in FVP, so may need to resolve from previous record
        lvleduc = self.uds.get_value("lvleduc", int)
        if lvleduc is None:
            raise AttributeDeriverError(
                "Unable to derive NACCEDULVL (V4): missing LVLEDUC"
            )

        return lvleduc

    def _create_naccpaff(self) -> int:
        """Creates NACCPAFF - Previously affiliated subject.

        Always set as long as being an affiliate is ever true.
        """
        naccpaff = self.__subject_derived.get_cross_sectional_value("naccpaff", int)
        if naccpaff == 1:
            return 1

        return 1 if self._create_affiliate() else 0

    def _create_affiliate(self) -> bool:
        """Returns whether or not the participant is an affiliate.

        There are some nuances, but for now just check for source == 4
        or sourcenw == 2 (non-ADC).
        """
        # check if affiliate status already determined
        # TODO - right now once affiliate always affilaite, but should this change
        # to non-affiliate if a later form defines it as such?
        affiliate = self.__subject_derived.get_value("affiliate", bool)
        if affiliate:
            return True

        # only provided in IVP
        if self.uds.is_initial():
            source = self.uds.get_value("source", int)
            sourcenw = self.uds.get_value("sourcenw", int)
            return source == 4 or sourcenw == 2

        return False
