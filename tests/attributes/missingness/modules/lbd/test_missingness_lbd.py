"""Tests LBD missingness attributes."""

import random
import pytest

from nacc_attribute_deriver.attributes.missingness.modules.lbd.missingness_lbd_prev_visit import (
    LBDFormPrevVisitMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
    INFORMED_MISSINGNESS_FLOAT,
)


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
        lbd_table['file.info.forms.json.lbanxage'] = 777
        assert attr._missingness_lbanxage() == 999

        # something in working, set to value
        lbd_table['subject.info.working.cross-sectional.lbanxage'] = 65
        assert attr._missingness_lbanxage() == 65
