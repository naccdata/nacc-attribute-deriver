"""Tests deriving MQT longitudinal variables."""

import pytest
from nacc_attribute_deriver.attributes.mqt.longitudinal import (
    LongitudinalAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "module": "UDS",
                        "formdate": "2025-01-01",
                        "visitdate": "2025-01-01",
                    }
                }
            }
        },
        "subject": {
            "info": {
                "working": {
                    "cross-sectional": {
                        "uds-visitdates": [
                            "1980-05-06",
                            "1980-10-10",
                            "2023-12-12",
                            "2024-01-01",
                            "2024-02-02",
                            "2025-03-03",
                        ]
                    }
                },
                "longitudinal-data": {
                    "uds": {"count": {"latest": {"value": 5, "date": "2025-01-01"}}}
                },
            }
        },
    }

    return SymbolTable(data)


class TestLongitudinalAttributeCollection:
    def test_create_total_uds_visits(self, table, form_prefix):
        """Tests _create_total_uds_visits."""
        attr = LongitudinalAttributeCollection(table)
        assert attr._create_total_uds_visits() == 6

    def test_create_years_of_uds(self, table):
        """Tests _create_years_of_uds, should only count unique years."""
        attr = LongitudinalAttributeCollection(table)
        assert attr._create_years_of_uds() == 4
