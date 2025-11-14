"""Tests UDS Form Cx missingness attributes."""

import random

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_cx import (
    UDSFormC1C2Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


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

    def test_memtime(self, uds_table):
        """Tests missingness for MEMTIME."""
        uds_table["file.info.forms.json"].update(
            {"formver": 1.0, "packet": "I", "memtime": 88, "memunits": 97}
        )
        attr = UDSFormC1C2Missingness(uds_table)
        assert attr._missingness_memtime() == INFORMED_MISSINGNESS

        uds_table["file.info.forms.json"].update({"memtime": 88, "memunits": 0})
        attr = UDSFormC1C2Missingness(uds_table)
        assert attr._missingness_memtime() == 99

    def test_trailbx(self, uds_table):
        """Tests TRAILBX variables."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "I",
                "trailb": "996",
                "trailbrr": None,
                "trailbli": None,
            }
        )
        attr = UDSFormC1C2Missingness(uds_table)

        # REGRESSION - should NOT subtract 900 in new version
        assert attr._missingness_trailbrr() == 96
        assert attr._missingness_trailbli() == 96

    def test_logidate(self, uds_table):
        """Tests LOGIDATE (LOGINO, LOGIDAY, LOGIYR) variables.

        Should parse from logidate_c1.
        """
        uds_table["file.info.forms.json"].update(
            {"logidate_c1": "2025-06-09", "logiprev": 8}
        )
        attr = UDSFormC1C2Missingness(uds_table)

        # real date, expect None to return as-is
        assert attr._missingness_logiyr() is None
        assert attr._missingness_logimo() is None
        assert attr._missingness_logiday() is None

        # need to parse invalid date
        uds_table["file.info.forms.json"].update(
            {
                "logidate_c1": "9999-99-99",
            }
        )
        # convert to 88/88/8888
        assert attr._missingness_logiyr() == 8888
        assert attr._missingness_logimo() == 88
        assert attr._missingness_logiday() == 88
