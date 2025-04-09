"""Tests UDS namespace."""

from datetime import datetime

import pytest

from nacc_attribute_deriver.attributes.nacc.modules.uds.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in a table."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "birthmo": "3",
                        "birthyr": "1990",
                        "module": "UDS",
                    }
                }
            }
        },
        "subject": {
            "info": {
                "derived": {
                    "target": 2,
                }
            }
        },
    }

    return SymbolTable(data)


class TestUDSNamespace:
    def test_generate_uds_dob(self, table):
        """Tests generate_uds_dob."""
        namespace = UDSNamespace(table)
        assert namespace.generate_uds_dob() == datetime(1990, 3, 1).date()

    def test_is_followup(self, table, form_prefix):
        """Tests is_followup."""
        # starts as non-followup
        namespace = UDSNamespace(table)
        assert not namespace.is_followup()

        # set to followup packet
        set_attribute(table, form_prefix, "packet", "F")
        assert namespace.is_followup()

    def test_check_default(self, table, form_prefix):
        """Tests check_default.

        Iterates over multiple forms and asserts target field always
        returns 2 except in the non-followup case.
        """
        namespace = UDSNamespace(table)
        assert namespace.check_default("target", "default") == "default"

        # set to followup packet
        set_attribute(table, form_prefix, "packet", "F")
        assert namespace.check_default("target", "default") == 2

        # set target in file to 777 - should still return 2
        set_attribute(table, form_prefix, "target", "777")
        assert namespace.check_default("target", "default") == 2
        set_attribute(table, form_prefix, "target", 777)
        assert namespace.check_default("target", "default") == 2
