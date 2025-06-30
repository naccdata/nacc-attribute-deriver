from typing import Any

from nacc_attribute_deriver.symbol_table import SymbolTable
from pytest import fixture


def set_attribute(table: SymbolTable, prefix: str, attribute: str, value: Any) -> None:
    table[f"{prefix}{attribute}"] = value


@fixture
def file_prefix():
    return "file.info."


@fixture
def form_prefix():
    return "file.info.forms.json."


@fixture
def raw_prefix():
    return "file.info.raw."


@fixture
def derived_prefix():
    return "file.info.derived."


@fixture
def subject_prefix():
    return "subject.info."


@fixture
def subject_derived_prefix():
    return "subject.info.derived."


@fixture
def working_derived_prefix():
    return "subject.info.working."
