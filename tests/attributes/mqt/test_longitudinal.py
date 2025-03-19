"""Tests deriving MQT longitudinal variables."""

import pytest

from nacc_attribute_deriver.attributes.mqt.longitudinal import LongitudinalAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def attr() -> LongitudinalAttribute:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {"forms": {"json": {"module": "UDS", "formdate": "2025-01-01"}}}
        },
        "subject": {
            "info": {
                "derived": {
                    "uds_visitdates": [
                        "1980-05-06",
                        "1980-10-10",
                        "2023-12-12",
                        "2024-01-01",
                        "2024-02-02",
                        "2025-03-03",
                    ]
                },
                "longitudinal-data": {
                    "uds": {"count": {"latest": {"value": 5, "date": "2025-01-01"}}}
                },
            }
        },
    }

    return LongitudinalAttribute(SymbolTable(data))


class TestLongitudinalAttribute:
    def test_create_total_uds_visits(self, attr):
        """Tests _create_total_uds_visits."""
        assert attr._create_total_uds_visits() == 6

        # set module to non-UDS
        attr.set_value("module", "LBD")
        assert attr._create_total_uds_visits() == 5

        # test null case
        attr.table = {}
        assert attr._create_total_uds_visits() == 0

    def test_create_years_of_uds(self, attr):
        """Tests _create_years_of_uds, should only count unique years."""
        assert attr._create_years_of_uds() == 4
