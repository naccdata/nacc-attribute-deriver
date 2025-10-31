"""Tests UDS namespace."""

from datetime import datetime

import pytest

from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.utils.errors import InvalidFieldError
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
                        "formver": "3.2",
                        "packet": "I",
                        "naccid": "NACC123456",
                        "adcid": 0,
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

    def test_is_initial(self, table, form_prefix):
        """Tests is_initial."""
        # starts as initial
        namespace = UDSNamespace(table)
        assert namespace.is_initial()

        # set to followup packet
        set_attribute(table, form_prefix, "packet", "F")
        assert not namespace.is_initial()

    def test_is_in_person(self, table, form_prefix):
        """Tests is_in_person."""
        namespace = UDSNamespace(table)
        assert namespace.is_in_person()

        set_attribute(table, form_prefix, "packet", "F")
        assert namespace.is_in_person()

        set_attribute(table, form_prefix, "packet", "IT")
        assert not namespace.is_in_person()

    def test_normalize_formver(self, table, form_prefix):
        """Tests normalize_formver."""
        # starts as non-followup
        namespace = UDSNamespace(table)
        assert namespace.normalized_formver() == 3

        # set to followup packet
        set_attribute(table, form_prefix, "formver", "3")
        assert namespace.normalized_formver() == 3

    def test_invalid_module(self, table, form_prefix):
        """Test invalid module; should throw InvalidFieldError."""
        set_attribute(table, form_prefix, "module", "FTLD")
        with pytest.raises(InvalidFieldError):
            UDSNamespace(table)

        set_attribute(table, form_prefix, "module", "UDS.")
        with pytest.raises(InvalidFieldError):
            UDSNamespace(table)
