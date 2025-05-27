"""Tests NCRAD genetic attributes."""

import pytest
from nacc_attribute_deriver.attributes.nacc.genetics.ncrad import (
    HistoricalNCRADAttributeCollection,
    NCRADAttributeCollection,
)
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def apoe_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {"info": {"raw": {"a1": "e3", "a2": "e3", "apoe": "1", "apoenp": "1"}}}
    }

    return SymbolTable(data)


class TestNCRADAttributeCollection:
    def test_create_naccapoe(self, apoe_table: SymbolTable, raw_prefix: str):
        """Tests creating NACCAPOE."""
        attr = NCRADAttributeCollection.create(apoe_table)
        assert attr._create_ncrad_apoe() == 1  # type: ignore

        for key, value in NCRADAttributeCollection.APOE_ENCODINGS.items():
            set_attribute(apoe_table, raw_prefix, "a1", key[0])
            set_attribute(apoe_table, raw_prefix, "a2", key[1])
            attr = NCRADAttributeCollection.create(apoe_table)

            assert attr._create_ncrad_apoe() == value  # type: ignore

    def test_undefined_pairs(self, apoe_table: SymbolTable, raw_prefix: str):
        set_attribute(apoe_table, raw_prefix, "a1", "e1")
        set_attribute(apoe_table, raw_prefix, "a2", "e7")
        attr = NCRADAttributeCollection.create(apoe_table)
        assert attr._create_ncrad_apoe() == 9  # type: ignore

    def test_empty_table(self):
        attr = NCRADAttributeCollection.create(SymbolTable())
        # assert attr is None
        assert attr._create_ncrad_apoe() == 9  # type: ignore


class TestHistoricalNCRADAttributeCollection:
    def test_create_historic_apoe(self, apoe_table: SymbolTable, raw_prefix: str):
        """Tests creating historical NACCAPOE."""
        attr = HistoricalNCRADAttributeCollection.create(apoe_table)
        assert attr._create_historic_apoe() == 1  # type: ignore

        # invalid cases
        set_attribute(apoe_table, raw_prefix, "apoenp", None)
        for invalid in [0, 7, None]:  # type: ignore
            set_attribute(apoe_table, raw_prefix, "apoe", invalid)
            attr = HistoricalNCRADAttributeCollection.create(apoe_table)
            assert attr._create_historic_apoe() == 9  # type: ignore

        set_attribute(apoe_table, raw_prefix, "apoe", "invalid")
        attr = HistoricalNCRADAttributeCollection.create(apoe_table)
        with pytest.raises(InvalidFieldError):
            attr._create_historic_apoe()  # type: ignore
