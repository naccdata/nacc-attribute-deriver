"""Tests UDS Form A3 missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_a3 import (
    UDSFormA3Missingness,
)


class TestUDSFormA3Missingness:
    def test_etpr(self, uds_table):
        """Test MOMETPR which basically tests all the ETPR variables."""
        attr = UDSFormA3Missingness(uds_table)
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
        attr = UDSFormA3Missingness(uds_table)
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

        attr = UDSFormA3Missingness(uds_table)
        assert attr._missingness_mometpr() == "10"

        # set newinfpar to 1, should now use current
        uds_table["file.info.forms.json.nwinfpar"] = "1"
        assert attr._missingness_mometpr() == "12"
