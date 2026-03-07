"""Tests UDS Form A4 missingness attributes."""

import copy
import random
import pytest

from typing import Any, Dict

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a4 import (
    UDSFormA4Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_BLANK


@pytest.fixture(scope="function")
def drugs_table(uds_table) -> Dict[str, Any]:
    drugs_table = copy.deepcopy(uds_table)
    drugs_table["subject.info.working.longitudinal"] = {
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
    return drugs_table


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

    def test_missingness_anymeds(self, drugs_table, uds_table):
        """Test ANYMEDS is solely based on drugs list."""
        attr = UDSFormA4Missingness(drugs_table)
        drugs_table["file.info.forms.json.anymeds"] = random.choice([0, 2])
        assert attr._missingness_anymeds() == 1

        attr = UDSFormA4Missingness(uds_table)
        uds_table["file.info.forms.json.anymeds"] = 1
        assert attr._missingness_anymeds() == 0

    def test_missingness_rxnormid(self, uds_table):
        """Test RXNORMIDs are handled correctly, including when there are gaps
        in the order."""
        uds_table["file.info.forms.json"].update(
            {
                # three random rxnormids were filled, should
                # resolve to rxnormid1 - 5 in order
                "rxnormid1": "00000",
                "rxnormid15": "12345",
                "rxnormid18": "67890",
                "rxnormid37": "11111",
                "rxnormid40": "99999",
                "rxnormid41": "xxxxx",  # not valid
                "formver": 4,
            }
        )
        attr = UDSFormA4Missingness(uds_table)
        assert attr._missingness_rxnormid1() == "00000"
        assert attr._missingness_rxnormid2() == "12345"
        assert attr._missingness_rxnormid3() == "67890"
        assert attr._missingness_rxnormid4() == "11111"
        assert attr._missingness_rxnormid5() == "99999"
        assert attr._missingness_rxnormid6() == INFORMED_BLANK
        assert attr._missingness_rxnormid15() == INFORMED_BLANK
        assert attr._missingness_rxnormid18() == INFORMED_BLANK
        assert attr._missingness_rxnormid37() == INFORMED_BLANK
        assert attr._missingness_rxnormid40() == INFORMED_BLANK
