"""Tests deriving MQT study parameters variables."""

import pytest
from nacc_attribute_deriver.attributes.mqt.study_parameters import (
    StudyParametersAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table(uds_table) -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    uds_table["file.info.forms.json"].update(
        {
            "formver": "4",
            "packet": "F",
        }
    )
    uds_table.update(
        {
            "subject": {"info": {"study-parameters": {"uds": {"versions": ["UDSv2"]}}}},
        }
    )

    return uds_table


class TestStudyParametersAttributeCollection:
    def test_create_uds_versions_available(self, table):
        """Tests _create_uds_versions_available."""
        attr = StudyParametersAttributeCollection(table)
        assert set(attr._create_uds_versions_available()) == {"UDSv4", "UDSv2"}
