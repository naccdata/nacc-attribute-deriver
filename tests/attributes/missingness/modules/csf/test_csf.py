"""Tests CSF missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.csf.missingness_csf import (
    CSFFormMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class TestCSFMissingness:
    def test_ranges_enforced(self):
        """Test the ranges are enforced."""
        table = SymbolTable(
            {
                "file": {
                    "info": {
                        "forms": {
                            "json": {
                                "visitdate": "2020-01-01",
                                "csfabeta": 1234.5,
                                "csfttau": "0.02",
                                "csfptau": 525.2,
                            }
                        }
                    }
                }
            }
        )

        attr = CSFFormMissingness(table)

        assert attr._missingness_csfabeta() == 1234.5
        assert attr._missingness_csfttau() == 1.0
        assert attr._missingness_csfptau() == 500.0
