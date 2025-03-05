"""Tests cross-module attributes."""
import pytest

from nacc_attribute_deriver.attributes.nacc.modules.cross_module import (
    CrossModuleAttribute, )
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='function')
def attr() -> CrossModuleAttribute:
    """Create dummy data and return it in an attribute object."""
    data = {
        'file': {
            'info': {
                'forms': {
                    'json': {
                        'visitdate': '2025-01-01',
                        'birthmo': 3,
                        'birthyr': 1990
                    }
                }
            }
        },
        'np': {
            'info': {
                'forms': {
                    'json': {
                        'npdage': '2025-01-01'
                    }
                }
            }
        },
        'mds': {
            'info': {
                'forms': {
                    'json': {
                        'deceased': 1,
                        'deathyr': 2030,
                        'deathmo': 1,
                        'deathdy': 1
                    }
                }
            }
        }
    }

    return CrossModuleAttribute(SymbolTable(data))


class TestCrossModuleAttribute:

    def test_create_naccdage(self, attr):
        """Tests creating NACCDAGE triggering each case."""
        # trigger NP case
        assert attr._create_naccdage() == 34

        # trigger MDS case
        attr.table['np'] = {}
        assert attr._create_naccdage() == 39

        # trigger none case
        attr.table['mds.info.forms.json.deceased'] = 0
        assert attr._create_naccdage() == 999

        attr.table['mds'] = {}
        assert attr._create_naccdage() == 999
