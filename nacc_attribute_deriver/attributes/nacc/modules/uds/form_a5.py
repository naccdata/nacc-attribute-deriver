"""Derived variables from form A5: Subject Health History.

From a5structrdd.sas.

TODO: these variables are heavily involved in a recode4g macro; it
is not entirely clear to me what this is doing, do regression test and
investigate.
"""

from typing import Optional

from .uds_attribute_collection import UDSAttributeCollection


class UDSFormA45ttribute(UDSAttributeCollection):
    """Class to collect UDS A5 attributes."""

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
        """
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
        the Initial Visit."""
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
        """Creates NACCTBI - History of traumatic brain injury (TBI)."""
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
