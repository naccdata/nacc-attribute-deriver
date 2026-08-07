"""Tests the UDS collections."""

from datetime import datetime

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
    UDSMissingness,
)

from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)


class TestUDSAttributeCollection:
    def test_get_date(self, uds_table):
        """Test getting the visitdate from an UDS form attribute."""
        # should be 2025-01-01
        attr = UDSAttributeCollection(uds_table)
        assert attr.get_date() == datetime(2025, 1, 1).date()


class TestUDSMissingness:
    def test_handle_optional_header_variables(self, uds_table):
        """Test handling an optional header variables."""
        # Valid values
        uds_table["file.info.forms.json"].update(
            {
                "langxxx": 2,
                "adminxxx": 1,
            }
        )

        attr = UDSMissingness(uds_table)
        assert attr.handle_optional_header_variables("lang", "xxx", [1, 2]) == 2
        assert attr.handle_optional_header_variables("admin", "xxx", [1, 2]) == 1

        # Invalid values
        uds_table["file.info.forms.json"].update({"langxxx": 3, "adminxxx": -1})
        assert (
            attr.handle_optional_header_variables("lang", "xxx", [1, 2])
            == INFORMED_MISSINGNESS
        )
        assert (
            attr.handle_optional_header_variables("admin", "xxx", [1, 2])
            == INFORMED_MISSINGNESS
        )
