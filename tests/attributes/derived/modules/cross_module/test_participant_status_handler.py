# mypy: disable-error-code="union-attr"
"""Tests overall participant statuses are handled correctly."""

import pytest

from typing import Any, Dict

from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.attributes.derived.modules.cross_module.participant_status_handler import (  # noqa: E501
    ParticipantStatusHandler,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


def create_working(data: Dict[str, Any]) -> WorkingNamespace:
    """Create dummy working data, add the specified data under working.cross-
    sectional, and return it in the working namespace."""
    table = SymbolTable({"subject": {"info": {"working": {"cross-sectional": data}}}})
    return WorkingNamespace(table=table)


@pytest.fixture(scope="function")
def base_data() -> Dict[str, Any]:
    """Base data for testing; need to set uds/rejoin relative to these based on
    whatever is being tested."""
    return {
        "milestone-discontinued-date": {"value": "2023-99-99", "date": "2020-01-02"},
        "milestone-death-date": {"value": "2024-01-01", "date": "2026-01-01"},
        "milestone-minimum-contact-date": {"value": "2024-12-15", "date": "2025-01-01"},
    }


class TestParticipantStatusHandler:
    def test_status_overrides_uds(self, base_data) -> None:
        """Tests the latest UDS visit overrides other statuses."""
        base_data.update(
            {
                # set so that expected latest UDS visitdate is 2025-01-01
                # and is later than everything else
                "uds-visitdates": ["2020-03-03", "2025-01-01", "2024-01-02"]
            }
        )

        working = create_working(base_data)
        participant = ParticipantStatusHandler(working)
        assert participant.latest_uds_visit().status_date == "2025-01-01"
        assert participant.rejoined() is None

        assert participant.discontinued() is None
        assert participant.deceased() is None
        assert participant.minimum_contact() is None

    def test_status_overrides_rejoin(self, base_data) -> None:
        """Tests the latest rejoin overrides other statuses."""
        base_data.update(
            {
                # set so that latest rejoin is 2025-01-01 and later
                # than everything else
                "milestone-rejoined-date": {"value": "2025-01-01", "date": "2025-01-01"}
            }
        )

        working = create_working(base_data)
        participant = ParticipantStatusHandler(working)
        assert participant.rejoined().status_date == "2025-01-01"
        assert participant.latest_uds_visit() is None

        assert participant.discontinued() is None
        assert participant.deceased() is None
        assert participant.minimum_contact() is None

    def test_status_no_overrides_uds(self, base_data) -> None:
        """Tests the latest UDS visit does NOT override other statuses because
        it is before the other dates."""
        base_data.update(
            {
                # set so it's before everything else
                "uds-visitdates": ["2000-01-01"]
            }
        )

        working = create_working(base_data)
        participant = ParticipantStatusHandler(working)
        assert participant.latest_uds_visit().status_date == "2000-01-01"
        assert participant.rejoined() is None

        assert participant.discontinued().status_date == "2023-99-99"
        assert participant.deceased().status_date == "2024-01-01"
        assert participant.minimum_contact().status_date == "2024-12-15"

    def test_status_no_overrides_rejoin(self, base_data) -> None:
        """Tests the latest rejoin does NOT override other statuses because it
        is before the other dates."""
        base_data.update(
            {
                # set so that latest rejoin is before everything else, even
                # if the form date was after everything else
                "milestone-rejoined-date": {"value": "2001-01-01", "date": "2030-01-01"}
            }
        )

        working = create_working(base_data)
        participant = ParticipantStatusHandler(working)
        assert participant.latest_uds_visit() is None
        assert participant.rejoined().status_date == "2001-01-01"

        assert participant.discontinued().status_date == "2023-99-99"
        assert participant.deceased().status_date == "2024-01-01"
        assert participant.minimum_contact().status_date == "2024-12-15"

    def test_initial_visit_only_handling(self, base_data) -> None:
        """Test initial visit only is handled correctly.

        Only ever set if it is the ONLY thing ever set.
        """
        prespart = {
            "prespart": {"value": 1, "date": "2020-01-10"},
            # requires a single corresponding UDS visit
            "uds-visitdates": ["2020-01-10"],
        }
        working = create_working(prespart)
        participant = ParticipantStatusHandler(working)
        assert participant.initial_visit_only() is not None
        assert participant.initial_visit_only().status_date == "2020-01-10"

        # now add other things
        prespart.update(base_data)
        participant = ParticipantStatusHandler(working)
        assert participant.initial_visit_only() is None

    def test_future_date_ignored(self) -> None:
        """Ensure a future date is ignored."""
        working = create_working(
            {
                "milestone-discontinued-date": {
                    "value": "5000-01-01",
                    "date": "2025-01-01",
                }
            }
        )
        participant = ParticipantStatusHandler(working)
        assert participant.discontinued() is None

    def test_np_death_final(self) -> None:
        """Tests that the existence of an NP form does not allow death to be
        unset, even if an UDS visit came after."""
        working = create_working(
            {
                "np-death-date": {
                    "value": "2025-01-99",
                    "date": "2025-07-19",
                },
                "np-death-age": 79,
                "uds-visitdates": ["2025-12-10"],
            }
        )

        participant = ParticipantStatusHandler(working)
        assert participant.latest_uds_visit().status_date == "2025-12-10"
        assert participant.deceased().status_date == "2025-01-99"
        assert participant.deceased().has_np
        assert participant.deceased().age_at_death == 79

        assert participant.rejoined() is None
        assert participant.discontinued() is None
        assert participant.minimum_contact() is None
