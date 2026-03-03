"""Tests overall participant statuses are handled correctly."""
import copy
import pytest
import random

from datetime import date
from typing import Any, Dict

from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.attributes.derived.modules.cross_module.participant_status_handler import (
    ParticipantStatusHandler
)
from nacc_attribute_deriver.symbol_table import SymbolTable


def create_working(data: Dict[str, Any]) -> WorkingNamespace:
    """Create dummy working data, add the specified data under
    working.cross-sectional, and return it in the working namespace.
    """
    table = SymbolTable(
        {
            "subject": {
                "info": {
                    "working": {
                        "cross-sectional": data
                    }
                }
            }
        }
    )
    return WorkingNamespace(table=table)


class TestParticipantStatusHandler:

    def test_status_overrides(self) -> None:
        """Tests the latest UDS visit or rejoin overrides other statuses."""
        base_data = {
            # milestone discontinued status has all unknowns, so need
            # to use visitdate which is still before our last UDS visit/rejoin
            "milestone-discontinued-date": {
                "value": "9999-99-99",
                "date": "2020-01-02"
            },

            # milestone death date is from BEFORE UDS visit even though form is
            # AFTER UDS visit/rejoin
            "milestone-death-date": {
                "value": "2024-01-01",
                "date": "2026-01-01"
            },

            # minimum contact status before date, but form date same as UDS visit/rejoin
            # should use status date though
            "milestone-minimum-contact-date": {
                "value": "2024-12-15",
                "date": "2025-01-01"
            },

            # prespart is set, should be invalidated by the fact that there is a
            # rejoin
            "prespart": {
                "value": 1,
                "date": "2020-03-03"
            },
        }

        # test when uds visit overrides
        data = copy.deepcopy(base_data)
        data.update({
            # set so that expected latest UDS visitdate is 2025-01-01
            "uds-visitdates": [
                "2020-03-03", "2025-01-01", "2024-01-02"
            ]
        })

        working = create_working(data)
        participant = ParticipantStatusHandler(working)
        assert participant.latest_uds_visit().status_date == "2025-01-01"
        assert participant.rejoined() is None

        assert participant.discontinued() is None
        assert participant.deceased() is None
        assert participant.minimum_contact() is None
        assert participant.initial_visit_only() is None


        # do the same for a rejoin
        data = copy.deepcopy(base_data)
        data.update({
            # set so that rejoin is 2025-01-01
            "milestone-rejoined-date": {
                "value": "2025-01-01",
                "date": "2025-01-01"
            },

            # create an initial visit just so prespart doesn't fail
            "uds-visitdates": [
                "2020-03-03"
            ]

        })

        working = create_working(data)
        participant = ParticipantStatusHandler(working)
        assert participant.rejoined().status_date == "2025-01-01"
        assert participant.latest_uds_visit().status_date == "2020-03-03"

        assert participant.discontinued() is None
        assert participant.deceased() is None
        assert participant.minimum_contact() is None
        assert participant.initial_visit_only() is None
