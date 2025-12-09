"""Tests UDS Form A4 missingness attributes."""

import pytest

from typing import Any, Dict

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a4 import (
    UDSFormA4Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_BLANK


@pytest.fixture(scope="function")
def drugs_table(uds_table) -> Dict[str, Any]:
    uds_table["subject.info.working.longitudinal"] = {
        "drugs-list": [
            # add multiple to make sure it maps to the right one
            {"date": "2000-01-01", "value": []},
            {
                "date": "2025-01-01",
                "value": ["d00134", "d00169", "d00248", "d00269", "d00689"],
            },
            {"date": "2025-12-12", "value": []},
        ]
    }
    return uds_table


class TestUDSFormA4Missingness:
    def test_missingess_drugs_name(self, drugs_table):
        """Test V1 - V3 where we have to map from a drugs list."""
        attr = UDSFormA4Missingness(drugs_table)
        assert attr._missingness_rxnormid1() == INFORMED_BLANK
        assert attr._missingness_drug1() == "METOPROLOL"
        assert attr._missingness_drug2() == "AMILORIDE"
        assert attr._missingness_drug3() == "GLYBURIDE"
        assert attr._missingness_drug4() == "ISOSORBIDE MONONITRATE"
        assert attr._missingness_drug5() == "AMLODIPINE"
        assert attr._missingness_drug6() == INFORMED_BLANK

    def test_missingess_drugs_id(self, drugs_table):
        """Test V1 - V3 where we have to map the IDs from a drugs list."""
        attr = UDSFormA4Missingness(drugs_table)
        assert attr._missingness_rxnormid1() == INFORMED_BLANK
        assert attr._missingness_drug_id1() == "d00134"
        assert attr._missingness_drug_id2() == "d00169"
        assert attr._missingness_drug_id3() == "d00248"
        assert attr._missingness_drug_id4() == "d00269"
        assert attr._missingness_drug_id5() == "d00689"
        assert attr._missingness_drug_id6() == INFORMED_BLANK
