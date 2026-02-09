"""Tests generic UDS missingness attributes."""

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSMissingness,
)
from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_uds import (
    GenericUDSMissingness,
)
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)


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


class TestGenericUDSMissingness:
    def test_frmdatex(self, uds_table):
        """Test missingness on FRMDATEX variables."""
        attr = GenericUDSMissingness(uds_table)

        # not there
        assert attr._missingness_uds("frmdatea1a", str) == INFORMED_BLANK

        # is there and valid, but differnt format
        uds_table["file.info.forms.json.frmdatea1a"] = "01/01/2025"
        assert attr._missingness_uds("frmdatea1a", str) == "2025-01-01"

        # is there but not valid
        uds_table["file.info.forms.json.frmdatea1a"] = "N/A"
        assert attr._missingness_uds("frmdatea1a", str) == INFORMED_BLANK

    def test_generic_missingness(self, uds_table):
        """Test correct generic types returned."""
        attr = GenericUDSMissingness(uds_table)

        assert attr._missingness_uds("someint", int) == INFORMED_MISSINGNESS
        assert isinstance(attr._missingness_uds("someint", int), int)

        assert attr._missingness_uds("somefloat", float) == float(INFORMED_MISSINGNESS)
        assert isinstance(attr._missingness_uds("somefloat", float), float)

        assert attr._missingness_uds("somestr", str) == INFORMED_BLANK
        assert isinstance(attr._missingness_uds("somestr", str), str)

        # test value is actually there
        uds_table["file.info.forms.json"]
