"""Tests UDS Form B3 missingness attributes."""

import random

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_b3 import (
    UDSFormB3Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class TestUDSFormB3LegacyMissingness:
    def test_pdnormal(self, uds_table):
        """Test PDNORMAL missingness."""
        # make them all 0
        uds_table["file.info.forms.json"].update(
            {x: 0 for x in UDSFormB3Missingness.ALL_B3_FIELDS}
        )
        uds_table["file.info.forms.json"].update({"pdnormal": 0})

        attr = UDSFormB3Missingness(uds_table)
        assert attr._missingness_pdnormal() == 1

        # make them all some value 1-4
        uds_table["file.info.forms.json"].update(
            {x: random.choice([1, 2, 3, 4]) for x in UDSFormB3Missingness.ALL_B3_FIELDS}
        )
        uds_table["file.info.forms.json"].update({"pdnormal": 1})

        assert attr._missingness_pdnormal() == 0

        # make them all None
        uds_table["file.info.forms.json"].update(
            {x: None for x in UDSFormB3Missingness.ALL_B3_FIELDS}
        )

        uds_table["file.info.forms.json.pdnormal"] = 1
        assert attr._missingness_pdnormal() is None

        uds_table["file.info.forms.json.pdnormal"] = None
        assert attr._missingness_pdnormal() == INFORMED_MISSINGNESS

        # make them all mix of 0, 8, blank
        uds_table["file.info.forms.json"].update(
            {x: random.choice([0, 8, None]) for x in UDSFormB3Missingness.ALL_B3_FIELDS}
        )

        assert attr._missingness_pdnormal() == 8

        # PDNORMAL = 0, but all are 0 or 8, with at least one 8
        uds_table["file.info.forms.json"].update(
            {x: random.choice([0, 8]) for x in UDSFormB3Missingness.ALL_B3_FIELDS}
        )
        uds_table["file.info.forms.json.pdnormal"] = 0
        uds_table["file.info.forms.json.speech"] = 8
        assert attr._missingness_pdnormal() == 8

        # if one is None, PDNORMAL stays as it is
        uds_table["file.info.forms.json.speech"] = None
        assert attr._missingness_pdnormal() is None
