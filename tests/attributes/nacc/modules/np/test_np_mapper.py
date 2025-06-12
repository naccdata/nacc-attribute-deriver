import pytest
from nacc_attribute_deriver.attributes.base.namespace import (
    FormNamespace,
)
from nacc_attribute_deriver.attributes.nacc.modules.np.np_mapper import (
    NPMapper,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
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
                        "visitdate": "2025-01-10",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


@pytest.fixture(scope="function")
def np_mapper() -> NPMapper:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "formver": 1,
                        "module": "NP",
                        "visitdate": "2025-01-10",
                    }
                }
            }
        }
    }

    np = FormNamespace(table=SymbolTable(data), required=frozenset(["formver"]))
    return NPMapper(np)


class TestNPMapper:
    def test_map_gross_null(self, np_mapper):
        assert np_mapper.map_gross(None) is None

    def test_map_sub4_null(self, np_mapper):
        assert np_mapper.map_sub4(None) == 9

    def test_map_vasc_null(self, np_mapper):
        assert np_mapper.map_vasc(None) is None
        assert np_mapper.map_vasc(1) == 1

    def test_map_v9_null(self, np_mapper):
        assert np_mapper.map_v9(None) == 9

    def test_map_sub1_null(self, np_mapper):
        assert np_mapper.map_sub1(None) == 9

    def test_map_lewy_null(self, np_mapper):
        assert np_mapper.map_lewy() == 9

    def test_map_gross(self, np_form_attribute_table, form_prefix):
        mapper = NPMapper(
            FormNamespace(
                table=np_form_attribute_table, required=frozenset(["formver"])
            )
        )
        assert mapper.map_gross(0) == 0
        set_attribute(np_form_attribute_table, form_prefix, "npgross", 9)
        assert mapper.map_gross(0) == 9

    def test_map_sub4(self, np_form_attribute_table):
        mapper = NPMapper(
            FormNamespace(
                table=np_form_attribute_table, required=frozenset(["formver"])
            )
        )
        assert mapper.map_sub4(1) == 3
        assert mapper.map_sub4(5) == 8
        assert mapper.map_sub4(6) == 9

    def test_map_v9(self, np_form_attribute_table):
        mapper = NPMapper(
            FormNamespace(
                table=np_form_attribute_table, required=frozenset(["formver"])
            )
        )
        assert mapper.map_v9(1) == 1
        assert mapper.map_v9(2) == 0
        assert mapper.map_v9(3) == 8
        assert mapper.map_v9(4) == 9

    def test_map_vasc(self, np_form_attribute_table, form_prefix):
        mapper = NPMapper(
            FormNamespace(
                table=np_form_attribute_table, required=frozenset(["formver"])
            )
        )
        assert mapper.map_vasc(0) == 0
        set_attribute(np_form_attribute_table, form_prefix, "npgross", 9)
        assert mapper.map_vasc(0) == 9
        set_attribute(np_form_attribute_table, form_prefix, "npvasc", 3)
        set_attribute(np_form_attribute_table, form_prefix, "npgross", 1)
        assert mapper.map_vasc(0) == 8

    def test_map_sub1(self, np_form_attribute_table):
        mapper = NPMapper(
            FormNamespace(
                table=np_form_attribute_table, required=frozenset(["formver"])
            )
        )
        assert mapper.map_sub1(1) == 0
        assert mapper.map_sub1(5) == 8
        assert mapper.map_sub1(6) == 9

    def test_map_lewy(self, np_form_attribute_table, form_prefix):
        mapper = NPMapper(
            FormNamespace(
                table=np_form_attribute_table, required=frozenset(["formver"])
            )
        )
        assert mapper.map_lewy() == 0

        set_attribute(np_form_attribute_table, form_prefix, "nplewy", 6)
        assert mapper.map_lewy() == 8

    def test_map_v10(self, np_mapper):
        assert np_mapper.map_v10(3, 8) == 3
        assert np_mapper.map_v10(None, 8) == 8
        assert np_mapper.map_v10(None, 3) == 9

    def test_map_comb2(self, np_mapper):
        assert np_mapper.map_comb2(0, 1) == 1
        assert np_mapper.map_comb2(1, 5) == 1
        assert np_mapper.map_comb2(3, 2) == 0
        assert np_mapper.map_comb2(3, 1) == 1
        assert np_mapper.map_comb2(0, 3) == 8
        assert np_mapper.map_comb2(8, 8) == 9

    def test_banked_v9(self, np_form_attribute_table, form_prefix):
        # v1-7 always return None unelss old is specified
        for i in [1, 7]:
            set_attribute(np_form_attribute_table, form_prefix, "formver", i)
            mapper = NPMapper(
                FormNamespace(
                    table=np_form_attribute_table, required=frozenset(["formver"])
                )
            )

            assert mapper.banked_v9(None) is None
            assert mapper.banked_v9(2) == 0
            assert mapper.banked_v9(99) == 9

        # v8/v9
        for i in [8, 9]:
            set_attribute(np_form_attribute_table, form_prefix, "formver", i)
            mapper = NPMapper(
                FormNamespace(
                    table=np_form_attribute_table, required=frozenset(["formver"])
                )
            )

            assert mapper.banked_v9(None) == 9
            assert mapper.banked_v9(1) == 1
            assert mapper.banked_v9(99) == 9

        # v10+ should not call this method - expect error to be raised
        with pytest.raises(AttributeDeriverError):
            for i in [10, 11]:
                set_attribute(np_form_attribute_table, form_prefix, "formver", i)
                mapper = NPMapper(
                    FormNamespace(
                        table=np_form_attribute_table, required=frozenset(["formver"])
                    )
                )
                mapper.banked_v9(None)
