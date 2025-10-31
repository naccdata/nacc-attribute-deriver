"""Tests UDS Form B5 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_b5 import (
    UDSFormB5Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_BLANK


class TestUDSFormB5Missingness:
    def test_missingness_npiqinfx(self, uds_table):
        """Test missing NPIQINFX - blank if NPIQINF != 3"""
        attr = UDSFormB5Missingness(uds_table)
        # test NPIQINF also missing
        assert attr._missingness_npiqinfx() == INFORMED_BLANK

        # test NPIQINF there but not 3, so whatever is in NPIQINFX gets overwritten
        uds_table["file.info.forms.json"].update({"npiqinf": 2, "npiqinfx": "dummy"})
        assert attr._missingness_npiqinfx() == INFORMED_BLANK

        # test NPIQINF is there and 3, so keep whatever is already in NPIQINFX
        # (does this by returning None so its not overwritten)
        uds_table["file.info.forms.json"].update({"npiqinf": 3, "npiqinfx": "dummy"})
        assert attr._missingness_npiqinfx() is None
