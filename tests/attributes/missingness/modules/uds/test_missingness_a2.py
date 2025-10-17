"""Tests UDS Form A2 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a2 import (
    UDSFormA2Missingness,
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS


class TestUDSFormA2Missingness:
    def test_missingness_inlivwth_gate(self, uds_table):
        """Test missing INCNTMOD and INCNTTIM, which have same condition."""
        attr = UDSFormA2Missingness(uds_table)
        # V3 and earlier
        assert attr._missingness_incntmod() == INFORMED_MISSINGNESS
        assert attr._missingness_incnttim() == INFORMED_MISSINGNESS

        # V4
        # test INLIVWTH is 1
        uds_table["file.info.forms.json"].update({"formver": 4.0, "inlivwth": 1})
        attr = UDSFormA2Missingness(uds_table)
        assert attr._missingness_incntmod() == 8
        assert attr._missingness_incnttim() == 8

        # test INLIVWTH is 0 but the values are missing
        uds_table["file.info.forms.json.inlivwth"] = 0
        assert attr._missingness_incntmod() == INFORMED_MISSINGNESS
        assert attr._missingness_incnttim() == INFORMED_MISSINGNESS

        # now the values are set to something, so should return None
        uds_table["file.info.forms.json"].update({"incntmod": 1, "incnttim": 2})
        assert attr._missingness_incntmod() is None
        assert attr._missingness_incnttim() is None
