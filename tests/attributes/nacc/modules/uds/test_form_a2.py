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
    uds_table['file.info.forms.json'].update({
        'packet': 'T',
        'newinf': '0',
        'invisits': '3',
        'incalls': '6',
        'a2sub': 0
    })
    return uds_table


class TestUDSFormA2Attribute:
    def test_create_naccninr_longitudinally(self, table):
        """Test NACCNINR over longitudinal values."""
        # V3 and earlier
        attr = UDSFormA2Attribute(table)
        # does NOT carry forward
        assert attr._create_naccninr() == INFORMED_MISSINGNESS

        table["file.info.forms.json.a2sub"] = 1
        table["file.info.forms.json.newinf"] = 1
        assert attr._create_naccninr() == 99

        # assert -4 for V4
        table['file.info.forms.json.formver'] = 4.0
        attr = UDSFormA2Attribute(table)
        assert attr._create_naccninr() == INFORMED_MISSINGNESS

    def test_create_naccincntfq(self, table):
        """Tests NACCINCNTFQ."""
        # not submitted
        attr = UDSFormA2Attribute(table)
        assert attr._create_naccninr() == INFORMED_MISSINGNESS

        # V3 and earlier, min of INVISITS and INCALLS
        table["file.info.forms.json.a2sub"] = 1
        attr = UDSFormA2Attribute(table)
        assert attr._create_naccincntfq() == 3
        table['file.info.forms.json.incalls'] = 1
        assert attr._create_naccincntfq() == 1

        # V4
        table['file.info.forms.json'].update({
            'formver': '4.0',
            'inlivwth': '1',
        })
        attr = UDSFormA2Attribute(table)
        assert attr._create_naccincntfq() == 8

        table['file.info.forms.json'].update({
            'inlivwth': '0',
            'incntfrq': '6'
        })
        assert attr._create_naccincntfq() == 6
