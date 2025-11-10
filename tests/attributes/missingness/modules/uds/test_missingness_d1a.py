"""Tests UDS Form D1a missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_d1a import (
    UDSFormD1aMissingness,
)


class TestUDSFormD1aMissingness:
    def test_cogothx(self, uds_table):
        """Tests the COGOTHX variables."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "I",
                "normcog": 1,
                "cogoth": 0,
                "cogoth2": None,
                "cogoth3": None,
                "cogothif": None,
                "cogoth2f": None,
                "cogoth3f": None,
            }
        )
        attr = UDSFormD1aMissingness(uds_table)
        assert attr._missingness_cogoth() is None  # uses raw value
        assert attr._missingness_cogoth2() == 8
        assert attr._missingness_cogoth3() == 8

        assert attr._missingness_cogothif() == 8
        assert attr._missingness_cogoth2f() == 8
        assert attr._missingness_cogoth3f() == 8

    def test_amndem(self, uds_table):
        """Tests missingness for AMNDEM."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.0,
                "packet": "I",
                "demented": 0,
                "amndem": 0,
            }
        )
        attr = UDSFormD1aMissingness(uds_table)
        assert attr._missingness_amndem() is None  # uses raw value

        uds_table["file.info.forms.json.amndem"] = None
        assert attr._missingness_amndem() == 8
