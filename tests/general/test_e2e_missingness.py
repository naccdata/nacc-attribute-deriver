"""Tests against the full schema end-to-end.

Mainly sanity checks to make sure modules run at all. Does not test UDS
fully due to its complexity/length.
"""

from nacc_attribute_deriver.attribute_deriver import MissingnessDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable


def test_uds_form(uds_table):
    """UDS is more of a runnable sanity check."""
    deriver = MissingnessDeriver(missingness_file="test_missingness.csv")
    deriver.curate(uds_table, "uds")

    assert uds_table["file.info.resolved"] == {"npiqinf": -4, "npiqinfx": None}


def test_np_form():
    """Test against a minimal NP form - all derived variables
    should be 9 with no data.
    """
    np_table = SymbolTable(
        {"file": {"info": {"forms": {"json": {"visitdate": "2020-01-01"}}}}}
    )
    deriver = MissingnessDeriver(missingness_file="test_missingness.csv")
    deriver.curate(np_table, "np")

    assert np_table["file.info.resolved"] == {"npsex": -4, "nppmih": -4}
