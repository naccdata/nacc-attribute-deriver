"""Tests participant statuses are set correctly."""
import pytest
import random

from datetime import date
from typing import Any, Dict

from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.attributes.derived.modules.cross_module.participant_status import (
    DeceasedStatus,
    DiscontinuedStatus,
    MinimumContactStatus,
    InitialVisitOnlyStatus,
    LatestUDSVisit,
    RejoinedStatus,
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


class TestParticipantStatusCreation:

    def test_no_status(self) -> None:
        """Test nothing is set"""
        working = create_working({})

        assert DeceasedStatus.create_from_working_namespace(working) is None
        assert DiscontinuedStatus.create_from_working_namespace(working) is None
        assert MinimumContactStatus.create_from_working_namespace(working) is None
        assert InitialVisitOnlyStatus.create_from_working_namespace(working) is None
        assert RejoinedStatus.create_from_working_namespace(working) is None
        assert LatestUDSVisit.create_from_working_namespace(working) is None

    # def test_deceased_status(self) -> None:
    #   """Test the deceased status is set correctly."""


    def test_discontinued_status(self) -> None:
        """Test the discontinued status is set correctly."""
        working = create_working({
            "milestone-discontinued-date": {
                "value": "2025-01-99",  # unknown day
                "date": "2025-03-03"
            }
        })

        status = DiscontinuedStatus.create_from_working_namespace(working)
        assert status.status == 'discontinued'
        assert status.status_date == '2025-01-99'
        assert status.form_date == date(2025, 3, 3)

    def test_minimum_contact_status(self) -> None:
        """Test the minimum contact status is set correctly."""
        working = create_working({
            "milestone-minimum-contact-date": {
                "value": "2025-99-99",  # unknown month and day
                "date": "2025-05-12"
            }
        })

        status = MinimumContactStatus.create_from_working_namespace(working)
        assert status.status == 'minimum_contact'
        assert status.status_date == '2025-99-99'
        assert status.form_date == date(2025, 5, 12)

    def test_initial_visit_only_status(self) -> None:
        """Test that the initial visit only status is set correctly."""
        # test when prespart is 1
        working = create_working({
            "prespart": {
                "value": 1,
                "date": "2025-01-05"
            },
            "uds-visitdates": [
                "2025-01-05"
            ]
        })

        status = InitialVisitOnlyStatus.create_from_working_namespace(working)
        assert status.status == 'initial_visit_only'
        assert status.status_date == '2025-01-05'
        assert status.form_date == date(2025, 1, 5)

        # test when prespart is not 1
        working = create_working({
            "prespart": {
                "value": random.choice([None, 0, 2]),
                "date": "2025-01-05"
            },
            "uds-visitdates": [
                "2025-01-05"
            ]
        }) 

        # should not be created
        assert InitialVisitOnlyStatus.create_from_working_namespace(working) is None

    def test_rejoined_status(self) -> None:
        """Test that the rejoin status is set correctly."""
        working = create_working({
            "milestone-rejoined-date": {
                "value": "9999-99-99",  # unknown everything
                "date": "2025-11-22"
            }
        })

        status = RejoinedStatus.create_from_working_namespace(working)
        assert status.status == 'rejoined'
        assert status.status_date == '9999-99-99'
        assert status.form_date == date(2025, 11, 22)

    def test_latest_uds_visit(self) -> None:
        """Test that the latest UDS visit is set correctly."""
        # give several UDS visit dates, out of order, to test
        # what we get is the latest one
        working = create_working({
            "uds-visitdates": [
                "2024-01,02", "2025-09-29", "2023-12-18"
            ]
        })

        status = LatestUDSVisit.create_from_working_namespace(working)
        assert status.status == 'latest_uds_visit'
        assert status.status_date == '2025-09-29'
        assert status.form_date == date(2025, 9, 29)
