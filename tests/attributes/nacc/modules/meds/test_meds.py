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
        }
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
                        "pmc": "unknown drug",  # unknown
                        "pmf": "hctz",  # abbreviation
                        "pmt": "hydrochlorathiazide",  # misspelled
                    }
                }
            }
        }
    }
    return SymbolTable(data)


@pytest.fixture(scope="function")
def empty_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "frmdatea4": "2011-08-10",
                        "module": "MEDS",
                        "formver": 1.0,
                    }
                }
            }
        }
    }
    return SymbolTable(data)


class TestMEDSFormAttributeCollection:
    def test_create_drugs_list(self, table):
        meds = MEDSFormAttributeCollection(table)
        assert meds._create_drugs_list() == ["d00004", "d00170", "d00269", "d00321", "d00732"]

    def test_create_drugs_list_v1(self, v1_table):
        meds = MEDSFormAttributeCollection(v1_table)
        assert meds._create_drugs_list() == ["d00003", "d00004", "d00253", "d00253", "unknown drug"]
