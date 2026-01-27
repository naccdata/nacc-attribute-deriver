"""Tests the missingness collection."""

import pytest

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
    UDSCorrelatedFormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


class TestFormMissingnessCollection:
    def test_generic_missingness(self):
        """Tests the bread and butter of missingness logic: generic
        missingness."""
        table = SymbolTable({})
        attr = FormMissingnessCollection(table=table, date_attribute=None)

        assert attr.generic_missingness("dummy", str) == INFORMED_BLANK
        assert attr.generic_missingness("dummy", int) == INFORMED_MISSINGNESS
        assert attr.generic_missingness("dummy", float) == float(INFORMED_MISSINGNESS)

        with pytest.raises(AttributeDeriverError):
            attr.generic_missingness("dummy", list)

        # with values
        table["file.info.forms.json"] = {
            "some-int": 1,
            "some-float": 2.5,
            "some-str": "hello",
        }

        assert attr.generic_missingness("some-str", str) == "hello"
        assert attr.generic_missingness("some-int", int) == 1
        assert attr.generic_missingness("some-float", float) == 2.5

    def test_get_visitdate(self):
        """Test getting the vistidate, standardized."""
        table = SymbolTable({})
        no_date_attr = FormMissingnessCollection(table=table, date_attribute=None)

        assert no_date_attr.get_visitdate() is None

        # differently named attribute in non-standard format
        table["file.info.forms.json.dummy-visitdate"] = "12/01/2025"
        with_date_attr = FormMissingnessCollection(
            table=table, date_attribute="dummy-visitdate"
        )

        assert with_date_attr.get_visitdate() == "2025-12-01"

        # not there
        table["file.info.forms.json.dummy-visitdate"] = None
        with pytest.raises(AttributeDeriverError):
            with_date_attr.get_visitdate()

        # badly formatted
        table["file.info.forms.json.dummy-visitdate"] = "not-a-date"
        with pytest.raises(AttributeDeriverError):
            with_date_attr.get_visitdate()

    def test_handle_prev_visit(self):
        """Tests handling the previous visit."""
        table = SymbolTable({})
        table["file.info.forms.json.dummy"] = 777
        attr = FormMissingnessCollection(table=table, date_attribute=None)

        # doesn't match prev code, so just falls through
        assert attr.handle_prev_visit("dummy", int, prev_code=None) == 777

        # matches prev code, so looks for previous, but since it can't find it,
        # falls to generic missingness
        assert attr.handle_prev_visit("dummy", int, prev_code=777) == 777

        # matches prev code, and previous is defined
        # directly from info.forms.json case
        table["_prev_record.info.forms.json.dummy"] = 3
        assert attr.handle_prev_visit("dummy", int, prev_code=777) == 3

        # matches prev code, and previous is defined
        # from resolved case
        table["_prev_record.info.resolved.dummy"] = 5
        assert attr.handle_prev_visit("dummy", int, prev_code=777) == 5

        # matches prev code, but grab from working instead
        table["subject.info.working.cross-sectional.dummy"] = 9
        working = WorkingNamespace(table=table)
        assert attr.handle_prev_visit("dummy", int, prev_code=777, working=working) == 9

        # test default is used when absolutely nothing is there
        assert (
            attr.handle_prev_visit("undefined", str, default="some-default")
            == "some-default"
        )


class TestUDSCorrelatedFormMissingnessCollection:
    def test_find_closest_uds_visit(self):
        """Test finding the closest visitdate."""
        table = SymbolTable({})
        table["file.info.forms.json.visitdate"] = "01/01/2025"
        table["subject.info.working.cross-sectional.uds-visitdates"] = [
            "1990/10/12",
            "2024/12/01",
            "10-15-2025",
            "2026-02-03",
        ]

        attr = UDSCorrelatedFormMissingnessCollection(table=table)
        assert attr.find_closest_uds_visit() == ("2024-12-01", 2)
