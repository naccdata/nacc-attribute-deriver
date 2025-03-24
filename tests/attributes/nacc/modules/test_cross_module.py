"""Tests cross-module attributes."""

import pytest

from nacc_attribute_deriver.attributes.nacc.modules.cross_module import (
    CrossModuleAttributeCollection,  # type: ignore
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
                        "visitdate": "2025-01-01",
                        "birthmo": 3,
                        "birthyr": 1990,
                        "module": "UDS",
                    }
                },
                "np": {"npdage": 83},
                "milestone": {
                    "deceased": "1",
                    "deathyr": "2050",
                    "deathmo": "2",
                    "deathdy": "2",
                },
                "mds": {"vitalst": 2, "deathyr": 2030, "deathmo": 1, "deathday": 1},
            }
        },
        "subject": {
            "info": {
                "derived": {
                    "mds_vital_status": 2,
                    "np_death_age": 83,
                    "mds_death_date": "2030-01-01",
                    "milestone_deceased": 1,
                    "milestone_death_date": "2050-02-02",
                }
            }
        },
    }

    return SymbolTable(data)


class TestCrossModuleAttribute:
    def test_create_naccdage(self, table):
        """Tests creating NACCDAGE triggering each case.

        This inherently tests _determine_death_date except in the NP
        case.
        """
        # trigger NP case
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccdage() == 83

        # trigger Milestone case
        table["subject.info.derived.np_death_age"] = None
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccdage() == 59

        # test when month/day is unknown for milestone
        # this will transform dmo = 7 and ddy = 1 which changes
        # the age since the birthday is before then
        table["subject.info.derived.milestone_death_date"] = "2050-07-01"
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccdage() == 60

        # trigger MDS case
        table["subject.info.derived.milestone_death_date"] = None
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccdage() == 39

        # test when year month/day is unknown for MDS,
        # similarly should change the age to 40
        table["subject.info.derived.mds_death_date"] = "2030-07-01"
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccdage() == 40

        # in MDS, deathyr can be 9999, in which case
        # naccdage should be unknown
        table["subject.info.derived.mds_death_date"] = None
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccdage() == 999

        # test death not reported
        # table["subject.info.derived.mds_death_date"] = None
        # attr = CrossModuleAttributeCollection.create(table)
        # assert attr._create_naccdage() == 888

    def test_create_naccdied(self, table):
        """Tests _create_naccdied."""
        # NP case
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccdied() == 1

        # Milestone case
        table["subject.info.derived.np_death_age"] = None
        table["subject.info.derived.milestone_deceased"] = 1
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccdied() == 1

        table["subject.info.derived.milestone_deceased"] = 0
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccdied() == 0

        table["file.info.milestone"] = {}
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccdied() == 0

    def test_create_naccautp(self, table):
        """Tests _create_naccautp."""
        # NP data available
        table["subject.info.derived.np_death_age"] = 80
        table["subject.info.derived.milestone_deceased"] = 1
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccautp() == 1

        # Only milestone data available
        table["subject.info.derived.np_death_age"] = None
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccautp() == 0

        # Neither available
        table["subject.info.derived.milestone_deceased"] = None
        attr = CrossModuleAttributeCollection.create(table)
        assert attr._create_naccautp() == 8
