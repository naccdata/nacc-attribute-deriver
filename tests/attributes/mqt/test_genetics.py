"""Tests deriving MQT genetics variables."""

import pytest

from nacc_attribute_deriver.attributes.mqt.genetics import GeneticAttributeCollection
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


class TestGeneticAttributeCollection:
    def test_create_apoe(self, table):
        """Tests creating apoe."""
        attr = GeneticAttributeCollection.create(table)
        assert attr._create_apoe() == "e4,e2"

        # test null case
        table["file.info.raw"].update({"a1": None, "a2": None})
        attr = GeneticAttributeCollection.create(table)
        assert attr._create_apoe() == "Missing/unknown/not assessed"

    def test_create_ngds_vars(self, table):
        """Tests creating the NIAGADS availability variables."""
        attr = GeneticAttributeCollection.create(table)
        assert attr._create_ngdsgwas_mqt()
        assert attr._create_ngdsexom_mqt()
        assert not attr._create_ngdswgs_mqt()
        assert not attr._create_ngdswes_mqt()

        # test null case
        table["file.info.derived"] = {
            "ngdsexom": None,
            "ngdsgwas": None,
            "ngdswes": None,
            "ngdswgs": None,
        }
        attr = GeneticAttributeCollection.create(table)
        assert not attr._create_ngdsgwas_mqt()
        assert not attr._create_ngdsexom_mqt()
        assert not attr._create_ngdswgs_mqt()
        assert not attr._create_ngdswes_mqt()
