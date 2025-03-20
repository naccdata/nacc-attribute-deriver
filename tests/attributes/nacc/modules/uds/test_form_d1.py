"""Tests UDS Form D1 attributes."""
import pytest

from nacc_attribute_deriver.attributes.nacc.modules.uds.form_d1 import (
    ContributionStatus,
    UDSFormD1Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='function')
def attr() -> UDSFormD1Attribute:
    """Create dummy data and return it in an attribute object.

    In this case most will want to manually set fields so only leave
    bare minimum in.
    """
    data = {
        'file': {
            'info': {
                'forms': {
                    'json': {
                        'visitdate': '2025-01-01',
                        'normcog': 1,
                        'formver': 4,
                        'module': 'uds'
                    }
                }
            }
        }
    }

    return UDSFormD1Attribute(SymbolTable(data))


class TestUDSFormD1Attribute:

    def test_create_mci(self, attr):
        """Tests creating MCI."""
        assert attr._create_mci() == 0

        for field in ['mciamem', 'mciaplus', 'mcinon1', 'mcinon2']:
            attr.set_value(field, 1)
            assert attr._create_mci() == 1
            attr.set_value(field, 0)

        assert attr._create_mci() == 0

    def test_create_naccalzp(self, attr):
        """Tests creating NACCALZP."""
        assert attr._create_naccalzp() == 8

        attr.set_value('normcog', 0)
        assert attr._create_naccalzp() == 7

        for field in ['probadif', 'possadif', 'alzdisif']:
            for status in ContributionStatus.all():
                attr.set_value(field, status)
                assert attr._create_naccalzp() == status
                attr.set_value(field, None)

        attr.set_value('probadif', 3)
        attr.set_value('possadif', 2)
        attr.set_value('alzdisif', 1)
        assert attr._create_naccalzp() == 1

    def test_create_nacclbde(self, attr):
        """Tests creating NACCLBDE."""
        assert attr._create_nacclbde() == 8

        attr.set_value('normcog', 0)
        assert attr._create_nacclbde() is None

        for value in [0, 1]:
            attr.set_value('lbdis', value)
            assert attr._create_nacclbde() == value
        attr.set_value('lbdis', 3)

        attr.set_value('park', 0)
        assert attr._create_nacclbde() is None
        attr.set_value('dlb', 0)
        assert attr._create_nacclbde() == 0

        attr.set_value('dlb', 1)
        assert attr._create_nacclbde() == 1

        attr.set_value('formver', 3)
        assert attr._create_nacclbde() is None

    def test_create_nacclbdp(self, attr):
        """Tests creating NACCLBDP."""
        assert attr._create_nacclbdp() == 8

        attr.set_value('normcog', 0)
        assert attr._create_nacclbdp() is None

        # relies on nacclbde == 0
        attr.set_value('lbdis', 0)
        assert attr._create_nacclbdp() == 7

        for status in ContributionStatus.all():
            attr.set_value('lbdif', status)
            assert attr._create_nacclbdp() == status

        attr.set_value('dlbif', 3)
        assert attr._create_nacclbdp() == 3
        attr.set_value('parkif', 1)
        assert attr._create_nacclbdp() == 1

        attr.set_value('formver', 3)
        assert attr._create_nacclbdp() == 3  # where lbdif left off
