"""Tests NCRAD genetic attributes."""
import pytest

from nacc_attribute_deriver.attributes.nacc.genetics.ncrad import NCRADAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='function')
def attr() -> NCRADAttribute:
    """Create dummy data and return it in an attribute object."""
    data = {'file': {'info': {'raw': {'ncrad': {'a1': 'e3', 'a2': 'e3'}}}}}

    return NCRADAttribute(SymbolTable(data))


class TestNCRADAttribute:

    def test_create_naccapoe(self, attr):
        """Tests creating NACCAPOE."""
        assert attr._create_naccapoe() == 1

        for key, value in NCRADAttribute.APOE_ENCODINGS.items():
            attr.set_value('a1', key[0])
            attr.set_value('a2', key[1])
            assert attr._create_naccapoe() == value

        # test undefined pairs
        attr.set_value('a1', "e1")
        attr.set_value('a2', "e7")
        assert attr._create_naccapoe() == 9

        # test null case
        attr.table = {}
        assert attr._create_naccapoe() == 9
