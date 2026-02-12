"""Tests MLST form."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.milestone.form_milestone import (
    MilestoneAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2020-01-01",
                        "visitday": "1",
                        "visitmo": "1",
                        "visityr": "2020",
                        "module": "MLST",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


class TestMilestoneAttributeCollection:
    def test_discontinued_date_explicit(self, table):
        """Test discontinued date parts are correct when explicitly
        discontinued."""
        table["file.info.forms.json"].update(
            {"discont": "1", "discday": "25", "discmo": "5", "discyr": "2021"}
        )
        attr = MilestoneAttributeCollection(table)

        assert attr._create_milestone_discday() == 25
        assert attr._create_milestone_discmo() == 5
        assert attr._create_milestone_discyr() == 2021

    def test_discontinued_date_minimum_contact(self, table):
        """Test discontinued date parts are correct when set.

        to minimum contact - anything after V1.
        """
        # PROTOCOL + CHANGEX dates
        table["file.info.forms.json"].update(
            {"protocol": 2, "changedy": "9", "changemo": "3", "changeyr": "2022"}
        )
        attr = MilestoneAttributeCollection(table)

        assert attr._create_milestone_discday() == 9
        assert attr._create_milestone_discmo() == 3
        assert attr._create_milestone_discyr() == 2022

    def test_discontinued_date_minimum_contact_v1(self, table):
        """Test discontinued date parts are correct when set.

        to minimum contact - V1.
        """
        # UDSACTIV + VISITX dates
        table["file.info.forms.json"].update(
            {"udsactiv": "3", "changedy": "16", "changemo": "11", "changeyr": "2023"}
        )
        attr = MilestoneAttributeCollection(table)

        assert attr._create_milestone_discday() == 16
        assert attr._create_milestone_discmo() == 11
        assert attr._create_milestone_discyr() == 2023
