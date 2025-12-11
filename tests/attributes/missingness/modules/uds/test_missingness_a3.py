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
        uds_table["file.info.forms.json.packet"] = "F"
        uds_table["file.info.forms.json.mometpr"] = "66"
        attr = UDSFormA3Missingness(uds_table)
        assert attr._missingness_mometpr() == "05"
