"""
CLI entrypoint for running regression tests
"""
import copy
import csv
import json
import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Dict, List

from nacc_attribute_deriver.attribute_deriver import AttributeDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.attributes.attribute_map import generate_attribute_schema

log = logging.getLogger(__name__)

# hack for now
SKIP_VALUES = [
    "naccdage",  # needs NP/MDS data
    "naccapoe",  # needs apoe data
    "ngdsgwas",  # needs niagads data
    "ngdsexom",
    "ngdswgs",
    "ngdswes",
    "naccnorm",  # relies on multiple visits
]


def curate_row(deriver: AttributeDeriver, key: str, row: Dict[str, Any], baseline: Dict[str, Any], debug_outfile: Path = None) -> List[str]:
    """Curate the row's raw variables and compare against baseline
    To create the raw variables, merge row and baseline.
    """
    table = SymbolTable()

    raw_vars = {}
    derived_vars = {}
    # map missing row -> baseline


    for group in [row, baseline]:
        for k, v in group.items():
            # hacky way to do type casting, just assume anything that looks like an integer
            # is supposed to be an integer
            try:
                group[k] = int(v) if v is not None else v
            except (TypeError, ValueError):
                try:
                    group[k] = float(v) if v is not None else v
                except (TypeError, ValueError):
                    pass

    table['file.info.forms.json'] = row
    # need to manually make visitdate and formver
    table['file.info.forms.json.visitdate'] = \
        f"{baseline['visityr']:02d}-{baseline['visitmo']:02d}-{baseline['visitday']:02d}"
    table['file.info.forms.json.formver'] = baseline['formver']
    deriver.curate(table)

    errors = []
    debug = None

    # assert derived variables are as expected
    for k, v in table['file.info.derived'].items():
        if k not in baseline:
            raise ValueError(
                f"Derived variable {k} not found in baseline, " +
                "possible typo?"
            )

        if k in SKIP_VALUES:
            continue

        if baseline[k] != v:
            errors.append(
                f"Record {key} derived variable {k} does " +
                f"not match: baseline {baseline[k]} vs computed {v}"
            )

    if errors and debug_outfile:
        data = None
        if debug_outfile.is_file():
            with debug_outfile.open('r') as fh:
                data = json.load(fh)

        if not data:
            data = {}

        with debug_outfile.open('w') as fh:
            data[key] = {'raw': row, 'baseline': baseline}
            json.dump(data, fh, indent=4)

    return errors


def run(args: Namespace):
    """Generate the attribute schema"""
    deriver = AttributeDeriver()
    with args.baseline_json.open('r') as fh:
        baselines = json.load(fh)

    log.info(f"Running regression test against {args.input_csv}")
    count = 0
    errors = []

    # set up empty debug file
    with args.debug_outfile.open('w') as fh:
        json.dump({}, fh, indent=4)

    with args.input_csv.open('r') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if args.num_records is not None and count >= args.num_records:
                log.info(f"Evaluated {args.num_records} records, stopping early")
                break

            # ignore non-initial visits
            if row['packet'] != 'I':
                continue

            count += 1
            naccid = row['naccid']
            visitdate = row['vstdate_a1']  # based off first form, should really get vistidate
            key = f"{naccid}_{visitdate}"
            if key not in baselines:
                log.warning(f"{key} not found in baseline")
                continue

            errors.extend(curate_row(deriver, key, row, baselines[key], args.debug_outfile))

        log.info(f"Tested {count} records")

    if errors:
        raise ValueError('\n'.join(errors))


def set_regression_cli(parser: ArgumentParser):
    """Set up the regression testing subparser

    Args:
        parser: The ArgumentParser to add arguments to
    """
    # add arguments
    parser.add_argument('-i', '--input-csv', dest="input_csv", type=Path, required=True,
                        help='Input CSV to run regression test against')
    parser.add_argument('-b', '--baseline-json', dest="baseline_json", type=Path, required=True,
                        help='Baseline JSON containing map of NACCIDs to NACC derived variables')
    parser.add_argument('-n', '--num_records', dest="num_records", type=int, required=False,
                        default=None,
                        help='Number of records to test against; defaults to all')
    parser.add_argument('-o', '--debug-outfile', dest="debug_outfile", type=Path, required=False,
                        default=None,
                        help='File to write record to for debugging. Writes to stdout if not specified')

    parser.set_defaults(run=run)
