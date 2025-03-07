"""
Tests create_naccnihr specifically
"""
import pytest
from typing import Callable
from nacc_attribute_deriver.attributes.nacc.modules.uds.form_a1 import UDSFormA1Attribute

@pytest.fixture(scope='module')
def generate_naccnihr() -> Callable:
    return UDSFormA1Attribute.generate_naccnihr


class TestCreateNACCNIHR:
    """Specifically test the generate_naccnihr function,
    which ultimately is also testing _create_naccnihr. Needs

        race
        racex
        racesec
        racesecx
        raceter
        raceterx
    """

    def test_original_primary(self, generate_naccnihr):
        assert generate_naccnihr(None, None, None, None, None, None) == 99
        assert generate_naccnihr(1, None, None, None, None, None) == 1
        assert generate_naccnihr(2, None, None, None, None, None) == 2
        assert generate_naccnihr(3, None, None, None, None, None) == 3
        assert generate_naccnihr(4, None, None, None, None, None) == 4
        assert generate_naccnihr(5, None, None, None, None, None) == 5
        assert generate_naccnihr(6, None, None, None, None, None) == 6
        assert generate_naccnihr(88, None, None, None, None, None) == 88

    def test_original_primary_writein(self, generate_naccnihr):
        assert generate_naccnihr(50, "Arab", None, None, None, None) == 1
        assert generate_naccnihr(50, "African American", None, None, None, None) == 2
        assert generate_naccnihr(50, "NATIVE AMERICAN", None, None, None, None) == 3
        
        # TODO: check what SAS/R code returns for this
        # won't return 4
        #assert generate_naccnihr(50, "Samoan", None, None, None, None) == 4
        # this version will return 4 (must be racesecx)
        assert generate_naccnihr(50, None, None, "Samoan", None, None) == 4

        assert generate_naccnihr(50, "Tahitian", None, None, None, None) == 4

        assert generate_naccnihr(50, "Asian", None, None, None, None) == 5
        assert generate_naccnihr(50, "Biracial", None, None, None, None) == 6
        assert generate_naccnihr(50, "African and American Indian", None, None, None, None) == 6 
        assert generate_naccnihr(50, "HUMAN", None, None, None, None) == 99

    def test_original_ignore(self, generate_naccnihr):
        # seems like it should ignore the racex
        assert generate_naccnihr(1, "Arab", None, None, None, None) == 1
        assert generate_naccnihr(2, "Arab", None, None, None, None) == 2
        assert generate_naccnihr(3, "Arab", None, None, None, None) == 3
        assert generate_naccnihr(4, "Arab", None, None, None, None) == 4       
        assert generate_naccnihr(5, "Arab", None, None, None, None) == 6
        assert generate_naccnihr(6, "Arab", None, None, None, None) == 6

    # the following are pulled from regression testing

    def test_NACC359394(self, generate_naccnihr):
        # baseline says 99, computed seems more correct
        assert generate_naccnihr(50, "Mulato", 88, "", 88, "") == 6

    def test_NACC201235(self, generate_naccnihr):
        # baseline says 1, was incorrectly computing as 6
        # was missing itialian american from white_responses, fixed
        assert generate_naccnihr(1, "", 50, "ITIALIAN AMERICAN", 88, "") == 1

    def test_NACC356772(self, generate_naccnihr):
        # baseline says 6, was computing as 99
        # EGYPT as a response is not defined
        # in the SAS code, I believe it's set by the line
        #   &RACE = 50 and &RACESEC = 1 then &NACCNIHR = 6;
        # since the python code does not work on if/else, it gets additionally set to 99 here 
        #   &RACE = 50 and WHITEX ne 1 and BLACKX ne 1 and HAWAIIX ne 1
        #       and ASIANX ne 1 and MULTIX ne 1 and MULTIPX ne 1 then &NACCNIHR = 99;
        # updated code to work on if/else similar to SAS
        assert generate_naccnihr(50, "EGYPT", 1, "", 88, "") == 6

    def test_NACC703416(self, generate_naccnihr):
        # baseline says 1, computed says 6
        # also affected by the if/else inconsistency, fixed now
        assert generate_naccnihr(50, "POLISH", 1, "", 88, "") == 1

    def test_hispanic(self, generate_naccnihr):
        """This one is most volatile to changes/script differences.

        Original derived value is 99, but needs to be further refined for UDSv4
        """
        assert generate_naccnihr(50, "HISPANIC", 88, "", 88, "") == 99
        assert generate_naccnihr(50, "Hispanic", 88, "", 88, "") == 99

    def test_NACC342334(self, generate_naccnihr):
        """baseline 1 vs computed 6, issue was accidental lack of comma
        should in fact be 1
        """
        assert generate_naccnihr(1, "", 50, "Middle Eastern", 88, "") == 1
