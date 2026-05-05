"""Tests B1a form."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.b1a.form_b1a import (
    B1aFormAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import MissingRequiredError


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "module": "b1a",
                        "bpsysl": 123,
                        "bpsysr": "234",
                        "bpdiasl": None,
                        "bpdiasr": 888,
                        "bpdevice": "9",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


class TestB1aFormAttributeCollection:
    def test_create_blood_addendum(self, table):
        """Tests _create_blood_addendum."""
        attr = B1aFormAttributeCollection(table)
        assert attr._create_bpsysl() == 123
        assert attr._create_bpsysr() == 234
        assert attr._create_bpdiasl() == 888  # default set
        assert attr._create_bpdiasr() == 888
        assert attr._create_bpdevice() == 9

    def test_b1a_date(self, table):
        """Test date comes from _uds_visitdate."""
        table["_uds_visitdate"] = "2020-01-01"
        attr = B1aFormAttributeCollection(table)
        assert str(attr.get_date()) == "2020-01-01"

        # assert error raised if no date found
        table["_uds_visitdate"] = None
        table["file.info.forms.json.visitdate"] = None
        table["file.info.forms.json.frmdateb1a"] = None

        with pytest.raises(MissingRequiredError) as e:
            B1aFormAttributeCollection(table)

        table["_uds_visitdate"] = None
        table["file.info.forms.json.visitdate"] = '01/05/2019'
        table["file.info.forms.json.frmdateb1a"] = None
        attr = B1aFormAttributeCollection(table)
        assert str(attr.get_date()) == "2019-01-05"