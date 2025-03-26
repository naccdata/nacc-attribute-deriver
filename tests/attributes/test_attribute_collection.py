"""Tests the base AttributeCollection classes."""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection


class TestAttributeCollection:
    def test_is_int_value(self):
        """Tests is_int_value."""
        assert AttributeCollection.is_int_value("5", 5)
        assert AttributeCollection.is_int_value(5, 5)
        assert not AttributeCollection.is_int_value(None, 5)
        assert not AttributeCollection.is_int_value(3, 5)
        assert not AttributeCollection.is_int_value("3", 5)
        assert not AttributeCollection.is_int_value("hello", 5)
