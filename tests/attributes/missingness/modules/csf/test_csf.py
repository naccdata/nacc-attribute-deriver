"""Tests CSF missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.csf.missingness_csf import (
    CSFFormMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


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

        # see how typical "unknown-looking" codes behave
        table["file.info.forms.json"].update(
            {
                "csfabeta": None,  # stays as informed missingness
                "csfttau": 999,  # should stay because its within range
                "csfptau": 888,  # should be range enforced
            }
        )

        assert attr._missingness_csfabeta() == INFORMED_MISSINGNESS
        assert attr._missingness_csfttau() == 999.0
        assert attr._missingness_csfptau() == 500.0
