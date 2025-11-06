"""Tests against the full schema end-to-end.

Mainly sanity checks to make sure modules run at all.
"""

from nacc_attribute_deriver.attribute_deriver import MissingnessDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable


def test_uds_form(uds_table):
    """Test UDS."""
    deriver = MissingnessDeriver(missingness_file="test_missingness.csv")

    uds_table["file.info.forms.json"].update({"height": "53.1", "heigdec": "5"})

    deriver.curate(uds_table, "uds")

    assert uds_table["file.info.resolved"] == {
        "npiqinf": -4,
        "npiqinfx": None,
        "height": 53.6,
    }


def test_np_form():
    """Test NP."""
    np_table = SymbolTable(
        {
            "file": {
                "info": {"forms": {"json": {"visitdate": "2020-01-01", "formver": 11}}}
            }
        }
    )
    deriver = MissingnessDeriver(missingness_file="test_missingness.csv")
    deriver.curate(np_table, "np")

    assert np_table["file.info.resolved"] == {"npsex": -4, "nppmih": -4}
