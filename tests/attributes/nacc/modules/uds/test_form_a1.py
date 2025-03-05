"""
Tests UDS Form A1 attributes.
"""
import pytest

from nacc_attribute_deriver.attributes.nacc.modules.uds.form_a1 import UDSFormA1Attribute
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='function')
def attr() -> UDSFormA1Attribute:
    """Create dummy data and return it in an attribute object.
    """
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


class TestCreateNACCNIHR:
    """Specifically test the generate_naccnihr function,
    which ultimately is also testing _create_naccnihr.
    """

    def test_original_primary(self):
        generate_naccnihr = UDSFormA1Attribute.generate_naccnihr
        assert generate_naccnihr(None, None, None, None, None, None) == 99
        assert generate_naccnihr(1, None, None, None, None, None) == 1
        assert generate_naccnihr(2, None, None, None, None, None) == 2
        assert generate_naccnihr(3, None, None, None, None, None) == 3
        assert generate_naccnihr(4, None, None, None, None, None) == 4
        assert generate_naccnihr(5, None, None, None, None, None) == 5
        assert generate_naccnihr(6, None, None, None, None, None) == 6
        assert generate_naccnihr(88, None, None, None, None, None) == 88

    def test_original_primary_writein(self):
        generate_naccnihr = UDSFormA1Attribute.generate_naccnihr
        assert generate_naccnihr(50, "Arab", None, None, None, None) == 1
        assert generate_naccnihr(50, "African American", None, None, None, None) == 2
        assert generate_naccnihr(50, "NATIVE AMERICAN", None, None, None, None) == 3
        assert generate_naccnihr(50, "Samoan", None, None, None, None) == 4   
        assert generate_naccnihr(50, "Tahitian", None, None, None, None) == 4           
        assert generate_naccnihr(50, "Asian", None, None, None, None) == 5
        assert generate_naccnihr(50, "Biracial", None, None, None, None) == 6       
        assert generate_naccnihr(50, "African and American Indian", None, None, None, None) == 6 
        assert generate_naccnihr(50, "HUMAN", None, None, None, None) == 99

    def test_original_ignore(self):
        generate_naccnihr = UDSFormA1Attribute.generate_naccnihr
        # seems like it should ignore the racex
        assert generate_naccnihr(1, "Arab", None, None, None, None) == 1        
        assert generate_naccnihr(2, "Arab", None, None, None, None) == 2
        assert generate_naccnihr(3, "Arab", None, None, None, None) == 3
        assert generate_naccnihr(4, "Arab", None, None, None, None) == 4       
        assert generate_naccnihr(5, "Arab", None, None, None, None) == 6
        assert generate_naccnihr(6, "Arab", None, None, None, None) == 6
