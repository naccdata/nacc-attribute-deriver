"""Tests UDS Form B1 attributes."""

from nacc_attribute_deriver.attributes.nacc.modules.uds.form_b1 import (
    UDSFormB1Attribute,
)


class TestUDSFormB1Attribute:
    def test_create_naccbmi(self, uds_table):
        """Tests NACCBMI."""
        uds_table["file.info.forms.json"].update(
            {
                "b1sub": 1,
                "weight": 165,
                "height": 60
            }
        )

        attr = UDSFormB1Attribute(uds_table)
        assert attr._create_naccbmi() == 32.2

        # this tests the half case
        uds_table["file.info.forms.json"].update(
            {
                "b1sub": 1,
                "weight": 180,
                "height": 60
            }
        )

        attr = UDSFormB1Attribute(uds_table)
        assert attr._create_naccbmi() == 35.2
