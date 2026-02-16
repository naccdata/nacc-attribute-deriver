"""Tests UDS Form B1 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_b1 import (
    UDSFormB1Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class TestUDSFormB1LegacyMissingness:
    def test_ranges(self, uds_table):
        """Test ranges are enforced."""
        # minimums
        uds_table["file.info.forms.json"].update(
            {
                "height": 35,
                "heigdec": 9,
                "weight": 49,
                "bpsys": 69,
                "bpdias": 29,
                "bpsysl": 69,
                "bpsysr": 69,
                "bpdiasl": 29,
                "bpdiasr": 29,
                "hrate": 32,
            }
        )
        attr = UDSFormB1Missingness(uds_table)
        assert attr._missingness_height() == 36.0
        assert attr._missingness_weight() == 50
        assert attr._missingness_bpsys() == 70
        assert attr._missingness_bpdias() == 30
        assert attr._missingness_bpsysl() == 70
        assert attr._missingness_bpsysr() == 70
        assert attr._missingness_bpdiasl() == 30
        assert attr._missingness_bpdiasr() == 30
        assert attr._missingness_hrate() == 33

        # maximums
        uds_table["file.info.forms.json"].update(
            {
                "height": 87,
                "heigdec": 99,
                "weight": 401,
                "bpsys": 231,
                "bpdias": 141,
                "bpsysl": 231,
                "bpsysr": 231,
                "bpdiasl": 141,
                "bpdiasr": 141,
                "hrate": 161,
            }
        )
        attr = UDSFormB1Missingness(uds_table)
        assert attr._missingness_height() == 87.9
        assert attr._missingness_weight() == 400
        assert attr._missingness_bpsys() == 230
        assert attr._missingness_bpdias() == 140
        assert attr._missingness_bpsysl() == 230
        assert attr._missingness_bpsysr() == 230
        assert attr._missingness_bpdiasl() == 140
        assert attr._missingness_bpdiasr() == 140
        assert attr._missingness_hrate() == 160

        # test 999s get set to 888 and Nones/777s/888s are untouched
        uds_table["file.info.forms.json"].update(
            {
                "height": 88,
                "heigdec": 8,
                "weight": 999,
                "bpsys": 777,
                "bpdias": 777,
                "bpsysl": None,
                "bpsysr": 888,
                "bpdiasl": 999,
                "bpdiasr": None,
                "hrate": 999,
            }
        )
        attr = UDSFormB1Missingness(uds_table)
        assert attr._missingness_height() == 88.8
        assert attr._missingness_weight() == 888
        assert attr._missingness_bpsys() == 777
        assert attr._missingness_bpdias() == 777
        assert attr._missingness_bpsysl() == INFORMED_MISSINGNESS
        assert attr._missingness_bpsysr() == 888
        assert attr._missingness_bpdiasl() == 888
        assert attr._missingness_bpdiasr() == INFORMED_MISSINGNESS
        assert attr._missingness_hrate() == 888

    def test_b1a_addendum(self, uds_table):
        """Test there is a B1a addendum."""
        uds_table["file.info.forms.json.visitdate"] = "2026-01-01"
        uds_table["subject.info.working.longitudinal"] = {
            "bpdevice": [
                {
                    "date": "2026-01-01",
                    "value": 1,
                },
            ],
            "bpdiasl": [
                {
                    "date": "2026-01-01",
                    "value": 50,
                },
            ],
            "bpdiasr": [
                {
                    "date": "2026-01-01",
                    "value": 70,
                },
            ],
            "bpsysl": [
                {
                    "date": "2026-01-01",
                    "value": 100,
                },
            ],
            "bpsysr": [
                {
                    "date": "2026-01-01",
                    "value": 110,
                },
            ],
        }

        attr = UDSFormB1Missingness(uds_table)
        assert attr._missingness_bpdevice() == 1
        assert attr._missingness_bpdiasl() == 50
        assert attr._missingness_bpdiasr() == 70
        assert attr._missingness_bpsysl() == 100
        assert attr._missingness_bpsysr() == 110

        # wrong date - all missing
        uds_table["file.info.forms.json.visitdate"] = "2025-01-01"
        attr = UDSFormB1Missingness(uds_table)
        assert attr._missingness_bpdevice() == INFORMED_MISSINGNESS
        assert attr._missingness_bpdiasl() == INFORMED_MISSINGNESS
        assert attr._missingness_bpdiasr() == INFORMED_MISSINGNESS
        assert attr._missingness_bpsysl() == INFORMED_MISSINGNESS
        assert attr._missingness_bpsysr() == INFORMED_MISSINGNESS
