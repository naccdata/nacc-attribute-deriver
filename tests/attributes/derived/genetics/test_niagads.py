"""Tests NIAGADS genetic attributes."""

import pytest
from nacc_attribute_deriver.attributes.derived.genetics.niagads import (
    NIAGADSAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "raw": {
                    "niagads_gwas": "NG00000",
                    "niagads_exomechip": "NG00000, NG00001",
                    "niagads_wgs": "0",
                    "niagads_wes": 0,
                    "adgc_gwas": 1,
                    "adgc_exomechip": 0,
                    "gwas_round": "ADC 0",
                    "exome_round": "Exome1",
                }
            }
        }
    }

    return SymbolTable(data)


class TestNIAGADSAttribute:
    def test_create_niagads(self, table):
        """Tests creating NGDS* variables."""
        attr = NIAGADSAttributeCollection(table)

        assert attr._create_ngdsgwas() == 1
        assert attr._create_ngdsexom() == 1
        assert attr._create_ngdswgs() == 0
        assert attr._create_ngdswes() == 0
        assert attr._create_adgcgwas() == 1
        assert attr._create_adgcexom() == 0
        assert attr._create_adgcrnd() == "ADC 0"
        assert attr._create_adgcexr() == "Exome1"

    def test_create_niagads_missingness(self, table):
        """Tests creating NGDS* variables in the missingness case."""
        table["file.info.raw"].update({"gwas_round": "0", "exome_round": 0})

        attr = NIAGADSAttributeCollection(table)
        assert attr._create_adgcrnd() == "88"
        assert attr._create_adgcexr() == "88"
