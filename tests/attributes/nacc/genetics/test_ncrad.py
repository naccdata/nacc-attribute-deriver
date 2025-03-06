"""Tests NCRAD genetic attributes."""
import pytest

from nacc_attribute_deriver.attributes.nacc.genetics.ncrad import NCRADAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='function')
def attr() -> NCRADAttribute:
    """Create dummy data and return it in an attribute object."""
    data = {'ncrad': {'info': {'raw': {'apoe': 5}}}}

    return NCRADAttribute(SymbolTable(data))


class TestNCRADAttribute:

    def test_create_naccapoe(self, attr):
        """Tests creating NACCAPOE."""
        assert attr._create_naccapoe() == 5

        # test null case
        attr.table = {}
        assert attr._create_naccapoe() == 9
