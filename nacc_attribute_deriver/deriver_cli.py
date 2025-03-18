"""CLI for attribute deriver.

Currently just used to generate current attributes schema.
"""
import logging
from argparse import ArgumentParser

from .bin.regression_cli import set_regression_cli

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def entrypoint():
    parser = ArgumentParser(prog="NACC Attribute Deriver")

    parser.add_argument('--debug',
                        dest="debug",
                        action='store_true',
                        help='Set logging mode to debug')

    # set subparsers
    subparsers = parser.add_subparsers(dest='action',
                                       required=True,
                                       help='Action to run')

    # regression testing
    regression = subparsers.add_parser('run-regression',
                                       help="Run regression testing")
    set_regression_cli(regression)

    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    args.run(args)


if __name__ == "__main__":
    entrypoint()
