import pytest
from nacc_attribute_deriver.attributes.base.namespace import (
    BaseNamespace,
    NamespaceScope,
)
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable


class TestNamespaceScope:
    def test_empty_scope(self):
        table = SymbolTable()
        namespace = BaseNamespace(table, attribute_prefix="zzz")
        scope = NamespaceScope(namespace, "dummy", fields=[])

        assert scope.get_value("aaaa") is None

    def test_missing_scope(self):
        table = SymbolTable()
        scope = NamespaceScope(
            namespace=BaseNamespace(table, attribute_prefix="zzz"),
            name="dummy",
            fields=["xxx"],
        )
        with pytest.raises(MissingRequiredError) as error:
            scope.get_value("xxx")
        assert str(error.value) == "Missing required field: zzz.xxx for scope dummy"
