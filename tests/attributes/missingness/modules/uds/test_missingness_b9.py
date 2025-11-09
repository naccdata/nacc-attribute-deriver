"""Tests UDS Form B9 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_b9 import (
    UDSFormB9Missingness,
)


class TestUDSFormB9Missingness:
    def test_handle_recodecbm(self, uds_table):
        """Test the V1 macro recodecbm."""
        uds_table["file.info.forms.json"].update({"testvar": 15})
        attr = UDSFormB9Missingness(uds_table)
        # Start with initial visit, so no b9chg or p_decclin
        # should just return None
        assert attr._handle_recodecbm("testvar") is None
        assert attr._handle_recodecbm("testvar", overall=True) is None

        # make FVP and add b9chg and prev record to trigger logic
        uds_table["file.info.forms.json"].update(
            {"packet": "F", "b9chg": 1, "testvar": None}
        )
        uds_table["_prev_record.info.forms.json"] = {
            "decclin": 0,
            "testvar": 13,
            "visitdate": "2000-01-01",
        }
        attr = UDSFormB9Missingness(uds_table)

        assert attr._handle_recodecbm("testvar") == 0
        assert attr._handle_recodecbm("testvar", overall=True) == 8
        uds_table["_prev_record.info.forms.json.decclin"] = 1
        assert attr._handle_recodecbm("testvar") == 13
        assert attr._handle_recodecbm("testvar", overall=True) == 13

        # condition: B9CHG == 2, DECCLIN == 0, FIELD != 1
        uds_table["file.info.forms.json"].update(
            {"b9chg": 2, "testvar": 11, "decclin": 1}
        )
        attr = UDSFormB9Missingness(uds_table)
        assert attr._handle_recodecbm("testvar") is None
        assert attr._handle_recodecbm("testvar", overall=True) is None

        uds_table["file.info.forms.json.decclin"] = 0
        assert attr._handle_recodecbm("testvar") == 0
        assert attr._handle_recodecbm("testvar", overall=True) == 8

        uds_table["file.info.forms.json.testvar"] = 1
        assert attr._handle_recodecbm("testvar") is None
        assert attr._handle_recodecbm("testvar", overall=True) is None

        # overall=True also allows B9CHG = 3
        uds_table["file.info.forms.json"].update(
            {"b9chg": 3, "testvar": None, "decclin": 1}
        )
        attr = UDSFormB9Missingness(uds_table)
        assert attr._handle_recodecbm("testvar") is None
        assert attr._handle_recodecbm("testvar", overall=True) == 13  # prev value

    def test_recoded_frstchg(self, uds_table):
        """Handle recoded FRSTCHG case."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "F",
                "b9chg": 3,
                "decclin": None,
                "frstchg": None,
            }
        )
        uds_table["_prev_record.info.forms.json"] = {
            "visitdate": "2000-01-01",
            "formver": 1.0,
            "packet": "I",
            "decclin": 1,
            "frstchg": 1,
        }
        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_frstchg() == 1
