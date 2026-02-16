"""Tests NP missingness attributes."""

import random
import pytest

from nacc_attribute_deriver.attributes.missingness.modules.np.missingness_np import (
    NPMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
    INFORMED_MISSINGNESS_FLOAT,
)


@pytest.fixture(scope="function")
def np_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "adcid": "0",
                        "formver": 10,
                        "module": "NP",
                        "visitdate": "2025-01-10",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


class TestNPMissingness:
    def test_recode_10a(self, np_table):
        """Tests the recode_10a logic."""
        attr = NPMissingness(np_table)
        assert attr._missingness_npinf1a() == INFORMED_MISSINGNESS

        # V10/V11: -4 cases
        np_table["file.info.forms.json.npinf"] = 0
        assert attr._missingness_npinf1a() == INFORMED_MISSINGNESS

        # V10/V11: 88 case
        np_table["file.info.forms.json.npinf"] = 8
        assert attr._missingness_npinf1a() == 88

        # V10/V11: 99 case
        np_table["file.info.forms.json.npinf"] = 9
        assert attr._missingness_npinf1a() == 99

        # V1-9: default case
        np_table["file.info.forms.json.formver"] = random.choice([1, 7, 8, 9])
        np_table["file.info.forms.json.npinf"] = None
        assert attr._missingness_npinf1a() == INFORMED_MISSINGNESS

        # any version; set to something case
        np_table["file.info.forms.json.formver"] = random.choice([1, 7, 8, 9, 10, 11])
        np_table["file.info.forms.json.npinf1a"] = 3
        assert attr._missingness_npinf1a() == 3

    def test_recode_10b(self, np_table):
        """Tests the recode_10b logic"""
        attr = NPMissingness(np_table)
        assert attr._missingness_npinf4f() == INFORMED_MISSINGNESS_FLOAT

        # V10/v11: -4.4 cases
        np_table["file.info.forms.json.npinf"] = 0
        assert attr._missingness_npinf4f() == INFORMED_MISSINGNESS_FLOAT

        # V10/V11: 99 case
        np_table["file.info.forms.json.npinf"] = 9
        assert attr._missingness_npinf4f() == 99.9
        np_table["file.info.forms.json.npinf"] = None
        np_table["file.info.forms.json.npinf4a"] = 99
        assert attr._missingness_npinf4f() == 99.9

        # V10/V11: 88 case, solely based on gates
        np_table["file.info.forms.json.npinf"] = 8
        assert attr._missingness_npinf4f() == 88.8
        np_table["file.info.forms.json.npinf"] = None
        np_table["file.info.forms.json.npinf4a"] = random.choice([88, 0])
        assert attr._missingness_npinf4f() == 88.8

        # V10/V11: 88 case, based on gate compared to num_infarcts
        np_table["file.info.forms.json.npinf"] = 1
        np_table["file.info.forms.json.npinf4a"] = random.choice([None, 3, 4])
        assert attr._missingness_npinf4f() == INFORMED_MISSINGNESS_FLOAT
        np_table["file.info.forms.json.npinf4a"] = random.choice([1, 2])
        assert attr._missingness_npinf4f() == 88.8

        # V1-9: Only really care about gate value is None or not
        np_table["file.info.forms.json.formver"] = random.choice([1, 7, 8, 9])
        np_table["file.info.forms.json.npinf4a"] = None
        assert attr._missingness_npinf4f() == INFORMED_MISSINGNESS_FLOAT

        # valid case for any version, make sure decimal is handled correctly
        np_table["file.info.forms.json"].update({
            "formver": random.choice([1, 7, 8, 9, 10, 11]),
            "npinf": None,
            "npinf4a": None,
            "npinf4f": 5,
            "npinf4g": 2
        })
        assert attr._missingness_npinf4f() == 5.2

        # test value is set to 88.8 even if decimal is bad
        np_table["file.info.forms.json"].update({
            "formver": random.choice([1, 7, 8, 9, 10, 11]),
            "npinf": None,
            "npinf4a": None,
            "npinf4f": 88,
            "npinf4g": 0
        })
        assert attr._missingness_npinf4f() == 88.8

    def test_recode_10c(self, np_table):
        """Tests the recode_10c logic"""
        attr = NPMissingness(np_table)
        assert attr._missingness_nphemo2() == INFORMED_MISSINGNESS

        # V10/V11: 8/9 cases
        np_table["file.info.forms.json.nphemo"] = 8
        assert attr._missingness_nphemo2() == 8
        np_table["file.info.forms.json.nphemo"] = 9
        assert attr._missingness_nphemo2() == 9

        # V10/V11: 0 case
        np_table["file.info.forms.json.nphemo"] = 0
        assert attr._missingness_nphemo2() == INFORMED_MISSINGNESS

        # any version, something is set case
        np_table["file.info.forms.json.formver"] = random.choice([1, 7, 8, 9, 10, 11])
        np_table["file.info.forms.json.nphemo2"] = 6
        assert attr._missingness_nphemo2() == 6


    def test_nppmih(self, np_table):
        """Test the NPPMIH decimal case."""
        attr = NPMissingness(np_table)

        # -4.4 cases
        assert attr._missingness_nppmih() == INFORMED_MISSINGNESS_FLOAT

        # NPPMIH value only
        np_table["file.info.forms.json.nppmih"] = 3.1
        assert attr._missingness_nppmih() == 3.1
        np_table["file.info.forms.json.nppmih"] = 7
        assert attr._missingness_nppmih() == 7

        # with NPPMIM
        np_table["file.info.forms.json.nppmih"] = 9
        np_table["file.info.forms.json.nppmim"] = 7
        assert attr._missingness_nppmih() == 9.7

    def test_np_headers(self, np_table):
        """Test NP headers."""
        attr = NPMissingness(np_table)

        assert attr._missingness_np_adcid() == 0
        assert attr._missingness_np_formver() == 10.0
        assert attr._missingness_np_visitdate() == "2025-01-10"

        # test when form uses npformdate instead of visitdate
        np_table["file.info.forms.json.visitdate"] = None
        np_table["file.info.forms.json.npformdate"] = "09/28/2025"

        attr = NPMissingness(np_table)
        assert attr._missingness_np_adcid() == 0
        assert attr._missingness_np_formver() == 10.0
        assert attr._missingness_np_visitdate() == "2025-09-28"
