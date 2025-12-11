"""Tests UDS Form A1 attributes."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.uds.form_cx import (
    UDSFormCXAttribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table(uds_table) -> SymbolTable:
    """Create dummy data and return it in a SymbolTable.

    Realistically only one of C2/C2 is filled out, but define both for
    testing
    """
    uds_table["file.info.forms.json"].update(
        {
            "frmdatec1": "2025-01-01",
            "frmdatec2": "2020-12-31",
            "frmdatea1": "2025-02-15",
            "mmse": 95,
            "mocatots": 29,
            "mocbtots": "15",
            "mocacomp": 1,
        }
    )
    uds_table["_prev_record.info.forms.json"].update({"educ": "3"})

    return uds_table


class TestUDSFormCXAttribute:
    def test_create_nacc1(self, table):
        """Tests creating NACCC1, < 90 days."""
        attr = UDSFormCXAttribute(table)
        assert attr._create_naccc1() == 0

    def test_create_nacc2(self, table):
        """Tests creating NACCC2, > 90 days."""
        attr = UDSFormCXAttribute(table)
        assert attr._create_naccc2() == 1

    def test_create_naccmmse(self, table, form_prefix):
        """Tests creating NACCMMSE."""
        attr = UDSFormCXAttribute(table)
        assert attr._create_naccmmse() == 95

        # should still return mmse value
        set_attribute(table, form_prefix, "mmsereas", 98)
        assert attr._create_naccmmse() == 95

        set_attribute(table, form_prefix, "mmse", None)
        assert attr._create_naccmmse() == 98

    def test_create_naccmoca(self, table, form_prefix):
        """Tests creating NACCMOCA."""
        set_attribute(table, form_prefix, "educ", "3")
        attr = UDSFormCXAttribute(table)
        assert attr._create_naccmoca() == 30

        # educ < 12 and mocatots > 30
        set_attribute(table, form_prefix, "mocatots", 34)
        assert attr._create_naccmoca() == 34

        # educ > 12 and mocatots < 30, should not + 1
        set_attribute(table, form_prefix, "educ", 20)
        set_attribute(table, form_prefix, "mocatots", 25)
        assert attr._create_naccmoca() == 25

        # educ is 99 or None
        set_attribute(table, form_prefix, "educ", 99)
        assert attr._create_naccmoca() == 99
        set_attribute(table, form_prefix, "educ", None)
        assert attr._create_naccmoca() == 99

        # mocatots is 88 or None
        set_attribute(table, form_prefix, "mocatots", 88)
        assert attr._create_naccmoca() == 88
        set_attribute(table, form_prefix, "mocatots", None)
        assert attr._create_naccmoca() == 88

        # if packet IT, ignore
        set_attribute(table, form_prefix, "packet", "IT")
        assert attr._create_naccmoca() == -4

    def test_create_naccmocb(self, table, form_prefix):
        """Tests creating NACCMOCB.

        Test the packets here as well.
        """
        set_attribute(table, form_prefix, "educ", "3")
        attr = UDSFormCXAttribute(table)

        # default does not fulfill packet conditions, should return None
        assert attr._create_naccmocb() == -4

        # set packet to IT, should run now
        set_attribute(table, form_prefix, "packet", "IT")
        attr = UDSFormCXAttribute(table)
        assert attr._create_naccmocb() == 16

        # also works if formver is 3.2
        set_attribute(table, form_prefix, "packet", "I")
        set_attribute(table, form_prefix, "formver", 3.2)
        attr = UDSFormCXAttribute(table)
        assert attr._create_naccmocb() == 16

        # educ > 12, mocbtots < 22, should not add 1
        set_attribute(table, form_prefix, "packet", "F")
        set_attribute(table, form_prefix, "educ", None)
        attr = UDSFormCXAttribute(table)
        table["_prev_record.info.forms.json.educ"] = 15
        assert attr._create_naccmocb() == 15

        # educ is 99 or None
        table["_prev_record.info.forms.json.educ"] = 99
        assert attr._create_naccmocb() == 99
        table["_prev_record.info.forms.json.educ"] = None
        assert attr._create_naccmocb() == 99

        # mocacomp == 0
        set_attribute(table, form_prefix, "mocacomp", 0)
        assert attr._create_naccmocb() == 88

    def test_create_naccmocb_case1(self, table):
        """Case from regression tests."""
        table["file.info.forms.json"].update(
            {
                "mocbtots": 21,
                "mocacomp": 1,
                "formver": 3.2,
                "frmdatec1": None,
                "frmdatec2": "2020-07-15",
                "packet": "F",
            }
        )
        table["_prev_record.info.forms.json"].update({"educ": 18})
        attr = UDSFormCXAttribute(table)
        assert attr._create_naccmocb() == 21
