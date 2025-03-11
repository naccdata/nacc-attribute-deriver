"""CLI entrypoint for generating attribute schema.

nacc-attribute-deriver generate-schema -o outfile.json
"""
import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path

from nacc_attribute_deriver.attributes.attribute_map import generate_attribute_schema

log = logging.getLogger(__name__)


def run(args: Namespace):
    """Generate the attribute schema."""
    log.info(f"Writing schema to {args.outfile}")
    generate_attribute_schema(outfile=args.outfile, date_key=args.date_key)


def set_schema_generator_cli(parser: ArgumentParser):
    """Set up the Attribute Generation subparser.

    Args:
        parser: The ArgumentParser to add arguments to
    """
    # add arguments
    parser.add_argument('-o',
                        '--outfile',
                        dest="outfile",
                        type=Path,
                        required=True,
                        help='Output file to write schema to')
    parser.add_argument('-k',
                        '--date-key',
                        dest='date_key',
                        type=str,
                        required=False,
                        default='file.info.forms.json.visitdate',
                        help='Form field date key to use to order attributes')

    parser.set_defaults(run=run)
