"""Tests UDS Form A1 attributes."""

import random
import pytest
from nacc_attribute_deriver.attributes.derived.modules.uds.form_a1 import (
    UDSFormA1Attribute,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
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
        assert attr._create_affiliate()

        # sourcenw case
        set_attribute(table, form_prefix, "source", 1)
        set_attribute(table, form_prefix, "sourcenw", 2)
        assert attr._create_affiliate()

        # set but something else case
        set_attribute(table, form_prefix, "sourcenw", 1)
        assert not attr._create_affiliate()

    def test_create_educ(self, table):
        """Tests _create_educ."""
        attr = UDSFormA1Attribute(table)
        assert attr._create_educ() == 3

        # none case
        table["file.info.forms.json.educ"] = None
        assert attr._create_educ() is None

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
