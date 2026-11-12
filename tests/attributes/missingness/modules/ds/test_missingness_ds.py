"""Tests DS missingness attributes."""

import pytest
from nacc_attribute_deriver.attributes.missingness.modules.ds.missingness_ds import (
    DSFormMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)

AGE_VARS = ["dsmomage", "dsmnsage", "dsmnpage", "dsagehrt"]

YEAR_GATES = {
    "dshrtryr": "dshrtrpr",
    "dscrdsyr": "dscrdsrg",
    "dsspinyr": "dsspin",
    "dslworyr": "dslworth",
    "dsuporyr": "dsuporth",
    "dsthysyr": "dsthysrg",
    "dsoncsyr": "dsoncsrg",
    "dsothsyr": "dsothsrg",
}


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "formver": 1.0,
                        "module": "DS",
                        "packet": "F",
                        "visitdate": "2025-01-01",
                    }
                }
            }
        }
    }
    return SymbolTable(data)


def missingness(attr: DSFormMissingness, field: str) -> int:
    return getattr(attr, f"_missingness_{field}")()


class TestDSFormMissingness:
    @pytest.mark.parametrize("field", AGE_VARS)
    def test_age_carry_forward(self, table, field):
        """777 carries forward the previous visit's value, else 999."""
        attr = DSFormMissingness(table)

        # blank
        assert missingness(attr, field) == INFORMED_MISSINGNESS

        # submitted value is kept
        table[f"file.info.forms.json.{field}"] = "15"
        assert missingness(attr, field) == 15

        # 777 with no previous visit
        table[f"file.info.forms.json.{field}"] = 777
        assert missingness(attr, field) == 999

        # 777 with previous visit
        table[f"_prev_record.info.resolved.{field}"] = 18
        assert missingness(attr, field) == 18

    @pytest.mark.parametrize("field,gate", list(YEAR_GATES.items()))
    def test_year(self, table, field, gate):
        """7777 carries forward; blank is 8888 if the gate is 0 or 9."""
        attr = DSFormMissingness(table)

        # gate not answered/blank year
        assert missingness(attr, field) == INFORMED_MISSINGNESS

        # gate = 0 or 9
        for value in [0, 9]:
            table[f"file.info.forms.json.{gate}"] = value
            assert missingness(attr, field) == 8888

        # gate = 1, should have been submitted
        table[f"file.info.forms.json.{gate}"] = 1
        assert missingness(attr, field) == INFORMED_MISSINGNESS

        # submitted value is kept
        table[f"file.info.forms.json.{field}"] = "2001"
        assert missingness(attr, field) == 2001

        # 7777 with no previous visit
        table[f"file.info.forms.json.{field}"] = 7777
        assert missingness(attr, field) == 9999

        # 7777 with previous visit
        table[f"_prev_record.info.resolved.{field}"] = 1999
        assert missingness(attr, field) == 1999

    @pytest.mark.parametrize("field", ["dsdxhs_mci", "dsdxhs_dem"])
    def test_dx_history_checkboxes(self, table, field):
        """Blank if DSDXHS_NO = 1, else generic."""
        attr = DSFormMissingness(table)

        # DSDXHS_NO not checked
        assert missingness(attr, field) == INFORMED_MISSINGNESS
        table["file.info.forms.json.dsdxhs_no"] = 0
        assert missingness(attr, field) == INFORMED_MISSINGNESS

        # DSDXHS_NO = 1
        table["file.info.forms.json.dsdxhs_no"] = 1
        assert missingness(attr, field) == INFORMED_BLANK

        # submitted value is kept
        table[f"file.info.forms.json.{field}"] = "0"
        assert missingness(attr, field) == 0

    @pytest.mark.parametrize(
        "field,gate",
        [
            ("dsmcimo", "dsdxhs_mci"),
            ("dsmciyr", "dsdxhs_mci"),
            ("dsdemmo", "dsdxhs_dem"),
            ("dsdemyr", "dsdxhs_dem"),
        ],
    )
    def test_dx_dates(self, table, field, gate):
        """Blank if GATE ne 1, else generic."""
        attr = DSFormMissingness(table)

        # gate blank or 0
        assert missingness(attr, field) == INFORMED_BLANK
        table[f"file.info.forms.json.{gate}"] = 0
        assert missingness(attr, field) == INFORMED_BLANK

        # gate = 1, should have been submitted
        table[f"file.info.forms.json.{gate}"] = 1
        assert missingness(attr, field) == INFORMED_MISSINGNESS

        # submitted value is kept
        table[f"file.info.forms.json.{field}"] = "99"
        assert missingness(attr, field) == 99

    @pytest.mark.parametrize("field", ["dsdxby", "dsonstmo", "dsonstyr"])
    @pytest.mark.parametrize("gate", ["dsdxhs_mci", "dsdxhs_dem"])
    def test_dx_followups(self, table, field, gate):
        """Blank unless DSDXHS_MCI = 1 or DSDXHS_DEM = 1, else generic."""
        attr = DSFormMissingness(table)

        # no MCI/dementia dx
        assert missingness(attr, field) == INFORMED_BLANK
        table["file.info.forms.json.dsdxhs_no"] = 1
        table["file.info.forms.json.dsdxhs_mci"] = 0
        assert missingness(attr, field) == INFORMED_BLANK

        # MCI or dementia dx, should have been submitted
        table["file.info.forms.json.dsdxhs_no"] = 0
        table[f"file.info.forms.json.{gate}"] = 1
        assert missingness(attr, field) == INFORMED_MISSINGNESS

        # submitted value is kept
        table[f"file.info.forms.json.{field}"] = "2"
        assert missingness(attr, field) == 2
