"""Tests COVID missingness attributes."""

from nacc_attribute_deriver.attributes.missingness.modules.covid.missingness_covid import (  # noqa: E501
    CovidFormMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class TestCovidMissingness:
    def test_fixing_test_year(self):
        """Test C19TxYR variables get fixed."""
        table = SymbolTable(
            {
                "file": {
                    "info": {
                        "forms": {
                            "json": {
                                "visitdate": "2020-01-01",
                                "c19t1yr": 99,
                                "c19t2yr": "88",
                                "c19t3yr": "2019",
                            }
                        }
                    }
                }
            }
        )

        attr = CovidFormMissingness(table)

        assert attr._missingness_c19t1yr() == 9999
        assert attr._missingness_c19t2yr() == 8888
        assert attr._missingness_c19t3yr() == 2019
