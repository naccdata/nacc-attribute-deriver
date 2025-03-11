import pytest

from nacc_attribute_deriver.attributes.nacc.modules.np.form_np import NPFormAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='function')
def np_form_attribute() -> NPFormAttribute:
    """Create dummy data and return it in an attribute object."""
    data = {
        'file': {
            'info': {
                'np': {
                    'npgross': 2,
                    'npvasc': 3,
                    'npneur': 1,
                    'npold': 1,
                    'npmicro': 1,
                    'nphem': 1,
                    'nparter': 1,
                    'nplewy': 5,
                    'formver': 1,
                    'npbraak': 7,
                    'nphemo': 1,
                    'npoldd': 1,
                    'nplbod': 4
                }
            }
        }
    }
    return NPFormAttribute(SymbolTable(data))


@pytest.fixture(scope='function')
def np_form_nulls() -> NPFormAttribute:
    """Create dummy data and return it in an attribute object."""
    data = {'file': {'info': {'np': {'formver': 1}}}}

    return NPFormAttribute(SymbolTable(data))


class TestHelpers:

    def test_mapgross_null(self, np_form_nulls):
        assert np_form_nulls._mapgross(None) is None

    def test_mapsub4_null(self, np_form_nulls):
        assert np_form_nulls._mapsub4(None) == 9

    def test_mapvasc_null(self, np_form_nulls):
        assert np_form_nulls._mapvasc(None) is None
        assert np_form_nulls._mapvasc(1) == 1

    def test_mapv9_null(self, np_form_nulls):
        assert np_form_nulls._mapv9(None) == 9

    def test_mapsub1_null(self, np_form_nulls):
        assert np_form_nulls._mapsub1(None) == 9

    def test_maylewy_null(self, np_form_nulls):
        assert np_form_nulls._maplewy() is None

    def test_mapgross(self, np_form_attribute):
        assert np_form_attribute._mapgross(0) == 0
        np_form_attribute.set_value('npgross', 9)
        assert np_form_attribute._mapgross(0) == 9

    def test_mapsub4(self, np_form_attribute):
        assert np_form_attribute._mapsub4(1) == 3
        assert np_form_attribute._mapsub4(5) == 8
        assert np_form_attribute._mapsub4(6) == 9

    def test_mapv9(self, np_form_attribute):
        assert np_form_attribute._mapv9(1) == 1
        assert np_form_attribute._mapv9(2) == 0
        assert np_form_attribute._mapv9(3) == 8
        assert np_form_attribute._mapv9(4) == 9

    def test_mapvasc(self, np_form_attribute):
        assert np_form_attribute._mapvasc(0) == 0
        np_form_attribute.set_value('npgross', 9)
        assert np_form_attribute._mapvasc(0) == 9
        np_form_attribute.set_value('npvasc', 3)
        np_form_attribute.set_value('npgross', 1)
        assert np_form_attribute._mapvasc(0) == 8

    def test_mapsub1(self, np_form_attribute):
        assert np_form_attribute._mapsub1(1) == 0
        assert np_form_attribute._mapsub1(5) == 8
        assert np_form_attribute._mapsub1(6) == 9

    def test_maplewy(self, np_form_attribute):
        assert np_form_attribute._maplewy() == 0
        np_form_attribute.set_value('nplewy', 6)
        assert np_form_attribute._maplewy() == 8


class TestCreateNACCBRAA:

    def test_create_naccbraa_null(self, np_form_nulls):
        assert np_form_nulls._create_naccbraa() is None
        np_form_nulls.set_value('formver', 8)
        assert np_form_nulls._create_naccbraa() is None
        np_form_nulls.set_value('formver', 10)
        assert np_form_nulls._create_naccbraa() is None

    def test_create_naccbraa(self, np_form_attribute):
        assert np_form_attribute._create_naccbraa() == 0
        np_form_attribute.set_value('formver', 10)
        assert np_form_attribute._create_naccbraa() == 7


class TestCreateNACCNEUR:

    def test_create_naccneur_null(self, np_form_nulls):
        assert np_form_nulls._create_naccneur() is None
        np_form_nulls.set_value('formver', 8)
        assert np_form_nulls._create_naccneur(
        ) == 9  # WARNING: Different behavior here!
        np_form_nulls.set_value('formver', 10)
        assert np_form_nulls._create_naccneur() is None

    def test_create_naccneur(self, np_form_attribute):
        assert np_form_attribute._create_naccneur() == 3
        np_form_attribute.set_value('formver', 10)
        assert np_form_attribute._create_naccneur() == 1


class TestCreateNACCMICR:

    def test_create_naccmicr_null(self, np_form_nulls):
        assert np_form_nulls._create_naccmicr() is None
        np_form_nulls.set_value('formver', 8)
        assert np_form_nulls._create_naccmicr(
        ) == 9  # WARNING: Different behavior here
        np_form_nulls.set_value('formver', 10)
        assert np_form_nulls._create_naccmicr() is None

    def test_create_naccmicr(self, np_form_attribute):
        assert np_form_attribute._create_naccmicr() == 1
        np_form_attribute.set_value('formver', 10)
        assert np_form_attribute._create_naccmicr() == 1


class TestCreateNACCHEM:

    def test_create_nacchem_null(self, np_form_nulls):
        assert np_form_nulls._create_nacchem() is None
        np_form_nulls.set_value('formver', 8)
        assert np_form_nulls._create_nacchem(
        ) == 9  # WARNING: Different behavior here
        np_form_nulls.set_value('formver', 10)
        assert np_form_nulls._create_nacchem(
        ) == 9  # WARNING: Different behavior here

    def test_create_nacchem(self, np_form_attribute):
        assert np_form_attribute._create_nacchem() == 1
        np_form_attribute.set_value('formver', 10)
        assert np_form_attribute._create_nacchem() == 1


class TestCreateNACCARTE:

    def test_create_naccarte_null(self, np_form_nulls):
        assert np_form_nulls._create_naccarte() is None
        np_form_nulls.set_value('formver', 8)
        assert np_form_nulls._create_naccarte(
        ) == 9  # WARNING: Different behavior here
        np_form_nulls.set_value('formver', 10)
        assert np_form_nulls._create_naccarte() is None

    def test_create_naccarte(self, np_form_attribute):
        assert np_form_attribute._create_naccarte() == 0
        np_form_attribute.set_value('formver', 10)
        assert np_form_attribute._create_naccarte() == 1


class TestCreateNACCLEWY:

    def test_create_nacclewy_null(self, np_form_nulls):
        assert np_form_nulls._create_nacclewy() is None
        np_form_nulls.set_value('formver', 8)
        assert np_form_nulls._create_nacclewy() is None
        np_form_nulls.set_value('formver', 10)
        assert np_form_nulls._create_nacclewy() is None

    def test_create_nacclewy(self, np_form_attribute):
        assert np_form_attribute._create_nacclewy() == 0
        np_form_attribute.set_value('formver', 10)
        assert np_form_attribute._create_nacclewy() == 2
