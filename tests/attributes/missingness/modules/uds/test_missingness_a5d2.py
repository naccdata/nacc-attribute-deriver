"""Tests UDS Form A5D2 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a5d2 import (
    UDSFormA5D2Missingness,
)


class TestUDSFormA5D2Missingness:
    def test_handle_a5d2_carry_forward(self, uds_table):
        """Test the handle_a5d2_carry_forward method."""
        attr = UDSFormA5D2Missingness(uds_table)

        uds_table["file.info.forms.json.hrtattack"] = "0"
        assert attr.handle_a5d2_carry_forward("hrtattack", "hrtattage") == 888
        uds_table["file.info.forms.json.hrtattack"] = "9"
        assert attr.handle_a5d2_carry_forward("hrtattack", "hrtattage") == 999

        # previous case
        uds_table["file.info.forms.json"].update(
            {"packet": "F", "hrtattack": 1, "hrtattage": 777}
        )
        uds_table["_prev_record.info.forms.json.hrtattage"] = 3
        attr = UDSFormA5D2Missingness(uds_table)  # need to remake to change to FVP
        assert attr.handle_a5d2_carry_forward("hrtattack", "hrtattage") == 3

        # prev is also 777, so use resolved
        uds_table["_prev_record.info.forms.json.hrtattage"] = 777
        uds_table["_prev_record.info.resolved.hrtattage"] = 5
        assert attr.handle_a5d2_carry_forward("hrtattack", "hrtattage") == 5
