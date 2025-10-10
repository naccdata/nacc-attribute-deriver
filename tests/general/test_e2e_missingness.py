"""Tests against the full schema end-to-end.

Mainly sanity checks to make sure modules run at all. Does not test UDS
due to its complexity/length.
"""

from nacc_attribute_deriver.attribute_deriver import MissingnessDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable


def test_uds_form(uds_table):
    """UDS is more of a runnable sanity check."""
    deriver = MissingnessDeriver(missingness_file="test_missingness.csv")
    deriver.curate(uds_table, "uds")

    assert uds_table['file.info.forms.missingness'] == {
        'npiqinf': -4,
        'npiqinfx': None
    }