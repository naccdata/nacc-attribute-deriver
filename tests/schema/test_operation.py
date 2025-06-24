"""Tests the operations."""

import pytest
from nacc_attribute_deriver.schema.operation import (
    DateTaggedValue,
    InitialOperation,
    LatestOperation,
    ListOperation,
    MaxOperation,
    MinOperation,
    OperationError,
    OperationRegistry,
    SetOperation,
    SortedListOperation,
    UpdateOperation,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="module")
def date_key() -> str:
    """Generate testing date key."""
    return "test.date"


@pytest.fixture(scope="module")
def location() -> str:
    """Generate testing location key."""
    return "test.location"


@pytest.fixture(scope="function")
def table(location, date_key) -> SymbolTable:
    """Generate dummy table for testing."""
    table = SymbolTable()
    table[date_key] = "2025-01-01"
    table[location] = {"date": "2024-01-01", "value": 10}
    return table


class TestOperation:
    def test_registry(self):
        """Test registry is instantiated correctly."""
        assert (
            len(
                set(OperationRegistry.operations.keys()).difference(
                    {
                        "update",
                        "list",
                        "sortedlist",
                        "set",
                        "initial",
                        "latest",
                        "min",
                        "max",
                    }
                )
            )
            == 0
        )
        assert list(OperationRegistry.operations.values()) == [
            UpdateOperation,
            ListOperation,
            SortedListOperation,
            SetOperation,
            InitialOperation,
            LatestOperation,
            MinOperation,
            MaxOperation,
        ]

    def test_update(self, table, location):
        """Tests the update operation."""
        op = UpdateOperation()
        assert op.LABEL == "update"
        op.evaluate(table=table, value=5, attribute=location)

        assert table.to_dict() == {"test": {"date": "2025-01-01", "location": 5}}

    def test_list(self, table, location):
        op = ListOperation()
        assert op.LABEL == "list"
        table[location] = [1, 2, 3, 4]
        op.evaluate(table=table, value=2, attribute=location)

        assert table.to_dict() == {
            "test": {"date": "2025-01-01", "location": [1, 2, 3, 4, 2]}
        }

    def test_set(self, table, location):
        """Tests the set operation."""
        op = SetOperation()
        assert op.LABEL == "set"
        table[location] = [1, 2, 3, 4]
        op.evaluate(table=table, value=5, attribute=location)

        assert table.to_dict() == {
            "test": {"date": "2025-01-01", "location": [1, 2, 3, 4, 5]}
        }

        # test doing it again will not change since it's a set
        for i in range(1, 6):
            op.evaluate(table=table, value=i, attribute=location)
            assert table.to_dict() == {
                "test": {"date": "2025-01-01", "location": [1, 2, 3, 4, 5]}
            }

        # test adding another list/set
        op.evaluate(table=table, value=[4, 5, 6], attribute=location)
        assert table.to_dict() == {
            "test": {"date": "2025-01-01", "location": [1, 2, 3, 4, 5, 6]}
        }

    def test_sorted_list(self, table, location):
        """Tests the sorted list operation."""
        op = SortedListOperation()
        assert op.LABEL == "sortedlist"
        table[location] = [1, 2, 3, 4]
        op.evaluate(table=table, value=2, attribute=location)

        assert table.to_dict() == {
            "test": {"date": "2025-01-01", "location": [1, 2, 2, 3, 4]}
        }

    def test_initial(self, table, location):
        """Tests the initial operation; will NOT be set since current date >
        destination date."""
        op = InitialOperation()
        assert op.LABEL == "initial"
        op.evaluate(
            table=table,
            value=DateTaggedValue(value=5, date="2025-01-01"),
            attribute=location,
        )

        assert table.to_dict() == {
            "test": {
                "date": "2025-01-01",
                "location": {"date": "2024-01-01", "value": 10},
            }
        }

        with pytest.raises(
            OperationError, match=r"Unable to perform initial operation without date"
        ):
            op.evaluate(table=table, value=5, attribute=location)

    def test_latest(self, table, location):
        """Tests the latest operation; WILL be set since current date >
        destination date."""
        op = LatestOperation()
        assert op.LABEL == "latest"
        op.evaluate(
            table=table,
            value=DateTaggedValue(value=5, date="2025-01-01"),
            attribute=location,
        )

        assert table.to_dict() == {
            "test": {
                "date": "2025-01-01",
                "location": {"date": "2025-01-01", "value": 5},
            }
        }

        with pytest.raises(
            OperationError, match=r"Unable to perform latest operation without date"
        ):
            op.evaluate(table=table, value=5, attribute=location)

    def test_min(self, table, location):
        """Tests the min operation; WILL be set since 5 < 10."""
        op = MinOperation()
        assert op.LABEL == "min"

        table[location] = 10
        op.evaluate(table=table, value=5, attribute=location)

        assert table.to_dict() == {"test": {"date": "2025-01-01", "location": 5}}

    def test_max(self, table, location):
        """Tests the max operation; will NOT be set since 5 < 10."""
        op = MaxOperation()
        assert op.LABEL == "max"

        table[location] = 10
        op.evaluate(table=table, value=5, attribute=location)

        assert table.to_dict() == {"test": {"date": "2025-01-01", "location": 10}}
