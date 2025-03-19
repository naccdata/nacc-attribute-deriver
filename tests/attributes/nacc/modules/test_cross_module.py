"""Tests cross-module attributes."""
import pytest

from nacc_attribute_deriver.attributes.nacc.modules.cross_module import (
    CrossModuleAttribute,  # type: ignore
)
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
                        'birthyr': 1990,
                        'module': 'UDS'
                    }
                },
                'np': {
                    'npdage': 83
                },
                'milestone': {
                    'deceased': '1',
                    'deathyr': '2050',
                    'deathmo': '2',
                    'deathdy': '2'
                },
                'mds': {
                    'vitalst': 2,
                    'deathyr': 2030,
                    'deathmo': 1,
                    'deathday': 1
                }
            }
        }
    }

    return CrossModuleAttribute(SymbolTable(data))


class TestCrossModuleAttribute:

    def test_create_naccdage(self, attr):
        """Tests creating NACCDAGE triggering each case.

        This inherently tests _determine_death_date except in the NP
        case.
        """
        # trigger NP case
        assert attr._create_naccdage() == 83

        # trigger Milestone case
        attr.table['file.info.np'] = {}
        assert attr._create_naccdage() == 59

        # test when month/day is unknown for milestone
        # this will transform dmo = 7 and ddy = 1 which changes
        # the age since the birthday is before then
        attr.table['file.info.milestone'].update({
            'deathmo': 99,
            'deathdy': 99
        })
        assert attr._create_naccdage() == 60

        # trigger MDS case
        attr.table['file.info.milestone'] = {}
        assert attr._create_naccdage() == 39

        # test when year month/day is unknown for MDS,
        # similarly should change the age to 40
        attr.table['file.info.mds'].update({'deathmo': 99, 'deathdy': 99})
        assert attr._create_naccdage() == 40

        # in MDS, deathyr can be 9999, in which case
        # naccdage should be unknown
        attr.table['file.info.mds.deathyr'] = '9999'
        assert attr._create_naccdage() == 999

    def test_create_naccdied(self, attr):
        """Tests _create_naccdied.

        TODO: the DED says it doesn't rely on MDS
            but maybe it should?
        """
        # # NP case
        assert attr._create_naccdied() == 1

        # # Milestone case
        attr.table['file.info.np'] = {}
        assert attr._create_naccdied() == 1
        attr.table['file.info.milestone.deceased'] = 0
        assert attr._create_naccdied() == 0

        attr.table['file.info.milestone'] = {}
        assert attr._create_naccdied() == 0
