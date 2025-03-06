"""Tests against the full schema end-to-end."""
import json
from pathlib import Path
from typing import Any

import pytest

from nacc_attribute_deriver.attribute_deriver import AttributeDeriver
from nacc_attribute_deriver.attributes.attribute_map import generate_attribute_schema
from nacc_attribute_deriver.symbol_table import SymbolTable

CUR_DIR = Path(__file__).resolve().parent
BASELINE_DIR = CUR_DIR / 'baseline'

UPDATE_BASELINES = False


@pytest.fixture(scope='function')
def tmp_dir():
    tmp_dir = CUR_DIR / 'tmp'
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir


def compare_baseline(baseline: Path, result: Any):
    """Compare against the baseline."""
    if UPDATE_BASELINES:
        with baseline.open('w') as fh:
            json.dump(result, fh, indent=4)

    with baseline.open('r') as fh:
        baseline = json.load(fh)
        assert result == baseline


def test_empty_form(tmp_dir):
    """Test against an empty form."""
    form = SymbolTable()  # make an empty form with date key
    form['file.info.forms.json.visitdate'] = '2025-01-01'

    schema_path = tmp_dir / 'schema.json'
    generate_attribute_schema(outfile=schema_path)

    with schema_path.open('r') as fh:
        schema = json.load(fh)

    compare_baseline(BASELINE_DIR / 'schema.json', schema)

    deriver = AttributeDeriver(schema=schema)
    deriver.curate(form)

    compare_baseline(BASELINE_DIR / 'empty_outfile.json', form.to_dict())


def test_full_form(tmp_dir):
    """Tests against a full form."""

    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "sex": 1,
                        "cdrglob": 0.5,
                        "visitdate": "2019-04-24",
                        "birthmo": 2,
                        "birthyr": 1980,
                        "primlang": 3,
                        "formver": 4.0,
                        "race": 3,
                        "normcog": 1,
                    }
                }
            }
        },
        "ncrad": {
            "info": {
                "raw": {
                    "apoe": 5
                }
            }
        },
        "niagads": {
            "info": {
                "raw": {
                    "niagads_gwas": "NG00000",
                    "niagads_exomechip": "NG00000",
                    "niagads_wgs": "0",
                    "niagads_wes": None
                }
            }
        }
    }
    form = SymbolTable(data)
    deriver = AttributeDeriver()
    deriver.curate(form)
    compare_baseline(BASELINE_DIR / 'full_form.json', form.to_dict())
