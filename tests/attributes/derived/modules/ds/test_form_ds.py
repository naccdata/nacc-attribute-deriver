"""Tests DS form."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.ds.form_ds import (
    DSFormAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import InvalidFieldError


def make_table(module: str) -> SymbolTable:
    """Create a minimal form for the given module."""
    return SymbolTable(
        {
            "file": {
                "info": {
                    "forms": {"json": {"module": module, "visitdate": "2025-01-01"}}
                }
            }
        }
    )


class TestDSFormAttributeCollection:
    def test_create_naccds(self):
        """NACCDS is 1 for any DS form."""
        attr = DSFormAttributeCollection(make_table("DS"))
        assert attr._create_naccds() == 1

    def test_not_ds_form(self):
        """Raises an error if the file is not a DS form."""
        with pytest.raises(InvalidFieldError):
            DSFormAttributeCollection(make_table("FTLD"))
