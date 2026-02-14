"""Tests MLST form."""

import random
import pytest
from nacc_attribute_deriver.attributes.derived.modules.mlst.form_mlst import (
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
    """General MLST attribute tests."""

    def test_create_milestone_renurse(self, table):
        """RENURSE was NURSEHOM in older versions; make sure both are accepted,
        and that it takes the NURSX date variables into account if both are
        missing."""
        # nursehom
        table["file.info.forms.json"].update({"nursehom": "1"})
        attr = MilestoneAttributeCollection(table)
        assert attr._create_milestone_renurse() == 1

        # renurse
        table["file.info.forms.json"].update({"nursehom": None, "renurse": 1})
        assert attr._create_milestone_renurse() == 1

        # nurse dates
        table["file.info.forms.json"].update(
            {
                "nursehom": None,
                "renurse": None,
                "nursedy": 2,
                "nursemo": 8,
                "nurseyr": 2001,
            }
        )
        assert attr._create_milestone_renurse() == 1

        # all blank
        table["file.info.forms.json"].update(
            {
                "nursehom": None,
                "renurse": None,
                "nursedy": None,
                "nursemo": None,
                "nurseyr": None,
            }
        )
        assert attr._create_milestone_renurse() is None

        # renurse explicitly set something to 0
        table["file.info.forms.json"].update(
            {random.choice(["renurse", "nursehom"]): 0}
        )
        assert attr._create_milestone_renurse() == 0

    def test_create_milestone_discontinued(self, table):
        """Test creating MLST set discontinued."""
        # discont explicitly = 1
        table["file.info.forms.json"].update({"discont": "1"})
        attr = MilestoneAttributeCollection(table)
        assert attr._create_milestone_discontinued() == 1

        # rejoin or rejoined set
        rejoin = random.choice(["rejoin", "rejoined"])
        table["file.info.forms.json"].update({"discont": None, rejoin: 1})
        assert attr._create_milestone_discontinued() == 0

        # test none set
        table["file.info.forms.json"].update({"discont": None, rejoin: None})
        assert attr._create_milestone_discontinued() is None


class TestDiscontinuedDates:
    """Specifically testing discontinued dates which are a bit conflated with
    minimum contact."""

    def test_date_explicit(self, table):
        """Test discontinued date parts are correct when explicitly
        discontinued."""
        table["file.info.forms.json"].update(
            {"discont": "1", "discday": "25", "discmo": "5", "discyr": "2021"}
        )
        attr = MilestoneAttributeCollection(table)

        assert attr._create_milestone_discday() == 25
        assert attr._create_milestone_discmo() == 5
        assert attr._create_milestone_discyr() == 2021

    def test_date_minimum_contact(self, table):
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

        # test CHANGEDAY/CHANGEMO = 99 get set to 88
        table["file.info.forms.json"].update(
            {"protocol": 2, "changedy": "99", "changemo": 99, "changeyr": "2024"}
        )
        attr = MilestoneAttributeCollection(table)

        assert attr._create_milestone_discday() == 88
        assert attr._create_milestone_discmo() == 88
        assert attr._create_milestone_discyr() == 2024

    def test_date_minimum_contact_v1(self, table):
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

    def test_date_carry_forward(self, table):
        """Test discontinued date is carried forward on a subsequent MLST form
        that isn't updating the status, for example one that is reporting
        death."""
        table["file.info.forms.json"].update(
            {"deathdy": "2", "deathmo": "5", "deathyr": "2020"}
        )
        table["subject.info.working.cross-sectional"] = {
            "milestone-discday": "16",
            "milestone-discmo": "3",
            "milestone-discyr": "2015",
        }

        attr = MilestoneAttributeCollection(table)

        assert attr._create_milestone_discday() == 16
        assert attr._create_milestone_discmo() == 3
        assert attr._create_milestone_discyr() == 2015

    def test_discday_multidefinition(self, table):
        """DISCDAY can come from either DISCDY or DISCDAY, make sure both
        work."""
        # discday
        table["file.info.forms.json"].update({"discont": "1", "discday": "19"})

        attr = MilestoneAttributeCollection(table)
        assert attr._create_milestone_discday() == 19

        # discdy
        table["file.info.forms.json"].update(
            {"discont": "1", "discday": None, "discdy": "11"}
        )

        attr = MilestoneAttributeCollection(table)
        assert attr._create_milestone_discday() == 11
