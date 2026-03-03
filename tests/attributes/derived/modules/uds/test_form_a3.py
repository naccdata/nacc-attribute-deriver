"""Tests form A3."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.uds.form_a3 import (
    UDSFormA3Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.utils.errors import AttributeDeriverError

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def table(uds_table) -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    uds_table["file.info.forms.json"].update(
        {
            "a3sub": 1,
            "fadmut": 3,
            "fadmuso": 2,
            "fothmut": 0,
            "sibs": 0,
            "kids": 0,
        }
    )
    return uds_table


@pytest.fixture(scope="function")
def naccfam_table(uds_table) -> SymbolTable:
    """Create dummy data and return it in a SymbolTable."""
    uds_table["file.info.forms.json"].update(
        {
            "a3sub": 1,
            "dadneur": 4,
            "dadprdx": 210,
            "momneur": 8,
            "sib1neu": 8,
            "sib2neu": 8,
            "sib3neu": 8,
            "kid1neu": 8,
            "kid2neu": 8,
            "sibs": 3,
            "kids": 2,
        }
    )
    return uds_table


class TestNACCParent:
    """Focus on the NACCDAD, which is the same as NACCMOM logic."""

    def test_create_naccdad_v4(self, table, form_prefix):
        """Test creating NACCDAD V4."""
        table["file.info.forms.json"].update({"formver": 4, "dadetpr": "00"})
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 0

        set_attribute(table, form_prefix, "dadetpr", "05")
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 1

        # -4 because IVP
        set_attribute(table, form_prefix, "dadetpr", None)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == -4

        # FVP form
        table["file.info.forms.json"].update(
            {"formver": 4, "packet": "F", "nwinfpar": 1, "dadetpr": "00"}
        )

        # when the FVP form still determines it
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 0

        set_attribute(table, form_prefix, "dadetpr", "12")
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 1

        # in this case it will be missing, set to -4
        set_attribute(table, form_prefix, "dadetpr", None)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == INFORMED_MISSINGNESS

        # when previous record informs
        table["_prev_record.info.forms.json"].update({"dadetpr": "00"})
        set_attribute(table, form_prefix, "dadetpr", "66")
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 0

        # 9 carried through via raw data
        table["_prev_record.info.forms.json"].update({"dadetpr": "99"})
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 9

        # test error is thrown if previous was missing value
        table["_prev_record.info.forms.json"].update({"dadetpr": None})
        with pytest.raises(AttributeDeriverError) as e:
            attr = UDSFormA3Attribute(table)
        assert str(e.value) == "dadetpr = 66 but previous dadetpr value not defined"

        # 1 carried through via the resolved
        table["_prev_record.info.resolved"] = {"dadetpr": "09"}
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 1

        # -4 carried through via the resolve
        table["_prev_record.info.resolved"] = {"dadetpr": INFORMED_MISSINGNESS}
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == INFORMED_MISSINGNESS

    def test_create_naccdad_v3(self, table, form_prefix):
        """Tests creating NACCDAD V3."""
        # no data
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == INFORMED_MISSINGNESS

        # when it's properly set
        set_attribute(table, form_prefix, "dadneur", 1)
        set_attribute(table, form_prefix, "dadprdx", 110)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 1

        # not a valid DX code
        set_attribute(table, form_prefix, "dadprdx", 789)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 0

        # unknown
        set_attribute(table, form_prefix, "dadneur", 9)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 9

        # definitely not
        set_attribute(table, form_prefix, "dadneur", 3)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 0

    def test_create_naccdad_v1v2(self, table, form_prefix):
        """Tests creating NACCDAD V1/V2."""
        set_attribute(table, form_prefix, "formver", 1.0)

        # not defined
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == INFORMED_MISSINGNESS

        # properly set to 1
        set_attribute(table, form_prefix, "daddem", 1)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 1

        # set to unkown
        set_attribute(table, form_prefix, "daddem", 9)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 9

        # set to 0
        set_attribute(table, form_prefix, "daddem", 0)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 0

    def test_create_naccdad_flip_flop(self, table, form_prefix, subject_derived_prefix):
        """Tests creating NACCDAD flipping between values at the derived
        level."""
        # no data, use working derived variable
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccdad", 1)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 1

        # 0 and 1 can flip-flop
        set_attribute(table, form_prefix, "dadneur", 3)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 0

        # everything overrides 9
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccdad", 9)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 0

        # -4 does not override a 9
        set_attribute(table, form_prefix, "dadneur", None)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 9

        # -4/9 cannot override a 0 or 1
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccdad", 1)
        set_attribute(table, form_prefix, "dadneur", None)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 1

        set_attribute(table, subject_derived_prefix, "cross-sectional.naccdad", 0)
        set_attribute(table, form_prefix, "dadneur", 9)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 0


class TestNACCFAM:
    """Class to test NACCFAM specifically."""

    def test_create_naccfam_v3_case1(self, table, naccfam_table, form_prefix):
        """Tests creating NACCFAM."""
        set_attribute(table, form_prefix, "dadneur", None)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 9

        set_attribute(naccfam_table, form_prefix, "dadneur", 1)
        set_attribute(naccfam_table, form_prefix, "dadprdx", 400)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 1

        set_attribute(naccfam_table, form_prefix, "dadprdx", 888)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 0

        # another case, both mom and dad neur == 1
        set_attribute(naccfam_table, form_prefix, "dadneur", 1)
        set_attribute(naccfam_table, form_prefix, "dadprdx", 110)
        set_attribute(naccfam_table, form_prefix, "moneur", 1)
        set_attribute(naccfam_table, form_prefix, "momprdx", 50)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 1

        set_attribute(naccfam_table, form_prefix, "dadneur", 4)
        set_attribute(naccfam_table, form_prefix, "dadprdx", 210)
        set_attribute(naccfam_table, form_prefix, "moneur", 8)
        set_attribute(naccfam_table, form_prefix, "momprdx", None)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 0

    def test_create_naccfam_v3_case2(self, table, form_prefix):
        """Tests creating NACCFAM with multiple siblings and varying neu
        statuses."""
        set_attribute(table, form_prefix, "dadneur", 8)
        set_attribute(table, form_prefix, "momneur", 8)
        set_attribute(table, form_prefix, "sib1neu", 9)
        set_attribute(table, form_prefix, "sib2neu", 8)
        set_attribute(table, form_prefix, "sib3neu", 9)
        set_attribute(table, form_prefix, "sib4neu", 8)
        set_attribute(table, form_prefix, "sib5neu", 8)
        set_attribute(table, form_prefix, "sibs", 5)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 9

        set_attribute(table, form_prefix, "dadneur", 4)
        set_attribute(table, form_prefix, "dadprdx", 210)
        set_attribute(table, form_prefix, "sib1neu", 8)
        set_attribute(table, form_prefix, "sib3neu", 8)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 0

        set_attribute(table, form_prefix, "dadneur", 8)
        set_attribute(table, form_prefix, "dadprdx", None)
        set_attribute(table, form_prefix, "sib1neu", 4)
        set_attribute(table, form_prefix, "sib1pdx", 240)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 0

        set_attribute(table, form_prefix, "sib1neu", 1)
        set_attribute(table, form_prefix, "sib1pdx", 240)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 1

    def test_create_naccfam_v2_case1(self, table, form_prefix):
        """Tests creating NACCFAM V2, no kids."""
        set_attribute(table, form_prefix, "formver", 2)
        set_attribute(table, form_prefix, "daddem", 0)
        set_attribute(table, form_prefix, "momdem", 0)
        set_attribute(table, form_prefix, "sib1dem", 0)
        set_attribute(table, form_prefix, "sib2dem", 0)
        set_attribute(table, form_prefix, "sib3dem", 0)
        set_attribute(table, form_prefix, "sibs", 3)
        set_attribute(table, form_prefix, "kids", 0)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 0

        set_attribute(table, form_prefix, "sib2dem", 9)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 9

    def test_create_naccfam_v3_no_sibs_kids(self, table, form_prefix):
        """Tests creating NACCFAM V3, no sibs/kids."""
        set_attribute(table, form_prefix, "dadneur", 8)
        set_attribute(table, form_prefix, "momneur", 8)
        set_attribute(table, form_prefix, "sibs", 0)
        set_attribute(table, form_prefix, "kids", 0)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 0

        # parents provided no data either, set to 9
        set_attribute(table, form_prefix, "dadneur", None)
        set_attribute(table, form_prefix, "momneur", None)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 9

    def test_create_naccfam_v1_v2_no_sibs_kids(self, table, form_prefix):
        """Tests creating NACCFAM V1/V2, no sibs/kids."""
        set_attribute(table, form_prefix, "formver", 1)
        set_attribute(table, form_prefix, "daddem", 0)
        set_attribute(table, form_prefix, "momdem", 0)
        set_attribute(table, form_prefix, "sibs", 0)
        set_attribute(table, form_prefix, "kids", 0)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 0

        set_attribute(table, form_prefix, "formver", 2)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 0

        # parents provided no data either, set to 9
        set_attribute(table, form_prefix, "daddem", None)
        set_attribute(table, form_prefix, "momdem", None)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 9

    def test_create_naccfam_v1(self, table, form_prefix):
        """Tests creating NACCFAM v1."""
        set_attribute(table, form_prefix, "formver", 1)
        set_attribute(table, form_prefix, "daddem", 0)
        set_attribute(table, form_prefix, "momdem", 0)
        set_attribute(table, form_prefix, "sibsdem", 0)
        set_attribute(table, form_prefix, "kidsdem", 0)
        set_attribute(table, form_prefix, "sibs", 5)
        set_attribute(table, form_prefix, "kids", 10)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 0

        set_attribute(table, form_prefix, "sibsdem", 99)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 9

        set_attribute(table, form_prefix, "kidsdem", 9)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 1

    def test_create_naccfam_momneur(self, table, form_prefix):
        """Tests creating NACCFAM when mom triggers event."""
        set_attribute(table, form_prefix, "formver", 3)
        set_attribute(table, form_prefix, "momneur", 1)
        set_attribute(table, form_prefix, "momprdx", 80)
        set_attribute(table, form_prefix, "dadneur", 4)
        set_attribute(table, form_prefix, "dadprdx", 280)
        set_attribute(table, form_prefix, "sibs", 0)
        set_attribute(table, form_prefix, "kids", 1)
        set_attribute(table, form_prefix, "kid1neu", 8)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 1

    def test_create_naccfam_superseded(
        self, table, form_prefix, subject_derived_prefix
    ):
        """Test NACCFAM superseded case."""
        # start with nothing is set
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 9

        set_attribute(table, subject_derived_prefix, "cross-sectional.naccfam", 9)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 9

        set_attribute(table, subject_derived_prefix, "cross-sectional.naccfam", 0)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 0

        set_attribute(table, subject_derived_prefix, "cross-sectional.naccfam", 1)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 1

    def test_create_naccfam_v3_all_8(self, uds_table):
        """Test NACCFAM when all are NEUR/NEU values are 8 in V3."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3,
                "a3sub": 1,
                "momneur": 8,
                "momprdx": None,
                "dadneur": 8,
                "dadprdx": None,
                "sibs": 1,
                "sib1neu": 8,
                "sib1pdx": None,
                "kids": 2,
                "kid1neu": 8,
                "kid1pdx": None,
                "kid2neu": 8,
                "kid2pdx": None,
            }
        )

        attr = UDSFormA3Attribute(uds_table)
        assert attr._create_naccfam() == 0

    def test_create_naccfam_all_8_except_one(self, uds_table):
        """Test NACCFAM when all are 8 expect dad which is 9; this should make
        it a9."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 3,
                "a3sub": 1,
                "momneur": 8,
                "momprdx": None,
                "dadneur": 9,
                "dadprdx": None,
                "sibs": 1,
                "sib1neu": 8,
                "sib1pdx": None,
                "kids": 2,
                "kid1neu": 8,
                "kid1pdx": None,
                "kid2neu": 8,
                "kid2pdx": None,
            }
        )

        attr = UDSFormA3Attribute(uds_table)
        assert attr._create_naccfam() == 9


class TestUDSFormA3Attribute:
    """Other derived variables."""

    def test_create_naccam(self, table, form_prefix, subject_derived_prefix):
        """Tests creating NACCAM."""
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccam() == 3
        set_attribute(table, form_prefix, "fadmut", 0)
        assert attr._create_naccam() == 0

        # test superseded cases
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccam", 2)
        assert attr._create_naccam() == 2
        set_attribute(table, form_prefix, "fadmut", 0)
        assert attr._create_naccam() == 2
        set_attribute(table, form_prefix, "fadmut", None)
        assert attr._create_naccam() == 2

        set_attribute(table, subject_derived_prefix, "cross-sectional.naccam", 0)
        assert attr._create_naccam() == 0
        set_attribute(table, form_prefix, "fadmut", 8)
        assert attr._create_naccam() == 8

        set_attribute(table, subject_derived_prefix, "cross-sectional.naccam", 9)
        assert attr._create_naccam() == 8
        set_attribute(table, form_prefix, "fadmut", 0)
        assert attr._create_naccam() == 0

    def test_create_naccams(self, table, form_prefix, subject_derived_prefix):
        """Tests creating NACCAMS."""
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccams() == 2
        set_attribute(table, form_prefix, "fadmuso", 9)
        assert attr._create_naccams() == 9
        set_attribute(table, form_prefix, "fadmuso", None)
        assert attr._create_naccams() == 9

        # test superseded cases
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccams", 9)
        assert attr._create_naccams() == 9
        set_attribute(table, form_prefix, "fadmuso", 9)
        assert attr._create_naccams() == 9

    def test_create_naccom(self, table, form_prefix, subject_derived_prefix):
        """Test creating NACCOM."""
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccom() == 0
        set_attribute(table, form_prefix, "fothmut", 1)
        assert attr._create_naccom() == 1
        set_attribute(table, form_prefix, "fothmut", 9)
        assert attr._create_naccom() == 9

        # check V2 case - should be -4 since no known value
        set_attribute(table, form_prefix, "formver", 2)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccom() == -4

        # test superseded cases
        set_attribute(table, form_prefix, "formver", 3)
        attr = UDSFormA3Attribute(table)
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccom", 9)
        assert attr._create_naccom() == 9
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccom", 0)
        assert attr._create_naccom() == 0
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccom", 1)
        assert attr._create_naccom() == 1

        # check V2 case - should use known value
        set_attribute(table, form_prefix, "formver", 2)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccom() == 1

    def test_create_naccam_v3_case(self, table, form_prefix, subject_derived_prefix):
        """Test create NACCAM when there are a pile of V2 visits before a V3
        one.

        Starts at -4 and expected to change to 9 once we get to V3.
        """
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccam", -4)
        set_attribute(table, form_prefix, "formver", 2)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccam() == -4

        set_attribute(table, form_prefix, "formver", 3)
        set_attribute(table, form_prefix, "fadmut", 9)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccam() == 9
