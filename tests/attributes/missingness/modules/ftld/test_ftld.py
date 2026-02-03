"""Tests FTLD missingness attributes."""

import pytest

from nacc_attribute_deriver.attributes.missingness.modules.ftld.missingness_ftld import (  # noqa: E501
    FTLDFormMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def ftld_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "formver": 3.0,
                        "module": "FTLD",
                        "visitdate": "2025-01-10",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


class TestFTLDMissingness:
    def test_ftdinfyr(self, ftld_table):
        """Test the 99 case is handled."""
        attr = FTLDFormMissingness(ftld_table)
        ftld_table["file.info.forms.json.ftdinfyr"] = 99
        assert attr._missingness_ftdinfyr() == 9999

        ftld_table["file.info.forms.json.ftdinfyr"] = 1990
        assert attr._missingness_ftdinfyr() == 1990

    def test_ftdlengt(self, ftld_table):
        """Test the 0 case is handled and ranges enforced."""
        attr = FTLDFormMissingness(ftld_table)
        ftld_table["file.info.forms.json.ftdlengt"] = 0
        assert attr._missingness_ftdlengt() == 999

        ftld_table["file.info.forms.json.ftdlengt"] = 15
        assert attr._missingness_ftdlengt() == 20

        ftld_table["file.info.forms.json.ftdlengt"] = 243
        assert attr._missingness_ftdlengt() == 240

    def test_ftdratio(self, ftld_table):
        """Test the 88.0 case is handled."""
        attr = FTLDFormMissingness(ftld_table)
        ftld_table["file.info.forms.json.ftdratio"] = 88
        assert attr._missingness_ftdratio() == 88.8

        ftld_table["file.info.forms.json.ftdratio"] = 12.3
        assert attr._missingness_ftdratio() == 12.3
