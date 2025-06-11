import pytest
from nacc_attribute_deriver.attributes.nacc.modules.np.form_np import (
    NPFormAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def np_form_attribute_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "npgross": 2,
                        "npvasc": 3,
                        "npneur": 1,
                        "npold": 1,
                        "npmicro": 1,
                        "nphem": 1,
                        "nparter": 1,
                        "nplewy": 5,
                        "npbraak": 7,
                        "nphemo": 1,
                        "npoldd": 1,
                        "nplbod": 4,
                        "formver": 1,
                        "module": "NP",
                        "visitdate": "2025-01-10",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


@pytest.fixture(scope="function")
def np_form_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {"formver": 1, "module": "NP", "visitdate": "2025-01-10"}
                }
            }
        }
    }

    return SymbolTable(data)


class TestCreateNACCBRAA:
    def test_create_naccbraa_null(self, np_form_table, form_prefix):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccbraa() == 9
        set_attribute(np_form_table, form_prefix, "formver", 8)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccbraa() == 9
        set_attribute(np_form_table, form_prefix, "formver", 10)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccbraa() == 9

    def test_create_naccbraa(self, np_form_attribute_table, form_prefix):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_naccbraa() == 0
        set_attribute(np_form_attribute_table, form_prefix, "formver", 10)
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_naccbraa() == 7


class TestCreateNACCNEUR:
    def test_create_naccneur_null(self, np_form_table, form_prefix):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccneur() == 9
        set_attribute(np_form_table, form_prefix, "formver", 8)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert (
            np_form_nulls._create_naccneur() == 9
        )  # WARNING: Different behavior here!
        set_attribute(np_form_table, form_prefix, "formver", 10)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccneur() == 9

    def test_create_naccneur(self, np_form_attribute_table, form_prefix):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_naccneur() == 3
        set_attribute(np_form_attribute_table, form_prefix, "formver", 10)
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_naccneur() == 1


class TestCreateNACCMICR:
    def test_create_naccmicr_null(self, np_form_table, form_prefix):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccmicr() == 9
        set_attribute(np_form_table, form_prefix, "formver", 8)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccmicr() == 9  # WARNING: Different behavior here
        set_attribute(np_form_table, form_prefix, "formver", 10)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccmicr() == 9

    def test_create_naccmicr(self, np_form_attribute_table, form_prefix):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_naccmicr() == 1
        set_attribute(np_form_attribute_table, form_prefix, "formver", 10)
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_naccmicr() == 1

    def test_create_naccmicr_v9(self, np_form_table, form_prefix):
        """Test V9 NACCMICR."""
        set_attribute(np_form_table, form_prefix, "formver", 9)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccmicr() == 9
        set_attribute(np_form_table, form_prefix, "npmicro", 1)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccmicr() == 1
        set_attribute(np_form_table, form_prefix, "npmicro", 2)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccmicr() == 0
        set_attribute(np_form_table, form_prefix, "npmicro", 3)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccmicr() == 8


class TestCreateNACCHEM:
    def test_create_nacchem_null(self, np_form_table, form_prefix):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_nacchem() == 9
        set_attribute(np_form_table, form_prefix, "formver", 8)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_nacchem() == 9  # WARNING: Different behavior here
        set_attribute(np_form_table, form_prefix, "formver", 10)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_nacchem() == 9  # WARNING: Different behavior here

    def test_create_nacchem(self, np_form_attribute_table, form_prefix):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_nacchem() == 1
        set_attribute(np_form_attribute_table, form_prefix, "formver", 10)
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_nacchem() == 1


class TestCreateNACCARTE:
    def test_create_naccarte_null(self, np_form_table, form_prefix):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccarte() == 9
        set_attribute(np_form_table, form_prefix, "formver", 8)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccarte() == 9  # WARNING: Different behavior here
        set_attribute(np_form_table, form_prefix, "formver", 10)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_naccarte() == 9

    def test_create_naccarte(self, np_form_attribute_table, form_prefix):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_naccarte() == 0
        set_attribute(np_form_attribute_table, form_prefix, "formver", 10)
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_naccarte() == 1


class TestCreateNACCLEWY:
    def test_create_nacclewy_null(self, np_form_table, form_prefix):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_nacclewy() == 9
        set_attribute(np_form_table, form_prefix, "formver", 8)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_nacclewy() == 9
        set_attribute(np_form_table, form_prefix, "formver", 10)
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._create_nacclewy() == 9

    def test_create_nacclewy(self, np_form_attribute_table, form_prefix):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_nacclewy() == 0
        set_attribute(np_form_attribute_table, form_prefix, "formver", 10)
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._create_nacclewy() == 2
