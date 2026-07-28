"""Tests UDS Form A3 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a3 import (
    UDSFormA3V4Missingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class TestUDSFormA3V4Missingness:
    def test_etpr(self, uds_table):
        """Test MOMETPR which basically tests all the ETPR variables."""
        attr = UDSFormA3V4Missingness(uds_table)
        assert attr._missingness_mometpr() == "-4"

        # from prev visit
        uds_table.update(
            {
                "_prev_record": {
                    "info": {
                        "forms": {"json": {"visitdate": "2020-01-01"}},
                        "resolved": {
                            "mometpr": "05",
                        },
                    }
                }
            }
        )
        uds_table["file.info.forms.json"].update(
            {
                "formver": 4,
                "packet": "F",
                "nwinfpar": "1",
                "mometpr": "66",  # should pull previous record
            }
        )
        attr = UDSFormA3V4Missingness(uds_table)
        assert attr._missingness_mometpr() == "05"

    def test_nwinf_gate(self, uds_table):
        """Test NWINFx correctly instructs that values are carried through."""
        # from prev visit
        uds_table.update(
            {
                "_prev_record": {
                    "info": {
                        "forms": {"json": {"visitdate": "2020-01-01"}},
                        "resolved": {
                            "mometpr": "10",
                        },
                    }
                }
            }
        )
        uds_table["file.info.forms.json"].update(
            {
                "formver": 4,
                "packet": "F",
                "nwinfpar": "0",  # will ignore current and pull through prev
                "mometpr": "12",
            }
        )

        attr = UDSFormA3V4Missingness(uds_table)
        assert attr._missingness_mometpr() == "10"

        # set newinfpar to 1, should now use current
        uds_table["file.info.forms.json.nwinfpar"] = "1"
        assert attr._missingness_mometpr() == "12"

    def test_no_prev_value(self, uds_table):
        """Test when the previous value was not actually provided; should use
        the default, not the prev missingness code."""
        # from prev visit
        uds_table.update(
            {
                "_prev_record": {
                    "info": {
                        "forms": {"json": {"visitdate": "2020-01-01"}},
                        "resolved": {
                            "kid2ago": -4,
                        },
                    }
                }
            }
        )
        uds_table["file.info.forms.json"].update(
            {
                "formver": 4,
                "packet": "F",
                "nwinfkid": "1",
                "kid2ago": "666",
            }
        )

        attr = UDSFormA3V4Missingness(uds_table)
        assert attr._missingness_kid2ago() == INFORMED_MISSINGNESS

    def test_prev_sibs_kids(self, uds_table):
        """Test SIBS/KIDS provided at previous vist."""
        # from prev visit
        uds_table.update(
            {
                "_prev_record": {
                    "info": {
                        "forms": {"json": {"visitdate": "2020-01-01"}},
                        "resolved": {"sibs": 2, "kids": "5"},
                    }
                }
            }
        )
        uds_table["file.info.forms.json"].update(
            {
                "formver": 4,
                "packet": "F",
                "nwinfsib": 0,
                "nwinfkid": "1",
                "sibs": 66,
                "kids": "66",
            }
        )

        attr = UDSFormA3V4Missingness(uds_table)
        assert attr._missingness_sibs() == 2
        assert attr._missingness_kids() == 5

    def test_sibs_kids(self, uds_table):
        """Test sibs/kids when not a previous visit."""
        attr = UDSFormA3V4Missingness(uds_table)
        assert attr._missingness_sibs() == INFORMED_MISSINGNESS
        assert attr._missingness_kids() == INFORMED_MISSINGNESS

        uds_table["file.info.forms.json"].update(
            {
                "packet": "I4",
                "sibs": 66,  # technically not allowed but will go through on curation
                "kids": "3",
            }
        )

        attr = UDSFormA3V4Missingness(uds_table)
        assert attr._missingness_sibs() == 66
        assert attr._missingness_kids() == 3

        # not V4
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3,
                "packet": "I",
                "sibs": None,
                "kids": "7",
            }
        )

        attr = UDSFormA3V4Missingness(uds_table)
        assert attr._missingness_sibs() == INFORMED_MISSINGNESS
        assert attr._missingness_kids() == 7
