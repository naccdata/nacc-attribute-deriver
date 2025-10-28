"""Tests base namespaces."""

from datetime import date
import pytest

from nacc_attribute_deriver.attributes.namespace.namespace import (
    BaseNamespace,
    INVALID_TEXT,
    PreviousRecordNamespace,
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.schema.rule_types import DateTaggedValue
from nacc_attribute_deriver.symbol_table import SymbolTable


class TestBaseNamespace:
    def test_get_value(self):
        """Tests getting value."""
        table = SymbolTable()
        table["test.value"] = 5
        table["some.other.prefix.value"] = 10

        namespace = BaseNamespace(table=table, attribute_prefix="test.")
        assert namespace.get_value("value", int) == 5
        assert namespace.get_value("missing", int) is None
        assert namespace.get_value("missing", str, default="default") == "default"

    def test_group_attributes(self):
        """Test grouping attributes."""
        table = SymbolTable({"test": {"var1": "1", "var2": "2", "var3": "3"}})

        namespace = BaseNamespace(table=table, attribute_prefix="test.")
        assert namespace.group_attributes(["var1", "var2", "var3"], int) == [1, 2, 3]

    def test_invalid_string(self):
        """Tests invalid string values return as None."""
        table = SymbolTable()
        attr = BaseNamespace(table=table, attribute_prefix="test.")

        for value in INVALID_TEXT:
            table["test.value"] = value
            assert attr.get_value("value", int) is None


class TestSubjectDerivedNamespace:
    def test_get_longitudinal_value(self):
        """Test getting a longitudinal value."""
        table = SymbolTable(
            {
                "subject": {
                    "info": {
                        "derived": {
                            "longitudinal": {
                                "var": [
                                    {"date": "2021-01-01", "value": 1},
                                    {"date": "2022-01-01", "value": "2"},
                                    {"date": "2023-01-01", "value": 3},
                                ]
                            }
                        }
                    }
                }
            }
        )

        namespace = SubjectDerivedNamespace(table=table)
        result = namespace.get_longitudinal_value("var", int)
        assert len(result) == 3
        for i, date_value in enumerate(result):
            assert isinstance(date_value, DateTaggedValue)
            assert str(date_value.date) == f"202{i + 1}-01-01"
            assert date_value.value == i + 1

        assert namespace.get_prev_value("var", int) == 3

    def test_get_cross_sectional_value(self):
        """Test getting a cross sectional value."""
        table = SymbolTable(
            {
                "subject": {
                    "info": {
                        "derived": {
                            "cross-sectional": {
                                "var": 5,
                                "dated-var": {"date": "2025-01-01", "value": "8"},
                            }
                        }
                    }
                }
            }
        )

        namespace = SubjectDerivedNamespace(table=table)
        assert namespace.get_cross_sectional_value("var", int) == 5
        assert namespace.get_cross_sectional_dated_value("dated-var", int).date == date(
            2025, 1, 1
        )
        assert namespace.get_cross_sectional_dated_value("dated-var", int).value == 8


@pytest.fixture(scope="function")
def prev_record() -> SymbolTable:
    """Create dummy data and return it in a table."""
    data = {
        "_prev_record": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "birthmo": "3",
                        "birthyr": "1990",
                        "module": "UDS",
                        "formver": "3.2",
                        "packet": "I",
                        "naccid": "NACC123456",
                        "adcid": 0,
                    },
                    "missingness": {"missingvar": 5},
                }
            }
        }
    }

    return SymbolTable(data)


class TestPreviousRecordNamespace:
    def test_get_values(self, prev_record):
        """Tests getting raw vs missingness form value."""
        namespace = PreviousRecordNamespace(table=prev_record)

        assert namespace.get_form_value("naccid", str) == "NACC123456"
        assert namespace.get_form_value("missingvar", int) is None

        assert namespace.get_missingness_value("naccid", str) is None
        assert namespace.get_missingness_value("missingvar", int) == 5

        assert namespace.get_resolved_value("naccid", str) == "NACC123456"
        assert namespace.get_resolved_value("missingvar", int) == 5
