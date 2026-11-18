"""Tests DS missingness attributes."""

import pytest
from nacc_attribute_deriver.attributes.missingness.modules.ds.missingness_ds import (
    DSFormMissingness,
    DSMissingness,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

AGE_VARS = ["dsmomage", "dsmnsage", "dsmnpage", "dsagehrt"]

B1D_BOXES = [
    *[f"dsdx_{x}" for x in ["aut", "cp", "ds", "frx", "id", "pw", "oth"]],
    *[
        f"dscn_{x}"
        for x in ["vim", "bld", "gls", "him", "df", "had", "mim", "uw", "miw"]
    ],
    *[
        f"dsle_{x}"
        for x in ["cd", "chl", "chs", "nrm", "ill", "sem", "sei", "sev", "oth"]
    ],
    *[f"dsre_{x}" for x in ["ref", "int", "ann", "rep"]],
]

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

        # 7777 with previous visit 8888 (not applicable) becomes unknown
        table[f"_prev_record.info.resolved.{field}"] = 8888
        assert missingness(attr, field) == 9999

    @pytest.mark.parametrize(
        "field,code",
        [
            ("dsdxby", 8),
            ("dsonstmo", 88),
            ("dsonstyr", 8888),
        ],
    )
    def test_no_dx_history(self, table, field, code):
        """CODE if DSDXHS_NO = 1, else generic."""
        attr = DSFormMissingness(table)

        # DSDXHS_NO blank or 0
        assert missingness(attr, field) == INFORMED_MISSINGNESS
        table["file.info.forms.json.dsdxhs_no"] = 0
        assert missingness(attr, field) == INFORMED_MISSINGNESS

        # DSDXHS_NO = 1
        table["file.info.forms.json.dsdxhs_no"] = 1
        assert missingness(attr, field) == code

        # submitted value is kept
        table[f"file.info.forms.json.{field}"] = "1"
        assert missingness(attr, field) == 1

    @pytest.mark.parametrize("field", B1D_BOXES)
    def test_b1d_boxes(self, table, field):
        """0 if blank and B1D was completed (FRMDATEB1D), else generic."""
        attr = DSFormMissingness(table)

        # B1D not completed
        assert missingness(attr, field) == INFORMED_MISSINGNESS

        # B1D completed
        table["file.info.forms.json.frmdateb1d"] = "2025-01-01"
        assert missingness(attr, field) == 0

        # submitted value is kept
        table[f"file.info.forms.json.{field}"] = "1"
        assert missingness(attr, field) == 1

    @pytest.mark.parametrize(
        "checked,expected",
        [
            ("dsdxhs_no", {"dsdxhs_no": 1, "dsdxhs_mci": 0, "dsdxhs_dem": 0}),
            ("dsdxhs_mci", {"dsdxhs_no": 0, "dsdxhs_mci": 1, "dsdxhs_dem": 0}),
            ("dsdxhs_dem", {"dsdxhs_no": 0, "dsdxhs_mci": 0, "dsdxhs_dem": 1}),
        ],
    )
    def test_q16_boxes(self, table, checked, expected):
        """A blank Q16 box is 0 if another Q16 box is checked."""
        attr = DSFormMissingness(table)

        # none checked
        for field in expected:
            assert missingness(attr, field) == INFORMED_MISSINGNESS

        table[f"file.info.forms.json.{checked}"] = "1"
        for field, value in expected.items():
            assert missingness(attr, field) == value

    @pytest.mark.parametrize(
        "field,gate,other,code",
        [
            ("dsmcimo", "dsdxhs_mci", "dsdxhs_dem", 88),
            ("dsmciyr", "dsdxhs_mci", "dsdxhs_dem", 8888),
            ("dsdemmo", "dsdxhs_dem", "dsdxhs_mci", 88),
            ("dsdemyr", "dsdxhs_dem", "dsdxhs_mci", 8888),
        ],
    )
    def test_gate_is_0(self, table, field, gate, other, code):
        """CODE if the GATE box resolves to 0, else generic."""
        attr = DSFormMissingness(table)

        # Q16 unanswered
        assert missingness(attr, field) == INFORMED_MISSINGNESS

        # gate blank but resolves to 0 (another box checked)
        table[f"file.info.forms.json.{other}"] = 1
        assert missingness(attr, field) == code
        table[f"file.info.forms.json.{other}"] = None
        table["file.info.forms.json.dsdxhs_no"] = 1
        assert missingness(attr, field) == code

        # gate submitted as 0
        table["file.info.forms.json.dsdxhs_no"] = None
        table[f"file.info.forms.json.{gate}"] = 0
        assert missingness(attr, field) == code

        # gate = 1, should have been submitted
        table[f"file.info.forms.json.{gate}"] = 1
        assert missingness(attr, field) == INFORMED_MISSINGNESS

        # submitted value is kept
        table[f"file.info.forms.json.{field}"] = "6"
        assert missingness(attr, field) == 6

    def test_dsrepmo(self, table):
        """DSREPMO is a float: 888.0 if DSRE_REP resolves to 0, else -4.0 if
        blank."""
        attr = DSFormMissingness(table)

        def check(expected: float) -> None:
            result = missingness(attr, "dsrepmo")
            assert isinstance(result, float)
            assert result == expected

        # B1D not completed, DSRE_REP blank
        check(-4.0)

        # B1D completed, DSRE_REP blank resolves to 0
        table["file.info.forms.json.frmdateb1d"] = "2025-01-01"
        check(888.0)

        # DSRE_REP submitted as 0
        table["file.info.forms.json.dsre_rep"] = 0
        check(888.0)

        # DSRE_REP = 1, should have been submitted
        table["file.info.forms.json.dsre_rep"] = 1
        check(-4.0)

        # submitted value is kept
        table["file.info.forms.json.dsrepmo"] = "6.5"
        check(6.5)


class TestDSMissingness:
    def test_naccds(self):
        """NACCDS is 0 if the subject has no DS visits."""
        table = SymbolTable({})
        assert DSMissingness(table)._missingness_naccds() == 0

        table["subject.info.derived.cross-sectional.naccds"] = 1
        assert DSMissingness(table)._missingness_naccds() == 1
