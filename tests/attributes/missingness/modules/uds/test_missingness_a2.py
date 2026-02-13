"""Tests UDS Form A2 missingness attributes."""

import random

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a2 import (
    UDSFormA2Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class TestUDSFormA2Missingness:
    def test_missingness_inlivwth_gate(self, uds_table):
        """Test missing INCNTMOD and INCNTTIM, which have same condition."""
        attr = UDSFormA2Missingness(uds_table)
        # V3 and earlier
        assert attr._missingness_incntmod() == INFORMED_MISSINGNESS
        assert attr._missingness_incnttim() == INFORMED_MISSINGNESS

        # V4
        # test INLIVWTH is 1
        uds_table["file.info.forms.json"].update({"formver": 4.0, "inlivwth": 1})
        attr = UDSFormA2Missingness(uds_table)
        assert attr._missingness_incntmod() == 8
        assert attr._missingness_incnttim() == 8

        # test INLIVWTH is 0 but the values are missing
        uds_table["file.info.forms.json.inlivwth"] = 0
        assert attr._missingness_incntmod() == INFORMED_MISSINGNESS
        assert attr._missingness_incnttim() == INFORMED_MISSINGNESS

        # now the values are set to something, so stay as-is
        uds_table["file.info.forms.json"].update({"incntmod": 1, "incnttim": 2})
        assert attr._missingness_incntmod() == 1
        assert attr._missingness_incnttim() == 2

    def test_missingness_inbiryr(self, uds_table):
        """Tests INBIRYR is corrected when set to 99."""
        attr = UDSFormA2Missingness(uds_table)

        uds_table["file.info.forms.json.inbiryr"] = "99"
        assert attr._missingness_inbiryr() == 9999

        uds_table["file.info.forms.json.inbiryr"] = "1999"
        assert attr._missingness_inbiryr() == 1999

    def test_newinf_packet(self, uds_table):
        """Test NEWINF is always -4 in IVP."""
        uds_table["file.info.forms.json"].update(
            {
                "packet": random.choice(["I", "I4"]),
                "newinf": 1,
            }
        )
        attr = UDSFormA2Missingness(uds_table)
        assert attr._missingness_newinf() == INFORMED_MISSINGNESS

        uds_table["file.info.forms.json"].update(
            {
                "packet": random.choice(["F", "T"]),
                "newinf": 1,
            }
        )
        attr = UDSFormA2Missingness(uds_table)
        assert attr._missingness_newinf() == 1

    def test_missingness_newinf_gate(self, uds_table):
        """Test NEWINF-gated variables."""
        # if IVP, ignore NEWINF even if it's set
        # spot check a few variables
        uds_table["file.info.forms.json"].update(
            {
                "packet": "I",
                "newinf": 0,
                "inknown": 32,
                "ineduc": 13,
                "inhisp": 9,
                "inhispor": 5,  # gets changed because of INHISP
            }
        )
        attr = UDSFormA2Missingness(uds_table)

        assert attr._missingness_inknown() == 32
        assert attr._missingness_ineduc() == 13
        assert attr._missingness_inhisp() == 9
        assert attr._missingness_inhispor() == 88

        # check INHISP behavior; now INHISP no longer
        # blocking it
        uds_table["file.info.forms.json.inhisp"] = 2
        assert attr._missingness_inhispor() == 5

        # now FVP, all should get set to -4
        uds_table["file.info.forms.json.packet"] = "F"
        attr = UDSFormA2Missingness(uds_table)

        assert attr._missingness_inknown() == INFORMED_MISSINGNESS
        assert attr._missingness_ineduc() == INFORMED_MISSINGNESS
        assert attr._missingness_inhisp() == INFORMED_MISSINGNESS
        assert attr._missingness_inhispor() == INFORMED_MISSINGNESS

    def test_inknown_version(self, uds_table):
        """Test inknkown respects version."""
        # in V3/V4
        uds_table["file.info.forms.json"].update(
            {"formver": random.choice([3, 4]), "inknown": 35}
        )
        attr = UDSFormA2Missingness(uds_table)
        assert attr._missingness_inknown() == 35

        # not in V1/V2
        uds_table["file.info.forms.json.formver"] = random.choice([1, 2])
        attr = UDSFormA2Missingness(uds_table)
        assert attr._missingness_inknown() == INFORMED_MISSINGNESS
