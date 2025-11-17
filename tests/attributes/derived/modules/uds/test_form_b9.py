"""Tests UDS Form B9 attributes."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.uds.form_b9 import (
    UDSFormB9Attribute,
)
from nacc_attribute_deriver.attributes.derived.modules.uds.form_b9_raw import (
    UDSFormB9RawAttribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def base_table(uds_table) -> SymbolTable:
    """Create dummy base table."""
    uds_table["file.info.forms.json"].update({"packet": "F"})
    return uds_table


class TestUDSFormB9Attribute:
    def test_naccbehf_case1(self, base_table):
        """Tests NACCBEHF case 1.

        V1 form b9_changes is True (3) and p_decclin == 1, p_befrst ==
        88, so naccbehf == 0 this should work with befrst/decclin is
        null since V1
        """
        base_table["file.info.forms.json"].update({"b9chg": 3, "formver": 1.0})
        base_table["_prev_record.info.forms.json"].update(
            {
                "befrst": 88,
                "decclin": 1,
            }
        )

        attr = UDSFormB9Attribute(base_table)
        assert attr._create_naccbehf() == 0

        # if b9chg is None, should return 99
        base_table["file.info.forms.json.b9chg"] = None
        attr = UDSFormB9Attribute(base_table)
        assert attr._create_naccbehf() == 99

        # of V3, then always return 0
        base_table["file.info.forms.json.formver"] = "3.2"
        attr = UDSFormB9Attribute(base_table)
        assert attr._create_naccbehf() == 0

    def test_naccbehf_case2(self, base_table):
        """Tests NACCBEHF case 2.

        V3 form befpred == 0, so should get previous value
        """
        base_table["file.info.forms.json.befpred"] = 0
        base_table["_prev_record.info.forms.json"].update(
            {
                "befpred": 3,
            }
        )

        attr = UDSFormB9Attribute(base_table)
        assert attr._create_naccbehf() == 3

        # if befpred is something, should set to that value
        base_table["file.info.forms.json.befpred"] = 1
        assert attr._create_naccbehf() == 1

        # if befpred is 88, should return 0
        base_table["file.info.forms.json.befpred"] = 88
        assert attr._create_naccbehf() == 0

    def test_nacccogf_case1(self, base_table):
        """Tests NACCCOGF case 1.

        V3 form look at different values of cogfpred
        """
        # not there, so assumes no decline, return 0
        attr = UDSFormB9Attribute(base_table)
        assert attr._create_nacccogf() == 0

        # now make 0 (look at previous) but previous is None,
        # so should be 99
        base_table["file.info.forms.json.cogfpred"] = 0
        assert attr._create_nacccogf() == 99

        # now add a previous, so should return previous
        base_table["_prev_record.info.forms.json"].update(
            {
                "cogfpred": 3,
            }
        )

        assert attr._create_nacccogf() == 3

        # now test cogfpred in range
        base_table["file.info.forms.json.cogfpred"] = 6
        assert attr._create_nacccogf() == 6

        # out of range
        base_table["file.info.forms.json.cogfpred"] = 15
        assert attr._create_nacccogf() == 99

        # 88 should return 99
        base_table["file.info.forms.json.cogfpred"] = 88
        assert attr._create_nacccogf() == 99

    def test_nacccogf_case2(self, base_table):
        """Tests NACCCOGF case 2.

        V2 form look at different values of cogfrst
        """
        base_table["file.info.forms.json.formver"] = 2.0
        attr = UDSFormB9Attribute(base_table)

        # starting with not defined, looks at previous but does
        # not find anything so should be 99
        assert attr._create_nacccogf() == 99

        # set to 88, so nacccogf should be 0
        base_table["file.info.forms.json.cogfrst"] = 88
        assert attr._create_nacccogf() == 0

        # check range
        # this should trigger harmonization, so + 1
        base_table["file.info.forms.json.cogfrst"] = 3
        assert attr._create_nacccogf() == 4

        # this should trigger harmonization, 6 goes to 8
        base_table["file.info.forms.json.cogfrst"] = 6
        assert attr._create_nacccogf() == 8

        # 8 does not trigger harmonization but is in range
        base_table["file.info.forms.json.cogfrst"] = 8
        assert attr._create_nacccogf() == 8

        # out of range
        base_table["file.info.forms.json.cogfrst"] = 15
        assert attr._create_nacccogf() == 99

        # b9 changes and p_decclin is 0
        base_table["file.info.forms.json.b9chg"] = 1
        base_table["_prev_record.info.forms.json"].update(
            {
                "decclin": 0,
                "cogfrst": 88,
            }
        )

        attr = UDSFormB9Attribute(base_table)
        assert attr._create_nacccogf() == 0

        # p_decclin is 1 and p_cogfrst is 88 so return 0
        base_table["_prev_record.info.forms.json.decclin"] = 1
        assert attr._create_nacccogf() == 0

        # now p_cogfrst is something valid
        base_table["_prev_record.info.forms.json.cogfrst"] = 3
        assert attr._create_nacccogf() == 3

        # out of range
        base_table["_prev_record.info.forms.json.cogfrst"] = 15
        assert attr._create_nacccogf() == 15

    def test_nacccogf_get_last_set(self, base_table):
        """Tests NACCCOGF when the last set value was several visits ago."""
        base_table["file.info.forms.json"].update(
            {
                "formver": 3.0,
                "packet": "F",
                "decclin": None,
                "cogfrst": None,
                "cogfpred": "0",
            }
        )

        # set prev record but these should be ignored in favor
        # of the working namespace
        base_table["_prev_record.info.forms.json"].update(
            {"decclin": None, "cogfrst": None, "cogfpred": None}
        )

        # set working namespace, which is where it should
        # actually be grabbing values
        base_table["subject.info.working.cross-sectional"] = {
            "decclin": None,
            "cogfrst": None,
            "cogfpred": "1",
        }

        attr = UDSFormB9Attribute(base_table)
        assert attr._create_nacccogf() == 1



class TestUDSFormB9RawAttribute:
    def test_create_bevhago(self, base_table):
        """Test BEVHAGO case. Tests __handle_b9_attribute
        by extension.
        """
        attr = UDSFormB9RawAttribute(base_table)

        # if bevhago something valid, set it
        base_table["file.info.forms.json.bevhago"] = 25
        assert attr._create_bevhago() == 25

        # if bevhago = 777, don't set it; this means
        # if something else set it previously it will
        # stay at that attribute location, since this
        # returns None
        base_table["file.info.forms.json.bevhago"] = 777
        assert attr._create_bevhago() is None

        # REGRESSION: same for 888
        base_table["file.info.forms.json.bevhago"] = 888
        assert attr._create_bevhago() is None

    def test_create_frstchg(self, base_table):
        """Test FRSTCHG case. Tests __handle_b9_attribute
        by extension.
        """
        attr = UDSFormB9RawAttribute(base_table)

        # if frstchg something valid, set it
        base_table["file.info.forms.json.frstchg"] = 5
        assert attr._create_frstchg() == 5

        # if frstchg = 0, don't set it; this means
        # if something else set it previously it will
        # stay at that attribute location, since this
        # returns None
        base_table["file.info.forms.json.frstchg"] = 0
        assert attr._create_frstchg() is None

        # 888 is NOT ignored in this case since prev_code is not 777
        base_table["file.info.forms.json.frstchg"] = 888
        assert attr._create_frstchg() == 888
