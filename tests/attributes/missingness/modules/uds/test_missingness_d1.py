"""Tests UDS Form D1 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_d1 import (
    UDSFormD1LegacyMissingness,
)


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
