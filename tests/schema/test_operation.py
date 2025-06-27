"""Tests the operations."""

import pytest
from datetime import date

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
def table(location) -> SymbolTable:
    """Generate dummy table for testing."""
    return SymbolTable()


@pytest.fixture(scope="function")
def dated_table(location, date_key) -> SymbolTable:
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

    def test_update(self, dated_table, location):
        """Tests the update operation."""
        op = UpdateOperation()
        assert op.LABEL == "update"
        op.evaluate(table=dated_table, value=5, attribute=location)

        assert dated_table.to_dict() == {"test": {"date": "2025-01-01", "location": 5}}

        # test on dated value - should override previous location
        value = DateTaggedValue(date=date(2025, 12, 31), value=10)
        op.evaluate(table=dated_table, value=value, attribute=location)
        assert dated_table.to_dict() == {
            "test": {
                "date": "2025-01-01",
                "location": {"date": "2025-12-31", "value": 10},
            }
        }

    def test_list(self, table, location):
        op = ListOperation()
        assert op.LABEL == "list"
        table[location] = [1, 2, 3, 4]
        op.evaluate(table=table, value=2, attribute=location)

        assert table.to_dict() == {"test": {"location": [1, 2, 3, 4, 2]}}

    def test_list_dated(self, table, location):
        # test adding dated value
        op = ListOperation()
        assert op.LABEL == "list"

        value = DateTaggedValue(date=date(2025, 12, 31), value=10)
        op.evaluate(table=table, value=value, attribute=location)
        assert table.to_dict() == {
            "test": {
                "location": [{"date": "2025-12-31", "value": 10}],
            }
        }

        # different date, same value
        value = DateTaggedValue(date=date(2025, 6, 1), value=10)
        op.evaluate(table=table, value=value, attribute=location)
        assert table.to_dict() == {
            "test": {
                "location": [
                    {"date": "2025-12-31", "value": 10},
                    {"date": "2025-06-01", "value": 10},
                ],
            }
        }

        # same date/value as first one
        value = DateTaggedValue(date=date(2025, 12, 31), value=10)
        op.evaluate(table=table, value=value, attribute=location)
        assert table.to_dict() == {
            "test": {
                "location": [
                    {"date": "2025-12-31", "value": 10},
                    {"date": "2025-06-01", "value": 10},
                    {"date": "2025-12-31", "value": 10},
                ],
            }
        }

    def test_set(self, dated_table, location):
        """Tests the set operation."""
        op = SetOperation()
        assert op.LABEL == "set"
        dated_table[location] = [1, 2, 3, 4]
        op.evaluate(table=dated_table, value=5, attribute=location)

        assert dated_table.to_dict() == {
            "test": {"date": "2025-01-01", "location": [1, 2, 3, 4, 5]}
        }

        # test doing it again will not change since it's a set
        for i in range(1, 6):
            op.evaluate(table=dated_table, value=i, attribute=location)
            assert dated_table.to_dict() == {
                "test": {"date": "2025-01-01", "location": [1, 2, 3, 4, 5]}
            }

        # test adding another list/set
        op.evaluate(table=dated_table, value=[4, 5, 6], attribute=location)
        assert dated_table.to_dict() == {
            "test": {"date": "2025-01-01", "location": [1, 2, 3, 4, 5, 6]}
        }

    def test_set_dated(self, table, location):
        """Test adding dates to a set."""
        op = SetOperation()

        for _ in range(3):
            value = DateTaggedValue(date=date(2025, 12, 31), value=10)
            op.evaluate(table=table, value=value, attribute=location)
            assert table.to_dict() == {
                "test": {
                    "location": [{"date": "2025-12-31", "value": 10}],
                }
            }

        # different date
        value = DateTaggedValue(date=date(2025, 6, 1), value=10)
        op.evaluate(table=table, value=value, attribute=location)
        assert table.to_dict() == {
            "test": {
                "location": [
                    {"date": "2025-06-01", "value": 10},
                    {"date": "2025-12-31", "value": 10},
                ],
            }
        }

    def test_sorted_list(self, table, location):
        """Tests the sorted list operation."""
        op = SortedListOperation()
        assert op.LABEL == "sortedlist"
        table[location] = [1, 2, 3, 4]
        op.evaluate(table=table, value=2, attribute=location)

        assert table.to_dict() == {"test": {"location": [1, 2, 2, 3, 4]}}

    def test_sorted_list_dated(self, table, location):
        op = SortedListOperation()

        value = DateTaggedValue(date=date(2025, 12, 31), value=10)
        op.evaluate(table=table, value=value, attribute=location)
        assert table.to_dict() == {
            "test": {
                "location": [{"date": "2025-12-31", "value": 10}],
            }
        }

        value = DateTaggedValue(date=date(2020, 6, 1), value=10)
        op.evaluate(table=table, value=value, attribute=location)
        assert table.to_dict() == {
            "test": {
                "location": [
                    {"date": "2020-06-01", "value": 10},
                    {"date": "2025-12-31", "value": 10},
                ],
            }
        }

        value = DateTaggedValue(date=date(2022, 8, 14), value=10)
        op.evaluate(table=table, value=value, attribute=location)
        assert table.to_dict() == {
            "test": {
                "location": [
                    {"date": "2020-06-01", "value": 10},
                    {"date": "2022-08-14", "value": 10},
                    {"date": "2025-12-31", "value": 10},
                ],
            }
        }

        value = DateTaggedValue(date=date(2022, 8, 14), value=10)
        op.evaluate(table=table, value=value, attribute=location)
        assert table.to_dict() == {
            "test": {
                "location": [
                    {"date": "2020-06-01", "value": 10},
                    {"date": "2022-08-14", "value": 10},
                    {"date": "2022-08-14", "value": 10},
                    {"date": "2025-12-31", "value": 10},
                ],
            }
        }

    def test_initial(self, dated_table, location):
        """Tests the initial operation; will NOT be set since current date >
        destination date."""
        op = InitialOperation()
        assert op.LABEL == "initial"
        op.evaluate(
            table=dated_table,
            value=DateTaggedValue(value=5, date="2025-01-01"),
            attribute=location,
        )

        assert dated_table.to_dict() == {
            "test": {
                "date": "2025-01-01",
                "location": {"date": "2024-01-01", "value": 10},
            }
        }

        with pytest.raises(
            OperationError,
            match=r"Unable to perform initial operation on attribute "
            + r"test.location without date",
        ):
            op.evaluate(table=dated_table, value=5, attribute=location)

    def test_latest(self, dated_table, location):
        """Tests the latest operation; WILL be set since current date >
        destination date."""
        op = LatestOperation()
        assert op.LABEL == "latest"
        op.evaluate(
            table=dated_table,
            value=DateTaggedValue(value=5, date="2025-01-01"),
            attribute=location,
        )

        assert dated_table.to_dict() == {
            "test": {
                "date": "2025-01-01",
                "location": {"date": "2025-01-01", "value": 5},
            }
        }

        with pytest.raises(
            OperationError,
            match=r"Unable to perform latest operation on attribute "
            + r"test.location without date",
        ):
            op.evaluate(table=dated_table, value=5, attribute=location)

    def test_min(self, table, location):
        """Tests the min operation; WILL be set since 5 < 10."""
        op = MinOperation()
        assert op.LABEL == "min"

        table[location] = 10
        op.evaluate(table=table, value=5, attribute=location)
        assert table.to_dict() == {"test": {"location": 5}}

        # test with date
        value = DateTaggedValue(date=date(2025, 12, 31), value=1)
        op.evaluate(table=table, value=value, attribute=location)
        assert table.to_dict() == {
            "test": {"location": {"date": "2025-12-31", "value": 1}}
        }

        # test a number again
        op.evaluate(table=table, value=-1, attribute=location)
        assert table.to_dict() == {"test": {"location": -1}}

    def test_max(self, table, location):
        """Tests the max operation; will NOT be set since 5 < 10."""
        op = MaxOperation()
        assert op.LABEL == "max"

        table[location] = 10
        op.evaluate(table=table, value=5, attribute=location)

        assert table.to_dict() == {"test": {"location": 10}}

        # test with date - this time start with date and override with date
        table[location] = {"date": "2025-01-01", "value": 10}
        value = DateTaggedValue(date=date(2024, 12, 31), value=20)
        op.evaluate(table=table, value=value, attribute=location)
        assert table.to_dict() == {
            "test": {"location": {"date": "2024-12-31", "value": 20}}
        }
