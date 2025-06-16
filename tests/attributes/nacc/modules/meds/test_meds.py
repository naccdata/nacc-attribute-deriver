"""Tests MEDS form."""

import pytest
from nacc_attribute_deriver.attributes.nacc.modules.meds.form_meds import (
    MEDSFormAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


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
