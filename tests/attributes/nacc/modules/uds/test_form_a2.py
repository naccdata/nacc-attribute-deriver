"""Tests UDS Form A2 attributes."""

import pytest
from nacc_attribute_deriver.attributes.nacc.modules.uds.form_a2 import (
    UDSFormA2Attribute,
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table(uds_table) -> SymbolTable:
    """Create dummy base table."""
    uds_table.update(
        {
            "subject": {
                "info": {
                    "derived": {
                        "longitudinal": {
                            "naccninr": [{"date": "2026-05-28", "value": 1}]
                        }
                    }
                }
            }
        }
    )
    uds_table["file.info.forms.json.packet"] = "T"
    uds_table["file.info.forms.json.newinf"] = "0"
    return uds_table


class TestUDSFormA2Attribute:
    def test_create_naccninr_longitudinally(self, table):
        """Test NACCNINR over longitudinal values."""
        attr = UDSFormA2Attribute(table)
        # does NOT carry forward
        assert attr._create_naccninr() == INFORMED_MISSINGNESS

        table["file.info.forms.json.a2sub"] = 1
        table["file.info.forms.json.newinf"] = 1
        assert attr._create_naccninr() == 99
