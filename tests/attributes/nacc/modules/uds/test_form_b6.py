"""Tests UDS Form B6 attributes.

Mostly GDS and test cases grabbed from regression testing.
"""

from nacc_attribute_deriver.attributes.nacc.modules.uds.form_b6 import (
    UDSFormB6Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class TestUDSFormB6Attribute:
    def test_create_naccgds_case1(self, uds_table):
        """Tests _create_naccgds - case 1. This is exactly 2.5, which
        we need to round up to 3 instead of Python's default down to 2."""
        uds_table['file.info.forms.json'].update({
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
        })

        attr = UDSFormB6Attribute(uds_table)
        assert attr._create_naccgds() == 3
