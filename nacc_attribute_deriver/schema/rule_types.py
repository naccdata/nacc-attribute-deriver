"""Methods for handling rule types."""

import datetime
from typing import (
    Generic,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel, ConfigDict, field_serializer


T = TypeVar("T")


class NoAssignment:
    pass


class DateTaggedValue(BaseModel, Generic[T]):
    """Model for a date-tagged attribute value."""

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    date: datetime.date
    value: T

    @field_serializer("date")
    def serialize_date_as_str(self, date: datetime.date):
        return str(date)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, DateTaggedValue):
            return False

        return self.date <= other.date


class TypeGetter:
    @classmethod
    def get_optional_type(cls, expression_type: type) -> type:
        origin = get_origin(expression_type)
        args = get_args(expression_type)
        if origin is Union and type(None) in args:
            return args[0]
        return expression_type

    @classmethod
    def get_list_type(cls, expression_type: type) -> type:
        origin = get_origin(expression_type)
        if origin is list:
            return get_args(expression_type)[0]
        return expression_type

    @classmethod
    def is_date_tagged_type(cls, expression_type: type) -> bool:
        if hasattr(expression_type, "__pydantic_generic_metadata__"):
            origin = expression_type.__pydantic_generic_metadata__["origin"]  # type: ignore
            return origin is DateTaggedValue

        return False

    @classmethod
    def get_date_tagged_type(cls, expression_type: type) -> type:
        if cls.is_date_tagged_type(expression_type):
            args = expression_type.__pydantic_generic_metadata__[  # type: ignore
                "args"
            ]  # type: ignore
            return args[0]  # type: ignore
        return expression_type

    @classmethod
    def get_date_str_type(cls, expression_type: type) -> type:
        if expression_type is datetime.date:
            return str
        return expression_type

    @classmethod
    def get_optional_date_tagged_type(cls, expression_type: type) -> type:
        return cls.get_date_tagged_type(cls.get_optional_type(expression_type))
