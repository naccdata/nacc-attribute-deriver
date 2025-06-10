"""Defines the operations to be performed on derived variables.

Uses a metaclass to keep track of operation types.
"""

from abc import abstractmethod
from datetime import date
from types import FunctionType
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Tuple,
    TypeAlias,
    Union,
    get_args,
    get_origin,
)

from nacc_attribute_deriver.attributes.base.namespace import DateTaggedValue
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import datetime_from_form_date


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


class OperationError(Exception):
    pass


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

        raise ValueError(f"Unrecognized operation: {label}")

    @abstractmethod
    def evaluate(self, *, table: SymbolTable, value: Any, attribute: str) -> None:
        """Evaluate the operation, and stores the computed value at the
        specified location.

        Args:
            table: Table to read/write from
            value: Value to perform the operation against
            attribute: Target location to write to
            date_key: Date key string
        """
        pass


class UpdateOperation(Operation):
    LABEL = "update"

    @classmethod
    def attribute_type(cls, expression_type: type) -> type:
        return get_date_tagged_type(get_optional_type(expression_type))

    def evaluate(  # type: ignore
        self, *, table: SymbolTable, value: Any, attribute: str
    ) -> None:
        """Simply updates the location."""

        if isinstance(value, DateTaggedValue):
            value = value.value  # type: ignore
        if value is None:
            return

        if isinstance(value, date):
            value = str(value)

        table[attribute] = value


class SetOperation(Operation):
    LABEL = "set"

    @classmethod
    def attribute_type(cls, expression_type: type) -> type:
        element_type: TypeAlias = get_list_type(  # type: ignore
            get_date_tagged_type(get_optional_type(expression_type))
        )
        return List[element_type]

    def evaluate(self, *, table: SymbolTable, value: Any, attribute: str) -> None:
        """Adds the value to a set, although it actually is saved as a list
        since the final output is a JSON."""
        if isinstance(value, DateTaggedValue):
            value = value.value  # type: ignore

        cur_set = table.get(attribute)  # type: ignore
        cur_set = set(cur_set) if cur_set else set()

        if isinstance(value, (list, set)):
            cur_set = cur_set.union(set(value))
        elif value is not None:
            cur_set.add(value)

        # sorts just for consistency
        table[attribute] = sorted(list(cur_set))


class SortedListOperation(Operation):
    LABEL = "sortedlist"

    @classmethod
    def attribute_type(cls, expression_type: type) -> type:
        element_type: TypeAlias = get_list_type(  # type: ignore
            get_date_tagged_type(get_optional_type(expression_type))
        )
        return List[element_type]

    def evaluate(self, *, table: SymbolTable, value: Any, attribute: str) -> None:
        """Adds the value to a sorted list."""
        if isinstance(value, DateTaggedValue):
            value = value.value  # type: ignore

        cur_list = table.get(attribute, [])
        if isinstance(value, (list, set)):
            cur_list.extend(list(value))  # type: ignore
        elif value is not None:
            cur_list.append(value)

        table[attribute] = sorted(cur_list)


class DateOperation(Operation):
    LABEL: str | None = None

    @abstractmethod
    def compare(self, left_value: date, right_value: date) -> bool:
        """Returns the comparison for this object."""
        raise OperationError(f"Unknown date operation: {self.LABEL}")

    @classmethod
    def attribute_type(cls, expression_type: type) -> type:
        temp_type = get_optional_type(expression_type)
        if hasattr(temp_type, "__pydantic_generic_metadata__"):
            origin = temp_type.__pydantic_generic_metadata__["origin"]  # type: ignore
            if origin is DateTaggedValue:
                return temp_type

        return NoAssignment

    def evaluate(
        self, *, table: SymbolTable, value: DateTaggedValue[Any] | Any, attribute: str
    ) -> None:
        """Compares dates to determine the result."""
        if value is None:
            return

        if not isinstance(value, DateTaggedValue):
            raise OperationError(
                f"Unable to perform {self.LABEL} operation without date"
            )

        if value.value is None:  # type: ignore
            return

        if self.LABEL not in ["initial", "latest"]:
            raise OperationError(f"Unknown date operation: {self.LABEL}")

        if not value.date:
            raise OperationError(f"Current date is required: {value.model_dump()}")

        dest_date = datetime_from_form_date(table.get(f"{attribute}.date"))

        if not dest_date or self.compare(value.date, dest_date.date()):
            table[attribute] = value.model_dump()


class InitialOperation(DateOperation):
    LABEL = "initial"

    def compare(self, left_value: date, right_value: date):
        return left_value <= right_value


class LatestOperation(DateOperation):
    LABEL = "latest"

    def compare(self, left_value: date, right_value: date):
        return left_value >= right_value


class ComparisonOperation(Operation):
    LABEL: str | None = None

    @abstractmethod
    def compare(self, left_value, right_value) -> bool:
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

    def evaluate(self, *, table: SymbolTable, value: Any, attribute: str) -> None:
        """Does a comparison between the value and location value."""
        dest_value = table.get(attribute)

        if self.LABEL not in ["min", "max"]:
            raise OperationError(f"Unknown comparison operation: {self.LABEL}")

        if isinstance(value, DateTaggedValue):
            value = value.value
        if value is None:
            return

        try:
            if not dest_value or self.compare(value, dest_value):
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

    def compare(self, left_value, right_value):
        return left_value < right_value


class MaxOperation(ComparisonOperation):
    LABEL = "max"

    def compare(self, left_value, right_value):
        return left_value > right_value
