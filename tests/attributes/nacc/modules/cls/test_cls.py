"""Tests CLS form."""

import pytest
from nacc_attribute_deriver.attributes.nacc.modules.cls.form_cls import (
    CLSFormAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "module": "CLS",
                        "formver": 3.0,
                        "aspkengl": 5,
                        "areaengl": 2,
                        "awriengl": None,
                        "aundengl": 1,
                        "aspkspan": 1,
                        "areaspan": 4,
                        "awrispan": 7,
                        "aundspan": 3,
                    }
                }
            }
        }
    }
    return SymbolTable(data)


class TestCLSFormAttributeCollection:
    def test_create_naccengl(self, table):
        """Tests _create_naccengl."""
        attr = CLSFormAttributeCollection(table)
        assert attr._create_naccengl() is None

    def test_create_naccspnl(self, table):
        """Tests _create_naccspnl."""
        attr = CLSFormAttributeCollection(table)
        assert attr._create_naccspnl() == 3.8
