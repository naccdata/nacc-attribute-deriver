"""Tests deriving MQT genetics variables."""

import pytest

from nacc_attribute_deriver.attributes.mqt.genetics import GeneticAttributeCollection
from nacc_attribute_deriver.attributes.nacc.genetics.niagads import (
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
                    "a1": "E4",  # NCRAD data
                    "a2": "E2",
                },
                "derived": {
                    "ngdsexom": 1,  # NIAGADS derived data
                    "ngdsgwas": 1,
                    "ngdswes": 0,
                    "ngdswgs": 0,
                },
            }
        }
    }

    return SymbolTable(data)


@pytest.fixture(scope="function")
def niagads_table() -> SymbolTable:
    table = SymbolTable()
    table["file.info.raw"] = {
        "niagads_gwas": 1,
        "niagads_exomechip": 1,
        "niagads_wgs": 0,
        "niagads_wes": 0,
    }

    return table


class TestGeneticAttributeCollection:
    def test_create_apoe(self, table):
        """Tests creating apoe."""
        attr = GeneticAttributeCollection.create(table)
        assert attr._create_apoe() == "e4,e2"

        # test null case
        table["file.info.raw"].update({"a1": None, "a2": None})
        attr = GeneticAttributeCollection.create(table)
        assert attr._create_apoe() == "Missing/unknown/not assessed"

    def test_create_ngds_vars(self, niagads_table):
        """Tests creating the NIAGADS availability variables."""
        attr = NIAGADSAttributeCollection.create(niagads_table)
        assert attr._create_niagads_gwas()
        assert attr._create_niagads_exome()
        assert not attr._create_niagads_wgs()
        assert not attr._create_niagads_wes()

        # test null case
        niagads_table["file.info.raw"] = {
            "niagads_gwas": None,
            "niagads_exomechip": None,
            "niagads_wgs": None,
            "niagads_wes": None,
        }
        attr = NIAGADSAttributeCollection.create(niagads_table)
        assert not attr._create_niagads_gwas()
        assert not attr._create_niagads_exome()
        assert not attr._create_niagads_wgs()
        assert not attr._create_niagads_wes()
