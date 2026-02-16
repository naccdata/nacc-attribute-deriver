"""Tests UDS Form B9 missingness attributes."""

import random

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_b9 import (
    UDSFormB9Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


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

    def test_frstchg_v1(self, uds_table):
        """Handle V1 recoded FRSTCHG case."""
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

    def test_frstchg_v3(self, uds_table):
        """Test V3 FRSTCHG missingness case."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.2,
                "packet": "T",
                "frstchg": 0,
            }
        )
        uds_table["_prev_record.info.forms.json"] = {
            "visitdate": "2000-01-01",
            "formver": 3.2,
            "packet": "T",
            "frstchg": 1,
        }
        attr = UDSFormB9Missingness(uds_table)

        # prev is not None, expect prev_frstchg (1)
        assert attr._missingness_frstchg() == 1

        # prev is None, expect 9
        uds_table["_prev_record.info.forms.json.frstchg"] = None
        assert attr._missingness_frstchg() == 9

        # from resolved
        uds_table["_prev_record.info.forms.json.frstchg"] = 0
        uds_table["_prev_record.info.resolved.frstchg"] = 1
        assert attr._missingness_frstchg() == 1

    def test_carry_forward_777(self, uds_table):
        """Test when 777 is specified and a value must be carried through."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 2.3,
                "packet": "T",
                "decclmot": 1,
                "moage": 777,
            }
        )
        uds_table["_prev_record.info.forms.json"] = {
            "visitdate": "2000-01-01",
            "formver": 1.0,
            "packet": "I",
            "decclin": 1,
            "moage": 4,  # and range enforced to 9
        }

        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_moage() == 9
        assert attr._missingness_decclin() == 1

    def test_cognitive_ivp(self, uds_table):
        """Test missingness of cognitive variables on an initial.

        packet - version should not matter here.
        """
        uds_table["file.info.forms.json"].update(
            {
                "formver": random.choice([1.0, 2.0, 3.0, 4.0]),
                "packet": "I",
                "b9chg": None,
                "decclin": 0,
                "decclcog": None,
            }
        )

        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_cogmem() == 0
        assert attr._missingness_cogjudg() == 0
        assert attr._missingness_coglang() == 0
        assert attr._missingness_cogvis() == 0
        assert attr._missingness_cogattn() == 0
        assert attr._missingness_cogothr() == 0

    def test_behavior_ivp(self, uds_table):
        """Test missingness of behavior variables on an initial.

        packet - version should not matter here.
        """
        uds_table["file.info.forms.json"].update(
            {
                "formver": random.choice([1.0, 2.0, 3.0, 4.0]),
                "packet": "I",
                "b9chg": None,
                "decclin": 0,
                "decclbe": None,
            }
        )

        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_beapathy() == 0
        assert attr._missingness_bedep() == 0
        assert attr._missingness_beirrit() == 0
        assert attr._missingness_beagit() == 0
        assert attr._missingness_bevhall() == 0
        assert attr._missingness_beahall() == 0
        assert attr._missingness_bedel() == 0
        assert attr._missingness_bedisin() == 0
        assert attr._missingness_beperch() == 0
        assert attr._missingness_beothr() == 0

    def test_motor_ivp(self, uds_table):
        """Test missingness of cognitive variables on an initial.

        packet - version should not matter here.
        """
        uds_table["file.info.forms.json"].update(
            {
                "formver": random.choice([1.0, 2.0, 3.0, 4.0]),
                "packet": "I",
                "b9chg": None,
                "decclin": 0,
                "decclmot": None,
            }
        )

        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_mogait() == 0
        assert attr._missingness_mofalls() == 0
        assert attr._missingness_moslow() == 0
        assert attr._missingness_motrem() == 0

    def test_bevwell(self, uds_table):
        """Tests missingness for BEVWELL."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 2.0,
                "packet": "I",
                "b9chg": None,
                "decclin": 1,
                "decclbe": None,
            }
        )

        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_bevwell() == INFORMED_MISSINGNESS

        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "I",
                "decclin": 1,
                "decclbe": None,
                "bevwell": 0,  # should use this
            }
        )
        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_bevwell() == 0

    def test_beagit(self, uds_table):
        """Tests missingness for BEAGIT."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "I",
                "b9chg": None,
                "decclin": 0,
                "decclbe": None,
                "beagit": None,
            }
        )
        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_beagit() == 0

    def test_beothr(self, uds_table):
        """Tests missingness for BEOTHR."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "I",
                "decclin": 1,
                "decclbe": None,
                "beothr": 9,  # should recode to 0
            }
        )
        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_beothr() == 0

    def test_momopark(self, uds_table):
        """Tests missingness for BEOTHR."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "I",
                "decclin": 1,
                "decclmot": None,
                "momopark": 88,  # should recode to 8
            }
        )
        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_momopark() == 8

    def test_berem(self, uds_table):
        """Tests missingness for BEREM."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "I",
                "decclin": 1,
                "decclbe": None,
                "berem": 1,  # should use this
            }
        )
        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_berem() == 1

    def test_bevhago(self, uds_table):
        """Tests missingness for BEVHAGO."""
        uds_table["file.info.forms.json"].update(
            {"formver": 3.0, "packet": "I", "bevhall": 1, "bevhago": None}
        )
        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_bevhago() == 888

        # test range is enforced
        uds_table["file.info.forms.json.bevhago"] = 5
        assert attr._missingness_bevhago() == 15
        uds_table["file.info.forms.json.bevhago"] = 114
        assert attr._missingness_bevhago() == 110

    def test_decage_get_last_set(self, uds_table):
        """Tests DECAGE when the last set value was several visits ago."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.0,
                "packet": "F",
                "decage": "777",
            }
        )

        # set prev record but these should be ignored in favor
        # of the working namespace
        uds_table["_prev_record.info.forms.json"].update(
            {
                "decage": None,
            }
        )

        # set working namespace, which is where it should
        # actually be grabbing values
        uds_table["subject.info.working.cross-sectional"] = {"decage": "78"}

        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_decage() == 78

    def test_decage_prev_visit(self, uds_table):
        """Tests DECAGE from previous visit."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.0,
                "packet": "F",
                "decage": "777",
            }
        )

        uds_table["_prev_record.info.forms.json"].update(
            {
                "decage": 65,
            }
        )

        uds_table["subject.info.working.cross-sectional"] = {"decage": None}

        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_decage() == 65

    def test_coglang(self, uds_table):
        """Test some specific COGLANG cases."""

        # CASE 1: decclin and decclcog are None, expect 0
        uds_table["file.info.forms.json"].update(
            {"formver": 2.0, "decclin": None, "decclcog": None, "coglang": None}
        )
        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_coglang() == 0

    def test_cogattn(self, uds_table):
        """Test some specific COGATTN cases."""

        # CASE 1:
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "F",
                "decclin": None,
                "decclcog": None,
                "cogattn": 1,  # should be what gets returned regardless of prev record
                "b9chg": 3,  # so doesn't do recodebm logic
            }
        )

        # so would trigger the previous check; however since
        # the CURRENT cogattn is set, we should return that (1)
        uds_table["_prev_record.info.forms.json"].update({"decclin": 1, "cogattn": 9})

        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_cogattn() == 1

        # CASE 2:
        # another similar case where it should actually return the
        # current value even when prev record has decclin = 1 and cogattn = 9
        # but slightly different values on the current form
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "F",
                "decclin": 1,
                "decclcog": None,
                "cogattn": 0,  # should be what gets returned regardless of prev record
                "b9chg": 2,  # this + decclin being 1 causes no recodebm logic
            }
        )

        # so would trigger the previous check; however since
        # the CURRENT cogattn is set, we should return that (0 for this case)
        uds_table["_prev_record.info.forms.json"].update({"decclin": 1, "cogattn": 9})

        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_cogattn() == 0

        # CASE 3:
        # this case does trigger recodebm logic; tests a correction from old behavior
        # regarding whether the previous form is the raw vs missingness values
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "F",
                "decclin": None,
                "decclcog": None,
                "cogattn": None,
                "b9chg": 1,  # this + decclin being null runs recodebm logic
            }
        )

        # since nothing set in the previous visit, causes the default = 0
        uds_table["_prev_record.info.forms.json"].update({"decclin": 1, "cogattn": 1})

        # old code would return 0 due to directly using previous raw
        # values; after discussion 1 is the better/more correct behavior
        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_cogattn() == 1

    def test_cogjudg(self, uds_table):
        """Test some specific COGJUDG cases."""
        # CASE 1: case where formver == 2 but formverb9 = 1, so this
        # should actually trigger V1 logic and look at previous form
        uds_table["file.info.forms.json"].update(
            {
                "formver": 2.0,
                "formverb9": 1.0,
                "packet": "F",
                "decclin": None,
                "decclcog": None,
                "cogjudg": None,
                "b9chg": 1,  # this + decclin being null runs recodebm logic
            }
        )

        # since nothing set in the previous visit, causes the default = 0
        uds_table["_prev_record.info.forms.json"].update({"decclin": 1, "cogjudg": 1})

        attr = UDSFormB9Missingness(uds_table)
        assert attr._missingness_cogjudg() == 1
