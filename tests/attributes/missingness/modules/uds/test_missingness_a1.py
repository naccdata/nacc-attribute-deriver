"""Tests UDS Form A1 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a1 import (
    UDSFormA1Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class TestUDSFormA1Missingness:
    def test_missingness_residenc(self, uds_table):
        """Test missing RESIDENC - expect recode on 5 for V1/V2"""
        uds_table["file.info.forms.json"].update({"formver": 1.0, "residenc": 5})
        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_residenc() == 9

        uds_table["file.info.forms.json.residenc"] = 3
        assert attr._missingness_residenc() == 3

        uds_table["file.info.forms.json.residenc"] = None
        assert attr._missingness_residenc() == INFORMED_MISSINGNESS

    def test_missingness_maristat(self, uds_table):
        """Test missing MARISTAT - expect recode on 8 for V1/V2"""
        uds_table["file.info.forms.json"].update({"formver": 2.0, "maristat": 8})
        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_maristat() == 9

        uds_table["file.info.forms.json.maristat"] = 5
        assert attr._missingness_maristat() == 5

        uds_table["file.info.forms.json.maristat"] = None
        assert attr._missingness_maristat() == INFORMED_MISSINGNESS
