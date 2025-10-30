"""Tests cross-module attributes."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.cross_module import (
    CrossModuleAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table(uds_table) -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    uds_table.update(
        {
            "subject": {
                "info": {
                    "working": {
                        "cross-sectional": {
                            "mds-vital-status": 2,
                            "np-death-age": 83,
                            "np-death-date": "2029-06-06",
                            "mds-death-date": "2030-01-01",
                            "milestone-deceased": 1,
                            "milestone-death-date": "2050-02-02",
                            "uds-visitdates": [
                                "1980-05-06",
                                "1980-10-10",
                                "2023-12-12",
                                "2024-01-01",
                                "2024-02-02",
                                "2025-03-03",
                            ],
                            "milestone-discyr": {
                                "latest": {"date": "2050-03-01", "value": 2050}
                            },
                            "milestone-discmo": {
                                "latest": {"date": "2050-03-01", "value": 3}
                            },
                            "milestone-discday": {
                                "latest": {"date": "2050-03-01", "value": 1}
                            },
                            "milestone-renurse": {
                                "latest": {"date": "2025-01-01", "value": 1}
                            },
                            "milestone-visitdates": ["2025-01-01", "2050-03-01"],
                        }
                    }
                }
            },
        }
    )

    return uds_table


class TestCrossModuleAttribute:
    def test_create_naccdage(self, table):
        """Tests creating NACCDAGE triggering each case.

        This inherently tests _determine_death_date except in the NP
        case.
        """
        # trigger NP case
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdage() == 83

        # trigger Milestone case
        table["subject.info.working.cross-sectional.np-death-age"] = None
        table["subject.info.working.cross-sectional.np-death-date"] = None
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdage() == 59

        # test when month/day is unknown for milestone
        # this will transform dmo = 7 and ddy = 1 which changes
        # the age since the birthday is before then
        table["subject.info.working.cross-sectional.milestone-death-date"] = (
            "2050-07-01"
        )
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdage() == 60

        # trigger MDS case
        table["subject.info.working.cross-sectional.milestone-death-date"] = None
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdage() == 39

        # test when year month/day is unknown for MDS,
        # similarly should change the age to 40
        table["subject.info.working.cross-sectional.mds-death-date"] = "2030-07-01"
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdage() == 40

        # in MDS, deathyr can be 9999, in which case
        # naccdage should be unknown
        table["subject.info.working.cross-sectional.mds-death-date"] = None
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdage() == 999

        # test death not reported
        # table["subject.info.working.cross-sectional.mds-death-date"] = None
        # attr = CrossModuleAttributeCollection(table)
        # assert attr._create_naccdage() == 888

    def test_create_naccdied(self, table):
        """Tests _create_naccdied."""
        # NP case
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdied() == 1

        # Milestone case
        table["subject.info.working.cross-sectional.np-death-age"] = None
        table["subject.info.working.cross-sectional.milestone-deceased"] = 1
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdied() == 1

        table["subject.info.working.cross-sectional.milestone-deceased"] = 0
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdied() == 0

        table["file.info.milestone"] = {}
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdied() == 0

    def test_create_naccautp(self, table):
        """Tests _create_naccautp."""
        # NP data available
        table["subject.info.working.cross-sectional.np-death-age"] = 80
        table["subject.info.working.cross-sectional.milestone-deceased"] = 1
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccautp() == 1

        # Only milestone data available
        table["subject.info.working.cross-sectional.np-death-age"] = None
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccautp() == 0

        # Neither available
        table["subject.info.working.cross-sectional.milestone-deceased"] = None
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccautp() == 8

    def test_create_naccint(self, table):
        """Tests _create_naccint."""
        # NP death date available
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccint() == 51

        # Milestone death date available
        table["subject.info.working.cross-sectional.np-death-date"] = None
        assert attr._create_naccint() == 299

        # MDS death date available
        # NOTE: NACCINT isn't officially calculated for MDS
        table["subject.info.working.cross-sectional.milestone-death-date"] = None
        assert attr._create_naccint() == 58

        # no death age but dead based on other variables
        table["subject.info.working.cross-sectional.mds-death-date"] = None
        assert attr._create_naccint() == 999

        # not dead
        table["subject.info.working.cross-sectional.np-death-age"] = None
        table["subject.info.working.cross-sectional.milestone-deceased"] = None
        assert attr._create_naccint() == 888

    def test_determine_discontinued_date(self, table):
        """Tests determine_discontinued_date through NACCDSDY, NACCDSMO and
        NACCDSYR."""
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsdy() == 1
        assert attr._create_naccdsmo() == 3
        assert attr._create_naccdsyr() == 2050

        # pretend UDS came after, should return 8888-88-88
        table["file.info.forms.json.visitdate"] = "4000-01-01"
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsdy() == 88
        assert attr._create_naccdsmo() == 88
        assert attr._create_naccdsyr() == 8888

    def test_determine_discontinued_date_close(self, table):
        """Tests determine_discontinued_date through NACCDSDY, NACCDSMO and
        NACCDSYR when dates are close."""
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsdy() == 1
        assert attr._create_naccdsmo() == 3
        assert attr._create_naccdsyr() == 2050

        # pretend UDS came after in the same year, should return 8888-88-88
        table["file.info.forms.json.visitdate"] = "2050-05-01"
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsdy() == 88
        assert attr._create_naccdsmo() == 88
        assert attr._create_naccdsyr() == 8888

        # pretend UDS came the day after, should return 8888-88-88
        table["file.info.forms.json.visitdate"] = "2050-03-02"
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsdy() == 88
        assert attr._create_naccdsmo() == 88
        assert attr._create_naccdsyr() == 8888

        # pretend UDS came the day before, should return 2050-03-01
        table["file.info.forms.json.visitdate"] = "2050-02-28"
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccdsdy() == 1
        assert attr._create_naccdsmo() == 3
        assert attr._create_naccdsyr() == 2050

    def test_create_naccnurp(self, table):
        """Tests _create_naccnurp."""
        attr = CrossModuleAttributeCollection(table)
        assert attr._create_naccnurp() == 1

        # if UDS has residenc == 4 or 9 and came later,
        # set to 0
        table["file.info.forms.json.visitdate"] = "2025-01-02"
        for value in [4, 9]:
            table["file.info.forms.json.residenc"] = value
            assert attr._create_naccnurp() == 0

        # if MLST explicitly sets to 0, should be 0
        table["subject.info.working.cross-sectional.milestone-renurse"] = {
            "latest": {"date": "2026-01-01", "value": 0}
        }
        assert attr._create_naccnurp() == 0
