"""Tests participant statuses are set correctly."""

import random
import pytest

from datetime import date
from typing import Any, Dict

from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.attributes.derived.modules.cross_module.participant_status import (  # noqa: E501
    DeceasedStatus,
    DiscontinuedStatus,
    MinimumContactStatus,
    InitialVisitOnlyStatus,
    LatestUDSVisit,
    RejoinedStatus,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable


def create_working(data: Dict[str, Any]) -> WorkingNamespace:
    """Create dummy working data, add the specified data under working.cross-
    sectional, and return it in the working namespace."""
    table = SymbolTable({"subject": {"info": {"working": {"cross-sectional": data}}}})
    return WorkingNamespace(table=table)


class TestParticipantStatusCreation:
    def test_no_status(self) -> None:
        """Test nothing is set."""
        working = create_working({})

        assert DeceasedStatus.create_from_working_namespace(working) is None
        assert DiscontinuedStatus.create_from_working_namespace(working) is None
        assert MinimumContactStatus.create_from_working_namespace(working) is None
        assert InitialVisitOnlyStatus.create_from_working_namespace(working) is None
        assert RejoinedStatus.create_from_working_namespace(working) is None
        assert LatestUDSVisit.create_from_working_namespace(working) is None

    def test_discontinued_status(self) -> None:
        """Test the discontinued status is set correctly."""
        working = create_working(
            {
                "milestone-discontinued-date": {
                    "value": "2025-01-99",  # unknown day
                    "date": "2025-03-03",
                }
            }
        )

        status = DiscontinuedStatus.create_from_working_namespace(working)
        assert status.status == "discontinued"
        assert status.status_date == "2025-01-99"
        assert status.form_date == date(2025, 3, 3)

    def test_minimum_contact_status(self) -> None:
        """Test the minimum contact status is set correctly."""
        working = create_working(
            {
                "milestone-minimum-contact-date": {
                    "value": "2025-99-99",  # unknown month and day
                    "date": "2025-05-12",
                }
            }
        )

        status = MinimumContactStatus.create_from_working_namespace(working)
        assert status.status == "minimum_contact"
        assert status.status_date == "2025-99-99"
        assert status.form_date == date(2025, 5, 12)

    def test_initial_visit_only_status(self) -> None:
        """Test that the initial visit only status is set correctly."""
        # test when prespart is 1
        working = create_working(
            {
                "prespart": {"value": 1, "date": "2025-01-05"},
                "uds-visitdates": ["2025-01-05"],
            }
        )

        status = InitialVisitOnlyStatus.create_from_working_namespace(working)
        assert status.status == "initial_visit_only"
        assert status.status_date == "2025-01-05"
        assert status.form_date == date(2025, 1, 5)

        # test when prespart is not 1
        working = create_working(
            {
                "prespart": {
                    "value": random.choice([None, 0, 2]),
                    "date": "2025-01-05",
                },
                "uds-visitdates": ["2025-01-05"],
            }
        )

        # should not be created
        assert InitialVisitOnlyStatus.create_from_working_namespace(working) is None

        # test when there are multiple UDS visits, should also not be created
        working = create_working(
            {
                "prespart": {"value": 1, "date": "2025-01-05"},
                "uds-visitdates": ["2025-01-05", "2026-02-02"],
            }
        )

        # should not be created
        assert InitialVisitOnlyStatus.create_from_working_namespace(working) is None

    def test_rejoined_status(self) -> None:
        """Test that the rejoin status is set correctly."""
        working = create_working(
            {
                "milestone-rejoined-date": {
                    "value": "9999-99-99",  # unknown everything
                    "date": "2025-11-22",
                }
            }
        )

        status = RejoinedStatus.create_from_working_namespace(working)
        assert status.status == "rejoined"
        assert status.status_date == "9999-99-99"
        assert status.form_date == date(2025, 11, 22)

    def test_latest_uds_visit(self) -> None:
        """Test that the latest UDS visit is set correctly."""
        # give several UDS visit dates, out of order, to test
        # what we get is the latest one
        working = create_working(
            {"uds-visitdates": ["2024-01-02", "2025-09-29", "2023-12-18"]}
        )

        status = LatestUDSVisit.create_from_working_namespace(working)
        assert status.status == "latest_uds_visit"
        assert status.status_date == "2025-09-29"
        assert status.form_date == date(2025, 9, 29)

    def test_deceased_status_np(self) -> None:
        """Test when the deceased status is set by an NP form."""
        working = create_working(
            {
                "np-death-date": {
                    "value": "2025-99-99",  # month and day unknown
                    "date": "2025-07-19",
                },
                "np-death-age": 73,
            }
        )

        status = DeceasedStatus.create_from_working_namespace(working)
        assert status.status == "deceased"
        assert status.status_date == "2025-99-99"
        assert status.form_date == date(2025, 7, 19)

        # deceased-specific variables
        assert status.age_at_death == 73
        assert status.has_np is True

        # test error is thrown if np-death-age not provided with NP form
        working = create_working(
            {
                "np-death-date": {
                    "value": "2025-01-12",
                    "date": "2025-07-19",
                }
            }
        )

        with pytest.raises(AttributeDeriverError) as e:
            DeceasedStatus.create_from_working_namespace(working)

        assert "Missing NP death age when NP death reported" in str(e)

    def test_deceased_status_mlst(self) -> None:
        """Test when the deceased status is set by a MLST form."""
        working = create_working(
            {
                "milestone-death-date": {"value": "2025-01-05", "date": "2025-07-23"},
                # provide date of birth to figure out death date from
                "uds-date-of-birth": "1960-04-01",
            }
        )

        status = DeceasedStatus.create_from_working_namespace(working)
        assert status.status == "deceased"
        assert status.status_date == "2025-01-05"
        assert status.form_date == date(2025, 7, 23)

        # deceased-specific variables
        assert status.age_at_death == 64
        assert status.has_np is False

        # make milestone death date not fully known, so age at death is 999
        # since we can't really calculate it
        working = create_working(
            {
                "milestone-death-date": {"value": "2025-99-99", "date": "2025-07-23"},
                # provide date of birth to figure out death date from
                "uds-date-of-birth": "1960-04-01",
            }
        )
        status = DeceasedStatus.create_from_working_namespace(working)
        assert status.status == "deceased"
        assert status.status_date == "2025-99-99"
        assert status.form_date == date(2025, 7, 23)

        # deceased-specific variables
        assert status.age_at_death == 999
        assert status.has_np is False

    def test_deceased_status_mds(self) -> None:
        """Test when the deceased status is set by an MDS form."""
        working = create_working(
            {
                "mds-death-date": {"value": "2025-01-99", "date": "2025-08-12"},
                # MDS should have tried to calculate age
                "mds-death-age": 81,
            }
        )
        status = DeceasedStatus.create_from_working_namespace(working)
        assert status.status == "deceased"
        assert status.status_date == "2025-01-99"
        assert status.form_date == date(2025, 8, 12)

        # deceased-specific variables
        assert status.age_at_death == 81
        assert status.has_np is False

    def test_status_equality(self) -> None:
        """Test equality."""
        # actual dates are the same, should return True
        working = create_working(
            {
                "milestone-discontinued-date": {
                    "value": "2000-11-12",
                    "date": "2024-01-19",
                },
                "milestone-minimum-contact-date": {
                    "value": "2000-11-12",
                    "date": "2024-01-19",
                },
            }
        )
        discontinued = DiscontinuedStatus.create_from_working_namespace(working)
        minimum_contact = MinimumContactStatus.create_from_working_namespace(working)
        assert discontinued == minimum_contact

        # form dates are the same, should return True
        working = create_working(
            {
                "milestone-discontinued-date": {
                    "value": "9999-99-99",
                    "date": "2024-01-19",
                },
                "milestone-minimum-contact-date": {
                    "value": "9999-12-15",
                    "date": "2024-01-19",
                },
            }
        )
        discontinued = DiscontinuedStatus.create_from_working_namespace(working)
        minimum_contact = MinimumContactStatus.create_from_working_namespace(working)
        assert discontinued == minimum_contact
