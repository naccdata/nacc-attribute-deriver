"""Tests UDS Form A1 attributes."""

import pytest

from nacc_attribute_deriver.attributes.nacc.modules.uds.form_a1 import (
    UDSFormA1Attribute,  # type: ignore
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "birthmo": 3,
                        "birthyr": 1990,
                        "module": "UDS",
                    }
                }
            }
        }
    }

    return SymbolTable(data)


class TestUDSFormA1Attribute:
    def test_create_naccage(self, table, form_prefix):
        """Tests creating NACCAGE."""
        attr = UDSFormA1Attribute(table)
        assert attr._create_naccage() == 34  # noqa: SLF001

        # exact birthday
        set_attribute(table, form_prefix, "birthmo", 1)
        attr = UDSFormA1Attribute(table)
        assert attr._create_naccage() == 35  # noqa: SLF001

    def test_visit_on_birthday(self, table, form_prefix):
        """Case that has issue due to visitdate == birthday."""
        set_attribute(table, form_prefix, "visitdate", "2007-06-01")
        set_attribute(table, form_prefix, "birthmo", 6)
        set_attribute(table, form_prefix, "birthyr", 1910)
        attr = UDSFormA1Attribute(table)

        assert attr._create_naccage() == 97  # noqa: SLF001

        """Case that has issue due to visitdate == birthday."""
        set_attribute(table, form_prefix, "visitdate", "2010-03-01")
        set_attribute(table, form_prefix, "birthmo", 3)
        set_attribute(table, form_prefix, "birthyr", 1956)
        attr = UDSFormA1Attribute(table)

        assert attr._create_naccage() == 54  # noqa: SLF001
