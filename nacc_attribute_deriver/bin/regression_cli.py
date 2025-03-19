"""CLI entrypoint for running regression tests.

This is very hacked together for the sake of testing - a more formalized
one should be done once we get better testing sources.
"""
import json
import logging
from argparse import ArgumentParser, Namespace
from importlib.resources import files
from pathlib import Path
from typing import Any, Dict, List, Optional

from nacc_attribute_deriver.attribute_deriver import AttributeDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable

log = logging.getLogger(__name__)

# hack for now
SKIP_VALUES = [
    #"naccdage",  # needs NP/MDS data
    "naccapoe",  # needs apoe data
    "ngdsgwas",  # needs niagads data
    "ngdsexom",
    "ngdswgs",
    "ngdswes",
    "naccnorm",  # relies on multiple visits
]


def curate_row(deriver: AttributeDeriver,
               key: str,
               row: Dict[str, Any],
               baseline: Dict[str, Any],
               debug_outfile: Optional[Path] = None) -> List[str]:
    """Curate the row's raw variables and compare against baseline To create
    the raw variables, merge row and baseline."""
    for k, v in baseline.items():
        # hacky way to do type casting from CSV, just assume anything that looks
        # like an integer is supposed to be an integer
        try:
            baseline[k] = int(v) if v is not None else v
        except (TypeError, ValueError):
            try:
                baseline[k] = float(v) if v is not None else v
            except (TypeError, ValueError):
                pass

    table = SymbolTable(row)
    deriver.curate(table)
    errors = []

    # assert derived variables are as expected
    for k, v in table['file.info.derived'].items():  # type: ignore
        if k not in baseline:
            raise ValueError(f"Derived variable {k} not found in baseline, " +
                             "possible typo?")

        if k in SKIP_VALUES:
            continue

        if baseline[k] != v:
            errors.append(f"Record {key} derived variable {k} does " +
                          f"not match: baseline {baseline[k]} vs computed {v}")

    if errors and debug_outfile:
        data = None
        if debug_outfile:
            with debug_outfile.open('r') as fh:
                data = json.load(fh)

        if not data:
            data = {}

        if debug_outfile:
            with debug_outfile.open('w') as fh:
                data[key] = {'raw': row, 'baseline': baseline}
                json.dump(data, fh, indent=4)

    return errors


def run(args: Namespace):
    """Generate the attribute schema."""
    rules_file = files(  # type: ignore
        "nacc_attribute_deriver").joinpath("config/form/uds_rules.csv")
    deriver = AttributeDeriver(rules_file=rules_file,
                               date_key='file.info.forms.json.visitdate')
    with args.baseline_json.open('r') as fh:
        baselines = json.load(fh)

    count = 0
    num_failed = 0
    errors = []

    # set up empty debug file
    if args.debug_outfile:
        with args.debug_outfile.open('w') as fh:
            json.dump({}, fh, indent=4)

    log.info(f"Running regression test against {args.input_json}")
    with args.input_json.open('r') as fh:
        data = json.load(fh)
        for row in data:
            count += 1
            naccid = row['file']['info']['forms']['json'][  # type: ignore
                'naccid']  # type: ignore
            visitdate = row['file']['info']['forms'][  # type: ignore
                'json'][  # type: ignore
                    'visitdate']  # type: ignore
            key = f"{naccid}_{visitdate}"
            if key not in baselines:
                log.warning(f"{key} not found in baseline")
                continue

            row_errors = curate_row(deriver, key, row, baselines[key],
                                    args.debug_outfile)
            errors.extend(row_errors)

            if row_errors:
                num_failed += 1

    if errors:
        log.error('\n'.join(errors))

    log.info(f"Tested {count} records, {num_failed} failed")


def set_regression_cli(parser: ArgumentParser):
    """Set up the regression testing subparser.

    Args:
        parser: The ArgumentParser to add arguments to
    """
    # add arguments
    parser.add_argument('-i',
                        '--input-json',
                        dest="input_json",
                        type=Path,
                        required=True,
                        help='Input JSON to run regression test against')

    parser.add_argument(
        '-b',
        '--baseline-json',
        dest="baseline_json",
        type=Path,
        required=True,
        help='Baseline JSON containing map of NACCIDs to NACC derived variables'
    )
    parser.add_argument(
        '-n',
        '--num_records',
        dest="num_records",
        type=int,
        required=False,
        default=None,
        help='Number of records to test against; defaults to all')
    parser.add_argument(
        '-d',
        '--debug-outfile',
        dest="debug_outfile",
        type=Path,
        required=False,
        default=None,
        help=
        'File to write record to for debugging. Writes to stdout if not specified'
    )

    parser.set_defaults(run=run)
