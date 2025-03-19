"""Tests against the full schema end-to-end.

Mainly sanity checks to make sure modules run at all.
"""
from importlib.resources import files
from nacc_attribute_deriver.attribute_deriver import AttributeDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable


def test_minimal_uds_form():
    """Test against a minimal UDS form, mainly sanity check."""
    data = {
        'file': {
            'info': {
                'forms': {
                    'json': {
                        'visitdate': '2025-01-01',
                        'module': 'uds',
                        'birthmo': 1,
                        'birthyr': 1960,
                    }
                }
            }
        }
    }

    form = SymbolTable(data)
    rules_file = files(  # type: ignore
        "nacc_attribute_deriver").joinpath("config/form/uds_rules.csv")

    deriver = AttributeDeriver(date_key='file.info.forms.json.visitdate',
                               rules_file=rules_file)
    deriver.curate(form)


def test_minimal_np_form():
    """Test against an NP form."""
    form = SymbolTable()  # make a minimum UDS form
    form['file.info.forms.json.visitdate'] = '2025-01-01'
    form['file.info.forms.json.module'] = 'np'

    rules_file = files(  # type: ignore
        "nacc_attribute_deriver").joinpath("config/form/np_rules.csv")

    deriver = AttributeDeriver(date_key='file.info.forms.json.visitdate',
                               rules_file=rules_file)
    deriver.curate(form)
    assert form.to_dict() == {}
