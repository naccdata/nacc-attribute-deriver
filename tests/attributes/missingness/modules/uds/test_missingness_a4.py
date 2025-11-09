"""Tests UDS Form A4 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a4 import (
    UDSFormA4Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_BLANK


class TestUDSFormA4Missingness:
    def test_missingess_drugs_list(self, uds_table):
        """Test V1 - V3 where we have to map from a drugs list."""
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

        attr = UDSFormA4Missingness(uds_table)
        assert attr._missingness_rxnormid1() == INFORMED_BLANK
        assert attr._missingness_drug1() == "METOPROLOL"
        assert attr._missingness_drug2() == "AMILORIDE"
        assert attr._missingness_drug3() == "GLYBURIDE"
        assert attr._missingness_drug4() == "ISOSORBIDE MONONITRATE"
        assert attr._missingness_drug5() == "AMLODIPINE"
        assert attr._missingness_drug6() == INFORMED_BLANK
