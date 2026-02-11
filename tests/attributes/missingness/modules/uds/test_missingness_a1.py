"""Tests UDS Form A1 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a1 import (
    UDSFormA1Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class TestUDSFormA1Missingness:
    def test_missingness_residenc(self, uds_table):
        """Test missing RESIDENC - expect recode on 5 for V1/V2"""
        uds_table["file.info.forms.json"].update({"formver": 1.0, "residenc": 5})
        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_residenc() == 9

        uds_table["file.info.forms.json.residenc"] = 3
        assert attr._missingness_residenc() == 3

        uds_table["file.info.forms.json.residenc"] = None
        assert attr._missingness_residenc() == INFORMED_MISSINGNESS

    def test_missingness_maristat(self, uds_table):
        """Test missing MARISTAT - expect recode on 8 for V1/V2"""
        uds_table["file.info.forms.json"].update({"formver": 2.0, "maristat": 8})
        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_maristat() == 9

        uds_table["file.info.forms.json.maristat"] = 5
        assert attr._missingness_maristat() == 5

        uds_table["file.info.forms.json.maristat"] = None
        assert attr._missingness_maristat() == INFORMED_MISSINGNESS

    def test_missingness_raceaian(self, uds_table):
        """Test missing RACEAIAN - uses generic A1 missingness so applies to most
        of the other variables as well."""
        uds_table["file.info.forms.json"].update({"formver": "4.0", "raceaian": 1})
        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_raceaian() == 1

        uds_table["file.info.forms.json.raceaian"] = None
        assert attr._missingness_raceaian() == 0

        # pull from prev visit - if prev was -4 (likely older version),
        # should set to 0 for V4 and -4 for older versions
        uds_table["file.info.forms.json"].update({"packet": "I4", "raceaian": None})
        uds_table.update(
            {
                "_prev_record": {
                    "info": {
                        "forms": {"json": {"visitdate": "2020-01-01"}},
                        "resolved": {"raceaian": -4},
                    }
                }
            }
        )
        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_raceaian() == 0

        uds_table["file.info.forms.json.formver"] = 3.0
        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_raceaian() == INFORMED_MISSINGNESS

        # if prev visit actually set it, pull forward regardless of
        # version
        uds_table["_prev_record.info.resolved.raceaian"] = 1
        assert attr._missingness_raceaian() == 1
        uds_table["file.info.forms.json.formver"] = 4.0
        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_raceaian() == 1

    def test_educ_overwrite(self, uds_table):
        """Test missingness on EDUC where they enter something in an FVP
        form."""
        uds_table["file.info.forms.json"].update(
            {"formver": "4.0", "educ": 16, "packet": "I"}
        )
        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_educ() == 16

        # ensure it's set to prev value, NOT current value on FVP form
        uds_table["file.info.forms.json"].update(
            {"formver": "4.0", "educ": 5, "packet": "F"}
        )
        uds_table.update(
            {
                "_prev_record": {
                    "info": {
                        "forms": {"json": {"visitdate": "2020-01-01"}},
                        "resolved": {"educ": 13},
                    }
                }
            }
        )

        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_educ() == 13

    def test_dob_variables(self, uds_table):
        """Test BIRTHMO/BIRTHYR are pulled from working metadata first, not
        file data."""
        uds_table["file.info.forms.json"].update(
            {"formver": "4.0", "birthmo": 5, "birthyr": 2000}
        )
        uds_table.update(
            {
                "subject": {
                    "info": {
                        "working": {"cross-sectional": {"birthmo": 9, "birthyr": 1950}}
                    }
                }
            }
        )
        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_birthmo() == 9
        assert attr._missingness_birthyr() == 1950

        # if subject metadata is not there, then default to
        # file-level
        uds_table.pop("subject")
        attr = UDSFormA1Missingness(uds_table)
        assert attr._missingness_birthmo() == 5
        assert attr._missingness_birthyr() == 2000
