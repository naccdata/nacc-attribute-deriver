"""Computes the types of derived attributes."""

import argparse
import logging
import sys
from csv import DictReader, DictWriter
from importlib import resources
from inspect import signature
from typing import List, Union, get_args, get_origin

from pydantic import BaseModel, ValidationError

from nacc_attribute_deriver import config
from nacc_attribute_deriver.attributes.attribute_collection import (
    AttributeCollectionRegistry,
)
from nacc_attribute_deriver.schema.operation import DateTaggedValue
from nacc_attribute_deriver.schema.schema import RuleFileModel

log = logging.getLogger(__name__)


def type_string(type_object: type) -> str:
    """Returns the type as a string.

    Args:
      type_object: the type
    Returns:
      the type as a string
    """
    if type_object is type(None):
        return "None"

    if hasattr(type_object, "__pydantic_generic_metadata__"):
        origin = type_object.__pydantic_generic_metadata__["origin"]  # type: ignore
        args = type_object.__pydantic_generic_metadata__["args"]  # type: ignore
    else:
        origin = get_origin(type_object)
        args = get_args(type_object)

    if not origin:
        return type_object.__name__

    if origin is Union and type(None) in args:
        str_args = [type_string(arg) for arg in args if arg is not type(None)]  # type: ignore
        return f"Optional[{', '.join(str_args)}]"

    str_args = [type_string(arg) for arg in args]  # type: ignore
    return f"{origin.__name__}[{', '.join(str_args)}]"  # type: ignore


class TypeWrapper:
    """Wrapper for a type."""

    def __init__(self, wrapped_type: type) -> None:
        self.wrapped_type = wrapped_type

    def __str__(self) -> str:
        return type_string(self.wrapped_type)

    def is_optional(self) -> bool:
        """Indicates whether this type is optional."""

        return get_origin(self.wrapped_type) is Union and type(None) in get_args(
            self.wrapped_type
        )


class RuleType(BaseModel):
    attribute: str
    attribute_type: str
    operation: str
    expression: str
    expression_type: str


def parse_arguments():
    parser = argparse.ArgumentParser(description="list source attributes in data model")
    parser.add_argument("--output", "-o", help="path to save output file")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    output_file = args.output if args.output else "rule-types.csv"

    instance_collections = AttributeCollectionRegistry.get_attribute_methods()
    rules_file = resources.files(config).joinpath("curation_rules.csv")
    with rules_file.open("r") as file_stream:
        reader = DictReader(file_stream)
        if not reader.fieldnames:
            log.error("Expecting fieldnames in rules file.")
            sys.exit(1)

        rule_types: List[RuleType] = []
        for row in reader:
            try:
                rule_schema = RuleFileModel.model_validate(row)
            except ValidationError as error:
                log.error("Rule validation error: %s", str(error))
                continue

            # location, operation, type
            expression = instance_collections.get(f"create_{rule_schema.function}")
            if not expression:
                continue

            return_type = signature(expression.function).return_annotation
            rule_types.append(
                RuleType(
                    attribute=rule_schema.location,
                    attribute_type=str(
                        TypeWrapper(
                            rule_schema.assignment.operation.attribute_type(
                                return_type
                                if not rule_schema.dated
                                else DateTaggedValue[return_type]  # type: ignore
                            )
                        )
                    ),
                    operation=rule_schema.operation,
                    expression=rule_schema.function,
                    expression_type=str(TypeWrapper(return_type)),
                )
            )

        with open(output_file, "w", encoding="utf-8") as out_file:
            fieldnames = [
                "attribute",
                "attribute_type",
                "operation",
                "expression",
                "expression_type",
            ]
            writer = DictWriter(out_file, fieldnames=fieldnames)
            writer.writeheader()
            for rule_type in rule_types:
                writer.writerow(rule_type.model_dump())


if __name__ == "__main__":
    main()
