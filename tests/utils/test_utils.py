"""Test utility methods."""

import pytest

from nacc_attribute_deriver.utils.date import (
    datetime_from_form_date,
    find_closest_date,
    standardize_date,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


class TestDateUtils:
    def test_datetime_from_form_date(self):
        """Assert all expected date formats pass without issue."""
        assert datetime_from_form_date("2025-01-01")
        assert datetime_from_form_date("2025/01/01")
        assert datetime_from_form_date("01-01-2025")
        assert datetime_from_form_date("01/01/2025")
        assert datetime_from_form_date(None) is None

        with pytest.raises(AttributeDeriverError) as e:
            datetime_from_form_date("20250101")

        assert str(e.value) == "Invalid date format: 20250101"

        with pytest.raises(AttributeDeriverError) as e:
            datetime_from_form_date("01/01/2025-extrastuff")

        assert (
            str(e.value)
            == "Failed to parse date 01/01/2025-extrastuff: "
            + "unconverted data remains: -extrastuff"
        )

    def test_standardize_date(self):
        """Test standardizing date."""
        assert standardize_date("2025-12-01") == "2025-12-01"
        assert standardize_date("2025/12/01") == "2025-12-01"
        assert standardize_date("12-01-2025") == "2025-12-01"
        assert standardize_date("12/01/2025") == "2025-12-01"

        assert standardize_date(None) is None

    def test_find_closest_date(self):
        """Test finding the closest date, also mix up the date formats."""
        # a year after the latest
        assert find_closest_date(
            ["2025-01-01", "2026/01/01", "01-01-2027"], "2028-01-01"
        ) == ("2027-01-01", 2)

        # a day before the middle
        assert find_closest_date(
            ["01/01/2025", "2026-01-01", "2027/01/01"], "2025/12/31"
        ) == ("2026-01-01", 1)

        # exactly the first
        assert find_closest_date(
            ["2025/01/01", "01/01/2026", "2027-01-01"], "01-01-2025"
        ) == ("2025-01-01", 0)
