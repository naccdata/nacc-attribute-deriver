"""Tests deriving UDS form header derived variables."""

import pytest
from datetime import date
from nacc_attribute_deriver.attributes.nacc.modules.uds.form_header import (
    UDSHeaderAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table(uds_table) -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    uds_table['file.info.forms.json'].update({
        "packet": "F",
        "formdate": "2025-01-01",
        "visitdate": "2025-06-01",
    })
    uds_table.update({
        "subject": {
            "info": {
                "derived": {"cross-sectional": {"naccnvst": 4}},
                "working": {
                    "cross-sectional": {
                        "uds-visitdates": [
                            "1980-05-06",
                            "1980-10-10",
                            "2023-12-12",
                            "2024-01-01",
                            "2024-02-02",
                            "2025-03-03",
                        ],
                        "initial-uds-visit": {
                            "date": "1980-05-06",
                            "value": "1980-05-06",
                        },
                    }
                },
            }
        },
    })

    return uds_table


class TestUDSHeaderAttributeCollection:
    def test_get_current_visitdate(self, table):
        """Test getting the current date."""
        attr = UDSHeaderAttributeCollection(table)
        assert attr.get_current_visitdate() == date(2025, 6, 1)

    def test_get_visitdates(self, table):
        """Tests get_visitdates - should add current visit"""
        attr = UDSHeaderAttributeCollection(table)
        assert attr.get_visitdates() == [
            date(1980, 5, 6),
            date(1980, 10, 10),
            date(2023, 12, 12),
            date(2024, 1, 1),
            date(2024, 2, 2),
            date(2025, 3, 3),
            date(2025, 6, 1),
        ]

    def test_create_naccavst(self, table):
        """Tests _create_naccavst."""
        attr = UDSHeaderAttributeCollection(table)
        assert attr._create_naccavst() == 7

        # test when there is no other visits
        table["subject.info.working.cross-sectional"] = {}
        assert attr._create_naccavst() == 1

    def test_create_naccdays(self, table, form_prefix, working_derived_prefix):
        """Tests _create_naccdays."""
        attr = UDSHeaderAttributeCollection(table)

        # actually 16,462 but maxes out at 5000
        # assert attr._create_naccdays() == 5000
        assert attr._create_naccdays() == 16462

        # set it closer
        set_attribute(
            table,
            working_derived_prefix,
            "cross-sectional.initial-uds-visit",
            {"date": "2024-02-02", "value": "2024-02-02"},
        )
        assert attr._create_naccdays() == 485

        # test no initial visit on record
        set_attribute(
            table, working_derived_prefix, "cross-sectional.initial-uds-visit", None
        )
        assert attr._create_naccdays() is None

        # test initial visit
        set_attribute(table, form_prefix, "packet", "IT")
        assert attr._create_naccdays() == 0

    def test_create_naccnvst(self, table):
        """Tsests _create_naccnvst."""
        attr = UDSHeaderAttributeCollection(table)
        assert attr._create_naccnvst() == 5
