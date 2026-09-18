"""Tests UDS Form A1 attributes."""

import random
import pytest
from nacc_attribute_deriver.attributes.derived.modules.uds.form_a1 import (
    UDSFormA1Attribute,
)
from nacc_attribute_deriver.attributes.derived.modules.uds.form_a1_raw import (
    UDSFormA1RawAttribute,
)
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table(uds_table) -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    uds_table["file.info.forms.json"].update(
        {
            "educ": "3",
        }
    )
    uds_table.update(
        {
            "subject": {
                "info": {
                    "derived": {
                        "cross-sectional": {
                            "naccnihr": 2,
                        }
                    }
                }
            },
        }
    )
    return uds_table


class TestUDSFormA1Attribute:
    def test_create_naccage(self, table, form_prefix):
        """Tests creating NACCAGE."""
        attr = UDSFormA1Attribute(table)
        assert attr._create_naccage() == 34

        # exact birthday
        set_attribute(table, form_prefix, "birthmo", 1)
        assert attr._create_naccage() == 35

    def test_visit_on_birthday(self, table, form_prefix):
        """Case that has issue due to visitdate == birthday."""
        set_attribute(table, form_prefix, "visitdate", "2007-06-01")
        set_attribute(table, form_prefix, "birthmo", 6)
        set_attribute(table, form_prefix, "birthyr", 1910)
        attr = UDSFormA1Attribute(table)

        assert attr._create_naccage() == 97

        """Case that has issue due to visitdate == birthday."""
        set_attribute(table, form_prefix, "visitdate", "2010-03-01")
        set_attribute(table, form_prefix, "birthmo", 3)
        set_attribute(table, form_prefix, "birthyr", 1956)

        assert attr._create_naccage() == 54

    def test_followup_packet(self, table, form_prefix):
        """Tests the followup cases."""
        # check not a followup packet so returns 99
        attr = UDSFormA1Attribute(table)
        assert attr._create_naccnihr() == 99

        # now set as followup packet, shsould return None
        # since race is only defined at initial visit
        set_attribute(table, form_prefix, "packet", "F")
        assert attr._create_naccnihr() is None

    def test_affiliate(self, table, form_prefix):
        """Tests affiliate case."""
        attr = UDSFormA1Attribute(table)
        assert not attr._create_affiliate()

        # source case
        set_attribute(table, form_prefix, "source", 4)
        assert attr._create_affiliate() == 1

        # sourcenw case
        set_attribute(table, form_prefix, "source", 1)
        set_attribute(table, form_prefix, "sourcenw", 2)
        assert attr._create_affiliate() == 1

        # set but something else case
        set_attribute(table, form_prefix, "sourcenw", 1)
        assert attr._create_affiliate() == 0

    def test_affiliate_update(self, table):
        """Tests affiliate case when updated."""
        # case 1: IVP; nothing set
        attr = UDSFormA1Attribute(table)
        assert attr._create_affiliate() == 0

        # case 2: IVP; subject is set to True
        table["subject.info.derived.affiliate"] = True
        assert attr._create_affiliate() == 1

        # case 3: IVP; overrides
        table["file.info.forms.json.sourcenw"] = 1
        assert attr._create_affiliate() == 0

    def test_create_naccsex(self, table):
        """Test _create_naccsex."""
        table["file.info.forms.json"].update(
            {
                "sex": 1,  # V3
                "birthsex": "2",  # V4
            }
        )
        attr = UDSFormA1Attribute(table)
        assert attr._create_naccsex() == 1

        table["file.info.forms.json.formver"] = 4.0
        attr = UDSFormA1Attribute(table)
        assert attr._create_naccsex() == 2

    def test_create_nacclang(self, table):
        """Tests _create_nacclang."""
        # cycle through mappings for V3 and earlier
        primlang_map = {1: 1, 2: 2, 3: 3, 4: 3, 5: 4, 6: 5, 8: 8, 9: 9}

        attr = UDSFormA1Attribute(table)
        for source, expected in primlang_map.items():
            table["file.info.forms.json.primlang"] = str(source)
            assert attr._create_nacclang() == expected

        # v4
        table["file.info.forms.json"].update({"formver": 4.0, "predomlan": "5"})
        attr = UDSFormA1Attribute(table)
        assert attr._create_nacclang() == 5

    def test_create_nacclangx(self, table):
        """Tests _create_nacclangx."""
        table["file.info.forms.json"].update(
            {
                "primlanx": "some legacy text",  # V3
                "predomlanx": "some current text",  # V4
            }
        )
        attr = UDSFormA1Attribute(table)
        assert attr._create_nacclangx() == "some legacy text"

        table["file.info.forms.json.formver"] = 4.0
        attr = UDSFormA1Attribute(table)
        assert attr._create_nacclangx() == "some current text"

        # check returns informed blank if missing
        table["file.info.forms.json.predomlanx"] = None
        assert attr._create_nacclangx() == INFORMED_BLANK

    def test_create_naccnihr_v1v3(self, table):
        """V1-3 race is kept for V1-3 rows and never written by an I4."""
        table["file.info.forms.json"].update({"race": 1})
        assert UDSFormA1Attribute(table)._create_naccnihr_v1v3() == 1

        # an I4 must not touch the V1-3 value; the base rule still takes V4
        table["file.info.forms.json"].update(
            {"formver": 4.0, "packet": "I4", "racemena": 1}
        )
        attr = UDSFormA1Attribute(table)
        assert attr._create_naccnihr_v1v3() is None
        assert attr._create_naccnihr() == 7

    def test_create_naccedulvl_v1v3(self, table):
        """V1-3 education is kept for V1-3 rows and never written by an I4."""
        table["file.info.forms.json"].update({"educ": 20})
        assert UDSFormA1Attribute(table)._create_naccedulvl_v1v3() == 6

        table["file.info.forms.json"].update(
            {"formver": 4.0, "packet": "I4", "lvleduc": 3}
        )
        attr = UDSFormA1Attribute(table)
        assert attr._create_naccedulvl_v1v3() is None
        assert attr._create_naccedulvl() == 3

    def test_v1v3_rules_skip_followups(self, table):
        """Only an initial packet establishes the V1-3 value."""
        table["file.info.forms.json"].update({"packet": "F", "race": 1, "educ": 20})
        attr = UDSFormA1Attribute(table)
        assert attr._create_naccnihr_v1v3() is None
        assert attr._create_naccedulvl_v1v3() is None

    def test_v4_unknowns_do_not_override_known_values(self, table):
        """A V4 packet must not replace a known value with an unknown."""
        table["subject.info.derived.cross-sectional"] = {
            "nacclangx": "Tagalog",
            "nacchisp": 0,
            "naccsex": 2,
            "nacclang": 8,
            "naccreas": 1,
        }
        table["file.info.forms.json"].update(
            {
                "formver": 4.0,
                "packet": "I4",
                "predomlanx": None,
                "predomlan": 9,
                "ethispanic": 0,
                "raceunkn": 1,
                "birthsex": None,
            }
        )
        attr = UDSFormA1Attribute(table)
        assert attr._create_nacclangx() == "Tagalog"
        assert attr._create_nacchisp() == 0
        assert attr._create_nacclang() == 8
        assert attr._create_naccreas() == 1
        assert attr._create_naccsex() == 2

    def test_v4_unknowns_still_apply_when_nothing_known(self, table):
        """With no prior value the existing fallbacks are unchanged."""
        table["subject.info.derived.cross-sectional"] = {}
        table["file.info.forms.json"].update(
            {
                "formver": 4.0,
                "packet": "I4",
                "predomlanx": None,
                "predomlan": 9,
                "ethispanic": 0,
                "raceunkn": 1,
            }
        )
        attr = UDSFormA1Attribute(table)
        assert attr._create_nacclangx() == INFORMED_BLANK
        assert attr._create_nacchisp() == 9
        assert attr._create_nacclang() == 9
        assert attr._create_naccreas() == INFORMED_MISSINGNESS

    def test_create_nacchisp(self, table):
        """Tests _create_nacchisp."""
        # v3 and earlier
        table["file.info.forms.json"].update({"hispanic": "0"})
        attr = UDSFormA1Attribute(table)
        assert attr._create_nacchisp() == 0

        # V4 - ethispanic == 1 case
        table["file.info.forms.json"].update({"formver": 4.0, "ethispanic": 1})
        attr = UDSFormA1Attribute(table)
        assert attr._create_nacchisp() == 1

        # V4 - check raceunkn case
        table["file.info.forms.json"].update({"ethispanic": None, "raceunkn": None})
        assert attr._create_nacchisp() == 0

        table["file.info.forms.json"].update({"raceunkn": 1})
        assert attr._create_nacchisp() == 9

    def test_create_naccedulvl(self, table):
        """Tests _create_naccedulvl."""
        # V3 and earlier; need to test educ in several
        # categories
        educ_mappings = {
            1: random.choice(range(0, 12)),
            2: 12,
            3: random.choice(range(13, 16)),
            4: random.choice(range(16, 18)),
            5: random.choice(range(18, 20)),
            6: random.choice(range(20, 37)),
            9: 99,
        }

        attr = UDSFormA1Attribute(table)
        for expected, source in educ_mappings.items():
            table["file.info.forms.json.educ"] = source
            assert attr._create_naccedulvl() == expected

        # assert error thrown when educ value is unrecognized
        with pytest.raises(AttributeDeriverError):
            table["file.info.forms.json.educ"] = 40
            attr._create_naccedulvl()

        # V4, just check lvleduc
        table["file.info.forms.json"].update({"formver": 4.0, "lvleduc": 3})
        attr = UDSFormA1Attribute(table)
        assert attr._create_naccedulvl() == 3


class TestUDSFormA1RawAttribute:
    def test_create_educ(self, table):
        """Tests _create_educ."""
        attr = UDSFormA1RawAttribute(table)
        assert attr._create_educ() == 3

        # none case
        table["file.info.forms.json.educ"] = None
        assert attr._create_educ() is None
