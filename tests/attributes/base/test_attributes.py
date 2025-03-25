import pytest

from nacc_attribute_deriver.attributes.base.namespace import BaseNamespace
from nacc_attribute_deriver.schema.errors import MissingRequiredError
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

    def test_assert_required(self):
        """Test the assert_required method."""
        table = SymbolTable()
        table["file.info.forms.json"] = {}
        attr = BaseNamespace(table, "file.info.forms.json.")

        # should raise error since there's nothing int able
        with pytest.raises(MissingRequiredError) as error:
            attr.assert_required(["testvar"])
        assert error.value.field == "file.info.forms.json.testvar"
