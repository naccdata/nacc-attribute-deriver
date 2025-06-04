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
                    }
                }
            }
        }
    }
    return SymbolTable(data)


@pytest.fixture(scope="function")
def np_form_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {"file": {"info": {"forms": {"json": {"formver": 1, "module": "NP"}}}}}

    return SymbolTable(data)


class TestHelpers:
    def test_mapgross_null(self, np_form_table):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._map_gross(None) is None

    def test_mapsub4_null(self, np_form_table):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._map_sub4(None) == 9

    def test_mapvasc_null(self, np_form_table):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._map_vasc(None) is None
        assert np_form_nulls._map_vasc(1) == 1

    def test_mapv9_null(self, np_form_table):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._map_v9(None) == 9

    def test_mapsub1_null(self, np_form_table):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._map_sub1(None) == 9

    def test_maplewy_null(self, np_form_table):
        np_form_nulls = NPFormAttributeCollection.create(np_form_table)
        assert np_form_nulls._map_lewy() is None

    def test_mapgross(self, np_form_attribute_table, form_prefix):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._map_gross(0) == 0
        set_attribute(np_form_attribute_table, form_prefix, "npgross", 9)
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._map_gross(0) == 9

    def test_mapsub4(self, np_form_attribute_table):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._map_sub4(1) == 3
        assert np_form_attribute._map_sub4(5) == 8
        assert np_form_attribute._map_sub4(6) == 9

    def test_mapv9(self, np_form_attribute_table):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._map_v9(1) == 1
        assert np_form_attribute._map_v9(2) == 0
        assert np_form_attribute._map_v9(3) == 8
        assert np_form_attribute._map_v9(4) == 9

    def test_mapvasc(self, np_form_attribute_table, form_prefix):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._map_vasc(0) == 0
        set_attribute(np_form_attribute_table, form_prefix, "npgross", 9)
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._map_vasc(0) == 9
        set_attribute(np_form_attribute_table, form_prefix, "npvasc", 3)
        set_attribute(np_form_attribute_table, form_prefix, "npgross", 1)
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._map_vasc(0) == 8

    def test_mapsub1(self, np_form_attribute_table):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._map_sub1(1) == 0
        assert np_form_attribute._map_sub1(5) == 8
        assert np_form_attribute._map_sub1(6) == 9

    def test_maplewy(self, np_form_attribute_table, form_prefix):
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._map_lewy() == 0

        set_attribute(np_form_attribute_table, form_prefix, "nplewy", 6)
        np_form_attribute = NPFormAttributeCollection.create(np_form_attribute_table)
        assert np_form_attribute._map_lewy() == 8


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
        assert np_form_nulls._create_naccneur() == 9  # WARNING: Different behavior here!
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
