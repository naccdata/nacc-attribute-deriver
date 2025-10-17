"""Tests UDS Form A2 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a2 import (
    UDSFormA2Missingness,
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS


class TestUDSFormA2Missingness:
    def test_missingness_inlivwth_gate(self, uds_table):
        """Test _missingness_inlivwth_gate."""
        attr = UDSFormA2Missingness(uds_table)
        # V3 and earlier
        assert attr._missingness_inlivwth_gate() == INFORMED_MISSINGNESS

        # V4
        # test INLIVWTH is 1
        uds_table["file.info.forms.json"].update({"formver": 4.0, "inlivwth": 1})
        attr = UDSFormA2Missingness(uds_table)
        assert attr._missingness_inlivwth_gate() == 8

        # test INLIVWTH is 0
        uds_table["file.info.forms.json.inlivwth"] = 0
        assert attr._missingness_inlivwth_gate() is None
