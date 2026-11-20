"""Tests UDS Form D1c missingness attributes."""

import pytest

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_d1c import (
    UDSFormD1cMissingness,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


@pytest.fixture
def d1c_table(uds_table):
    """UDS V4 table with a completed D1c."""
    uds_table["file.info.forms.json"].update(
        {"formver": 4.0, "packet": "I4", "moded1c": 1}
    )
    return uds_table


class TestUDSFormD1cMissingness:
    def test_checkbox(self, d1c_table):
        """Checkboxes: 8 if gate = 0, 0 if gate = 1, else kept/-4."""
        form = d1c_table["file.info.forms.json"]

        form.update({"dxplsmabio": 0})
        assert UDSFormD1cMissingness(d1c_table)._missingness_dxptau217() == 8

        form.update({"dxplsmabio": 1})
        attr = UDSFormD1cMissingness(d1c_table)
        assert attr._missingness_dxptau217() == 0
        assert attr._missingness_dxothplsma() == 0

        form.update({"dxptau217": 1})
        assert UDSFormD1cMissingness(d1c_table)._missingness_dxptau217() == 1

        # gate unanswered
        form.update({"dxplsmabio": None, "dxptau217": None})
        assert (
            UDSFormD1cMissingness(d1c_table)._missingness_dxptau217()
            == INFORMED_MISSINGNESS
        )

        # other gates
        form.update({"dxapet": 1, "aacritmet": 0, "inforisch": 1})
        attr = UDSFormD1cMissingness(d1c_table)
        assert attr._missingness_apetvis() == 0
        assert attr._missingness_cr1oth() == 8
        assert attr._missingness_imgrsinf() == 0

    def test_unchecked_box(self, d1c_table):
        """Follow-ups to a checkbox: 8 if the checkbox is blank."""
        form = d1c_table["file.info.forms.json"]

        form.update({"dxplsmabio": 1, "dxptau217": None})
        attr = UDSFormD1cMissingness(d1c_table)
        assert attr._missingness_ptau217rs() == 8
        assert attr._missingness_pt217anlys() == 8
        assert attr._missingness_pt217int() == 8

        # also 8 when the whole section was skipped (gate = 0)
        form.update({"dxcsfbio": 0})
        assert UDSFormD1cMissingness(d1c_table)._missingness_ab42ab40it() == 8

        # checked but follow-up blank is missing data
        form.update({"dxptau217": 1})
        assert (
            UDSFormD1cMissingness(d1c_table)._missingness_ptau217rs()
            == INFORMED_MISSINGNESS
        )

        # submitted value kept
        form.update({"ptau217rs": 1})
        assert UDSFormD1cMissingness(d1c_table)._missingness_ptau217rs() == 1

    def test_gate_no(self, d1c_table):
        """Questions skipped by a yes/no gate: 8 if gate = 0."""
        form = d1c_table["file.info.forms.json"]

        form.update({"dxapet": 0, "aacritmet": 0, "dxasyn": 0})
        attr = UDSFormD1cMissingness(d1c_table)
        assert attr._missingness_apetrs() == 8
        assert attr._missingness_biostage() == 8
        assert attr._missingness_clinstage() == 8
        assert attr._missingness_asynassay() == 8

        form.update({"aacritmet": 1})
        assert (
            UDSFormD1cMissingness(d1c_table)._missingness_clinstage()
            == INFORMED_MISSINGNESS
        )

        form.update({"clinstage": 3})
        assert UDSFormD1cMissingness(d1c_table)._missingness_clinstage() == 3

    def test_imgrsinf_boxes(self, d1c_table):
        """IMGRSINFLC/IMGRSINFCT: 8 if INFORISCH = 0 or IMGRSINF blank, 0 if
        IMGRSINF = 1."""
        form = d1c_table["file.info.forms.json"]

        form.update({"inforisch": 0})
        attr = UDSFormD1cMissingness(d1c_table)
        assert attr._missingness_imgrsinflc() == 8
        assert attr._missingness_imgrsinfct() == 8

        form.update({"inforisch": 1, "imgrsinf": 1})
        attr = UDSFormD1cMissingness(d1c_table)
        assert attr._missingness_imgrsinflc() == 0
        assert attr._missingness_imgrsinfct() == 0

        form.update({"imgrsinflc": 1})
        assert UDSFormD1cMissingness(d1c_table)._missingness_imgrsinflc() == 1

        # INFORISCH = 1 but Infarction on MRI not selected
        form.update({"imgrsinf": None, "imgrsinflc": None})
        attr = UDSFormD1cMissingness(d1c_table)
        assert attr._missingness_imgrsinflc() == 8
        assert attr._missingness_imgrsinfct() == 8

        # INFORISCH unanswered is missing data
        form.update({"inforisch": None})
        assert (
            UDSFormD1cMissingness(d1c_table)._missingness_imgrsinflc()
            == INFORMED_MISSINGNESS
        )

    @pytest.mark.parametrize("moded1c", [0, None])
    def test_not_completed(self, d1c_table, moded1c):
        """If D1c not completed, everything falls back to -4."""
        d1c_table["file.info.forms.json"].update({"moded1c": moded1c})
        attr = UDSFormD1cMissingness(d1c_table)

        assert not attr.submitted
        assert attr._missingness_dxptau217() == INFORMED_MISSINGNESS
        assert attr._missingness_ptau217rs() == INFORMED_MISSINGNESS
        assert attr._missingness_apetrs() == INFORMED_MISSINGNESS
        assert attr._missingness_imgrsinflc() == INFORMED_MISSINGNESS
        assert attr._missingness_clinstage() == INFORMED_MISSINGNESS

    def test_langd1c(self, d1c_table):
        """Test LANGD1C missingness."""
        form = d1c_table["file.info.forms.json"]

        form.update({"langd1c": 2})
        assert UDSFormD1cMissingness(d1c_table)._missingness_langd1c() == 2

        form.update({"langd1c": 5})
        assert (
            UDSFormD1cMissingness(d1c_table)._missingness_langd1c()
            == INFORMED_MISSINGNESS
        )
