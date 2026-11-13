"""Tests BDS missingness attributes."""

import pytest
from nacc_attribute_deriver.attributes.missingness.modules.bds.missingness_bds import (
    BDSFormMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

BDSCO_VARS = [
    "bdscoalz",
    "bdscolbd",
    "bdscomsa",
    "bdscopsp",
    "bdscocbd",
    "bdscofmo",
    "bdscofot",
    "bdscovas",
    "bdscotbi",
    "bdscodwn",
    "bdscoo1f",
    "bdscoo2f",
    "bdscoo3f",
]


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "formver": 1.0,
                        "module": "BDS",
                        "visitdate": "2025-01-01",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


def missingness(attr: BDSFormMissingness, field: str) -> int:
    return getattr(attr, f"_missingness_{field}")()


class TestBDSFormMissingness:
    @pytest.mark.parametrize("field", BDSCO_VARS)
    def test_bdsco_gate(self, table, field):
        """BDSCO* is 8 if BDSUDSD = 1, 9 if BDSUDSD = 9."""
        attr = BDSFormMissingness(table)

        table["file.info.forms.json.bdsudsd"] = 1
        assert missingness(attr, field) == 8

        table["file.info.forms.json.bdsudsd"] = 9
        assert missingness(attr, field) == 9

        # impaired - should have been submitted, so generic missingness
        for bdsudsd in [2, 3, 4]:
            table["file.info.forms.json.bdsudsd"] = bdsudsd
            assert missingness(attr, field) == INFORMED_MISSINGNESS

        # gate blank
        table["file.info.forms.json.bdsudsd"] = None
        assert missingness(attr, field) == INFORMED_MISSINGNESS

        # submitted value is kept
        table["file.info.forms.json.bdsudsd"] = 4
        table[f"file.info.forms.json.{field}"] = 0
        assert missingness(attr, field) == 0
        table[f"file.info.forms.json.{field}"] = "1"
        assert missingness(attr, field) == 1

    def test_bdsetpr(self, table):
        """BDSETPR is 88 if BDSUDSD = 1, 99 if BDSUDSD = 9."""
        attr = BDSFormMissingness(table)

        table["file.info.forms.json.bdsudsd"] = 1
        assert attr._missingness_bdsetpr() == 88

        table["file.info.forms.json.bdsudsd"] = 9
        assert attr._missingness_bdsetpr() == 99

        table["file.info.forms.json.bdsudsd"] = 4
        assert attr._missingness_bdsetpr() == INFORMED_MISSINGNESS

        table["file.info.forms.json.bdsetpr"] = 2
        assert attr._missingness_bdsetpr() == 2

    def test_bdstmci(self, table):
        """BDSTMCI is 8 if BDSUDSD ne 3 (not MCI)."""
        attr = BDSFormMissingness(table)

        for bdsudsd in [1, 2, 4, 9]:
            table["file.info.forms.json.bdsudsd"] = bdsudsd
            assert attr._missingness_bdstmci() == 8

        # MCI - should have been submitted, so generic missingness
        table["file.info.forms.json.bdsudsd"] = 3
        assert attr._missingness_bdstmci() == INFORMED_MISSINGNESS

        # gate blank
        table["file.info.forms.json.bdsudsd"] = None
        assert attr._missingness_bdstmci() == INFORMED_MISSINGNESS

        # submitted value is kept
        table["file.info.forms.json.bdsudsd"] = 3
        table["file.info.forms.json.bdstmci"] = 2
        assert attr._missingness_bdstmci() == 2
