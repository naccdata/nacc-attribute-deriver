"""Tests UDS Form D1 attributes."""

import pytest
from nacc_attribute_deriver.attributes.nacc.modules.uds.form_d1 import (
    ContributionStatus,
    UDSFormD1Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table(uds_table) -> SymbolTable:
    """Create dummy data and return it in a SymbolTable.

    In this case most will want to manually set fields so only leave
    bare minimum in.
    """
    uds_table["file.info.forms.json"].update(
        {
            "probad": 1,
            "normcog": 1,
            "formver": 2,
        }
    )

    return uds_table


class TestUDSFormD1Attribute:
    def test_generate_mci(self, table, form_prefix):
        """Tests generating MCI."""
        attr = UDSFormD1Attribute(table)
        assert attr.generate_mci() == 0

        for field in ["mciamem", "mciaplus", "mcinon1", "mcinon2"]:
            set_attribute(table, form_prefix, field, 1)
            attr = UDSFormD1Attribute(table)
            assert attr.generate_mci() == 1
            attr = UDSFormD1Attribute(table)
            set_attribute(table, form_prefix, field, 0)

        assert attr.generate_mci() == 0

    def test_create_naccalzp(self, table, form_prefix):
        """Tests creating NACCALZP."""
        attr = UDSFormD1Attribute(table)
        assert attr._create_naccalzp() == 8

        set_attribute(table, form_prefix, "normcog", 0)
        attr = UDSFormD1Attribute(table)
        assert attr._create_naccalzp() == 7

        for field in ["probadif", "possadif", "alzdisif"]:
            for status in ContributionStatus.all():
                set_attribute(table, form_prefix, field, status)
                attr = UDSFormD1Attribute(table)
                assert attr._create_naccalzp() == status
                set_attribute(table, form_prefix, field, None)

        set_attribute(table, form_prefix, "probadif", 3)
        set_attribute(table, form_prefix, "possadif", 2)
        set_attribute(table, form_prefix, "alzdisif", 1)
        attr = UDSFormD1Attribute(table)
        assert attr._create_naccalzp() == 1

    def test_create_nacclbde(self, table, form_prefix):
        """Tests creating NACCLBDE."""
        attr = UDSFormD1Attribute(table)
        assert attr._create_nacclbde() == 8

        set_attribute(table, form_prefix, "normcog", 0)

        # formver != 3
        set_attribute(table, form_prefix, "park", 0)
        set_attribute(table, form_prefix, "dlb", 0)
        attr = UDSFormD1Attribute(table)
        assert attr._create_nacclbde() == 0

        set_attribute(table, form_prefix, "dlb", 1)
        attr = UDSFormD1Attribute(table)
        assert attr._create_nacclbde() == 1

        # formver == 3
        set_attribute(table, form_prefix, "formver", 3)
        for value in [0, 1, 3]:
            set_attribute(table, form_prefix, "lbdis", value)
            attr = UDSFormD1Attribute(table)

            if value == 3:
                assert attr._create_nacclbde() == 0
            else:
                assert attr._create_nacclbde() == value

    def test_create_nacclbdp(self, table, form_prefix):
        """Tests creating NACCLBDP."""
        attr = UDSFormD1Attribute(table)
        assert attr._create_nacclbdp() == 8

        set_attribute(table, form_prefix, "normcog", 0)

        # relies on nacclbde == 0
        set_attribute(table, form_prefix, "lbdis", 0)
        attr = UDSFormD1Attribute(table)
        assert attr._create_nacclbdp() == 7

        set_attribute(table, form_prefix, "formver", 3.0)
        for status in ContributionStatus.all():
            set_attribute(table, form_prefix, "lbdif", status)
            attr = UDSFormD1Attribute(table)
            assert attr._create_nacclbdp() == status

        set_attribute(table, form_prefix, "formver", 2.0)
        set_attribute(table, form_prefix, "dlbif", 3)
        attr = UDSFormD1Attribute(table)
        assert attr._create_nacclbdp() == 3
        set_attribute(table, form_prefix, "parkif", 1)
        attr = UDSFormD1Attribute(table)
        assert attr._create_nacclbdp() == 1

        set_attribute(table, form_prefix, "formver", 3)
        attr = UDSFormD1Attribute(table)
        assert attr._create_nacclbdp() == 3

    def test_naccppme(self, table, form_prefix):
        """Tests NACCPPME."""
        attr = UDSFormD1Attribute(table)
        set_attribute(table, form_prefix, "semdemag", 1)
        assert attr._create_naccppme() == 3

        # this part relies on NACCPPA
        set_attribute(table, form_prefix, "semdemag", 0)
        set_attribute(table, form_prefix, "impnomci", 1)
        assert attr._create_naccppa() == 8
        assert attr._create_naccppme() == 7

        # this causes nodx = 1, so with impnomci = 1, naccppme = 6
        set_attribute(table, form_prefix, "probad", 0)
        assert attr._create_naccppme() == 6

        # v3+ should return None
        set_attribute(table, form_prefix, "formver", 3.0)
        attr = UDSFormD1Attribute(table)
        assert attr._create_naccppme() is None

    def test_ivcstat(self, table, form_prefix):
        """Tests ivcstat - helper variable for fvmci/naccmcii."""
        # normcog already 1 so should return 1
        attr = UDSFormD1Attribute(table)
        assert attr._create_ivcstat() == 1

        # make impnomci 1
        set_attribute(table, form_prefix, "normcog", 0)
        set_attribute(table, form_prefix, "impnomci", 1)
        attr = UDSFormD1Attribute(table)
        assert attr._create_ivcstat() == 1

        # both 0 so ivcstat is 0
        set_attribute(table, form_prefix, "impnomci", 0)
        assert attr._create_ivcstat() == 0

        # followup visits should never override
        set_attribute(table, form_prefix, "impnomci", 1)
        set_attribute(table, form_prefix, "packet", "f")
        attr = UDSFormD1Attribute(table)
        assert attr._create_ivcstat() is None

    def test_fvmci(self, table, form_prefix, working_derived_prefix):
        """Tests fvmci - helper variable for naccmcii."""
        # should return None on initial visits
        attr = UDSFormD1Attribute(table)
        assert attr._create_fvmci() is None

        set_attribute(table, form_prefix, "packet", "f")

        # should return 1 when mci == 1 and fvmci is None
        set_attribute(table, form_prefix, "mcinon1", 1)
        attr = UDSFormD1Attribute(table)
        assert attr._create_fvmci() == 1

        # test when fvmci == 1 and ivcstat == 1
        set_attribute(table, working_derived_prefix, "cross-sectional.fvmci", 0)
        set_attribute(table, working_derived_prefix, "cross-sectional.ivcstat", 1)
        set_attribute(table, form_prefix, "mcinon1", 0)
        set_attribute(table, form_prefix, "demented", 1)
        attr = UDSFormD1Attribute(table)
        assert attr._create_fvmci() == 2

        # mci == 1, return fvmci
        set_attribute(table, working_derived_prefix, "cross-sectional.fvmci", 1)
        set_attribute(table, form_prefix, "mcinon2", 1)
        assert attr._create_fvmci() == 1
