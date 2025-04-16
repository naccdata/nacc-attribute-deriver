"""Tests NCRAD genetic attributes."""

import pytest

from nacc_attribute_deriver.attributes.nacc.genetics.ncrad import (
    NCRADAPOEAttributeCollection,
    NCRADBioSamplesAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def apoe_table() -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    data = {"file": {"info": {"raw": {"a1": "e3", "a2": "e3"}}}}

    return SymbolTable(data)


class TestNCRADAPOEAttributeCollection:
    def test_create_naccapoe(self, apoe_table, raw_prefix):
        """Tests creating NACCAPOE."""
        attr = NCRADAPOEAttributeCollection.create(apoe_table)
        assert attr._create_ncrad_apoe() == 1  # noqa: SLF001

        for key, value in NCRADAPOEAttributeCollection.APOE_ENCODINGS.items():
            set_attribute(apoe_table, raw_prefix, "a1", key[0])
            set_attribute(apoe_table, raw_prefix, "a2", key[1])
            attr = NCRADAPOEAttributeCollection.create(apoe_table)

            assert attr._create_ncrad_apoe() == value  # noqa: SLF001

    def test_undefined_pairs(self, apoe_table, raw_prefix):
        set_attribute(apoe_table, raw_prefix, "a1", "e1")
        set_attribute(apoe_table, raw_prefix, "a2", "e7")
        attr = NCRADAPOEAttributeCollection.create(apoe_table)
        assert attr._create_ncrad_apoe() == 9  # noqa: SLF001

    def test_empty_table(self):
        attr = NCRADAPOEAttributeCollection.create(SymbolTable())
        assert attr is None


@pytest.fixture(scope="function")
def biosample_table() -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    data = {
        "file": {
            "info": {
                "raw": {
                    "date_sample_received": "2025-11-05",
                    "sample_received": "Blood",
                }
            }
        }
    }

    return SymbolTable(data)


class TestNCRADBioSamplesAttributeCollection:
    def test_create_naccncrd(self, biosample_table, raw_prefix):
        """Tests creating NACCNCRD."""
        attr = NCRADBioSamplesAttributeCollection.create(biosample_table)
        assert attr._create_naccncrd() == 1  # noqa: SLF001

    def test_empty_table(self):
        attr = NCRADBioSamplesAttributeCollection.create(SymbolTable())
        assert attr is None
