"""Tests deriving MQT genetics variables."""

import pytest

from nacc_attribute_deriver.attributes.mqt.genetics import GeneticAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def attr() -> GeneticAttribute:
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

    return GeneticAttribute(SymbolTable(data))


class TestGeneticAttribute:
    def test_create_apoe(self, attr):
        """Tests creating apoe."""
        assert attr._create_apoe() == "e4,e2"

        # test null case
        attr.table["file.info.raw"].update({"a1": None, "a2": None})
        assert attr._create_apoe() == "Missing/unknown/not assessed"

    def test_create_ngds_vars(self, attr):
        """Tests creating the NIAGADS availability variables."""
        assert attr._create_ngdsgwas_mqt()
        assert attr._create_ngdsexom_mqt()
        assert not attr._create_ngdswgs_mqt()
        assert not attr._create_ngdswes_mqt()

        # test null case
        attr.table["file.info.derived"] = {
            "ngdsexom": None,
            "ngdsgwas": None,
            "ngdswes": None,
            "ngdswgs": None,
        }
        assert not attr._create_ngdsgwas_mqt()
        assert not attr._create_ngdsexom_mqt()
        assert not attr._create_ngdswgs_mqt()
        assert not attr._create_ngdswes_mqt()
