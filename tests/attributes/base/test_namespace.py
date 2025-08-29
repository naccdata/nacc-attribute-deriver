"""Tests Base namespaces."""

from nacc_attribute_deriver.attributes.base.namespace import BaseNamespace, INVALID_TEXT
from nacc_attribute_deriver.symbol_table import SymbolTable


class TestAttribute:
    def test_get_value(self):
        """Tests getting value."""
        table = SymbolTable()
        table["test.value"] = 5
        table["some.other.prefix.value"] = 10

        attr = BaseNamespace(table=table, attribute_prefix="test.")
        assert attr.get_value("value", int) == 5
        assert attr.get_value("missing", int) is None
        assert attr.get_value("missing", str, default="default") == "default"

    def test_invalid_string(self):
        """Tests invalid string values return as None."""
        table = SymbolTable()
        attr = BaseNamespace(table=table, attribute_prefix="test.")

        for value in INVALID_TEXT:
            table["test.value"] = value
            assert attr.get_value("value", int) is None
