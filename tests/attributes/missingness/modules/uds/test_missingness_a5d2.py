"""Tests UDS Form A5D2 missingness attributes."""

import random

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a5d2 import (
    UDSFormA5D2Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


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

    def test_quitsmok(self, uds_table):
        """Test QUITSMOK missingness."""
        attr = UDSFormA5D2Missingness(uds_table)
        uds_table["file.info.forms.json"].update(
            {"formver": 3.0, "quitsmok": None, "smokyrs": None, "tobac100": 9}
        )

        # in legacy this returned 888; now should return 999
        assert attr._missingness_quitsmok() == 999

    def test_3_digit_adjustment(self, uds_table):
        """Test 88/99 gets adjusted."""
        uds_table["file.info.forms.json"].update(
            {
                "menarche": "88",
                "nomensage": 99,
                "hrtyears": 99,
                "hrtstrtage": 99,  # can't adjust due to range
                "hrtendage": 99,  # can't adjust due to range
                "bcpillsyr": 99,
                "bcstartage": "99",
                "bcendage": 88,
            }
        )

        attr = UDSFormA5D2Missingness(uds_table)
        assert attr._missingness_menarche() == 888
        assert attr._missingness_nomensage() == 999
        assert attr._missingness_hrtyears() == 999
        assert attr._missingness_hrtstrtage() == 99
        assert attr._missingness_hrtendage() == 99
        assert attr._missingness_bcpillsyr() == 999
        assert attr._missingness_bcstartage() == 999
        assert attr._missingness_bcendage() == 888

    def test_handle_arth_gate(self, uds_table):
        """Test old legacy D2-only variables that rely
        on ARTH. Using ARTLOEX as a representative to
        check but several other variables rely on this.
        """
        # ARTH = 0 case, expect 8
        uds_table["file.info.forms.json"].update(
            {
                "arth": 0,
                "artloex": random.choice([None, 0]),
            }
        )

        attr = UDSFormA5D2Missingness(uds_table)
        assert attr._missingness_artloex() == 8

        # ARTH = 8/blank case, expect -4
        uds_table["file.info.forms.json"].update(
            {
                "arth": random.choice([None, 8]),
                "artloex": random.choice([None, 0]),
            }
        )
        assert attr._missingness_artloex() == INFORMED_MISSINGNESS

        # ARTH = 1 case, generic missingness, returns whatever
        # it was set to else INFORMED_MISSINGNESS
        value = random.choice([1, 2, 3, 8, 9])
        uds_table["file.info.forms.json"].update(
            {
                "arth": 1,
                "artloex": value,
            }
        )
        assert attr._missingness_artloex() == value

        uds_table["file.info.forms.json.artloex"] = 0
        assert attr._missingness_artloex() == 0

        uds_table["file.info.forms.json.artloex"] = None
        assert attr._missingness_artloex() == INFORMED_MISSINGNESS
