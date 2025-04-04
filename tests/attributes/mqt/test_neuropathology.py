"""Tests deriving MQT neuropathology variables."""

import pytest

from nacc_attribute_deriver.attributes.mqt.neuropathology import (
    NeuropathologyAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {"file": {"info": {"derived": {"naccint": 75}}}}

    return SymbolTable(data)


class TestNeuropathologyAttributeCollection:
    def test_create_visit_to_death_interval(self, table):
        """Tests _create_visit_to_death_interval."""
        attr = NeuropathologyAttributeCollection.create(table)
        assert attr._create_visit_to_death_interval() == 75  # noqa: SLF001
