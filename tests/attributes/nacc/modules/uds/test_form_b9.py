"""Tests UDS Form B9 attributes."""

import pytest
from nacc_attribute_deriver.attributes.nacc.modules.uds.form_b9 import (
    UDSFormB9Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "birthmo": 3,
                        "birthyr": 1990,
                        "module": "UDS",
                        "packet": "I",
                        "formver": "3.0",
                        "b9chg": 1,
                        "befpred": 0,
                    }
                }
            }
        },
        "subject": {
            "info": {
                "working": {
                    # "longitudinal": {
                    #     "decclin": [{"date": "2024-12-01", "value": 0}],
                    #     "befrst": [
                    #         {"date": "2024-01-01", "value": 88},
                    #         {"date": "2025-01-01", "value": 0},
                    #     ],
                    "cross-sectional": {
                        "decclin": 0,
                        "befrst": 0,
                        "mofrst": 3
                    }
                }
            }
        },
    }

    return SymbolTable(data)


class TestUDSFormB9Attribute:
    # def test_grab_prev(self, table):
    #     """Test the grab_prev method.

    #     Need to get around name mangling just for this test.
    #     """
    #     attr = UDSFormB9Attribute(table)
    #     assert attr.grab_prev("decclin", attr._UDSFormB9Attribute__working_derived) == 0

    #     # this should ignore the second record since it has the
    #     # same visitdate as the current record
    #     assert attr.grab_prev("befrst", attr._UDSFormB9Attribute__working_derived) == 88

    #     # no previous record
    #     assert attr.grab_prev("cogfrst", attr._UDSFormB9Attribute__working_derived) is None

    def test_create_naccbehf(self, table, working_derived_prefix):
        """Tests create NACCBEHF."""
        attr = UDSFormB9Attribute(table)
        assert attr._create_naccbehf() == 0

        # p_befpred drives value when formver >= 3
        set_attribute(
            table,
            working_derived_prefix,
            "cross-sectional.befpred",
            [{"date": "2024-01-01", "value": "3"}],
        )
        assert attr._create_naccbehf() == 3
        set_attribute(
            table,
            working_derived_prefix,
            "cross-sectional.befpred",
            [{"date": "2024-01-01", "value": "0"}],
        )
        assert attr._create_naccbehf() == 99

    def test_create_naccbehf_case1(self, table, form_prefix):
        """Case when all are None - befrst becomes 88."""
        set_attribute(table, form_prefix, 'formver', 1.0)

        # all are None
        set_attribute(table, form_prefix, 'befrst', None)
        set_attribute(table, form_prefix, 'befpred', None)
        set_attribute(table, form_prefix, 'b9chg', None)
        attr = UDSFormB9Attribute(table)
        assert attr._create_naccbehf() == 0

        # should be same for v3
        set_attribute(table, form_prefix, 'formver', 3.0)
        assert attr._create_naccbehf() == 0

    def test_create_naccmotf(self, table, form_prefix):
        """Tests creating NACCMOTF."""
        attr = UDSFormB9Attribute(table)
        assert attr._create_naccmotf() == 0

        set_attribute(table, form_prefix, 'b9chg', 0)
        attr = UDSFormB9Attribute(table)
        assert attr._create_naccmotf() == 99

        set_attribute(table, form_prefix, 'mofrst', 0)
        assert attr._create_naccmotf() == 3
