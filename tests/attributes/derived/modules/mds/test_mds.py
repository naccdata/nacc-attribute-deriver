"""Tests MDS form."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.mds.form_mds import (
    MDSFormAttributeCollection,
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
                        "visitdate": "2008-12-13",
                        "module": "MDS",
                        "vitalst": 2,
                        "deathyr": "2008",
                        "deathmo": "11",
                        "deathday": "21",
                        "birthyr": "1960",
                        "birthmo": "2",
                        "birthday": "17",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


class TestMilestoneAttributeCollection:
    """General MDS attribute tests."""

    def test_create_mds_death_date(self, table) -> None:
        """Test create_mds_death_date works as expected."""
        attr = MDSFormAttributeCollection(table)

        # test when all is set
        assert attr._create_mds_death_date() == "2008-11-21"

        # test when unknown parts
        table["file.info.forms.json"].update(
            {
                "deathyr": "9999",
                "deathmo": "3",
                "deathday": "99",
            }
        )
        assert attr._create_mds_death_date() == "9999-03-99"

        # test when not dead
        table["file.info.forms.json.vitalst"] = 1
        assert attr._create_mds_death_date() is None

    def test_create_mds_death_age(self, table) -> None:
        """Test _create_mds_death_age works as expected."""
        attr = MDSFormAttributeCollection(table)

        # test when all is set
        assert attr._create_mds_death_age() == 48

        # test when death cannot be calculated
        table["file.info.forms.json"].update(
            {
                "deathyr": "9999",
                "deathmo": "99",
                "deathday": "1",
            }
        )
        assert attr._create_mds_death_age() == 999

        # test when birth date cannot be calculated
        table["file.info.forms.json"].update(
            {
                "deathyr": "2008",
                "deathmo": "11",
                "deathday": "21",
                "birthyr": "1960",
                "birthmo": "99",
                "birthday": "99",
            }
        )
        assert attr._create_mds_death_age() == 999

        # test when not dead
        table["file.info.forms.json.vitalst"] = 1
        assert attr._create_mds_death_age() is None
