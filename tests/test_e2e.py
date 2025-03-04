"""
Tests against the full schema.

TODO: make this more refined, mostly just setting this up
to make sure the module runs at all.
"""
import json
import pytest

from pathlib import Path

from nacc_attribute_deriver.attributes.attribute_map import (
    generate_attribute_schema
)
from nacc_attribute_deriver import AttributeDeriver, SymbolTable

CUR_DIR = Path(__file__).resolve().parent

def test_full_schema():
    tmp_dir = CUR_DIR / 'tmp'
    tmp_dir.mkdir(parents=True, exist_ok=True)

    schema_path = tmp_dir / 'schema.json'
    generate_attribute_schema(outfile=schema_path)

    with schema_path.open('r') as fh:
        schema = json.load(fh)

    form = SymbolTable()  # make an empty form
    # add date key
    form['file.info.forms.json.visitdate'] = '2025-01-01'

    deriver = AttributeDeriver(schema=schema)

    deriver.curate(form)

    outfile = tmp_dir / 'outfile.json'
    with outfile.open('w') as fh:
        json.dump(form.to_dict(), fh, indent=4)
