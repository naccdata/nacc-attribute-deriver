"""Defines the operations to be performed on derived variables. Uses a
metaclass to keep track of operation types.

This kind of feels overengineered?
"""

from abc import abstractmethod
from datetime import date
from typing import Any, Dict, Optional

from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import datetime_from_form_date


class OperationError(Exception):
    pass


class OperationRegistry(type):
    operations: Dict[str, type] = {}

    def __init__(cls, name, bases, attrs):
        if name != "OperationRegistry" and cls.LABEL is not None:
            if name not in OperationRegistry.operations:
                OperationRegistry.operations[cls.LABEL] = cls


class Operation(object, metaclass=OperationRegistry):
    LABEL: str | None = None

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
    def evaluate(
        self,
        *,
        table: SymbolTable,
        value: Any,
        attribute: str,
        date_key: Optional[str] = None,
    ) -> None:
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

    def evaluate(  # type: ignore
        self,
        *,
        table: SymbolTable,
        value: Any,
        attribute: str,
        date_key: Optional[str] = None,
    ) -> None:
        """Simply updates the location."""
        if isinstance(value, date):
            value = str(value)

        table[attribute] = value


class SetOperation(Operation):
    LABEL = "set"

    def evaluate(
        self,
        *,
        table: SymbolTable,
        value: Any,
        attribute: str,
        date_key: Optional[str] = None,
    ) -> None:
        """Adds the value to a set, although it actually is saved as a list
        since the final output is a JSON."""
        cur_set = table.get(attribute)
        cur_set = set(cur_set) if cur_set else set()

        if isinstance(value, (list, set)):
            cur_set = cur_set.union(set(value))
        elif value is not None:
            cur_set.add(value)

        table[attribute] = list(cur_set)


class SortedListOperation(Operation):
    LABEL = "sortedlist"

    def evaluate(
        self,
        *,
        table: SymbolTable,
        value: Any,
        attribute: str,
        date_key: Optional[str] = None,
    ) -> None:
        """Adds the value to a sorted list."""
        cur_list = table.get(attribute, [])

        if isinstance(value, (list, set)):
            cur_list.extend(list(value))
        elif value is not None:
            cur_list.append(value)

        table[attribute] = sorted(cur_list)


class DateOperation(Operation):
    LABEL: str | None = None

    @abstractmethod
    def compare(self, left_value, right_value) -> bool:
        """Returns the comparison for this object."""
        raise OperationError(f"Unknown date operation: {self.LABEL}")

    def evaluate(
        self,
        *,
        table: SymbolTable,
        value: Any,
        attribute: str,
        date_key: Optional[str] = None,
    ) -> None:
        """Compares dates to determine the result."""
        if value is None:
            return

        if not date_key:
            raise OperationError("Value for date_key is required")

        if self.LABEL not in ["initial", "latest"]:
            raise OperationError(f"Unknown date operation: {self.LABEL}")

        cur_date = datetime_from_form_date(table.get(date_key))
        dest_date = datetime_from_form_date(table.get(f"{attribute}.date"))

        if not cur_date:
            raise OperationError("Current date cannot be determined")

        if not dest_date or self.compare(cur_date, dest_date):
            table[attribute] = {"date": str(cur_date.date()), "value": value}


class InitialOperation(DateOperation):
    LABEL = "initial"

    def compare(self, left_value, right_value):
        return left_value < right_value


class LatestOperation(DateOperation):
    LABEL = "latest"

    def compare(self, left_value, right_value):
        return left_value > right_value


class CountOperation(Operation):
    LABEL = "count"

    def evaluate(
        self,
        *,
        table: SymbolTable,
        value: Any,
        attribute: str,
        date_key: Optional[str] = None,
    ) -> None:
        """Counts the result."""
        if not value:  # TODO: should we count 0s/Falses?
            return

        cur_count = table.get(attribute, 0)
        table[attribute] = cur_count + 1


class ComparisonOperation(Operation):
    LABEL: str | None = None

    @abstractmethod
    def compare(self, left_value, right_value) -> bool:
        """Returns the comparison for this object."""
        raise OperationError(f"Unknown comparison operation: {self.LABEL}")

    def evaluate(
        self,
        *,
        table: SymbolTable,
        value: Any,
        attribute: str,
        date_key: Optional[str] = None,
    ) -> None:
        """Does a comparison between the value and location value."""
        dest_value = table.get(attribute)

        if self.LABEL not in ["min", "max"]:
            raise OperationError(f"Unknown comparison operation: {self.LABEL}")

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

    def compare(self, left_value, right_value):
        return left_value < right_value


class MaxOperation(ComparisonOperation):
    LABEL = "max"

    def compare(self, left_value, right_value):
        return left_value > right_value
