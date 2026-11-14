"""Tests UDS Form D1b missingness attributes."""

import pytest

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_d1b import (
    UDSFormD1bMissingness,
)
from nacc_attribute_deriver.utils.errors import InvalidFieldError


class TestUDSFormD1bMissingness:
    def test_ftldsubt(self, uds_table):
        """Test FTLDSUBT missingness - from regression tests."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.0,
                "packet": "I",
                "normcog": 1,
                "psp": 0,
                "cort": 0,
                "ftldmo": 0,
                "ftldnos": 0,
                "ftldsubt": None,
            }
        )

        attr = UDSFormD1bMissingness(uds_table)
        assert attr._missingness_ftldsubt() == 8

        uds_table["file.info.forms.json"].update(
            {
                "normcog": 0,
                "psp": 0,
                "cort": 0,
                "ftldmo": 0,
                "ftldnos": 1,
                "ftldsubt": 2,
            }
        )

        assert attr._missingness_ftldsubt() == 2

    def test_cognitive_impairment_gate_v4_mbi(self, uds_table):
        """V4 *IF fields: NORMCOG = 0 (including MBI only) -> 7."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 4.0,
                "packet": "I4",
                "normcog": 0,
                "mbi": 1,
                "msa": 0,
                "msaif": None,
            }
        )

        attr = UDSFormD1bMissingness(uds_table)
        assert not attr.has_cognitive_impairment()
        assert attr._missingness_msaif() == 7

        # diagnosis selected with MSAIF blank is invalid (not caught by QC)
        uds_table["file.info.forms.json"].update({"msa": 1})
        attr = UDSFormD1bMissingness(uds_table)
        with pytest.raises(InvalidFieldError):
            attr._missingness_msaif()

        # a filled-in contribution status is kept
        uds_table["file.info.forms.json"].update({"msaif": 2})
        attr = UDSFormD1bMissingness(uds_table)
        assert attr._missingness_msaif() == 2
        uds_table["file.info.forms.json"].update({"msa": 0, "msaif": None})

        uds_table["file.info.forms.json"].update({"normcog": 1, "mbi": None})
        attr = UDSFormD1bMissingness(uds_table)
        assert attr._missingness_msaif() == 8

    def test_ctecert_v4_mbi_unchanged(self, uds_table):
        """CTECERT is not a contribution field; MBI alone does not give 7."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 4.0,
                "packet": "I4",
                "normcog": 0,
                "mbi": 1,
                "cte": 0,
                "ctecert": None,
            }
        )

        attr = UDSFormD1bMissingness(uds_table)
        assert attr._missingness_ctecert() != 7

        uds_table["file.info.forms.json"].update({"demented": 1})
        attr = UDSFormD1bMissingness(uds_table)
        assert attr._missingness_ctecert() == 7

        # not a contribution field, so a selected CTE does not raise
        uds_table["file.info.forms.json"].update({"cte": 1})
        attr = UDSFormD1bMissingness(uds_table)
        assert attr._missingness_ctecert() != 7

    def test_cognitive_impairment_gate_v3_selected_no_error(self, uds_table):
        """V1-V3 diagnosis selected with *IF blank does not raise."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.0,
                "packet": "I",
                "normcog": 0,
                "demented": 1,
                "msa": 1,
                "msaif": None,
            }
        )

        attr = UDSFormD1bMissingness(uds_table)
        assert attr._missingness_msaif() != 7

    def test_cognitive_impairment_gate_v3_unchanged(self, uds_table):
        """V1-V3 *IF fields still require DEMENTED, MCI, or IMPNOMCI for 7."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.0,
                "packet": "I",
                "normcog": 0,
                "msa": 0,
                "msaif": None,
            }
        )

        attr = UDSFormD1bMissingness(uds_table)
        assert attr._missingness_msaif() != 7

        uds_table["file.info.forms.json"].update({"demented": 1})
        attr = UDSFormD1bMissingness(uds_table)
        assert attr._missingness_msaif() == 7
