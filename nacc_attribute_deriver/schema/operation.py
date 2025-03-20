"""Defines the operations to be performed on derived variables. Uses a
metaclass to keep track of operation types.

This kind of feels overengineered?
"""

from typing import Any, List

from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import datetime_from_form_date


class OperationException(Exception):
    pass


class OperationRegistry(type):
    operations: List["Operation"] = []

    def __init__(cls, name, bases, attrs):
        if name != "OperationRegistry" and cls.LABEL is not None:
            if name not in OperationRegistry.operations:
                OperationRegistry.operations.append(cls)


class Operation(object, metaclass=OperationRegistry):
    LABEL: str | None = None

    @classmethod
    def create(cls, label: str) -> "Operation":
        """Create the operation based on the label.

        Args:
            label: label of the operation
        """
        for op in OperationRegistry.operations:
            if op.LABEL == label:
                return op()  # type: ignore

        raise ValueError(f"Unrecognized operation: {label}")

    def evaluate(
        self, table: SymbolTable, value: Any, location: str, date_key: str, **kwargs
    ) -> None:
        """Evaluate the operation, and stores the computed value at the
        specified location.

        Args:
            table: Table to read/write from
            value: Value to perform the operation against
            location: Target location to write to
            date_key: Date key string
        """
        pass


class UpdateOperation(Operation):
    LABEL = "update"

    def evaluate(  # type: ignore
        self, table: SymbolTable, value: Any, location: str, **kwargs
    ) -> None:
        """Simply updates the location."""
        table[location] = value


class SetOperation(Operation):
    LABEL = "set"

    def evaluate(  # type: ignore
        self, table: SymbolTable, value: Any, location: str, **kwargs
    ) -> None:
        """Adds the value to a set, although it actually is saved as a list
        since the final output is a JSON."""
        cur_set = table.get(location)
        cur_set = set(cur_set) if cur_set else set()

        if isinstance(value, (list, set)):
            cur_set = cur_set.union(set(value))
        elif value is not None:
            cur_set.add(value)

        table[location] = list(cur_set)


class SortedListOperation(Operation):
    LABEL = "sortedlist"

    def evaluate(  # type: ignore
        self, table: SymbolTable, value: Any, location: str, **kwargs
    ) -> None:
        """Adds the value to a sorted list."""
        cur_list = table.get(location, [])

        if isinstance(value, (list, set)):
            cur_list.extend(list(value))
        elif value is not None:
            cur_list.append(value)

        table[location] = sorted(cur_list)


class DateOperation(Operation):
    LABEL: str | None = None

    def evaluate(
        self, table: SymbolTable, value: Any, location: str, date_key: str, **kwargs
    ) -> None:
        """Compares dates to determine the result."""
        try:
            cur_date = datetime_from_form_date(table.get(date_key))  # type: ignore
            dest_date = datetime_from_form_date(table.get(f"{location}.date"))  # type: ignore
        except ValueError as e:
            raise OperationException(
                f"Cannot parse date for date operation: {e}"
            ) from e

        if self.LABEL not in ["initial", "latest"]:
            raise OperationException(f"Unknown date operation: {self.LABEL}")

        if not cur_date:
            raise OperationException("Current date cannot be determined")

        if value is None:
            return

        if (
            not dest_date
            or (self.LABEL == "initial" and cur_date < dest_date)
            or (self.LABEL == "latest" and cur_date > dest_date)
        ):
            table[location] = {"date": str(cur_date.date()), "value": value}


class InitialOperation(DateOperation):
    LABEL = "initial"


class LatestOperation(DateOperation):
    LABEL = "latest"


class CountOperation(Operation):
    LABEL = "count"

    def evaluate(  # type: ignore
        self, table: SymbolTable, value: Any, location: str, **kwargs
    ) -> None:
        """Counts the result."""
        if not value:  # TODO: should we count 0s/Falses?
            return

        cur_count = table.get(location, 0)
        table[location] = cur_count + 1


class ComparisonOperation(Operation):
    LABEL: str | None = None

    def evaluate(  # type: ignore
        self, table: SymbolTable, value: Any, location: str, **kwargs
    ) -> None:
        """Does a comparison between the value and location value."""
        dest_value = table.get(location)

        if self.LABEL not in ["min", "max"]:
            raise OperationException(f"Unknown comparison operation: {self.LABEL}")

        if value is None:
            return

        try:
            if (
                not dest_value
                or (self.LABEL == "min" and value < dest_value)
                or (self.LABEL == "max" and value > dest_value)
            ):
                table[location] = value
        except TypeError as e:
            raise OperationException(
                f"Cannot compare types for {self.LABEL} operation: {e}"
            ) from e


class MinOperation(ComparisonOperation):
    LABEL = "min"


class MaxOperation(ComparisonOperation):
    LABEL = "max"
