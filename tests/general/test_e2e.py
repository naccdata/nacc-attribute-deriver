"""Tests against the full schema end-to-end."""
from nacc_attribute_deriver.attribute_deriver import AttributeDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable


def test_minimal_uds_form():
    """Test against an empty form; mainly a sanity check to make sure the
    module runs at all."""
    form = SymbolTable()  # make a minimum UDS form
    form['file.info.forms.json.visitdate'] = '2025-01-01'
    form['file.info.forms.json.module'] = 'uds'
    form['file.info.raw'] = {}

    deriver = AttributeDeriver(date_key='file.info.forms.json.visitdate')
    deriver.curate(form)
