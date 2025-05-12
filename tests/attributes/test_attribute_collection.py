"""Tests the base AttributeCollection classes."""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection


class TestAttributeCollection:
    def test_is_target_int(self):
        """Tests is_target_int."""
        assert AttributeCollection.is_target_int("5", 5)
        assert AttributeCollection.is_target_int(5, 5)
        assert not AttributeCollection.is_target_int(None, 5)
        assert not AttributeCollection.is_target_int(3, 5)
        assert not AttributeCollection.is_target_int("3", 5)
        assert not AttributeCollection.is_target_int("hello", 5)
