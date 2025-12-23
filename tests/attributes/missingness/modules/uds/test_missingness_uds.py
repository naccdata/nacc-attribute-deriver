"""Tests generic UDS missingness attributes."""

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSMissingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class TestUDSMissingness:
    def test_handle_prev_visit(self, uds_table):
        """Test when a previous visit is involved."""
        attr = UDSMissingness(uds_table)

        # sanity check - return if its in the current and no prev visit
        uds_table["file.info.forms.json.testval"] = 6
        assert attr.handle_prev_visit("testval", int) == 6

        # Case 1: Initial visit, so should return generic
        # missingness
        uds_table["file.info.forms.json.testval"] = None
        assert attr.handle_prev_visit("testval", int) == INFORMED_MISSINGNESS
        assert attr.handle_prev_visit("testval", int, default=0) == 0

        # Case 2: FVP visit - pull from prev_record
        uds_table["file.info.forms.json"].update({"packet": "F", "testval": None})
        uds_table["_prev_record.info.forms.json"] = {
            "visitdate": "1900-01-01",
            "packet": "I",
            "testval": 3,
        }
        attr = UDSMissingness(uds_table)
        assert attr.handle_prev_visit("testval", int) == 3
        uds_table["_prev_record.info.forms.json.testval"] = None
        assert attr.handle_prev_visit("testval", int) == INFORMED_MISSINGNESS
        assert attr.handle_prev_visit("testval", int, default=0) == 0

        # Case 3: I4 visit (same as FVP) - pull from resolved
        uds_table["file.info.forms.json"].update(
            {
                "packet": "I4",  # I4 should be treated identically to FVP
            }
        )
        uds_table["_prev_record.info.forms.json"] = {
            "visitdate": "1900-01-01",
            "packet": "F",
            "testval": None,
        }
        uds_table["_prev_record.info.resolved.testval"] = 5
        attr = UDSMissingness(uds_table)
        assert attr.handle_prev_visit("testval", int) == 5
        uds_table["_prev_record.info.resolved.testval"] = None
        assert attr.handle_prev_visit("testval", int) == INFORMED_MISSINGNESS
        assert attr.handle_prev_visit("testval", int, default=0) == 0
