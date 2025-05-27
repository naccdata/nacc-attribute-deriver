from nacc_attribute_deriver.attributes.base.namespace import BaseNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class TestAttribute:
    def test_get_value(self):
        """Tests getting value."""
        table = SymbolTable()
        table["test.value"] = 5
        table["some.other.prefix.value"] = 10

        attr = BaseNamespace(table, attribute_prefix="test.")
        assert attr.get_value("value") == 5
        assert attr.get_value("missing") is None
        assert attr.get_value("missing", "default") == "default"
