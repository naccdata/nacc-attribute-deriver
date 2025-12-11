"""Tests UDS Form D1 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_d1 import (
    UDSFormD1LegacyMissingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class TestUDSFormD1LegacyMissingness:
    def test_possadif(self, uds_table):
        """Test POSSADIF missingness."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "I",
                "normcog": 1,
                "possad": None,
                "possadif": None,
            }
        )

        attr = UDSFormD1LegacyMissingness(uds_table)
        assert attr._missingness_possadif() == 8

    def test_vascpsif(self, uds_table):
        """Tests VASCPSIF missingness."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 2.0,
                "packet": "I",
                "vasc": 1,
                "vascps": None,
                "vascpsif": None,
                "demented": 1,
            }
        )

        attr = UDSFormD1LegacyMissingness(uds_table)
        assert attr._missingness_vascpsif() == 7

        uds_table["file.info.forms.json"].update(
            {
                "formver": 2.0,
                "packet": "F",
                "vasc": 0,
                "vascps": None,
                "vascpsif": None,
                "normcog": 0,
                "demented": 0,
                "impnomci": 0,
                "mciaplus": 1,
                "formverd1": 1.0,  # what triggers
            }
        )

        attr = UDSFormD1LegacyMissingness(uds_table)
        assert attr._missingness_vascpsif() == INFORMED_MISSINGNESS

    def test_park(self, uds_table):
        """Test PARK missingness."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.0,
                "packet": "I",
                "lbdis": 0,
                "park": None,
            }
        )

        attr = UDSFormD1LegacyMissingness(uds_table)
        assert attr._missingness_park() == 0

        uds_table["file.info.forms.json"].update(
            {
                "park": 1,  # set so should keep
            }
        )
        assert attr._missingness_park() == 1
