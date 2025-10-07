"""Tests NCRAD genetic attributes."""

import pytest
from nacc_attribute_deriver.attributes.nacc.genetics.ncrad import (
    HistoricalNCRADAPOEAttributeCollection,
    NCRADAPOEAttributeCollection,
)
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {"info": {"raw": {"a1": "e3", "a2": "e3", "apoe": "1", "apoenp": "1"}}}
    }

    return SymbolTable(data)


class TestNCRADAPOEAttributeCollection:
    def test_create_naccapoe(self, table, raw_prefix):
        """Tests creating NACCAPOE."""
        attr = NCRADAPOEAttributeCollection(table)
        assert attr._create_naccapoe() == 1

        for key, value in NCRADAPOEAttributeCollection.APOE_ENCODINGS.items():
            set_attribute(table, raw_prefix, "a1", key[0])
            set_attribute(table, raw_prefix, "a2", key[1])
            attr = NCRADAPOEAttributeCollection(table)

            assert attr._create_naccapoe() == value

    def test_undefined_pairs(self, table, raw_prefix):
        set_attribute(table, raw_prefix, "a1", "e1")
        set_attribute(table, raw_prefix, "a2", "e7")
        attr = NCRADAPOEAttributeCollection(table)
        assert attr._create_naccapoe() == 9

    def test_empty_table(self):
        with pytest.raises(MissingRequiredError):
            NCRADAPOEAttributeCollection(SymbolTable())

    def test_historical_different(self, table, working_derived_prefix):
        set_attribute(table, working_derived_prefix, "cross-sectional.historic-apoe", 4)
        attr = NCRADAPOEAttributeCollection(table)
        assert attr._create_naccapoe() == 9

    def test_create_naccne4s(self, table, raw_prefix):
        attr = NCRADAPOEAttributeCollection(table)
        assert attr._create_naccne4s() == 0
        set_attribute(table, raw_prefix, "a1", "e4")
        assert attr._create_naccne4s() == 1
        set_attribute(table, raw_prefix, "a2", "e4")
        assert attr._create_naccne4s() == 2

        set_attribute(table, raw_prefix, "a2", "aa")
        set_attribute(table, raw_prefix, "a2", "aa")
        assert attr._create_naccne4s() == 9


class TestHistoricalNCRADAPOEAttributeCollection:
    def test_create_historic_apoe(self, table, raw_prefix):
        """Tests creating historical NACCAPOE."""
        attr = HistoricalNCRADAPOEAttributeCollection(table)
        assert attr._create_historic_apoe() == 1

        # invalid cases
        set_attribute(table, raw_prefix, "apoenp", None)
        for invalid in [0, 7]:
            set_attribute(table, raw_prefix, "apoe", invalid)
            attr = HistoricalNCRADAPOEAttributeCollection(table)
            assert attr._create_historic_apoe() == 9

        for invalid in [None, ""]:
            with pytest.raises(MissingRequiredError):
                set_attribute(table, raw_prefix, "apoe", invalid)
                HistoricalNCRADAPOEAttributeCollection(table)

    def test_create_historic_naccne4s(self, table, raw_prefix):
        attr = HistoricalNCRADAPOEAttributeCollection(table)
        assert attr._create_historic_naccne4s() == 0

        set_attribute(table, raw_prefix, "apoe", 4)
        set_attribute(table, raw_prefix, "apoenp", None)
        assert attr._create_historic_naccne4s() == 2

        for i in [2, 5]:
            set_attribute(table, raw_prefix, "apoe", i)
            assert attr._create_historic_naccne4s() == 1
