"""Derived variables from form B6: GDS.

Form B6 may not have been filled out.
"""

import math
from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_attribute import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS


class UDSFormB6Attribute(UDSAttributeCollection):
    """Class to collect UDS B6 attributes."""

    @property
    def submitted(self) -> bool:
        return self.uds.get_value("b6sub", int) == 1

    GDS_VARS: frozenset[str] = frozenset(
        [
            "satis",
            "dropact",
            "empty",
            "bored",
            "spirits",
            "afraid",
            "happy",
            "helpless",
            "stayhome",
            "memprob",
            "wondrful",
            "wrthless",
            "energy",
            "hopeless",
            "better",
        ]
    )

    def _create_naccgds(self) -> int:
        """Create NACCGDS, total GDS score.

        See coding guidebook for details.
        """
        if not self.submitted:
            return INFORMED_MISSINGNESS

        nogds = self.uds.get_value('nogds', int)
        if nogds == 1:
            return 88

        num_completed = 0
        completed_score = 0
        unanswered = 0

        for field in self.GDS_VARS:
            value = self.uds.get_value(field, int)
            if value in [0, 1]:
                num_completed += 1
                completed_score += value
            else:
                unanswered += 1

        # if more than 3 items are unanswered, incomplete
        if unanswered > 3:
            return 88

        # calculate prorated score
        # (total score of completed / # of completed) * (# unanswered)
        if unanswered > 0:
            prorated = (completed_score / num_completed) * (unanswered)

            # this ensures 0.5 rounds up, not down
            return int(math.floor(completed_score + prorated + 0.5))

        return completed_score
