"""Tests for the attribute_type meta-methods for Operations to make sure they
match the types set by the operation."""

from datetime import date
from types import NoneType
from typing import List

import pytest
from nacc_attribute_deriver.attributes.base.namespace import DateTaggedValue
from nacc_attribute_deriver.schema.operation import (
    InitialOperation,
    LatestOperation,
    MinOperation,
    NoAssignment,
    OperationError,
    SetOperation,
    SortedListOperation,
    UpdateOperation,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class TestOperationAttributeType:
    def test_update(self):
        table = SymbolTable()
        operation = UpdateOperation()

        value = None
        operation.evaluate(table=table, value=value, attribute="empty")
        assert operation.attribute_type(type(value)) is type(table.get("empty"))

        value = "blah"
        operation.evaluate(table=table, value=value, attribute="string")
        assert operation.attribute_type(type(value)) is type(table.get("string"))

        value = "blah"
        wrapper = DateTaggedValue(date=date(year=2025, month=1, day=10), value=value)
        operation.evaluate(table=table, value=wrapper, attribute="date-tagged")
        assert operation.attribute_type(type(value)) is type(table.get("date-tagged"))

        value = date(year=2025, month=1, day=10)
        operation.evaluate(table=table, value=value, attribute="date")
        assert operation.attribute_type(type(value)) is type(table.get("date"))

    def test_set(self):
        """Tests the set operation.

        A couple things:
        - we have to deconstruct the value in the symbol table to test the types
          because a list object doesn't carry it's full type.
        - typing here assumes the rules are well-behaved in the sense of not
          adding different types to the same set.
        """
        table = SymbolTable()
        operation = SetOperation()

        value = None
        operation.evaluate(table=table, value=value, attribute="none-case")
        assert operation.attribute_type(type(value)) is List
        assert type(table.get("none-case")) is list

        value = "blah"
        operation.evaluate(table=table, value=value, attribute="single-value")
        assert operation.attribute_type(type(value)) is List[type(value)]
        assert type(table.get("single-value")[0]) is type(value)  # type: ignore

        value = "blah"
        wrapper = DateTaggedValue(date=date(year=2025, month=1, day=10), value=value)
        operation.evaluate(table=table, value=wrapper, attribute="date-tagged")
        assert operation.attribute_type(type(value)) is List[type(value)]
        assert type(table.get("date-tagged")[0]) is type(value)  # type: ignore

        value = "blah"
        wrapper = [value]
        operation.evaluate(table=table, value=wrapper, attribute="list-wrapped")
        assert operation.attribute_type(type(value)) is List[type(value)]
        assert type(table.get("list-wrapped")[0]) is type(value)  # type: ignore

    def test_sorted_list(self):
        """Tests the sorted list operation.

        A couple things:
        - we have to deconstruct the value in the symbol table to test the types
          because a list object doesn't carry it's full type.
        - typing here assumes the rules are well-behaved in the sense of not
          adding different types to the same list.
        """
        table = SymbolTable()
        operation = SortedListOperation()

        value = None
        operation.evaluate(table=table, value=value, attribute="none-case")
        assert operation.attribute_type(type(value)) is List
        assert type(table.get("none-case")) is list

        value = "blah"
        operation.evaluate(table=table, value=value, attribute="single-value")
        assert operation.attribute_type(type(value)) is List[type(value)]
        assert type(table.get("single-value")[0]) is type(value)  # type: ignore

        value = "blah"
        wrapper = DateTaggedValue(date=date(year=2025, month=1, day=10), value=value)
        operation.evaluate(table=table, value=wrapper, attribute="date-tagged")
        assert operation.attribute_type(type(value)) is List[type(value)]
        assert type(table.get("date-tagged")[0]) is type(value)  # type: ignore

        value = "blah"
        wrapper = [value]
        operation.evaluate(table=table, value=wrapper, attribute="list-wrapped")
        assert operation.attribute_type(type(value)) is List[type(value)]
        assert type(table.get("list-wrapped")[0]) is type(value)  # type: ignore

    def test_initial(self):
        table = SymbolTable()
        operation = InitialOperation()

        value = None
        operation.evaluate(table=table, value=value, attribute="none-case")
        assert operation.attribute_type(type(value)) is NoAssignment
        assert type(table.get("none-case")) is NoneType

        value = "blah"
        with pytest.raises(OperationError):
            operation.evaluate(table=table, value=value, attribute="single-value")
        assert operation.attribute_type(type(value)) is NoAssignment
        assert type(table.get("single-value")) is NoneType

        value = "blah"
        wrapper = DateTaggedValue(date=date(year=2025, month=1, day=10), value=value)
        assert type(wrapper) is DateTaggedValue
        operation.evaluate(table=table, value=wrapper, attribute="date-tagged")
        assert (
            operation.attribute_type(DateTaggedValue[str])
            is DateTaggedValue[type(value)]
        )
        assert type(table.get("date-tagged")["value"]) is type(value)  # type: ignore

        value = "blah"
        wrapper = [value]
        with pytest.raises(OperationError):
            operation.evaluate(table=table, value=wrapper, attribute="list-wrapped")
        assert operation.attribute_type(type(wrapper)) is NoAssignment
        assert type(table.get("list-wrapped")) is NoneType

    def test_latest(self):
        table = SymbolTable()
        operation = LatestOperation()

        value = None
        operation.evaluate(table=table, value=value, attribute="none-case")
        assert operation.attribute_type(type(value)) is NoAssignment
        assert type(table.get("none-case")) is NoneType

        value = "blah"
        with pytest.raises(OperationError):
            operation.evaluate(table=table, value=value, attribute="single-value")
        assert operation.attribute_type(type(value)) is NoAssignment
        assert type(table.get("single-value")) is NoneType

        value = "blah"
        wrapper = DateTaggedValue(date=date(year=2025, month=1, day=10), value=value)
        assert type(wrapper) is DateTaggedValue
        operation.evaluate(table=table, value=wrapper, attribute="date-tagged")
        assert (
            operation.attribute_type(DateTaggedValue[str])
            is DateTaggedValue[type(value)]
        )
        assert type(table.get("date-tagged")["value"]) is type(value)  # type: ignore

        value = "blah"
        wrapper = [value]
        with pytest.raises(OperationError):
            operation.evaluate(table=table, value=wrapper, attribute="list-wrapped")
        assert operation.attribute_type(type(wrapper)) is NoAssignment
        assert type(table.get("list-wrapped")) is NoneType

    def test_min(self):
        table = SymbolTable()
        operation = MinOperation()

        value = None
        operation.evaluate(table=table, value=value, attribute="none-case")
        assert operation.attribute_type(type(value)) is NoneType
        assert type(table.get("none-case")) is NoneType

        value = "blah"
        operation.evaluate(table=table, value=value, attribute="single-value")
        assert operation.attribute_type(type(value)) is str
        assert type(table.get("single-value")) is str

        value = "blah"
        wrapper = DateTaggedValue(date=date(year=2025, month=1, day=10), value=value)
        assert type(wrapper) is DateTaggedValue
        operation.evaluate(table=table, value=wrapper, attribute="date-tagged")
        assert operation.attribute_type(DateTaggedValue[type(value)]) is type(value)
        assert type(table.get("date-tagged")) is type(value)

        value = "blah"
        wrapper = [value]
        operation.evaluate(table=table, value=wrapper, attribute="list-wrapped")
        assert operation.attribute_type(List[type(value)]) is List[type(value)]
        assert type(table.get("list-wrapped")) is list
        assert type(table.get("list-wrapped")[0]) is type(value)  # type: ignore

    def test_max(self):
        table = SymbolTable()
        operation = MinOperation()

        value = None
        operation.evaluate(table=table, value=value, attribute="none-case")
        assert operation.attribute_type(type(value)) is NoneType
        assert type(table.get("none-case")) is NoneType

        value = "blah"
        operation.evaluate(table=table, value=value, attribute="single-value")
        assert operation.attribute_type(type(value)) is str
        assert type(table.get("single-value")) is str

        value = "blah"
        wrapper = DateTaggedValue(date=date(year=2025, month=1, day=10), value=value)
        assert type(wrapper) is DateTaggedValue
        operation.evaluate(table=table, value=wrapper, attribute="date-tagged")
        assert operation.attribute_type(DateTaggedValue[type(value)]) is type(value)
        assert type(table.get("date-tagged")) is type(value)

        value = "blah"
        wrapper = [value]
        operation.evaluate(table=table, value=wrapper, attribute="list-wrapped")
        assert operation.attribute_type(List[type(value)]) is List[type(value)]
        assert type(table.get("list-wrapped")) is list
        assert type(table.get("list-wrapped")[0]) is type(value)  # type: ignore
