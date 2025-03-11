"""Tests UDS Form A1 attributes."""
import pytest

from nacc_attribute_deriver.attributes.nacc.modules.uds.form_a1 import UDSFormA1Attribute
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='function')
def attr() -> UDSFormA1Attribute:
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
        }
    }

    return UDSFormA1Attribute(SymbolTable(data))


class TestUDSFormA1Attribute:

    def test_create_naccage(self, attr):
        """Tests creating NACCAGE."""
        assert attr._create_naccage() == 34

        # exact birthday
        attr.set_value('birthmo', 1)
        assert attr._create_naccage() == 35

    def test_NACC961734(self, attr):
        """Case that has issue due to visitdate == birthday."""
        attr.set_value('visitdate', '2007-06-01')
        attr.set_value('birthmo', 6)
        attr.set_value('birthyr', 1910)

        assert attr._create_naccage() == 97

    def test_NACC190430(self, attr):
        """Case that has issue due to visitdate == birthday."""
        attr.set_value('visitdate', '2010-03-01')
        attr.set_value('birthmo', 3)
        attr.set_value('birthyr', 1956)

        assert attr._create_naccage() == 54
