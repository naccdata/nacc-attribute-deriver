"""Tests header missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.header.missingness_header import (  # noqa: E501
    HeaderFormMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class TestHeaderMissingness:
    def test_visitdate(self):
        """Test VISITDATE resolves to the same format."""
        table = SymbolTable()
        table["file.info.forms.json.visitdate"] = "2025-01-01"
        attr = HeaderFormMissingness(table)

        # YYYY-MM-DD
        assert attr._missingness_header_visitdate() == "2025-01-01"

        # YYYY/MM/DD
        table["file.info.forms.json.visitdate"] = "2025/01/01"
        assert attr._missingness_header_visitdate() == "2025-01-01"

        # MM-DD-YYYY
        table["file.info.forms.json.visitdate"] = "01-01-2025"
        assert attr._missingness_header_visitdate() == "2025-01-01"

        # MM/DD/YYYY
        table["file.info.forms.json.visitdate"] = "01/01/2025"
        assert attr._missingness_header_visitdate() == "2025-01-01"
