"""Tests CSF missingness attributes."""

import pytest

from nacc_attribute_deriver.attributes.missingness.modules.csf.missingness_csf import (
    CSFFormMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


@pytest.fixture(scope="function")
def csf_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    return SymbolTable(
        {
            "file": {
                "info": {
                    "forms": {
                        "json": {
                            "visitdate": "2020-01-01",
                            "csflpdate": "09/11/2023",
                            "csfabeta": 1234.5,
                            "csfttau": "0.02",
                            "csfptau": 525.2,
                        }
                    }
                }
            }
        }
    )


class TestCSFMissingness:
    def test_missingness_csflpdate(self, csf_table):
        """Test _missingness_csflpdate is handled correctly."""
        attr = CSFFormMissingness(csf_table)
        assert attr._missingness_csflpdate() == "2023-09-11"

    def test_ranges_enforced(self, csf_table):
        """Test the ranges are enforced."""
        attr = CSFFormMissingness(csf_table)

        assert attr._missingness_csfabeta() == 1234.5
        assert attr._missingness_csfttau() == 1.0
        assert attr._missingness_csfptau() == 500.0

        # see how typical "unknown-looking" codes behave
        csf_table["file.info.forms.json"].update(
            {
                "csfabeta": None,  # stays as informed missingness
                "csfttau": 999,  # should stay because its within range
                "csfptau": 888,  # should be range enforced
            }
        )

        assert attr._missingness_csfabeta() == INFORMED_MISSINGNESS
        assert attr._missingness_csfttau() == 999.0
        assert attr._missingness_csfptau() == 500.0
