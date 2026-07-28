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
        """Test handling an optional header variable when form is and isn't
        submitted."""
        # Submitted
        uds_table["file.info.forms.json"].update(
            {
                "modexxx": 1,
                "langxxx": 2,
                "adminxxx": None,
            }
        )

        attr = UDSMissingness(uds_table)
        assert attr.handle_optional_header_variables("lang", "xxx") == 2
        assert (
            attr.handle_optional_header_variables("admin", "xxx")
            == INFORMED_MISSINGNESS
        )

        # not submitted
        uds_table["file.info.forms.json"].update(
            {
                "modexxx": 0,
            }
        )
        assert (
            attr.handle_optional_header_variables("lang", "xxx") == INFORMED_MISSINGNESS
        )
        assert (
            attr.handle_optional_header_variables("admin", "xxx")
            == INFORMED_MISSINGNESS
        )
