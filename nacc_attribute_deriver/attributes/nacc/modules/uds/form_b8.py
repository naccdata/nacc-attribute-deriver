"""Derived variables from form B8: Neurological Examination Findings.

Form B8 is required and expected to have been filled out.
"""

from typing import Optional

from .uds_attribute_collection import UDSAttributeCollection


class UDSFormB8Attribute(UDSAttributeCollection):
    """Class to collect UDS B8 attributes."""

    def _create_naccnrex(self) -> Optional[int]:
        """Creates NACCNREX, were all findings unremarkable?"""
        normal = self.uds.get_value("normal", int)
        normexam = self.uds.get_value("normexam", int)

        if normal == 1 or normexam in [0, 2]:
            return 1
        if normal == 0 or normexam == 1:
            return 0
        if normal == 9:
            return 9

        return None
