"""Test utility methods."""

import pytest

from nacc_attribute_deriver.utils.date import (
    datetime_from_form_date,
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
