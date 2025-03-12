"""Tests deriving MQT SCAN variables."""
import pytest

from nacc_attribute_deriver.attributes.mqt.scan import MQTSCANAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='function')
def table() -> SymbolTable:
    """Create dummy data - since tests need to augment it often just return the
    SymbolTable."""
    data = {
        'file': {
            'info': {
                'scan': {
                    "mri": {
                        "seriestype": "T1w",
                        "cerebrumtcv": "2.5",
                        "wmh": "3.5",
                        "amyloid_status": "1"  # TODO may need to change type
                    },
                    "pet": {
                        "radiotracer": "1",
                        "centiloids": "1.5"
                    }
                }
            }
        },
        'subject': {
            'info': {
                'derived': {
                    'scan_mri_dates': [
                        '1995-01-01', '1996-01-01', '1997-01-01', '1997-02-02',
                        '1997-03-03'
                    ],
                    'scan_pet_dates': ['2000-12-12']
                }
            }
        }
    }

    return SymbolTable(data)


class TestMQTSCANAttribute:

    def test_create_scan_mri_scan_types(self, table):
        """Tests _create_scan_mri_scan_types, which should just return the
        seriestype."""
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_mri_scan_types() == "T1w"

        # empty
        attr = MQTSCANAttribute(SymbolTable({}))
        assert attr._create_scan_mri_scan_types() is None

    def test_create_volume_analysis_indicator(self, table):
        """Tests _create_volume_analysis_indicator, which looks at cerebrumtcv
        when series_type == T1w."""
        attr = MQTSCANAttribute(table)
        assert attr._create_volume_analysis_indicator()

        # not T1w, should return False
        table['file.info.scan.mri.seriestype'] = 'dummy'
        attr = MQTSCANAttribute(table)
        assert not attr._create_volume_analysis_indicator()

        # 0 case, is a valid number so should return True
        table['file.info.scan.mri.seriestype'] = 'T1w'
        table['file.info.scan.mri.cerebrumtcv'] = '0'
        attr = MQTSCANAttribute(table)
        assert attr._create_volume_analysis_indicator()

        # empty
        attr = MQTSCANAttribute(SymbolTable({}))
        assert not attr._create_volume_analysis_indicator()

    def test_create_t1_wmh_indicator(self, table):
        """Tests _create_t1_wmh_indicator, which looks at wmh when series_type.

        == "T1w".
        """
        attr = MQTSCANAttribute(table)
        assert attr._create_t1_wmh_indicator()

        # not T1w, should return False
        table['file.info.scan.mri.seriestype'] = 'dummy'
        attr = MQTSCANAttribute(table)
        assert not attr._create_t1_wmh_indicator()

        # 0 case, is a valid number so should return True
        table['file.info.scan.mri.seriestype'] = 'T1w'
        table['file.info.scan.mri.wmh'] = '0'
        attr = MQTSCANAttribute(table)
        assert attr._create_t1_wmh_indicator()

        # empty
        attr = MQTSCANAttribute(SymbolTable({}))
        assert not attr._create_t1_wmh_indicator()

    def test_create_flair_wmh_indicator(self, table):
        """Tests _create_flair_wmh_indicator, which looks at wmh when
        series_type == "T2w"."""
        # not T2w, should return False
        attr = MQTSCANAttribute(table)
        assert not attr._create_flair_wmh_indicator()

        # now T2w, should pass
        table['file.info.scan.mri.seriestype'] = 'T2w'
        attr = MQTSCANAttribute(table)
        assert attr._create_flair_wmh_indicator()

        # 0 case, is a valid number so should return True
        table['file.info.scan.mri.wmh'] = '0'
        attr = MQTSCANAttribute(table)
        assert attr._create_flair_wmh_indicator()

        # empty
        attr = MQTSCANAttribute(SymbolTable({}))
        assert not attr._create_flair_wmh_indicator()

    def test_create_flair_volume_analysis_indicator(self, table):
        """Tests _create_flair_wmh_indicator, which looks at cerebrumtcv when
        series_type == "T2w"."""
        # not T2w, should return False
        attr = MQTSCANAttribute(table)
        assert not attr._create_flair_volume_analysis_indicator()

        # now T2w, should pass
        table['file.info.scan.mri.seriestype'] = 'T2w'
        attr = MQTSCANAttribute(table)
        assert attr._create_flair_volume_analysis_indicator()

        # 0 case, is a valid number so should return True
        table['file.info.scan.mri.cerebrumtcv'] = '0'
        attr = MQTSCANAttribute(table)
        assert attr._create_flair_volume_analysis_indicator()

        # empty
        attr = MQTSCANAttribute(SymbolTable({}))
        assert not attr._create_flair_volume_analysis_indicator()

    def test_create_scan_pet_scan_types(self, table):
        """Tests _create_scan_pet_scan_types, loop over all options."""
        for k, v in MQTSCANAttribute.TRACER_MAPPING.items():
            # convert to string just to make sure type conversion is correct
            table['file.info.scan.pet.radiotracer'] = str(k)
            attr = MQTSCANAttribute(table)
            assert attr._create_scan_pet_scan_types() == v

        # None case
        attr = MQTSCANAttribute(SymbolTable({}))
        assert attr._create_scan_pet_scan_types() is None

    def test_create_scan_pet_amyloid_tracers(self, table):
        """Tests _create_scan_pet_amyloid_tracers, loop over all options."""
        for k, v in MQTSCANAttribute.TRACER_MAPPING.items():
            # convert to string just to make sure type conversion is correct
            table['file.info.scan.pet.radiotracer'] = str(k)
            attr = MQTSCANAttribute(table)

            # needs to == amyloid
            if k in [2, 3, 4, 5]:
                assert attr._create_scan_pet_amyloid_tracers() == v
            else:
                assert attr._create_scan_pet_amyloid_tracers() is None

        # None case
        attr = MQTSCANAttribute(SymbolTable({}))
        assert attr._create_scan_pet_amyloid_tracers() is None

    def test_create_scan_pet_centaloid(self, table):
        """Tests _create_scan_pet_centaloid, should just return centaloid as a
        float."""
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_centaloid() == 1.5

        # empty
        attr = MQTSCANAttribute(SymbolTable({}))
        assert attr._create_scan_pet_centaloid() is None

    def test_create_scan_pet_centaloid_x(self, table):
        """Tests _create_scan_pet_centaloid_*, should return centerloid as a
        float if the tracer is the given value."""
        table['file.info.scan.pet.radiotracer'] = '2'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_centaloid_pib() == 1.5

        table['file.info.scan.pet.radiotracer'] = '3'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_centaloid_florbetapir() == 1.5

        table['file.info.scan.pet.radiotracer'] = '4'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_centaloid_florbetaben() == 1.5

        table['file.info.scan.pet.radiotracer'] = '5'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_centaloid_nav4694() == 1.5

        # 99, should all be None
        table['file.info.scan.pet.radiotracer'] = '99'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_centaloid_pib() is None
        assert attr._create_scan_pet_centaloid_florbetapir() is None
        assert attr._create_scan_pet_centaloid_florbetaben() is None
        assert attr._create_scan_pet_centaloid_nav4694() is None

    def test_create_scan_pet_amyloid_positivity_indicator(self, table):
        """Tests _create_scan_pet_amyloid_positivity_indicator, which just gets
        amyloid_status."""
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_amyloid_positivity_indicator()

        # TODO: check what 0 case should be?
        table['file.info.scan.pet.amyloid_status'] = '0'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_amyloid_positivity_indicator()

        # empty
        attr = MQTSCANAttribute(SymbolTable({}))
        assert not attr._create_scan_pet_amyloid_positivity_indicator()

    def test_create_scan_pet_tau_tracers(self, table):
        """Tests _create_scan_pet_tau_tracers, which just checks if scan_type.

        == tau and returns tracer string if so.
        """
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_tau_tracers() is None

        # tau scans
        for i in [6, 7, 8, 9]:
            table['file.info.scan.pet.radiotracer'] = i
            attr = MQTSCANAttribute(table)
            assert attr._create_scan_pet_tau_tracers() == \
                attr.TRACER_MAPPING[i]

    def test_create_scan_mri_year_count(self, table):
        """Tests _create_scan_mri_year_count, which should jsut count
        scan_mri_years."""
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_mri_year_count() == 3

        # empty
        table['subject.info.derived.scan_mri_dates'] = []
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_mri_year_count() == 0

    def test_create_scan_pet_year_count(self, table):
        """Tests _create_scan_pet_year_count, which should jsut count
        scan_mri_years."""
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_year_count() == 1

        # empty
        table['subject.info.derived.scan_pet_dates'] = []
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_year_count() == 0
