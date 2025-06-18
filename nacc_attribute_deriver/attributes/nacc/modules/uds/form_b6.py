"""Derived variables from form B6: GDS.

Form B6 may not have been filled out.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormB6Attribute(AttributeCollection):
    """Class to collect UDS B6 attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)
        self.__submitted = self.__uds.get_value("b6sub", int) == 1

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

    def _create_naccgds(self) -> Optional[int]:
        """Create NACCGDS, total GDS score.

        See coding guidebook for details.
        """
        if not self.__submitted:
            return None

        num_completed = 0
        completed_score = 0
        unanswered = 0

        for field in self.GDS_VARS:
            value = self.__uds.get_value(field, int)
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
            return round(completed_score + prorated)

        return completed_score
