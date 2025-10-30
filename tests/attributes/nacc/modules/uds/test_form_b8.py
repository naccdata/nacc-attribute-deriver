"""Tests UDS Form B8 attributes."""

import random

from nacc_attribute_deriver.attributes.derived.modules.uds.form_b8 import (
    UDSFormB8Attribute,
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS


class TestUDSFormB8Attribute:
    def test_create_naccnrex_v3(self, uds_table):
        """Tests _create_naccnrex V3."""
        attr = UDSFormB8Attribute(uds_table)

        # first case
        uds_table["file.info.forms.json"].update({"normal": 1, "normexam": 1})
        assert attr._create_naccnrex() == 1
        uds_table["file.info.forms.json"].update(
            {"normal": 2, "normexam": random.choice([0, 2])}
        )
        assert attr._create_naccnrex() == 1

        # second case
        uds_table["file.info.forms.json"].update({"normal": 0, "normexam": 9})
        assert attr._create_naccnrex() == 0
        uds_table["file.info.forms.json"].update({"normal": 9, "normexam": 1})
        assert attr._create_naccnrex() == 0

        # third case
        uds_table["file.info.forms.json"].update({"normal": 9, "normexam": 9})
        assert attr._create_naccnrex() == 9

        # default case
        uds_table["file.info.forms.json"].update({"normal": None, "normexam": 9})
        assert attr._create_naccnrex() == INFORMED_MISSINGNESS

    def test_create_naccnrex_v4(self, uds_table):
        """Tests _create_naccnrex V4."""
        uds_table["file.info.forms.json.formver"] = 4.0
        attr = UDSFormB8Attribute(uds_table)

        # first case
        uds_table["file.info.forms.json"].update({"normnrexam": 0})
        assert attr._create_naccnrex() == 1

        # second case
        uds_table["file.info.forms.json"].update({"normnrexam": 1})
        assert attr._create_naccnrex() == 0

        # third case
        uds_table["file.info.forms.json"].update({"normnrexam": None, "neurexam": 8})
        assert attr._create_naccnrex() == 8

        # default case
        uds_table["file.info.forms.json"].update({"normnrexam": 9, "neurexam": 9})
        assert attr._create_naccnrex() == INFORMED_MISSINGNESS
