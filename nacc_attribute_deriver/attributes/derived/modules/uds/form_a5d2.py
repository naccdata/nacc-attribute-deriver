"""Derived variables from

V3 and earlier: Form A5: Subject Health History - see a5structrdd.sas
V4: Form A5/D2: Participant Health History/Clinician-assessed Medical Conditions

Form A5 was combined with Form D2 in V4; as such, the variables listed here
are derived from both forms.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)

from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class UDSFormA5D2Attribute(UDSAttributeCollection):
    """Class to collect UDS A5/D2 attributes."""

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

        Only computed in V3 and earlier from form A5.
        """
        if self.formver >= 4:
            return INFORMED_MISSINGNESS

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
            return None
        if cbstroke == 0:
            return 8888

        return None

    def _create_nacctiyr(self) -> Optional[int]:
        """Creates NACCTIYR - Most recently reported year of TIA as of
        the Initial Visit.

        Only computed in V3 and earlier from form A5.
        """
        if self.formver >= 4:
            return INFORMED_MISSINGNESS

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
            return None
        if cbtia == 0:
            return 8888

        return None

    def _create_nacctbi(self) -> Optional[int]:
        """Creates NACCTBI - History of traumatic brain injury (TBI).

        V4: From form A5D2
        V3 and earlier: From form A5
        """
        if self.formver >= 4:
            return self.uds.get_value(
                "headinjury", int, default=INFORMED_MISSINGNESS)

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
            return None

        return 9
