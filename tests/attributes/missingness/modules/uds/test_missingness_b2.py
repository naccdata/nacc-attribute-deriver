"""Tests UDS Form B2 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_b2 import (
    UDSFormB2Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class TestUDSFormB2LegacyMissingness:
    def test_formver(self, uds_table):
        """Test the v1/v2 distinctino is enforced."""
        # formver = 2.0 but formverb2 = 1.0 case
        uds_table["file.info.forms.json"].update(
            {
                "formver": "2.0",
                "formverb2": 1.0,
                "cvdcog": 0,
                "cvdimag": 0,
                "cvdimag1": 0
            }
        )

        attr = UDSFormB2Missingness(uds_table)
        assert attr._missingness_cvdcog() == INFORMED_MISSINGNESS
        assert attr._missingness_cvdimag() == INFORMED_MISSINGNESS
        assert attr._missingness_cvdimag1() == INFORMED_MISSINGNESS

        # formver = 1.0 but formverb2 = 2.0; in which case logic should go
        # through
        uds_table["file.info.forms.json"].update(
            {
                "formver": "1.0",
                "formverb2": 2.0,
                "cvdcog": 0,
                "cvdimag": 8,
                "cvdimag1": 2
            }
        )

        attr = UDSFormB2Missingness(uds_table)
        assert attr._missingness_cvdcog() == 0
        assert attr._missingness_cvdimag() == 8
        assert attr._missingness_cvdimag1() == 8
