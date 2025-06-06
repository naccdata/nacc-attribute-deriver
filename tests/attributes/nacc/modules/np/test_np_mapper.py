import pytest
from nacc_attribute_deriver.attributes.base.namespace import (
    FormNamespace,
)
from nacc_attribute_deriver.attributes.nacc.modules.np.form_np import (
    NPFormAttributeCollection,
)
from nacc_attribute_deriver.attributes.nacc.modules.np.np_mapper import (
    NPMapper,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def np_form_attribute_table() -> SymbolTable:
    """Create dummy NP data."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "npgross": 2,
                        "npvasc": 3,
                        "nplewy": 5,
                        "formver": 1,
                        "module": "NP",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


@pytest.fixture(scope="function")
def np_mapper() -> NPMapper:
    """Create dummy data and return it in an attribute object."""
    data = {"file": {"info": {"forms": {"json": {"formver": 1, "module": "NP"}}}}}

    np = FormNamespace(SymbolTable(data))
    return NPMapper(np)


class TestNPMapper:
    def test_mapgross_null(self, np_mapper):
        assert np_mapper.map_gross(None) is None

    def test_mapsub4_null(self, np_mapper):
        assert np_mapper.map_sub4(None) == 9

    def test_mapvasc_null(self, np_mapper):
        assert np_mapper.map_vasc(None) is None
        assert np_mapper.map_vasc(1) == 1

    def test_mapv9_null(self, np_mapper):
        assert np_mapper.map_v9(None) == 9

    def test_mapsub1_null(self, np_mapper):
        assert np_mapper.map_sub1(None) == 9

    def test_maplewy_null(self, np_mapper):
        assert np_mapper.map_lewy() is None

    def test_mapgross(self, np_form_attribute_table, form_prefix):
        mapper = NPMapper(FormNamespace(np_form_attribute_table))
        assert mapper.map_gross(0) == 0
        set_attribute(np_form_attribute_table, form_prefix, "npgross", 9)
        assert mapper.map_gross(0) == 9

    def test_mapsub4(self, np_form_attribute_table):
        mapper = NPMapper(FormNamespace(np_form_attribute_table))
        assert mapper.map_sub4(1) == 3
        assert mapper.map_sub4(5) == 8
        assert mapper.map_sub4(6) == 9

    def test_mapv9(self, np_form_attribute_table):
        mapper = NPMapper(FormNamespace(np_form_attribute_table))
        assert mapper.map_v9(1) == 1
        assert mapper.map_v9(2) == 0
        assert mapper.map_v9(3) == 8
        assert mapper.map_v9(4) == 9

    def test_mapvasc(self, np_form_attribute_table, form_prefix):
        mapper = NPMapper(FormNamespace(np_form_attribute_table))
        assert mapper.map_vasc(0) == 0
        set_attribute(np_form_attribute_table, form_prefix, "npgross", 9)
        assert mapper.map_vasc(0) == 9
        set_attribute(np_form_attribute_table, form_prefix, "npvasc", 3)
        set_attribute(np_form_attribute_table, form_prefix, "npgross", 1)
        assert mapper.map_vasc(0) == 8

    def test_mapsub1(self, np_form_attribute_table):
        mapper = NPMapper(FormNamespace(np_form_attribute_table))
        assert mapper.map_sub1(1) == 0
        assert mapper.map_sub1(5) == 8
        assert mapper.map_sub1(6) == 9

    def test_maplewy(self, np_form_attribute_table, form_prefix):
        mapper = NPMapper(FormNamespace(np_form_attribute_table))
        assert mapper.map_lewy() == 0

        set_attribute(np_form_attribute_table, form_prefix, "nplewy", 6)
        assert mapper.map_lewy() == 8
