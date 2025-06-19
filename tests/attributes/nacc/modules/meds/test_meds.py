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
                        "pmc": "unknown drug",  # unknown
                        "pmf": "PERCOSET 5/325",  # known typo/alternative name
                        "pmt": "PSEUDO TRIPRODINE",  # known typo/alternative name
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

    def test_create_drugs_list_v1(self, v1_table):
        meds = MEDSFormAttributeCollection(v1_table)
        assert meds._create_drugs_list() == {
            "2000-01-01": ["d00004", "d00170"],
            "2011-08-10": ["d00003", "d00004", "d03316", "d03431", "unknown drug"],
        }


class TestPrefixTree:
    """Test the prefix tree can find closest matches."""

    def test_closest_match(self, empty_table, form_prefix):
        meds = MEDSFormAttributeCollection(empty_table)

        # should match flomax, d04121
        set_attribute(empty_table, form_prefix, "pma", "flomax hcl")
        assert meds._create_drugs_list() == {"2011-08-10": ["d04121"]}

        # should match novolinr, d04369
        set_attribute(empty_table, form_prefix, "pma", "novolin")
        assert meds._create_drugs_list() == {"2011-08-10": ["d04369"]}

        # should match lisinopril, d00732
        set_attribute(empty_table, form_prefix, "pma", "lisinopril/hctz")
        assert meds._create_drugs_list() == {"2011-08-10": ["d00732"]}

        # should match tramadol, d03826
        set_attribute(empty_table, form_prefix, "pma", "tramadol hcl")
        assert meds._create_drugs_list() == {"2011-08-10": ["d03826"]}

        # should match coumadin, d00022
        set_attribute(empty_table, form_prefix, "pma", "coumadin 2-3mg")
        assert meds._create_drugs_list() == {"2011-08-10": ["d00022"]}
