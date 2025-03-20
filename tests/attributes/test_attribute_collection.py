"""Tests the base AttributeCollection classes."""

import pytest

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.base_attribute import FormAttribute
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable


class TestAttributeCollection:
    def test_get_value(self):
        """Tests getting value."""
        table = SymbolTable()
        table["test.value"] = 5
        table["some.other.prefix.value"] = 10

        attr = AttributeCollection(table, attribute_prefix="test.")
        assert attr.get_value("value") == 5
        assert attr.get_value("missing") is None
        assert attr.get_value("missing", "default") == "default"

        assert attr.get_value("value", prefix="some.other.prefix.") == 10
        assert (
            attr.get_value("missing", "default", prefix="some.other.prefix.")
            == "default"
        )

    def test_set_value(self):
        """Tests setting value."""
        table = SymbolTable()
        table["test"] = {}
        attr = AttributeCollection(table, attribute_prefix="test.")
        attr.set_value("value", 5)

        # make sure it used the prefix
        assert table.to_dict() == {"test": {"value": 5}}

    def test_aggregate_variables(self):
        """Tests aggregating variables."""
        table = SymbolTable()
        table["test"] = {"val1": 1, "val2": 2, "val3": 3}
        attr = AttributeCollection(table, attribute_prefix="test.")
        assert attr.aggregate_variables(
            ["val1", "val2", "val3", "val4"], default="missing"
        ) == {"val1": 1, "val2": 2, "val3": 3, "val4": "missing"}

    def test_is_int_value(self):
        """Tests is_int_value."""
        assert AttributeCollection.is_int_value("5", 5)
        assert AttributeCollection.is_int_value(5, 5)
        assert not AttributeCollection.is_int_value(None, 5)
        assert not AttributeCollection.is_int_value(3, 5)
        assert not AttributeCollection.is_int_value("3", 5)
        assert not AttributeCollection.is_int_value("hello", 5)


class TestMQTAttribute:
    def test_assert_required(self):
        """Test the assert_required method."""
        table = SymbolTable()
        table["file.info.forms.json"] = {}
        attr = FormAttribute(table)

        # should raise error since there's nothing int able
        with pytest.raises(MissingRequiredError) as e:
            attr.assert_required(["testvar"], prefix="file.info.derived.")
        assert (
            str(e.value)
            == "file.info.derived.testvar must be "
            + "derived before test_assert_required can run"
        )
