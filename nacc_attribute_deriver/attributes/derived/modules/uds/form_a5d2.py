"""Derived variables from.

V3 and earlier:
    Form A5: Subject Health History - see a5structrdd.sas
    Form D2: Clinician-assessed Medical Conditions (not
        used for older derived variables)
V4: Form A5/D2: Participant Health History/Clinician-assessed Medical Conditions

Form A5 was combined with Form D2 in V4; as such, the variables listed here
are derived from both forms.
"""

from typing import List, Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class UDSFormA5D2Attribute(UDSAttributeCollection):
    """Class to collect UDS A5/D2 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

    def calculate_mrsyear(self, prefix: str, max_index: int = 6) -> Optional[int]:
        """Calculate mrsyear, which is the maximum of all {PREFIX}{I}YR
        variables.

        Prefix expected to be STROK or TIA (UDS formver < 3)
        """
        if self.formver >= 3:
            return None

        found = []
        for i in range(1, max_index + 1):
            value = self.uds.get_value(f"{prefix}{i}yr", int)
            if value is not None and value not in [-4, 8888, 9999]:
                found.append(value)

        return max(found) if found else None

    def _create_naccstyr(self) -> Optional[int]:
        """Creates NACCSTYR - Most recently reported year of stroke
        as of the initial visit.

        Only computed in V3 and earlier from form A5; if now V3 but
        had previous V3 values, carry forward.
        """
        known_value = self.__subject_derived.get_cross_sectional_value("naccstyr", int)

        if self.formver >= 4:
            return known_value if known_value is not None else INFORMED_MISSINGNESS

        if not self.uds.is_initial():
            return None

        cbstroke = self.uds.get_value("cbstroke", int)
        if cbstroke in [1, 2]:
            mrsyear = self.calculate_mrsyear("strok")  # v1, v2
            strokyr = self.uds.get_value("strokyr", int)  # v3+
            if mrsyear is None and strokyr is not None:
                mrsyear = strokyr

            return mrsyear if mrsyear is not None else 9999

        if cbstroke == 9:
            return INFORMED_MISSINGNESS
        if cbstroke == 0:
            return 8888

        return INFORMED_MISSINGNESS

    def _create_nacctiyr(self) -> Optional[int]:
        """Creates NACCTIYR - Most recently reported year of TIA as of
        the Initial Visit.

        Only computed in V3 and earlier from form A5; if now V3 but
        had previous V3 values, carry forward.
        """
        known_value = self.__subject_derived.get_cross_sectional_value("nacctiyr", int)

        if self.formver >= 4:
            return known_value if known_value is not None else INFORMED_MISSINGNESS

        if not self.uds.is_initial():
            return None

        cbtia = self.uds.get_value("cbtia", int)
        if cbtia in [1, 2]:
            mrsyear = self.calculate_mrsyear("tia")  # v1, v2
            tiayear = self.uds.get_value("tiayear", int)  # v3+
            if mrsyear is None and tiayear is not None:
                mrsyear = tiayear

            return mrsyear if mrsyear is not None else 9999

        if cbtia == 9:
            return INFORMED_MISSINGNESS
        if cbtia == 0:
            return 8888

        return INFORMED_MISSINGNESS

    def _create_nacctbi(self) -> int:
        """Creates NACCTBI - History of traumatic brain injury (TBI).

        V4: From form A5D2
        V3 and earlier: From form A5
        """
        if self.formver >= 4:
            result = self.uds.get_value("headinjury", int)
            return result if result is not None else INFORMED_MISSINGNESS

        traumbrf = self.uds.get_value("traumbrf", int)
        traumchr = self.uds.get_value("traumchr", int)
        traumext = self.uds.get_value("traumext", int)
        tbi = self.uds.get_value("tbi", int)
        all_vars = [traumbrf, traumchr, traumext, tbi]

        if any(x in [1, 2] for x in all_vars):
            return 1
        if (traumbrf == 0 and traumchr == 0 and traumext == 0) or tbi == 0:
            return 0
        if all(x == -4 or x is None for x in all_vars):
            return INFORMED_MISSINGNESS

        return 9

    def _create_naccsubst(self) -> int:
        """Creates NACCSUBST - Participant used substances including
        prescription or recreational drugs that caused significant
        impairment in work, legal, driving, or social areas within
        the past 12 months.

        New in V4, but applied to all versions.

        V4: From form A5D2
        V3 and earlier: From form A5
        """
        if self.formver < 4:
            abusothr = self.uds.get_value("abusothr", int)
            if abusothr in [0, 2]:
                return 0
            if abusothr == 1:
                return 1
            if abusothr == 9:
                return 9

        result = self.uds.get_value("substyear", int)
        return result if result is not None else INFORMED_MISSINGNESS

    def _create_naccheart(self) -> int:  # noqa: C901
        """Creates NACCHEART - Heart attack / cardiac arrest

        New in V4, but applied to all versions.

        V4: From form A5D2
        V3 and earlier: From both form A5 and form D2
        """
        # V1 and V2
        if self.formver < 3:
            result = self.uds.get_value("cvhatt", int)
            return result if result is not None else INFORMED_MISSINGNESS

        # V3
        if self.formver < 4:
            cvhatt = self.uds.get_value("cvhatt", int)
            myoinf = self.uds.get_value("myoinf", int)
            if cvhatt == 1 or myoinf == 1:
                return 1
            if cvhatt == 0 or myoinf == 0:
                return 0
            if cvhatt == 2:
                return 2
            if cvhatt == 9 and myoinf == 8:
                return 9

            return INFORMED_MISSINGNESS

        # V4
        hrtattack = self.uds.get_value("hrtattack", int)
        cardarrest = self.uds.get_value("cardarrest", int)
        if hrtattack == 1 or cardarrest == 1:
            return 1
        if hrtattack == 2 or cardarrest == 2:
            return 2
        if hrtattack == 0 or cardarrest == 0:
            return 0
        if hrtattack == 9 and myoinf == 9:
            return 9

        return INFORMED_MISSINGNESS

    def __v3_determine_arthritis_result(
        self, yes_conditions: List[int], no_conditions: List[int]
    ) -> int:
        """V3 arthritis helper for NACCRHEUM, NACCOSTEO, and NACCARTOTH, which
        ALL follow the below logic for V3:

        If ARTHRIT is blank and ARTH is blank than VAR = -4
        Elif ARTHTYPE or ARTYPE is YES_CONDITION then VAR = 1
        Elif ARTHTYPE or ARTYPE in NO_CONDITION then VAR = 0
        Elif ARTHRIT or ARTH = 0 then VAR = 0
        ELIF ARTHTYPE or ARTYPE = 9 then VAR = 9
        Else -4.
        """
        arth = self.uds.get_value("arth", int)
        arthrit = self.uds.get_value("arthrit", int)
        if arthrit is None and arthrit is None:
            return INFORMED_MISSINGNESS

        arthtype = self.uds.get_value("arthtype", int)
        artype = self.uds.get_value("artype", int)
        if arthtype in yes_conditions or artype in yes_conditions:
            return 1
        if arthtype in no_conditions or artype in no_conditions:
            return 0
        if arthrit == 0 or arth == 0:
            return 8
        if arthtype == 9 and artype == 9:
            return 9

        return INFORMED_MISSINGNESS

    def __v4_determine_arthritis_result(self, field: str) -> int:
        """V4 arthritis helper for NACCRHEUM, NACCOSTEO, and NACCARTOTH, which
        ALL follow the below logic for V4:

        If TARGET_FIELD = 1 then VAR = 1
        Elif ARTHRIT in (1,2) and FIELD is blank and ARTHTYPUNK is blank, then VAR = 0
        Elif ARTHRIT=0 then VAR = 8
        Elif ARTHTYPUNK=1 then VAR = 9
        Else -4
        """
        target_value = self.uds.get_value(field, int)
        arthrit = self.uds.get_value("arthrit", int)
        arthtypunk = self.uds.get_value("arthtypunk", int)

        if target_value == 1:
            return 1
        if arthrit in [1, 2] and target_value is None and arthtypunk is None:
            return 0
        if arthrit == 0:
            return 8
        if arthtypunk == 1:
            return 9

        return INFORMED_MISSINGNESS

    def _create_naccrheum(self) -> int:
        """Creates NACCRHEUM - Type of arthritis: Rheumatoid

        New in V4, but applied to earlier versions.

        V4: From form A5D2
        V3: From form A5
        V2 and earlier: Not applicable
        """
        if self.formver < 3:
            return INFORMED_MISSINGNESS

        if self.formver < 4:
            return self.__v3_determine_arthritis_result(
                yes_conditions=[1], no_conditions=[2, 3]
            )

        return self.__v4_determine_arthritis_result("arthrrheum")

    def _create_naccosteo(self) -> int:
        """Creates NACCOSTEO - Type of arthritis: Osteoarthritis

        New in V4, but applied to earlier versions.

        V4: From form A5D2
        V3: From form A5
        V2 and earlier: Not applicable
        """
        if self.formver < 3:
            return INFORMED_MISSINGNESS

        if self.formver < 4:
            return self.__v3_determine_arthritis_result(
                yes_conditions=[2], no_conditions=[1, 3]
            )

        return self.__v4_determine_arthritis_result("arthrosteo")

    def _create_naccartoth(self) -> int:
        """Creates NACCARTOTH - Type of arthritis: Other

        New in V4, but applied to earlier versions.

        V4: From form A5D2
        V3: From form A5
        V2 and earlier: Not applicable
        """
        if self.formver < 3:
            return INFORMED_MISSINGNESS

        if self.formver < 4:
            return self.__v3_determine_arthritis_result(
                yes_conditions=[3], no_conditions=[1, 2]
            )

        return self.__v4_determine_arthritis_result("arthrothr")

    def _create_nacccancer(self) -> int:
        """Creates NACCCANCER - Cancer present in the last 12 months
        (excluding non-melanoma skin cancer)

        New in V4, but applied to earlier versions.

        V4: From form A5D2 (CANCERACTV)
        V3: From form D2 (CANCER)
        V2 and earlier: Not applicable
        """
        if self.formver < 3:
            return INFORMED_MISSINGNESS

        field = "canceractv" if self.formver >= 4 else "cancer"
        cancer_value = self.uds.get_value(field, int)
        if cancer_value == 0:
            return 0
        if cancer_value in [1, 2]:
            return 1
        if cancer_value == 9:
            return 9

        return INFORMED_MISSINGNESS

    def _create_naccothcon(self) -> int:
        """Creates NACCOTHCON - Other medical conditions or procedures
        within the past 12 months

        New in V4, but applied to earlier versions.

        V4: From form A5D2
        V3: From form D2
        V2 and earlier: Not applicable
        """
        if self.formver < 3:
            return INFORMED_MISSINGNESS

        if self.formver < 4:
            result = self.uds.get_value("othcond", int)
            return result if result is not None else INFORMED_MISSINGNESS

        othercond = self.uds.get_value("othercond", int)
        if othercond == 0:
            return 0
        if othercond in [0, 2]:
            return 1
        if othercond == 9:
            return 9

        return INFORMED_MISSINGNESS

    def _create_naccdep(self) -> int:
        """Creates NACCDEP - Depression (recent or remote)

        New in V4, but applied to all versions.

        V4: From form A5D2
        V3 and earlier: From form A5
        """
        if self.formver < 4:
            dep2yrs = self.uds.get_value("dep2yrs", int)
            depothr = self.uds.get_value("depothr", int)
            if dep2yrs == 1 or depothr == 1:
                return 1
            if dep2yrs == 0 and depothr == 0:
                return 0
            if dep2yrs == 9 or depothr == 9:
                return 9

            return INFORMED_MISSINGNESS

        majordep = self.uds.get_value("majordep", int)
        otherdep = self.uds.get_value("otherdep", int)

        if majordep in [1, 2] or otherdep in [1, 2]:
            return 1
        if majordep == 0 and otherdep == 0:
            return 0
        if majordep == 9 or otherdep == 9:
            return 9

        return INFORMED_MISSINGNESS

    def _create_naccanx(self) -> int:
        """Creates NACCANX - Anxiety disorder (including OCD)

        New in V4, but applied to earlier versions.

        V4: From form A5D2
        V3: From form D2
        V2 and earlier: Not applicable
        """
        if self.formver < 3:
            return INFORMED_MISSINGNESS

        if self.formver < 4:
            anxiety = self.uds.get_value("anxiety", int)
            ocd = self.uds.get_value("ocd", int)

            if anxiety == 1 or ocd == 1:
                return 1
            if anxiety == 2 or ocd == 2:
                return 2
            if anxiety == 0 and ocd == 0:
                return 0
            if anxiety == 9 or ocd == 9:
                return 9

            return INFORMED_MISSINGNESS

        result = self.uds.get_value("anxiety", int)
        return result if result is not None else INFORMED_MISSINGNESS
