"""Test utility methods."""

import pytest

from nacc_attribute_deriver.utils.date import datetime_from_form_date
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


class TestDateUtils:
    def test_datetime_from_form_date(self):
        """Assert all expected date formats pass without issue."""
        assert datetime_from_form_date("2025-01-01")
        assert datetime_from_form_date("2025/01/01")
        assert datetime_from_form_date("01/01/2025")
        assert datetime_from_form_date(None) is None

        with pytest.raises(AttributeDeriverError) as e:
            datetime_from_form_date("20250101")

        assert (
            str(e.value)
            == "Failed to parse date 20250101: time data "
            + "'20250101' does not match format '%m/%d/%Y'"
        )
