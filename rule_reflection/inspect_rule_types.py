from csv import DictReader
from importlib import resources
from inspect import signature
from typing import Union, get_args, get_origin

from pydantic import ValidationError

from nacc_attribute_deriver import config
from nacc_attribute_deriver.attributes.attribute_collection import (
    AttributeCollectionRegistry,
)
from nacc_attribute_deriver.schema.schema import RuleFileModel


def type_string(type_object: type) -> str:
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
    def __init__(self, wrapped_type: type) -> None:
        self.wrapped_type = wrapped_type

    def __str__(self) -> str:
        return type_string(self.wrapped_type)

    def is_optional(self) -> bool:
        return get_origin(self.wrapped_type) is Union and type(None) in get_args(
            self.wrapped_type
        )


def main():
    instance_collections = AttributeCollectionRegistry.get_attribute_methods()
    rules_file = resources.files(config).joinpath("curation_rules.csv")
    with rules_file.open("r") as file_stream:
        reader = DictReader(file_stream)
        if not reader.fieldnames:
            print("whoa. no fieldnames")

        print("attribute,attribute_type,operation,expression,expression_type")
        for row in reader:
            try:
                rule_schema = RuleFileModel.model_validate(row)
            except ValidationError as error:
                print(error)
                continue

            # location, operation, type
            expression = instance_collections.get(f"create_{rule_schema.function}")
            if not expression:
                continue
            sig = signature(expression.function)
            return_type = sig.return_annotation
            expression_type = TypeWrapper(return_type)
            operation = rule_schema.assignment.operation
            attribute_type = TypeWrapper(operation.attribute_type(return_type))

            print(
                f"{rule_schema.location},{attribute_type},{rule_schema.operation},{rule_schema.function},{expression_type}"
            )


if __name__ == "__main__":
    main()
