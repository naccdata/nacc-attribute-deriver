"""Tests deriving MQT study parameters variables."""

import pytest

from nacc_attribute_deriver.attributes.mqt.study_parameters import (
    StudyParametersAttribute,  # type: ignore
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def attr() -> StudyParametersAttribute:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {"info": {"forms": {"json": {"formver": "4"}}}},
        "subject": {"info": {"study-parameters": {"uds": {"versions": [2]}}}},
    }

    return StudyParametersAttribute(SymbolTable(data))


class TestStudyParametersAttribute:
    def test_create_uds_versions_available(self, attr):
        """Tests _create_uds_versions_available."""
        assert attr._create_uds_versions_available() == [2, 4]
