"""Tests deriving MQT study parameters variables."""

import pytest
from nacc_attribute_deriver.attributes.mqt.study_parameters import (
    StudyParametersAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "formver": "4",
                        "module": "UDS",
                        "packet": "F",
                        "birthmo": 1,
                        "birthyr": 1950,
                        "visitdate": "2025-01-10",
                        "naccid": "NACC123456",
                        "adcid": 0,
                    }
                }
            }
        },
        "subject": {"info": {"study-parameters": {"uds": {"versions": ["UDSv2"]}}}},
    }

    return SymbolTable(data)


class TestStudyParametersAttributeCollection:
    def test_create_uds_versions_available(self, table):
        """Tests _create_uds_versions_available."""
        attr = StudyParametersAttributeCollection(table)
        assert set(attr._create_uds_versions_available()) == {"UDSv4", "UDSv2"}
