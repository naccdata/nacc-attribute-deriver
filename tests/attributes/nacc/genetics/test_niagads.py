"""Tests NIAGADS genetic attributes."""

import pytest
from nacc_attribute_deriver.attributes.nacc.genetics.niagads import (
    NIAGADSAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def attr() -> NIAGADSAttributeCollection:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "raw": {
                    "niagads_gwas": "NG00000",
                    "niagads_exomechip": "NG00000, NG00001",
                    "niagads_wgs": "0",
                    "niagads_wes": None,
                }
            }
        }
    }

    return NIAGADSAttributeCollection(SymbolTable(data))


class TestNIAGADSAttribute:
    def test_create_niagads(self, attr):
        """Tests creating NGDS* variables."""
        assert attr._create_niagads_gwas() == 1
        assert attr._create_niagads_exome() == 1
        assert attr._create_niagads_wgs() == 0
        assert attr._create_niagads_wes() == 0
