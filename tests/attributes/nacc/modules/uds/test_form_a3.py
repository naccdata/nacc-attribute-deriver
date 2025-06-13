"""
Tests form A3
"""
import pytest
from nacc_attribute_deriver.attributes.nacc.modules.uds.form_a3 import (
    UDSFormA3Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute

@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "birthmo": 3,
                        "birthyr": 1990,
                        "module": "UDS",
                        "packet": "I",
                        "formver": "3.0",
                        "a3sub": 1,
                        "daddem": None,
                        "dadneur": 1,
                        "dadprdx": 110
                    }
                }
            }
        }
    }

    return SymbolTable(data)


class TestUDSFormA3Attribute:
    def test_create_naccdad(self, table, form_prefix):
        """Tests creating NACCDAD."""
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 1

        set_attribute(table, form_prefix, 'dadneur', None)
        set_attribute(table, form_prefix, 'dadprdx', None)
        assert attr._create_naccdad() == 9

        set_attribute(table, form_prefix, 'dadneur', 3)
        assert attr._create_naccdad() == 0