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
                'raw': {
                    "mri": {
                        "scan_mri_qc": {
                            "seriestype": "T1w"
                        },
                        "mri_sbm": {
                            "cerebrumtcv": "2.5",
                            "wmh": "3.5"
                        }
                    },
                    "pet": {
                        "scan_pet_qc": {
                            "radiotracer": 1
                        },
                        "amyloid_pet_gaain": {
                            "tracer": "1.0",
                            "centiloids": "1.5",
                            "amyloid_status": "1"
                        },
                        "amyloid_pet_npdka": {},
                        "fdg_pet_npdka": {},
                        "tau_pet_npdka": {}
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

    def test_create_scan_volume_analysis_indicator(self, table):
        """Tests _create_scan_volume_analysis_indicator, which looks at
        cerebrumtcv when series_type == T1w."""
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_volume_analysis_indicator()

        # 0 case, is a valid number so should return True
        table['file.info.raw.mri.mri_sbm.cerebrumtcv'] = '0'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_volume_analysis_indicator()

        # empty
        attr = MQTSCANAttribute(SymbolTable({}))
        assert not attr._create_scan_volume_analysis_indicator()

    def test_create_scan_flair_wmh_indicator(self, table):
        """Tests _create_scan_flair_wmh_indicator, which looks at wmh."""
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_flair_wmh_indicator()

        # 0 case, is a valid number so should return True
        table['file.info.raw.mri.mri_sbm.wmh'] = '0'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_flair_wmh_indicator()

        # empty
        attr = MQTSCANAttribute(SymbolTable({}))
        assert not attr._create_scan_flair_wmh_indicator()

    def test_create_scan_pet_scan_types(self, table):
        """Tests _create_scan_pet_scan_types, loop over all options."""
        for k, v in MQTSCANAttribute.TRACER_MAPPING.items():
            # convert to string just to make sure type conversion is correct
            table['file.info.raw.pet.scan_pet_qc.radiotracer'] = str(k)
            attr = MQTSCANAttribute(table)
            assert attr._create_scan_pet_scan_types() == v

        # None case
        attr = MQTSCANAttribute(SymbolTable({}))
        assert attr._create_scan_pet_scan_types() is None

    def test_create_scan_pet_amyloid_tracers(self, table):
        """Tests _create_scan_pet_amyloid_tracers, loop over all options."""
        for k, v in MQTSCANAttribute.TRACER_MAPPING.items():
            # convert to string just to make sure type conversion is correct
            table['file.info.raw.pet.scan_pet_qc.radiotracer'] = str(k)
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
        table['file.info.raw.pet.amyloid_pet_gaain.tracer'] = '2'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_centaloid_pib() == 1.5

        table['file.info.raw.pet.amyloid_pet_gaain.tracer'] = '3'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_centaloid_florbetapir() == 1.5

        table['file.info.raw.pet.amyloid_pet_gaain.tracer'] = '4'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_centaloid_florbetaben() == 1.5

        table['file.info.raw.pet.amyloid_pet_gaain.tracer'] = '5'
        attr = MQTSCANAttribute(table)
        assert attr._create_scan_pet_centaloid_nav4694() == 1.5

        # 99, should all be None
        table['file.info.raw.pet.amyloid_pet_gaain.tracer'] = '99'
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

        # 0 case, should be False
        table['file.info.raw.pet.amyloid_pet_gaain.amyloid_status'] = '0'
        attr = MQTSCANAttribute(table)
        assert not attr._create_scan_pet_amyloid_positivity_indicator()

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
            table['file.info.raw.pet.scan_pet_qc.radiotracer'] = i
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
