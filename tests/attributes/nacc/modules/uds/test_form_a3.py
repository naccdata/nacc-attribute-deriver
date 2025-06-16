"""Tests form A3."""

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
                        "dadprdx": 110,
                    }
                }
            }
        }
    }

    return SymbolTable(data)


@pytest.fixture(scope="function")
def naccfam_table() -> SymbolTable:
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
                        "dadneur": 4,
                        "dadprdx": 210,
                        "momneur": 8,
                        "sib1neu": 8,
                        "sib2neu": 8,
                        "sib3neu": 8,
                        "kid1neu": 8,
                        "kid2neu": 8,
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

        set_attribute(table, form_prefix, "dadneur", None)
        set_attribute(table, form_prefix, "dadprdx", None)
        assert attr._create_naccdad() == 9

        set_attribute(table, form_prefix, "dadneur", 3)
        assert attr._create_naccdad() == 0

    def test_create_naccfam(self, table, naccfam_table, form_prefix):
        """Tests creating NACCFAM."""
        attr = UDSFormA3Attribute(table)
        set_attribute(table, form_prefix, "dadneur", None)
        assert attr._create_naccfam() == 9

        attr = UDSFormA3Attribute(naccfam_table)
        assert attr._create_naccfam() == 0

        set_attribute(naccfam_table, form_prefix, "dadneur", 1)
        set_attribute(naccfam_table, form_prefix, "dadprdx", 400)
        assert attr._create_naccfam() == 1

        set_attribute(naccfam_table, form_prefix, "dadprdx", 888)
        assert attr._create_naccfam() == 0

        # another case, both mom and dad neur == 1
        set_attribute(naccfam_table, form_prefix, "dadneur", 1)
        set_attribute(naccfam_table, form_prefix, "dadprdx", 110)
        set_attribute(naccfam_table, form_prefix, "moneur", 1)
        set_attribute(naccfam_table, form_prefix, "momprdx", 50)
        assert attr._create_naccfam() == 1
