"""Tests BDS form."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.bds.form_bds import (
    BDSFormAttributeCollection,
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
                        "module": "BDS",
                    }
                }
            }
        },
        "subject": {"info": {"working": {"cross-sectional": {"np-death-age": "86"}}}},
    }
    return SymbolTable(data)


class TestBDSFormAttributeCollection:
    def test_create_bds_naccdage(self, table):
        """Tests _create_bds_naccdage."""
        attr = BDSFormAttributeCollection(table)
        assert attr._create_bds_naccdage() == 86

        # when not there
        table.pop("subject")
        assert attr._create_bds_naccdage() == 999
