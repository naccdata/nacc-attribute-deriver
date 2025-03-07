"""
CLI for attribute deriver

Currently just used to generate current attributes schema.
"""
import logging
from argparse import ArgumentParser

from .bin.schema_generator_cli import set_schema_generator_cli
from .bin.regression_cli import set_regression_cli

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('niagads_gwas_data_transfer')

def entrypoint():
    parser = ArgumentParser(prog="NACC Attribute Deriver")

    parser.add_argument('--debug', dest="debug", action='store_true',
                        help='Set logging mode to debug')

    # set subparsers
    subparsers = parser.add_subparsers(dest='action', required=True, help='Action to run')

    # attribute schema generator
    schema_generator = subparsers.add_parser('generate-schema', help='Generate attribute schema')
    set_schema_generator_cli(schema_generator)

    # regression testing
    regression = subparsers.add_parser('run-regression', help="Run regression testing")
    set_regression_cli(regression)

    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    args.run(args)

if __name__ == "__main__":
    entrypoint()
