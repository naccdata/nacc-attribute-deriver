"""Tests UDS Form Cx missingness attributes."""

import random

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_cx import (
    UDSFormC1C2Missingness,
)


class TestUDSFormC1C2Missingness:
    def test_reyxrec_cascade(self, uds_table):
        """Test the REYXREC cascade effect."""
        cascade_value = random.choice([88, 95, 96, 97, 98])
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.2,
                "packet": "T",
                "reydrec": cascade_value,
                "rey1rec": cascade_value,
            }
        )

        attr = UDSFormC1C2Missingness(uds_table)

        # these don't require gate_mresult since
        # REYDREC and REY1REC should be there
        assert attr._missingness_reydint() == cascade_value
        assert attr._missingness_reytcor() == cascade_value
        assert attr._missingness_reyfpos() == cascade_value
        assert attr._missingness_rey1int() == cascade_value
        assert attr._missingness_rey2rec() == cascade_value
        assert attr._missingness_rey2int() == cascade_value

        # these need to call their gate's missingness,
        # e.g. set gate_mresult. should cascade
        assert attr._missingness_rey3rec() == cascade_value
        assert attr._missingness_rey3int() == cascade_value
        assert attr._missingness_rey4rec() == cascade_value
        assert attr._missingness_rey4int() == cascade_value
        assert attr._missingness_rey5rec() == cascade_value
        assert attr._missingness_rey5int() == cascade_value

        assert attr._missingness_reybrec() == cascade_value
        assert attr._missingness_reybint() == cascade_value
        assert attr._missingness_rey6rec() == cascade_value
        assert attr._missingness_rey6int() == cascade_value
