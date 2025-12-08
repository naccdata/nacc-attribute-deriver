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

        # -4 cases
        assert attr._missingness_npinf1a() == INFORMED_MISSINGNESS
        np_table["file.info.forms.json.npinf"] = 0
        assert attr._missingness_npinf1a() == INFORMED_MISSINGNESS

        # 88 case
        np_table["file.info.forms.json.npinf"] = 8
        assert attr._missingness_npinf1a() == 88

        # 99 case
        np_table["file.info.forms.json.npinf"] = 9
        assert attr._missingness_npinf1a() == 99

    def test_recode_10b(self, np_table):
        """Tests the recode_10b logic."""
        attr = NPMissingness(np_table)

        # -4.4 cases
        assert attr._missingness_npinf4f() == INFORMED_MISSINGNESS_FLOAT
        np_table["file.info.forms.json.npinf"] = 0
        assert attr._missingness_npinf4f() == INFORMED_MISSINGNESS_FLOAT

        # 99 case
        np_table["file.info.forms.json.npinf"] = 9
        assert attr._missingness_npinf4f() == 99.9
        np_table["file.info.forms.json.npinf"] = None
        np_table["file.info.forms.json.npinf4a"] = 99
        assert attr._missingness_npinf4f() == 99.9

        # 88 case, solely based on gates
        np_table["file.info.forms.json.npinf"] = 8
        assert attr._missingness_npinf4f() == 88.8
        np_table["file.info.forms.json.npinf"] = None
        np_table["file.info.forms.json.npinf4a"] = random.choice([88, 0])
        assert attr._missingness_npinf4f() == 88.8

        # 88 case, based on gate compared to num_infarcts
        np_table["file.info.forms.json.npinf"] = 1
        np_table["file.info.forms.json.npinf4a"] = random.choice([None, 3, 4])
        assert attr._missingness_npinf4f() == INFORMED_MISSINGNESS_FLOAT
        np_table["file.info.forms.json.npinf4a"] = random.choice([1, 2])
        assert attr._missingness_npinf4f() == 88.8
