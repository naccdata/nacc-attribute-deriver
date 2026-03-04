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
                        "module": "MLST",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


class TestMilestoneAttributeCollection:
    """General MLST attribute tests."""

    def test_create_milestone_renurse_date(self, table):
        """RENURSE was NURSEHOM in older versions; make sure both are accepted,
        and that it takes the NURSX date variables into account if both are
        missing."""
        attr = MilestoneAttributeCollection(table)

        # nursehom
        table["file.info.forms.json"].update(
            {"nursehom": "1", "nurseyr": "2000", "nursemo": "99", "nursedy": 99}
        )
        assert attr._create_milestone_renurse_date() == "2000-99-99"

        # renurse
        table["file.info.forms.json"].update(
            {
                "nursehom": None,
                "renurse": 1,
                "nurseyr": "2005",
                "nursemo": 5,
                "nursedy": 21,
            }
        )
        assert attr._create_milestone_renurse_date() == "2005-05-21"

        # date values are missing, should use form date
        table["file.info.forms.json"].update(
            {"nurseyr": None, "nursemo": None, "nursedy": None}
        )
        assert attr._create_milestone_renurse_date() == "2020-01-01"

        # explicitly set to 0
        table["file.info.forms.json"].update({"renurse": 0, "nursehom": 0})
        assert attr._create_milestone_renurse_date() is None

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
        assert attr._create_milestone_renurse_date() is None

    def test_create_milestone_discontinued_date(self, table):
        """Test creating MLST set discontinued."""
        attr = MilestoneAttributeCollection(table)

        # discont explicitly = 1
        table["file.info.forms.json"].update(
            {"discont": "1", "discyr": "2019", "discmo": 12, "discdy": "25"}
        )
        assert attr._create_milestone_discontinued_date() == "2019-12-25"

        # test when using discday, discmo unknown
        table["file.info.forms.json"].update(
            {
                "discont": "1",
                "discyr": "2018",
                "discmo": 99,
                "discdy": None,
                "discday": 18,
            }
        )
        assert attr._create_milestone_discontinued_date() == "2018-99-18"

        # test when udsactiv was what was set, all dates are 9999-99-99
        table["file.info.forms.json"].update(
            {
                "discont": None,
                "udsactiv": 4,
                "discyr": "9999",
                "discmo": 99,
                "discday": "99",
            }
        )
        assert attr._create_milestone_discontinued_date() == "9999-99-99"

        # test when date values are missing, so use form date
        table["file.info.forms.json"].update(
            {"discyr": None, "discmo": None, "discday": None}
        )
        assert attr._create_milestone_discontinued_date() == "2020-01-01"
