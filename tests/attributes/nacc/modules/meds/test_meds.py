"""Tests MEDS form."""

import pytest
from nacc_attribute_deriver.attributes.nacc.modules.meds.form_meds import (
    MEDSFormAttributeCollection,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "frmdatea4g": "2011-08-10",
                        "drugs_list": "d00004,d00170,d00269,d00321,d00732",
                        "module": "MEDS",
                        "formver": 2.0,
                    }
                }
            }
        },
        "subject": {
            "info": {"derived": {"drugs_list": {"2000-01-01": ["d00004", "d00170"]}}}
        },
    }
    return SymbolTable(data)


@pytest.fixture(scope="function")
def v1_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "frmdatea4": "2011-08-10",
                        "module": "MEDS",
                        "formver": 1.0,
                        "pma": "atenoLOL",
                        "pmb": "     ampicillin",
                        "pmf": "PERCOSET 5/325",
                    }
                }
            }
        },
        "subject": {
            "info": {"derived": {"drugs_list": {"2000-01-01": ["d00004", "d00170"]}}}
        },
    }
    return SymbolTable(data)


class TestMEDSForm:
    def test_create_drugs_list(self, table):
        meds = MEDSFormAttributeCollection(table)
        assert meds._create_drugs_list() == {
            "2000-01-01": ["d00004", "d00170"],
            "2011-08-10": ["d00004", "d00170", "d00269", "d00321", "d00732"],
        }

    def test_create_drugs_list_invalid(self, table, form_prefix):
        set_attribute(table, form_prefix, "frmdatea4g", "2000-01-01")
        meds = MEDSFormAttributeCollection(table)

        with pytest.raises(AttributeDeriverError):
            meds._create_drugs_list()

    def test_create_drugs_list_v1(self, v1_table, form_prefix):
        meds = MEDSFormAttributeCollection(v1_table)
        assert meds._create_drugs_list() == {
            "2000-01-01": ["d00004", "d00170"],
            "2011-08-10": ["atenolol", "ampicillin", "percoset 5/325"],
        }
