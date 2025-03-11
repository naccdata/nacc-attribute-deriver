"""Tests the operations."""
import pytest

from nacc_attribute_deriver.schema.operation import (
    CountOperation,
    InitialOperation,
    LatestOperation,
    MaxOperation,
    MinOperation,
    OperationRegistry,
    SetOperation,
    UpdateOperation,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='module')
def date_key() -> str:
    """Generate testing date key."""
    return 'test.date'


@pytest.fixture(scope='module')
def location() -> str:
    """Generate testing location key."""
    return 'test.location'


@pytest.fixture(scope='function')
def table(location, date_key) -> SymbolTable:
    """Generate dummy table for testing."""
    table = SymbolTable()
    table[date_key] = '2025-01-01'
    table[location] = {'date': '2024-01-01', 'value': 10}
    return table


class TestOperation():

    def test_registry(self):
        """Test registry is instantiated correctly."""
        assert OperationRegistry.operations == [
            UpdateOperation, SetOperation, InitialOperation, LatestOperation,
            CountOperation, MinOperation, MaxOperation
        ]

    def test_update(self, table, location):
        """Tests the update operation."""
        op = UpdateOperation()
        assert op.LABEL == 'update'
        op.evaluate(table, 5, location)

        assert table.to_dict() == {
            'test': {
                'date': '2025-01-01',
                'location': 5
            }
        }

    def test_set(self, table, location):
        """Tests the set operation."""
        op = SetOperation()
        assert op.LABEL == 'set'
        table[location] = [1, 2, 3, 4]
        op.evaluate(table, 5, location)

        assert table.to_dict() == {
            'test': {
                'date': '2025-01-01',
                'location': [1, 2, 3, 4, 5]
            }
        }

        # test doing it again will not change since it's a set
        for i in range(1, 6):
            op.evaluate(table, i, location)
            assert table.to_dict() == {
                'test': {
                    'date': '2025-01-01',
                    'location': [1, 2, 3, 4, 5]
                }
            }

    def test_initial(self, table, location, date_key):
        """Tests the initial operation; will NOT be set since current date >
        destination date."""
        op = InitialOperation()
        assert op.LABEL == 'initial'
        op.evaluate(table, 5, location, date_key)

        assert table.to_dict() == {
            'test': {
                'date': '2025-01-01',
                'location': {
                    'date': '2024-01-01',
                    'value': 10
                }
            }
        }

    def test_latest(self, table, location, date_key):
        """Tests the latest operation; WILL be set since current date >
        destination date."""
        op = LatestOperation()
        assert op.LABEL == 'latest'
        op.evaluate(table, 5, location, date_key)

        assert table.to_dict() == {
            'test': {
                'date': '2025-01-01',
                'location': {
                    'date': '2025-01-01',
                    'value': 5
                }
            }
        }

    def test_min(self, table, location):
        """Tests the min operation; WILL be set since 5 < 10."""
        op = MinOperation()
        assert op.LABEL == 'min'

        table[location] = 10
        op.evaluate(table, 5, location)

        assert table.to_dict() == {
            'test': {
                'date': '2025-01-01',
                'location': 5
            }
        }

    def test_max(self, table, location):
        """Tests the max operation; will NOT be set since 5 < 10."""
        op = MaxOperation()
        assert op.LABEL == 'max'

        table[location] = 10
        op.evaluate(table, 5, location)

        assert table.to_dict() == {
            'test': {
                'date': '2025-01-01',
                'location': 10
            }
        }
