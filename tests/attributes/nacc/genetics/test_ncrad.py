"""Tests NCRAD genetic attributes."""

import pytest

from nacc_attribute_deriver.attributes.nacc.genetics.ncrad import (
    HistoricalNCRADAttributeCollection,
    NCRADAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {"file": {"info": {"raw": {"a1": "e3", "a2": "e3", "apoe": "1"}}}}

    return SymbolTable(data)


class TestNCRADAttributeCollection:
    def test_create_naccapoe(self, table, raw_prefix):
        """Tests creating NACCAPOE."""
        attr = NCRADAttributeCollection.create(table)
        assert attr._create_ncrad_apoe() == 1  # noqa: SLF001

        for key, value in NCRADAttributeCollection.APOE_ENCODINGS.items():
            set_attribute(table, raw_prefix, "a1", key[0])
            set_attribute(table, raw_prefix, "a2", key[1])
            attr = NCRADAttributeCollection.create(table)

            assert attr._create_ncrad_apoe() == value  # noqa: SLF001

    def test_undefined_pairs(self, table, raw_prefix):
        set_attribute(table, raw_prefix, "a1", "e1")
        set_attribute(table, raw_prefix, "a2", "e7")
        attr = NCRADAttributeCollection.create(table)
        assert attr._create_ncrad_apoe() == 9  # noqa: SLF001

    def test_empty_table(self):
        attr = NCRADAttributeCollection.create(SymbolTable())
        assert attr is None
        # assert attr._create_naccapoe() == 9


class TestHistoricalNCRADAttributeCollection:
    def test_create_historical_apoe(self, table, raw_prefix):
        """Tests creating historical NACCAPOE."""
        attr = HistoricalNCRADAttributeCollection.create(table)
        assert attr._create_historical_apoe() == 1  # noqa: SLF001

        # invalid cases
        for invalid in [0, 7, None, ""]:
            set_attribute(table, raw_prefix, "apoe", invalid)
            attr = HistoricalNCRADAttributeCollection.create(table)
            assert attr._create_historical_apoe() == 9  # noqa: SLF001
