"""Tests UDS Form A2 attributes."""

import pytest
import random
from nacc_attribute_deriver.attributes.derived.modules.uds.form_a2 import (
    UDSFormA2Attribute,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table(uds_table) -> SymbolTable:
    """Create dummy base table."""
    uds_table["file.info.forms.json"].update(
        {"packet": "T", "newinf": "0", "invisits": "3", "incalls": "6", "a2sub": 0}
    )
    return uds_table


class TestUDSFormA2Attribute:
    def test_create_naccninr_longitudinally(self, table):
        """Test NACCNINR over longitudinal values."""
        # V3 and earlier
        attr = UDSFormA2Attribute(table)
        # not submitted/newinf != 1, no previous value to carry forward
        assert attr._create_naccninr() == INFORMED_MISSINGNESS

        # newinf != 1 and carry forward from previous visit
        table["_prev_record.info"] = {
            "forms": {"json": {"visitdate": "2020-01-01"}},
            "derived": {"naccninr": 3},
        }
        attr = UDSFormA2Attribute(table)
        assert attr._create_naccninr() == 3

        # newinf = 1, so generate
        table["file.info.forms.json.a2sub"] = 1
        table["file.info.forms.json.newinf"] = 1
        assert attr._create_naccninr() == 99

        # assert -4 for V4
        table["file.info.forms.json.formver"] = 4.0
        attr = UDSFormA2Attribute(table)
        assert attr._create_naccninr() == INFORMED_MISSINGNESS

    def test_create_naccincntfq(self, table):
        """Tests NACCINCNTFQ."""
        # not submitted
        attr = UDSFormA2Attribute(table)
        assert attr._create_naccninr() == INFORMED_MISSINGNESS

        # V3 and earlier, min of INVISITS and INCALLS
        table["file.info.forms.json.a2sub"] = 1
        attr = UDSFormA2Attribute(table)
        assert attr._create_naccincntfq() == 3
        table["file.info.forms.json.incalls"] = 1
        assert attr._create_naccincntfq() == 1

        # test one or both missing
        table["file.info.forms.json"].update(
            {
                "invisits": None,
            }
        )
        assert attr._create_naccincntfq() == INFORMED_MISSINGNESS
        table["file.info.forms.json"].update({"incalls": None})
        assert attr._create_naccincntfq() == INFORMED_MISSINGNESS

        # V4
        table["file.info.forms.json"].update(
            {"formver": "4.0", "inlivwth": "1", "modea2": random.choice([1, 2])}
        )
        attr = UDSFormA2Attribute(table)
        assert attr._create_naccincntfq() == 8

        table["file.info.forms.json"].update({"inlivwth": "0", "incntfrq": "6"})
        assert attr._create_naccincntfq() == 6

        # not submitted
        table["file.info.forms.json.modea2"] = 0
        assert attr._create_naccincntfq() == INFORMED_MISSINGNESS
