"""Tests UDS Form B8 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_b8 import (
    UDSFormB8Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class TestUDSFormB8Missingness:
    def test_missingness_gaitfind(self, uds_table):
        """Tests _missingness_gaitfind."""
        # V3 and earlier is just informed missingness
        attr = UDSFormB8Missingness(uds_table)
        assert attr._missingness_gaitfind() == INFORMED_MISSINGNESS

        # V4
        uds_table["file.info.forms.json.formver"] = 4.0
        attr = UDSFormB8Missingness(uds_table)

        # 8 if NORMNREXAM or GAITBN is 0
        uds_table["file.info.forms.json"].update({"normnrexam": 0, "gaitabn": 1})
        assert attr._missingness_gaitfind() == 8

        uds_table["file.info.forms.json"].update({"normnrexam": 1, "gaitabn": 0})
        assert attr._missingness_gaitfind() == 8

        # no conditions passed, generic missingness
        uds_table["file.info.forms.json"].update({"normnrexam": 1, "gaitabn": 1})
        assert attr._missingness_gaitfind() == INFORMED_MISSINGNESS
        uds_table["file.info.forms.json.gaitfind"] = 5
        assert attr._missingness_gaitfind() is None

    def test_handle_normnrexam_gate(self, uds_table):
        """Test _handle_normnrexam_gate."""
        # V3 and earlier is just informed missingness
        attr = UDSFormB8Missingness(uds_table)
        assert attr._handle_normnrexam_gate("somevar") == INFORMED_MISSINGNESS

        # V4
        uds_table["file.info.forms.json.formver"] = 4.0
        attr = UDSFormB8Missingness(uds_table)

        # if normnrexam == 0, should return 0
        uds_table["file.info.forms.json.normnrexam"] = 0
        assert attr._handle_normnrexam_gate("somevar") == 0

        # no conditions passed, generic missingness
        uds_table["file.info.forms.json.normnrexam"] = 1
        assert attr._handle_normnrexam_gate("somevar") == INFORMED_MISSINGNESS
        uds_table["file.info.forms.json.somevar"] = 5
        assert attr._handle_normnrexam_gate("somevar") is None

    def test_handle_normnrexam_with_gate(self, uds_table):
        """Tests _handle_normnrexam_with_gate."""
        # V3 and earlier is just informed missingness
        attr = UDSFormB8Missingness(uds_table)
        assert (
            attr._handle_normnrexam_with_gate("gate", "somevar") == INFORMED_MISSINGNESS
        )

        # V4
        uds_table["file.info.forms.json.formver"] = 4.0
        attr = UDSFormB8Missingness(uds_table)

        # 0 if NORMNREXAM or GATE is 0
        uds_table["file.info.forms.json"].update({"normnrexam": 0, "gate": 1})
        assert attr._handle_normnrexam_with_gate("gate", "somevar") == 0

        uds_table["file.info.forms.json"].update({"normnrexam": 1, "gate": 0})
        assert attr._handle_normnrexam_with_gate("gate", "somevar") == 0

        # 8 if gate is 8
        uds_table["file.info.forms.json"].update({"normnrexam": 1, "gate": 8})
        assert attr._handle_normnrexam_with_gate("gate", "somevar") == 8

        # default case, missing
        uds_table["file.info.forms.json"].update({"normnrexam": None, "gate": None})
        assert (
            attr._handle_normnrexam_with_gate("gate", "somevar") == INFORMED_MISSINGNESS
        )

        # default case, not missing so return None (so doesn't override)
        uds_table["file.info.forms.json"].update(
            {"normnrexam": None, "gate": None, "somevar": 5}
        )
        assert attr._handle_normnrexam_with_gate("gate", "somevar") is None

    def test_postinst(self, uds_table):
        """Tests postinst."""

        # V3 - falls to normexam case
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.0,
                "packet": "I",
                "postinst": None,
                "normexam": 2,
            }
        )

        attr = UDSFormB8Missingness(uds_table)
        assert attr._missingness_postinst() == 0

        # V3 - falls to parksign case
        uds_table["file.info.forms.json"].update({"normexam": 1, "parksign": 0})
        assert attr._missingness_postinst() == 0

        # V3 - falls to neither case
        uds_table["file.info.forms.json"].update({"normexam": None, "parksign": None})
        assert attr._missingness_postinst() == INFORMED_MISSINGNESS
