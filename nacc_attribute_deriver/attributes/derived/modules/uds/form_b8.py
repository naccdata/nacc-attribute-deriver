"""Derived variables from form B8: Neurological Examination Findings.

Form B8 is required and expected to have been filled out.
"""

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class UDSFormB8Attribute(UDSAttributeCollection):
    """Class to collect UDS B8 attributes."""

    def _create_naccnrex(self) -> int:
        """Creates NACCNREX, were all findings unremarkable?"""
        if self.formver < 4:
            normexam = self.uds.get_value("normexam", int)
            normal = self.uds.get_value("normal", int)
            if normal == 1 or normexam in [0, 2]:
                return 1
            if normal == 0 or normexam == 1:
                return 0
            if normal == 9:
                return 9
        # V4
        else:
            normnrexam = self.uds.get_value("normnrexam", int)
            neurexam = self.uds.get_value("neurexam", int)
            if normnrexam == 0:
                return 1
            if normnrexam == 1:
                return 0
            if neurexam == 0:
                return 8

        return INFORMED_MISSINGNESS
