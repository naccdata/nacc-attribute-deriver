"""Tests form A3."""

import pytest
from nacc_attribute_deriver.attributes.derived.modules.uds.form_a3 import (
    UDSFormA3Attribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

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


class TestUDSFormA3Attribute:
    def test_create_naccdad_v4(self, table, form_prefix):
        """Test creating NACCDAD V4."""
        table["file.info.forms.json"].update({"formver": 4, "dadetpr": "00"})
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 0

        set_attribute(table, form_prefix, "dadetpr", "05")
        assert attr._create_naccdad() == 1

        # -4 because IVP
        set_attribute(table, form_prefix, "dadetpr", None)
        assert attr._create_naccdad() == -4

        # FVP form
        table["file.info.forms.json"].update(
            {"formver": 4, "packet": "F", "dadetpr": "00"}
        )

        # when the FVP form still determines it
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 0

        set_attribute(table, form_prefix, "dadetpr", "12")
        assert attr._create_naccdad() == 1

        # in this case it will be 9, -4 only set in IVP
        set_attribute(table, form_prefix, "dadetpr", None)
        assert attr._create_naccdad() == 9

        # when previous record informs
        table["file.info.forms.json"].update(
            {
                "nwinfpar": 0,  # triggers to check previous record
                "dadetpr": "09",
            }
        )
        table["_prev_record.info.forms.json"].update({"dadetpr": "00"})
        assert attr._create_naccdad() == 0

        # now the current form's 09 will trigger look at current
        set_attribute(table, form_prefix, "nwinfpar", 1)
        assert attr._create_naccdad() == 1

        # now the current form's 66 will trigger look at prev
        set_attribute(table, form_prefix, "dadetpr", "66")
        assert attr._create_naccdad() == 0

        # test -4 or 9 is carried forward
        table["_prev_record.info.forms.json"].update({"dadetpr": None, "packet": "I"})
        assert attr._create_naccdad() == -4

        table["_prev_record.info.forms.json"].update(
            {"dadetpr": "nonsesnse to turn into a 9", "packet": "I"}
        )
        assert attr._create_naccdad() == 9

        # pull from missingness when previous record is not IVP
        table["_prev_record.info.forms.json"].update({"dadetpr": "66", "packet": "F"})
        table["_prev_record.info.forms.resolved"] = {"dadetpr": "01"}
        assert attr._create_naccdad() == 1

        table["_prev_record.info.forms.resolved"] = {"dadetpr": "00"}
        assert attr._create_naccdad() == 0

    def test_create_naccdad_v3(self, table, form_prefix):
        """Tests creating NACCDAD V3."""
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 9

        set_attribute(table, form_prefix, "dadneur", 1)
        set_attribute(table, form_prefix, "dadprdx", 110)
        assert attr._create_naccdad() == 1

        set_attribute(table, form_prefix, "dadprdx", 789)
        assert attr._create_naccdad() == 0

        set_attribute(table, form_prefix, "dadneur", 9)
        assert attr._create_naccdad() == 0

        set_attribute(table, form_prefix, "dadneur", 3)
        assert attr._create_naccdad() == 0

    def test_create_naccdad_v1v2(self, table, form_prefix):
        """Tests creating NACCDAD V1/V2."""
        set_attribute(table, form_prefix, "formver", 1.0)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccdad() == 9

        set_attribute(table, form_prefix, "daddem", 1)
        assert attr._create_naccdad() == 1

        set_attribute(table, form_prefix, "daddem", 9)
        assert attr._create_naccdad() == 9

        set_attribute(table, form_prefix, "daddem", 0)
        assert attr._create_naccdad() == 0

    # def test_create_naccdad_superseded(
    #     self, table, form_prefix, subject_derived_prefix
    # ):
    #     """Tests creating NACCDAD when an already-computed value supersedes."""
    #     attr = UDSFormA3Attribute(table)
    #     set_attribute(table, subject_derived_prefix, "cross-sectional.naccdad", 1)
    #     assert attr._create_naccdad() == 1

    #     set_attribute(table, form_prefix, "dadneur", 3)
    #     assert attr._create_naccdad() == 1

    #     set_attribute(table, subject_derived_prefix, "cross-sectional.naccdad", 9)
    #     assert attr._create_naccdad() == 0
    #     set_attribute(table, form_prefix, "dadneur", None)
    #     assert attr._create_naccdad() == 9

    # def test_create_naccfam(self, table, naccfam_table, form_prefix):
    #     """Tests creating NACCFAM."""
    #     attr = UDSFormA3Attribute(table)
    #     set_attribute(table, form_prefix, "dadneur", None)
    #     assert attr._create_naccfam() == 9

    #     set_attribute(naccfam_table, form_prefix, "dadneur", 1)
    #     set_attribute(naccfam_table, form_prefix, "dadprdx", 400)
    #     assert attr._create_naccfam() == 1

    #     set_attribute(naccfam_table, form_prefix, "dadprdx", 888)
    #     assert attr._create_naccfam() == 0

    #     # another case, both mom and dad neur == 1
    #     set_attribute(naccfam_table, form_prefix, "dadneur", 1)
    #     set_attribute(naccfam_table, form_prefix, "dadprdx", 110)
    #     set_attribute(naccfam_table, form_prefix, "moneur", 1)
    #     set_attribute(naccfam_table, form_prefix, "momprdx", 50)
    #     assert attr._create_naccfam() == 1

    #     set_attribute(naccfam_table, form_prefix, "dadneur", 4)
    #     set_attribute(naccfam_table, form_prefix, "dadprdx", 210)
    #     set_attribute(naccfam_table, form_prefix, "moneur", 8)
    #     set_attribute(naccfam_table, form_prefix, "momprdx", None)
    #     assert attr._create_naccfam() == 0

    def test_create_naccfam_v3(self, table, form_prefix):
        """Tests creating NACCFAM with multiple siblings and varying neu
        statuses."""
        attr = UDSFormA3Attribute(table)
        set_attribute(table, form_prefix, "dadneur", 8)
        set_attribute(table, form_prefix, "momneur", 8)
        set_attribute(table, form_prefix, "sib1neu", 9)
        set_attribute(table, form_prefix, "sib2neu", 8)
        set_attribute(table, form_prefix, "sib3neu", 9)
        set_attribute(table, form_prefix, "sib4neu", 8)
        set_attribute(table, form_prefix, "sib5neu", 8)
        set_attribute(table, form_prefix, "sibs", 5)
        assert attr._create_naccfam() == 9

        set_attribute(table, form_prefix, "dadneur", 4)
        set_attribute(table, form_prefix, "dadprdx", 210)
        set_attribute(table, form_prefix, "sib1neu", 8)
        set_attribute(table, form_prefix, "sib3neu", 8)
        assert attr._create_naccfam() == 0

        set_attribute(table, form_prefix, "dadneur", 8)
        set_attribute(table, form_prefix, "dadprdx", None)
        set_attribute(table, form_prefix, "sib1neu", 4)
        set_attribute(table, form_prefix, "sib1pdx", 240)
        assert attr._create_naccfam() == 0

        set_attribute(table, form_prefix, "sib1neu", 1)
        set_attribute(table, form_prefix, "sib1pdx", 240)
        assert attr._create_naccfam() == 1

    def test_create_naccfam_v2(self, table, form_prefix):
        """Tests creating NACCFAM V2."""
        set_attribute(table, form_prefix, "formver", 2)
        attr = UDSFormA3Attribute(table)
        set_attribute(table, form_prefix, "daddem", 0)
        set_attribute(table, form_prefix, "momdem", 0)
        set_attribute(table, form_prefix, "sib1dem", 0)
        set_attribute(table, form_prefix, "sib2dem", 0)
        set_attribute(table, form_prefix, "sib3dem", 0)
        set_attribute(table, form_prefix, "sibs", 5)
        assert attr._create_naccfam() == 0

        set_attribute(table, form_prefix, "sib2dem", 9)
        assert attr._create_naccfam() == 9

    def test_create_naccfam_v3_no_sibs_kids(self, table, form_prefix):
        """Tests creating NACCFAM V3, no sibs/kids."""
        attr = UDSFormA3Attribute(table)
        set_attribute(table, form_prefix, "dadneur", 0)
        set_attribute(table, form_prefix, "momneur", 0)
        set_attribute(table, form_prefix, "sibs", 0)
        set_attribute(table, form_prefix, "kids", 0)
        assert attr._create_naccfam() == 0

    def test_create_naccfam_v1_v2_no_sibs_kids(self, table, form_prefix):
        """Tests creating NACCFAM V1/V2, no sibs/kids."""
        set_attribute(table, form_prefix, "formver", 1)
        attr = UDSFormA3Attribute(table)
        set_attribute(table, form_prefix, "daddem", 0)
        set_attribute(table, form_prefix, "momdem", 0)
        set_attribute(table, form_prefix, "sibs", 0)
        set_attribute(table, form_prefix, "kids", 0)
        assert attr._create_naccfam() == 0

        set_attribute(table, form_prefix, "formver", 2)
        attr = UDSFormA3Attribute(table)
        assert attr._create_naccfam() == 0

    def test_create_naccfam_v1(self, table, form_prefix):
        """Tests creating NACCFAM v1."""
        set_attribute(table, form_prefix, "formver", 1)
        attr = UDSFormA3Attribute(table)
        set_attribute(table, form_prefix, "daddem", 0)
        set_attribute(table, form_prefix, "momdem", 0)
        set_attribute(table, form_prefix, "sibsdem", 0)
        set_attribute(table, form_prefix, "kidsdem", 0)
        set_attribute(table, form_prefix, "sibs", 5)
        set_attribute(table, form_prefix, "kids", 10)
        assert attr._create_naccfam() == 0

        set_attribute(table, form_prefix, "sibsdem", 99)
        assert attr._create_naccfam() == 9
        set_attribute(table, form_prefix, "kidsdem", 9)
        assert attr._create_naccfam() == 1

    # def test_create_naccfam_superseded(
    #     self, table, form_prefix, subject_derived_prefix
    # ):
    #     """Test NACCFAM superseded case."""
    #     attr = UDSFormA3Attribute(table)
    #     set_attribute(table, subject_derived_prefix, "cross-sectional.naccfam", 9)
    #     assert attr._create_naccfam() == 9

    #     set_attribute(table, subject_derived_prefix, "cross-sectional.naccfam", 0)
    #     assert attr._create_naccfam() == 9

    #     set_attribute(table, subject_derived_prefix, "cross-sectional.naccfam", 1)
    #     assert attr._create_naccfam() == 1

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

        # test superseded cases
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccom", 9)
        assert attr._create_naccom() == 9
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccom", 0)
        assert attr._create_naccom() == 0
        set_attribute(table, subject_derived_prefix, "cross-sectional.naccom", 1)
        assert attr._create_naccom() == 1
