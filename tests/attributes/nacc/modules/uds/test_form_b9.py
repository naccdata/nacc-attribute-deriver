"""Tests UDS Form B9 attributes."""

import pytest
from nacc_attribute_deriver.attributes.nacc.modules.uds.form_b9 import (
    UDSFormB9Attribute,
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
                    }
                }
            }
        },
        "subject": {
            "info": {
                "derived": {
                    "longitudinal": {
                        "decclin": 2,
                    }
                }
            }
        },
    }

    return SymbolTable(data)