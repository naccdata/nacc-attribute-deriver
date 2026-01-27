"""Tests LBD missingness attributes."""

import pytest

from nacc_attribute_deriver.attributes.missingness.modules.lbd.missingness_lbd_prev_visit import (  # noqa: E501
    LBDFormPrevVisitMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


@pytest.fixture(scope="function")
def lbd_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "formver": 3.1,
                        "module": "LBD",
                        "visitdate": "2025-01-10",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


class TestLBDMissingness:
    def test_prev_visit(self, lbd_table):
        """Test 999 is returned if 777 references something invalid."""
        attr = LBDFormPrevVisitMissingness(lbd_table)

        # nothing in prev visit, return 999
        lbd_table["file.info.forms.json.lbanxage"] = 777
        assert attr._missingness_lbanxage() == 999

        # something in working, set to value
        lbd_table["subject.info.working.cross-sectional.lbanxage"] = 65
        assert attr._missingness_lbanxage() == 65

        # 0 prev code case
        lbd_table["file.info.forms.json.sccofrst"] = 0
        assert attr._missingness_sccofrst() == INFORMED_MISSINGNESS
        lbd_table["subject.info.working.cross-sectional.sccofrst"] = 2
        assert attr._missingness_sccofrst() == 2

    def test_range_enforced(self, lbd_table):
        """Test ranges are enforced."""
        attr = LBDFormPrevVisitMissingness(lbd_table)

        # just random fields for testing, they all call the same method
        # anyways
        lbd_table["file.info.forms.json.sccoagen"] = 120
        assert attr._missingness_sccoagen() == 110

        lbd_table["file.info.forms.json.lbdage2"] = 7
        assert attr._missingness_lbdage2() == 15

        lbd_table["file.info.forms.json.lbsagetr"] = 3
        assert attr._missingness_lbsagetr() == 9

        # Nones get defaulted to 999
        lbd_table["file.info.forms.json.lbpsyage"] = None
        assert attr._missingness_lbpsyage() == 999
