"""Tests UDS Form D1 attributes."""

import pytest
import random

from nacc_attribute_deriver.attributes.derived.modules.uds.form_d1 import (
    UDSFormDxAttribute,
)
from nacc_attribute_deriver.attributes.derived.modules.uds.form_d1a import (
    UDSFormD1aAttribute,
)
from nacc_attribute_deriver.attributes.derived.modules.uds.form_d1b import (
    ContributionStatus,
    UDSFormD1bAttribute,
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
        attr = UDSFormDxAttribute(table)
        assert attr.generate_mci() == 0

        for field in ["mciamem", "mciaplus", "mcinon1", "mcinon2"]:
            set_attribute(table, form_prefix, field, 1)
            attr = UDSFormDxAttribute(table)
            assert attr.generate_mci() == 1
            attr = UDSFormDxAttribute(table)
            set_attribute(table, form_prefix, field, 0)

        assert attr.generate_mci() == 0


class TestUDSFormD1bAttribute:
    def test_create_naccalzp(self, table, form_prefix):
        """Tests creating NACCALZP."""
        attr = UDSFormD1bAttribute(table)
        assert attr._create_naccalzp() == 8

        set_attribute(table, form_prefix, "normcog", 0)
        attr = UDSFormD1bAttribute(table)
        assert attr._create_naccalzp() == 7

        for field in ["probadif", "possadif", "alzdisif"]:
            for status in ContributionStatus.all():
                set_attribute(table, form_prefix, field, status)
                attr = UDSFormD1bAttribute(table)
                assert attr._create_naccalzp() == status
                set_attribute(table, form_prefix, field, None)

        set_attribute(table, form_prefix, "probadif", 3)
        set_attribute(table, form_prefix, "possadif", 2)
        set_attribute(table, form_prefix, "alzdisif", 1)
        attr = UDSFormD1bAttribute(table)
        assert attr._create_naccalzp() == 1

    def test_create_nacclbde(self, table, form_prefix):
        """Tests creating NACCLBDE."""
        attr = UDSFormD1bAttribute(table)
        assert attr._create_nacclbde() == 8

        set_attribute(table, form_prefix, "normcog", 0)

        # formver != 3
        set_attribute(table, form_prefix, "park", 0)
        set_attribute(table, form_prefix, "dlb", 0)
        attr = UDSFormD1bAttribute(table)
        assert attr._create_nacclbde() == 0

        set_attribute(table, form_prefix, "dlb", 1)
        attr = UDSFormD1bAttribute(table)
        assert attr._create_nacclbde() == 1

        # formver == 3
        set_attribute(table, form_prefix, "formver", 3)
        for value in [0, 1, 3]:
            set_attribute(table, form_prefix, "lbdis", value)
            attr = UDSFormD1bAttribute(table)

            if value == 3:
                assert attr._create_nacclbde() == 0
            else:
                assert attr._create_nacclbde() == value

    def test_create_nacclbdp(self, table, form_prefix):
        """Tests creating NACCLBDP."""
        attr = UDSFormD1bAttribute(table)
        assert attr._create_nacclbdp() == 8

        set_attribute(table, form_prefix, "normcog", 0)

        # relies on nacclbde == 0
        set_attribute(table, form_prefix, "lbdis", 0)
        attr = UDSFormD1bAttribute(table)
        assert attr._create_nacclbdp() == 7

        set_attribute(table, form_prefix, "formver", 3.0)
        for status in ContributionStatus.all():
            set_attribute(table, form_prefix, "lbdif", status)
            attr = UDSFormD1bAttribute(table)
            assert attr._create_nacclbdp() == status

        set_attribute(table, form_prefix, "formver", 2.0)
        set_attribute(table, form_prefix, "dlbif", 3)
        attr = UDSFormD1bAttribute(table)
        assert attr._create_nacclbdp() == 3
        set_attribute(table, form_prefix, "parkif", 1)
        attr = UDSFormD1bAttribute(table)
        assert attr._create_nacclbdp() == 1

        set_attribute(table, form_prefix, "formver", 3)
        attr = UDSFormD1bAttribute(table)
        assert attr._create_nacclbdp() == 3


class TestUDSFormD1aAttribute:
    def test_naccppme(self, table, form_prefix):
        """Tests NACCPPME."""
        attr = UDSFormD1aAttribute(table)
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

        # v3+ should return -4
        set_attribute(table, form_prefix, "formver", 3.0)
        attr = UDSFormD1aAttribute(table)
        assert attr._create_naccppme() == -4

    def test_naccmcii_initial_visit(self, uds_table):
        """Test NACCMCII and its helper working variable at the initial
        visit."""
        uds_table["file.info.forms.json.packet"] = "I"
        uds_table["file.info.forms.json.normcog"] = 1

        # no mci/demented case
        attr = UDSFormD1aAttribute(uds_table)
        assert attr._create_naccmcii() == 8
        assert attr._create_naccmcii_working() == 2

        # mci case
        mci_var = random.choice(["mciamem", "mciaplus", "mcinon1", "mcinon2"])
        uds_table["file.info.forms.json"].update({"normcog": 0, mci_var: 1})
        attr = UDSFormD1aAttribute(uds_table)
        assert attr._create_naccmcii() == 8
        assert attr._create_naccmcii_working() == 8

        # demented case
        uds_table["file.info.forms.json"].update(
            {"normcog": 0, mci_var: 0, "demented": 1}
        )
        attr = UDSFormD1aAttribute(uds_table)
        assert attr._create_naccmcii() == 8
        assert attr._create_naccmcii_working() == 8

    def test_naccmcii_followup_visit(self, uds_table):
        """Test NACCMCII and its helper working variable at follow-up
        visits."""
        uds_table["file.info.forms.json.packet"] = "F"
        uds_table["file.info.forms.json.normcog"] = 1

        # start NACCMCII at 2 or 0 has only had an initial visit
        # with no MCI/DEMENTED status
        uds_table.update(
            {
                "subject": {
                    "info": {
                        "working": {
                            "cross-sectional": {
                                "naccmcii-working": random.choice([0, 2])
                            }
                        }
                    }
                }
            }
        )
        # nothing reported on this visit, so returns 0
        attr = UDSFormD1aAttribute(uds_table)
        assert attr._create_naccmcii() == 0
        assert attr._create_naccmcii_working() == 0

        # set progressed directly to dementia
        uds_table["file.info.forms.json"].update({"normcog": 0, "demented": 1})
        attr = UDSFormD1aAttribute(uds_table)
        assert attr._create_naccmcii() == 8
        assert attr._create_naccmcii_working() == 3

        # set progressed to MCI
        mci_var = random.choice(["mciamem", "mciaplus", "mcinon1", "mcinon2"])
        uds_table["file.info.forms.json"].update(
            {"normcog": 0, "demented": 0, mci_var: 1}
        )
        attr = UDSFormD1aAttribute(uds_table)
        assert attr._create_naccmcii() == 1
        assert attr._create_naccmcii_working() == 1

        # now start NACCMCII at 1, 3, or 8; should just return as-is
        # regardless of what's been set
        naccmcii = random.choice([1, 3, 8])
        uds_table["subject.info.working.cross-sectional.naccmcii-working"] = naccmcii
        attr = UDSFormD1aAttribute(uds_table)
        assert attr._create_naccmcii() == 1 if naccmcii == 1 else 8
        assert attr._create_naccmcii_working() == naccmcii
