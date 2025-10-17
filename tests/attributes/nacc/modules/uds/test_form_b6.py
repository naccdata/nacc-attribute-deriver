"""Tests UDS Form B6 attributes.

Mostly GDS and test cases grabbed from regression testing.
"""

import pytest

from nacc_attribute_deriver.attributes.nacc.modules.uds.form_b6 import (
    UDSFormB6Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def gds_table(uds_table) -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    uds_table["file.info.forms.json"].update(
        {
            "satis": 0,
            "dropact": 0,
            "empty": 0,
            "bored": 1,
            "spirits": 0,
            "afraid": 0,
            "happy": 0,
            "helpless": 0,
            "stayhome": 9,
            "memprob": 9,
            "wondrful": 0,
            "wrthless": 0,
            "energy": 1,
            "hopeless": 0,
            "better": 9,
            "b6sub": 1,
        }
    )
    return uds_table


class TestUDSFormB6Attribute:
    def test_create_naccgds(self, gds_table):
        """Tests _create_naccgds. This is exactly 2.5, which
        we need to round up to 3 instead of Python's default down to 2."""
        attr = UDSFormB6Attribute(gds_table)
        assert attr._create_naccgds() == 3

    def test_create_naccgds_nogds(self, gds_table):
        """Tests _create_naccgds - when NOGDS == 1."""
        gds_table["file.info.forms.json.nogds"] = 1
        attr = UDSFormB6Attribute(gds_table)
        assert attr._create_naccgds() == 88
