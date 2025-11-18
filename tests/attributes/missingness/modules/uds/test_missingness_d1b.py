"""Tests UDS Form D1b missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_d1b import (
    UDSFormD1bMissingness,
)


class TestUDSFormD1bMissingness:
    def test_ftldsubt(self, uds_table):
        """Test FTLDSUBT missingness - from regression tests."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.0,
                "packet": "I",
                "normcog": 1,
                "psp": 0,
                "cort": 0,
                "ftldmo": 0,
                "ftldnos": 0,
                "ftldsubt": None,
            }
        )

        attr = UDSFormD1bMissingness(uds_table)
        assert attr._missingness_ftldsubt() == 8

        uds_table["file.info.forms.json"].update(
            {
                "normcog": 0,
                "psp": 0,
                "cort": 0,
                "ftldmo": 0,
                "ftldnos": 1,
                "ftldsubt": 2,
            }
        )

        assert attr._missingness_ftldsubt() == 2
