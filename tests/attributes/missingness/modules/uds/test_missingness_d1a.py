"""Tests UDS Form D1a missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_d1a import (
    UDSFormD1aMissingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_BLANK, INFORMED_MISSINGNESS


class TestUDSFormD1aMissingness:
    def test_cogothx(self, uds_table):
        """Tests the COGOTHX variables."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "I",
                "normcog": 1,
                "cogoth": 0,
            }
        )
        attr = UDSFormD1aMissingness(uds_table)
        # this specific set always force-resolves due to
        # potential need to reorder
        assert attr._missingness_cogoth() == 0
        assert attr._missingness_cogoth2() == 8
        assert attr._missingness_cogoth3() == 8

        assert attr._missingness_cogothif() == 8
        assert attr._missingness_cogoth2f() == 8
        assert attr._missingness_cogoth3f() == 8

        assert attr._missingness_cogothx() == INFORMED_BLANK
        assert attr._missingness_cogoth2x() == INFORMED_BLANK
        assert attr._missingness_cogoth3x() == INFORMED_BLANK

        # test when formverd1 == 1.0, some should explicitly
        # be INFORMED_MISSINGNESS now instead
        uds_table["file.info.forms.json"].update(
            {
                "formver": 2.0,
                "formverd1": 1.0
            }
        )
        attr = UDSFormD1aMissingness(uds_table)
        assert attr._missingness_cogoth() == 0
        assert attr._missingness_cogoth2() == INFORMED_MISSINGNESS
        assert attr._missingness_cogoth3() == INFORMED_MISSINGNESS

        assert attr._missingness_cogothif() == 8
        assert attr._missingness_cogoth2f() == INFORMED_MISSINGNESS
        assert attr._missingness_cogoth3f() == INFORMED_MISSINGNESS

        assert attr._missingness_cogothx() == INFORMED_BLANK
        assert attr._missingness_cogoth2x() == INFORMED_BLANK
        assert attr._missingness_cogoth3x() == INFORMED_BLANK

    def test_cogothx_reordering(self, uds_table):
        """Tests when we need to reorder the COGOTH variables.

        3 needs to move up to 1
        """
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.0,
                "packet": "F",
                "normcog": 1,
                "cogoth": 0,
                "cogoth2": 0,
                "cogoth3": 1,
                "cogothif": None,
                "cogoth2f": None,
                "cogoth3f": 1,
                "cogothx": None,
                "cogoth2x": None,
                "cogoth3x": "some text",
            }
        )
        attr = UDSFormD1aMissingness(uds_table)
        assert attr._missingness_cogoth() == 1
        assert attr._missingness_cogoth2() == 0
        assert attr._missingness_cogoth3() == 0

        assert attr._missingness_cogothif() == 1
        assert attr._missingness_cogoth2f() == 8
        assert attr._missingness_cogoth3f() == 8

        assert attr._missingness_cogothx() == "some text"
        assert attr._missingness_cogoth2x() == INFORMED_BLANK
        assert attr._missingness_cogoth3x() == INFORMED_BLANK

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
