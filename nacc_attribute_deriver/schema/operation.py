"""Defines the operations to be performed on derived variables.

Uses a metaclass to keep track of operation types.
"""

import datetime
from abc import abstractmethod
from types import FunctionType, NoneType
from typing import (
    Any,
    ClassVar,
    Dict,
    Generic,
    List,
    Tuple,
    TypeAlias,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel, ConfigDict, ValidationError, field_serializer

from nacc_attribute_deriver.attributes.base.namespace import T
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import datetime_from_form_date

from .errors import OperationError


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


class NoAssignment:
    pass


def get_optional_type(expression_type: type) -> type:
    origin = get_origin(expression_type)
    args = get_args(expression_type)
    if origin is Union and type(None) in args:
        return args[0]
    return expression_type


def get_list_type(expression_type: type) -> type:
    origin = get_origin(expression_type)
    if origin is list:
        return get_args(expression_type)[0]
    return expression_type


def get_date_tagged_type(expression_type: type) -> type:
    if hasattr(expression_type, "__pydantic_generic_metadata__"):
        origin = expression_type.__pydantic_generic_metadata__["origin"]  # type: ignore
        if origin is DateTaggedValue:
            args = expression_type.__pydantic_generic_metadata__[  # type: ignore
                "args"
            ]  # type: ignore
            return args[0]  # type: ignore
    return expression_type


def get_date_str_type(expression_type: type) -> type:
    if expression_type is datetime.date:
        return str
    return expression_type


class OperationRegistry(type):
    operations: ClassVar[Dict[str, type]] = {}

    def __init__(
        cls, name: str, bases: Tuple[type], attrs: Dict[str, str | FunctionType]
    ):
        """Registers the class in the registry when the class has this class as
        a metaclass."""
        if (
            name != "OperationRegistry"
            and cls.LABEL is not None  # type: ignore
            and name not in OperationRegistry.operations
        ):
            OperationRegistry.operations[cls.LABEL] = cls  # type: ignore


class Operation(object, metaclass=OperationRegistry):
    LABEL: str | None = None

    @classmethod
    def attribute_type(cls, expression_type: type) -> type:
        """Returns the type assigned to the attribute by this operation."""
        return NoAssignment

    @classmethod
    def create(cls, label: str) -> "Operation":
        """Create the operation based on the label.

        Args:
            label: label of the operation
        """
        operation = OperationRegistry.operations.get(label, None)
        if operation:
            return operation()

        raise OperationError(f"Unrecognized operation: {label}")

    @abstractmethod
    def evaluate(
        self, *, table: SymbolTable, value: DateTaggedValue[Any] | Any, attribute: str
    ) -> None:
        """Evaluate the operation, and stores the computed value at the
        specified location.

        Args:
            table: Table to read/write from
            value: Value to perform the operation against
            attribute: Target location to write to
        """
        pass


class UpdateOperation(Operation):
    LABEL = "update"

    @classmethod
    def attribute_type(cls, expression_type: type) -> type:
        return get_date_str_type(
            get_date_tagged_type(get_optional_type(expression_type))
        )

    def evaluate(
        self, *, table: SymbolTable, value: DateTaggedValue[Any] | Any, attribute: str
    ) -> None:
        """Simply updates the location."""
        if value is None:
            return
        elif isinstance(value, datetime.date):
            value = str(value)
        elif isinstance(value, DateTaggedValue):
            if value.value is None:
                return
            value = value.model_dump()

        table[attribute] = value


class ListOperation(Operation):
    LABEL = "list"

    @classmethod
    def attribute_type(cls, expression_type: type) -> type:
        element_type: TypeAlias = get_list_type(  # type: ignore
            get_date_tagged_type(get_optional_type(expression_type))
        )

        return List[element_type] if element_type is not NoneType else List

    def add_to_list(
        self, *, table: SymbolTable, value: DateTaggedValue[Any] | Any, attribute: str
    ) -> List[Any]:
        """Handles the current list - insert order is retained."""
        cur_list = table.get(attribute, [])
        if not isinstance(cur_list, list):
            raise OperationError(
                f"Attempting to perform list operation on non-list attribute: {attribute}")

        # try converting any dicts to DateTaggedValues so list can be sorted
        for i, item in enumerate(cur_list):
            if isinstance(item, dict):
                try:
                    cur_list[i] = DateTaggedValue(**item)
                except ValidationError:
                    pass

        if isinstance(value, (list, set)):
            cur_list.extend(list(value))  # type: ignore
        elif value is not None:
            cur_list.append(value)

        return cur_list

    def serialize(self, *, table: SymbolTable, attribute: str) -> None:
        """Serialize - may need to be done after sorting."""
        cur_list = table.get(attribute)
        if not isinstance(cur_list, list):
            return

        for i, item in enumerate(cur_list):
            if isinstance(item, DateTaggedValue):
                cur_list[i] = item.model_dump()

        table[attribute] = cur_list

    def evaluate(
        self, *, table: SymbolTable, value: DateTaggedValue[Any] | Any, attribute: str
    ) -> None:
        """Adds the value to list - insert order is retained."""
        cur_list = self.add_to_list(table=table, value=value, attribute=attribute)
        table[attribute] = cur_list
        self.serialize(table=table, attribute=attribute)


class SortedListOperation(ListOperation):
    LABEL = "sortedlist"

    def evaluate(
        self, *, table: SymbolTable, value: DateTaggedValue[Any] | Any, attribute: str
    ) -> None:
        """Adds the value to a sorted list."""
        cur_list = self.add_to_list(table=table, value=value, attribute=attribute)
        try:
            table[attribute] = sorted(cur_list)
        except TypeError as e:
            raise OperationError(f"Cannot sort mixed types for {self.LABEL}: {e}")

        self.serialize(table=table, attribute=attribute)


class SetOperation(ListOperation):
    LABEL = "set"

    def evaluate(
        self, *, table: SymbolTable, value: DateTaggedValue[Any] | Any, attribute: str
    ) -> None:
        """Adds the value to a set, although it actually is saved as a list
        since the final output is a JSON.

        Attempts to sort if hashable.
        """
        cur_list = self.add_to_list(table=table, value=value, attribute=attribute)
        try:
            table[attribute] = sorted(list(set(cur_list)))
        except TypeError as e:
            raise OperationError(f"Cannot sort mixed types for {self.LABEL}: {e}")

        self.serialize(table=table, attribute=attribute)


class DateMapOperation(Operation):
    LABEL = "datemap"

    def evaluate(
        self, *, table: SymbolTable, value: DateTaggedValue[Any] | Any, attribute: str
    ) -> None:
        """Adds the value to mapping where the key is the date and mapped to a
        DateTaggedValue.

        Having the nested DateTaggedValue is a little redundant with the
        key, but done so that pulled values can easily be casted back as
        a DateTaggedValue as needed.
        """
        if value.value is None:
            return

        if not isinstance(value, DateTaggedValue):
            raise OperationError(
                f"Unable to perform {self.LABEL} operation without date"
            )

        cur_map = table.get(attribute, {})
        cur_map[str(value.date)] = value.model_dump()
        table[attribute] = cur_map


class DateOperation(Operation):
    LABEL: str | None = None

    @abstractmethod
    def compare(self, left_value: datetime.date, right_value: datetime.date) -> bool:
        """Returns the comparison for this object."""
        raise OperationError(f"Unknown date operation: {self.LABEL}")

    @classmethod
    def attribute_type(cls, expression_type: type) -> type:
        temp_type: TypeAlias = get_date_tagged_type(get_optional_type(expression_type))  # type: ignore
        if temp_type is not expression_type:
            return DateTaggedValue[temp_type]

        return NoAssignment

    def evaluate(
        self, *, table: SymbolTable, value: DateTaggedValue[Any] | Any, attribute: str
    ) -> None:
        """Compares dates to determine the result."""
        if value is None:
            return None

        if not isinstance(value, DateTaggedValue):
            raise OperationError(
                f"Unable to perform {self.LABEL} operation without date"
            )

        if value.value is None:  # type: ignore
            return

        if self.LABEL not in ["initial", "latest"]:
            raise OperationError(f"Unknown date operation: {self.LABEL}")

        dest_date = datetime_from_form_date(table.get(f"{attribute}.date"))

        if not dest_date or self.compare(value.date, dest_date.date()):
            table[attribute] = value.model_dump()


class InitialOperation(DateOperation):
    LABEL = "initial"

    def compare(self, left_value: datetime.date, right_value: datetime.date):
        return left_value <= right_value


class LatestOperation(DateOperation):
    LABEL = "latest"

    def compare(self, left_value: datetime.date, right_value: datetime.date):
        return left_value >= right_value


class ComparisonOperation(Operation):
    LABEL: str | None = None

    @abstractmethod
    def compare(self, left_value: Any, right_value: Any) -> bool:
        """Returns the comparison for this object."""
        raise OperationError(f"Unknown comparison operation: {self.LABEL}")

    @classmethod
    def attribute_type(cls, expression_type: type) -> type:
        temp_type = get_optional_type(expression_type)
        if hasattr(temp_type, "__pydantic_generic_metadata__"):
            origin = temp_type.__pydantic_generic_metadata__["origin"]  # type: ignore
            if origin is DateTaggedValue:
                args = temp_type.__pydantic_generic_metadata__[  # type: ignore
                    "args"
                ]  # type: ignore
                return args[0]  # type: ignore

        return temp_type

    def evaluate(
        self, *, table: SymbolTable, value: DateTaggedValue[Any] | Any, attribute: str
    ) -> None:
        """Does a comparison between the value and location value."""
        if self.LABEL not in ["min", "max"]:
            raise OperationError(f"Unknown comparison operation: {self.LABEL}")

        dest_value = table.get(attribute)
        if isinstance(dest_value, dict):
            try:
                dest_value = DateTaggedValue(**dest_value).value
            except ValidationError as e:
                raise OperationError(
                    f"Cannot use comparison operator on dict (from {attribute})"
                ) from e

        raw_value = value.value if isinstance(value, DateTaggedValue) else value
        if raw_value is None:
            return

        try:
            if not dest_value or self.compare(raw_value, dest_value):
                if isinstance(value, DateTaggedValue):
                    value = value.model_dump()

                table[attribute] = value
        except TypeError as error:
            raise OperationError(
                f"Cannot compare types for {self.LABEL} operation: {error}"
            ) from error


class MinOperation(ComparisonOperation):
    LABEL = "min"

    @classmethod
    def attribute_type(cls, expression_type: type) -> type:
        return super().attribute_type(expression_type)

    def compare(self, left_value: Any, right_value: Any) -> bool:
        return left_value < right_value


class MaxOperation(ComparisonOperation):
    LABEL = "max"

    def compare(self, left_value: Any, right_value: Any) -> bool:
        return left_value > right_value
