"""Tests NIAGADS genetic attributes."""
import pytest

from nacc_attribute_deriver.attributes.nacc.genetics.niagads import NIAGADSAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='function')
def attr() -> NIAGADSAttribute:
    """Create dummy data and return it in an attribute object."""
    data = {
        'file': {
            'info': {
                'raw': {
                    'niagads_gwas': "NG00000",
                    'niagads_exomechip': "NG00000, NG00001",
                    'niagads_wgs': "0",
                    'niagads_wes': None
                }
            }
        }
    }

    return NIAGADSAttribute(SymbolTable(data))


class TestNIAGADSAttribute:

    def test_create_niagads(self, attr):
        """Tests creating NGDS* variables."""
        assert attr._create_ngdsgwas() == 1
        assert attr._create_ngdsexom() == 1
        assert attr._create_ngdswgs() == 0
        assert attr._create_ngdswes() == 0
