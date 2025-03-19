"""Tests against the full schema end-to-end.

Mainly sanity checks to make sure modules run at all.
"""
from importlib.resources import files
from nacc_attribute_deriver.attribute_deriver import AttributeDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable


def test_uds_form():
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

    deriver = AttributeDeriver(rules_file=rules_file,
                               date_key='file.info.forms.json.visitdate')
    deriver.curate(form)
    # UDS has too much data/is messy to do a direct comparison


def test_np_form():
    """Test against a minimal NP form - all derived variables should be 9 with no data."""
    form = SymbolTable()
    form['file.info.forms.json.visitdate'] = '2025-01-01'
    form['file.info.forms.json.module'] = 'np'

    rules_file = files(  # type: ignore
        "nacc_attribute_deriver").joinpath("config/form/np_rules.csv")

    deriver = AttributeDeriver(rules_file=rules_file,
                               date_key='file.info.forms.json.visitdate',)
    deriver.curate(form)
    assert form.to_dict() == {
        'file': {
            'info': {
                'forms': {
                    'json': {
                        'visitdate': '2025-01-01',
                        'module': 'np'
                    }
                },
                'derived': {
                    'naccarte': 9,
                    'naccbraa': 9,
                    'nacchem': 9,
                    'nacclewy': 9,
                    'naccmicr': 9,
                    'naccneur': 9
                }
            }
        }
    }


def test_ncrad_apoe():
    """Test against NCRAD APOE, which just derives APOE."""
    form = SymbolTable()
    form['file.info.raw'] = {"a1": "E4", "a2": "E2"}
    rules_file = files(  # type: ignore
        "nacc_attribute_deriver").joinpath("config/genetics/ncrad_rules.csv")

    deriver = AttributeDeriver(rules_file=rules_file)
    deriver.curate(form)
    assert form.to_dict() == {
        'file': {
            'info': {
                'raw': {
                    'a1': 'E4',
                    'a2': 'E2'
                },
                'derived': {
                    'naccapoe': 5
                }
            }
        },
        'subject': {
            'info': {
                'genetics': {
                    'apoe': 'e4,e2'
                }
            }
        }
    }


def test_niagads_investigator():
    """Test against NIAGADS investigator data."""
    form = SymbolTable()
    form['file.info.raw'] = {
        'niagads_gwas': "NG00000",
        'niagads_exomechip': "NG00000, NG00001",
        'niagads_wgs': "0",
        'niagads_wes': None
    }
    rules_file = files(  # type: ignore
        "nacc_attribute_deriver").joinpath("config/genetics/niagads_rules.csv")

    deriver = AttributeDeriver(rules_file=rules_file)
    deriver.curate(form)
    assert form.to_dict() == {
        'file': {
            'info': {
                'raw': {
                    'niagads_gwas': "NG00000",
                    'niagads_exomechip': "NG00000, NG00001",
                    'niagads_wgs': "0",
                    'niagads_wes': None
                },
                'derived': {
                    'ngdsgwas': 1,
                    'ngdsexom': 1,
                    'ngdswgs': 0,
                    'ngdswes': 0
                }
            }
        },
        'subject': {
            'info': {
                'genetics': {
                    'ngdsgwas': True,
                    'ngdsexom': True,
                    'ngdswgs': False,
                    'ngdswes': False
                }
            }
        }
    }
