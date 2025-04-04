"""Tests deriving MQT neuropathology variables."""

import pytest

from nacc_attribute_deriver.attributes.mqt.neuropathology import (
    NeuropathologyAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "derived": {
                    "naccint": 75,
                    "naccbraa": 3,
                    "naccneur": 4,
                    "naccmicr": 1,
                    "nacchem": 1,
                    "naccarte": 2,
                    "nacclewy": 8,
                }
            }
        }
    }

    return SymbolTable(data)


class TestNeuropathologyAttributeCollection:
    """These all just copy from the derived NACC variable."""

    def test_create_np_visit_to_death_interval(self, table):
        """Tests _create_np_visit_to_death_interval."""
        attr = NeuropathologyAttributeCollection.create(table)
        assert attr._create_np_visit_to_death_interval() == 75  # noqa: SLF001

    def test_create_np_b_score(self, table):
        """Tests _create_np_b_score."""
        attr = NeuropathologyAttributeCollection.create(table)
        assert attr._create_np_b_score() == 3  # noqa: SLF001

    def test_create_np_c_score(self, table):
        """Tests _create_np_c_score."""
        attr = NeuropathologyAttributeCollection.create(table)
        assert attr._create_np_c_score() == 4  # noqa: SLF001

    def test_create_np_microinfarcts(self, table):
        """Tests _create_np_microinfarcts."""
        attr = NeuropathologyAttributeCollection.create(table)
        assert attr._create_np_microinfarcts() == 1  # noqa: SLF001

    def test_create_np_hemorrhages_and_microbleeds(self, table):
        """Tests _create_np_hemorrhages_and_microbleeds."""
        attr = NeuropathologyAttributeCollection.create(table)
        assert attr._create_np_hemorrhages_and_microbleeds() == 1  # noqa: SLF001

    def test_create_np_arteriolosclerosis(self, table):
        """Tests _create_np_arteriolosclerosis."""
        attr = NeuropathologyAttributeCollection.create(table)
        assert attr._create_np_arteriolosclerosis() == 2  # noqa: SLF001

    def test_create_np_lewy_pathology(self, table):
        """Tests _create_np_lewy_pathology."""
        attr = NeuropathologyAttributeCollection.create(table)
        assert attr._create_np_lewy_pathology() == 8  # noqa: SLF001
