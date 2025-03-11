"""CLI entrypoint for running regression tests.

This is very hacked together for the sake of testing - a more formalized
one should be done once we get better testing sources.
"""
import csv
import json
import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Dict, List, Optional

from nacc_attribute_deriver.attribute_deriver import AttributeDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable

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


def curate_row(deriver: AttributeDeriver,
               key: str,
               row: Dict[str, Any],
               baseline: Dict[str, Any],
               debug_outfile: Optional[Path] = None,
               update_form: bool = False) -> List[str]:
    """Curate the row's raw variables and compare against baseline To create
    the raw variables, merge row and baseline."""
    for group in [row, baseline]:
        for k, v in group.items():
            # hacky way to do type casting on CSV, just assume anything that looks
            # like an integer is supposed to be an integer
            try:
                group[k] = int(v) if v is not None else v
            except (TypeError, ValueError):
                try:
                    group[k] = float(v) if v is not None else v
                except (TypeError, ValueError):
                    pass

    if update_form:
        table = SymbolTable()
        table['file.info.forms.json'] = row
        # need to manually make visitdate and formver
        table['file.info.forms.json.visitdate'] = \
            f"{baseline['visityr']:02d}-{baseline['visitmo']:02d}-{baseline['visitday']:02d}"
        table['file.info.forms.json.formver'] = baseline['formver']
    else:
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
    if not args.input_csv and not args.input_json:
        raise ValueError("One of input CSV or input JSON must be provided")

    deriver = AttributeDeriver()
    with args.baseline_json.open('r') as fh:
        baselines = json.load(fh)

    log.info(f"Running regression test against {args.input_csv}")
    count = 0
    num_failed = 0
    errors = []

    # set up empty debug file
    if args.debug_outfile:
        with args.debug_outfile.open('w') as fh:
            json.dump({}, fh, indent=4)

    if args.input_csv:
        with args.input_csv.open('r') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                if args.num_records is not None and count >= args.num_records:
                    log.info(
                        f"Evaluated {args.num_records} records, stopping early"
                    )
                    break

                # ignore non-initial visits
                if row['packet'] != 'I':
                    continue

                count += 1
                naccid = row['naccid']
                visitdate = row[
                    'vstdate_a1']  # based off first form, should really get vistidate
                key = f"{naccid}_{visitdate}"
                if key not in baselines:
                    continue

                row_errors = curate_row(deriver, key, row, baselines[key],
                                        args.debug_outfile)
                errors.extend(row_errors)

                if row_errors:
                    num_failed += 1

    elif args.input_json:
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

                row_errors = curate_row(deriver,
                                        key,
                                        row,
                                        baselines[key],
                                        args.debug_outfile,
                                        update_form=False)
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
    parser.add_argument(
        '-i',
        '--input-csv',
        dest="input_csv",
        type=Path,
        required=False,
        help=
        'Input CSV to run regression test against; this or a JSON must be provided'
    )
    parser.add_argument(
        '-j',
        '--input-json',
        dest="input_json",
        type=Path,
        required=False,
        help=
        'Input JSON to run regression test against; this or a CSV must be provided'
    )

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
