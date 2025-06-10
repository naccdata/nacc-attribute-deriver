import pytest
from nacc_attribute_deriver.attributes.base.namespace import BaseNamespace
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable


class TestNamespace:
    def test_get_value(self):
        """Tests getting value."""
        table = SymbolTable()
        table["test.value"] = 5
        table["some.other.prefix.value"] = 10

        attr = BaseNamespace(table, attribute_prefix="test.")
        assert attr.get_value("value") == 5
        assert attr.get_value("missing") is None
        assert attr.get_value("missing", "default") == "default"

    def test_required(self):
        """Tests namespace with required attributes."""

        table = SymbolTable()
        with pytest.raises(MissingRequiredError) as error:
            BaseNamespace(
                table=table, attribute_prefix="test", required=frozenset({"buzz"})
            )
        assert str(error.value) == "missing required attributes: test.buzz"
        assert error.value.fields == ["test.buzz"]

        date_attribute_name = "data-date"
        with pytest.raises(MissingRequiredError) as error:
            BaseNamespace(
                table=table,
                attribute_prefix="test",
                required=frozenset(),
                date_attribute=date_attribute_name,
            )
        assert (
            str(error.value)
            == f"missing required attributes: test.{date_attribute_name}"
        )
        assert error.value.fields == [f"test.{date_attribute_name}"]

        with pytest.raises(MissingRequiredError) as error:
            BaseNamespace(
                table=table,
                attribute_prefix="test",
                required=frozenset(["buzz"]),
                date_attribute=date_attribute_name,
            )
        assert (
            str(error.value)
            == f"missing required attributes: test.{date_attribute_name}, test.buzz"
        )
        assert error.value.fields == [f"test.{date_attribute_name}", "test.buzz"]

        table["test.buzz"] = 1
        table[f"test.{date_attribute_name}"] = "2005-01-10"
        try:
            BaseNamespace(
                table=table,
                attribute_prefix="test",
                required=frozenset(["buzz"]),
                date_attribute=date_attribute_name,
            )
            assert True
        except MissingRequiredError:
            assert False, "should be no exception"  # noqa: B011
