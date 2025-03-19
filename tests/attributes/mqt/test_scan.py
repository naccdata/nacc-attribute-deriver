"""Tests deriving MQT SCAN variables."""
import pytest

from nacc_attribute_deriver.attributes.mqt.scan import MQTSCANAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='function')
def scan_mri_qc_attr() -> MQTSCANAttribute:
    """Create dummy data for a SCAN MRI QC-focused curation."""
    data = {
        'file': {
            'info': {
                'raw': {
                    "seriestype": "T1w",
                    "studydate": "2025-01-01"
                }
            }
        },
        'subject': {
            'info': {
                'derived': {
                    'scan_mri_dates': [
                        '1995-01-01', '1996-01-01', '1997-01-01', '1997-02-02',
                        '1997-03-03'
                    ]
                }
            }
        }
    }

    return MQTSCANAttribute(SymbolTable(data))


class TestSCANMRIQCAttribute:
    """From scan_mridashboard.csv"""

    def test_create_scan_mri_scan_types(self, scan_mri_qc_attr):
        """Tests _create_scan_mri_scan_types, which should just return the
        seriestype."""
        attr = scan_mri_qc_attr
        assert attr._create_scan_mri_scan_types() == "T1w"

        # empty
        attr.table['file.info.raw.seriestype'] = None
        assert attr._create_scan_mri_scan_types() is None

    def test_create_scan_mri_session_count(self, scan_mri_qc_attr):
        """Tests _create_scan_mri_session_count, which should just count
        scan_mri_dates."""
        attr = scan_mri_qc_attr
        assert attr._create_scan_mri_session_count() == 5

        # empty
        attr.table['subject.info.derived.scan_mri_dates'] = []
        assert attr._create_scan_mri_session_count() == 0

    def test_create_scan_mri_year_count(self, scan_mri_qc_attr):
        """Tests _create_scan_mri_year_count, which should just count the
        unique years in scan_mri_dates."""
        attr = scan_mri_qc_attr
        assert attr._create_scan_mri_year_count() == 3

        # empty
        attr.table['subject.info.derived.scan_mri_dates'] = []
        assert attr._create_scan_mri_year_count() == 0


@pytest.fixture(scope='function')
def scan_pet_qc_attr() -> MQTSCANAttribute:
    """Create dummy data for a SCAN PET QC-focused curation."""
    data = {
        'file': {
            'info': {
                'raw': {
                    "radiotracer": 1,
                    "scan_date": "2025-01-01"
                }
            }
        },
        'subject': {
            'info': {
                'derived': {
                    'scan_pet_dates': ['2000-12-12']
                }
            }
        }
    }

    return MQTSCANAttribute(SymbolTable(data))


class TestSCANPETQCAttribute:
    """From scan_petdashboard.csv"""

    def test_create_scan_pet_scan_types(self, scan_pet_qc_attr):
        """Tests _create_scan_pet_scan_types, loop over all options."""
        attr = scan_pet_qc_attr
        for k, v in MQTSCANAttribute.TRACER_SCAN_TYPE_MAPPING.items():
            # convert to string just to make sure type conversion is correct
            attr.table['file.info.raw.radiotracer'] = str(k)
            assert attr._create_scan_pet_scan_types() == v

            # string float case
            attr.table['file.info.raw.radiotracer'] = str(float(k))
            assert attr._create_scan_pet_scan_types() == v

        # None case
        attr.table['file.info.raw.radiotracer'] = ""
        assert attr._create_scan_pet_scan_types() is None

    def test_create_scan_pet_session_count(self, scan_pet_qc_attr):
        """Tests _create_scan_pet_session_count, which should just count
        scan_pet_dates."""
        attr = scan_pet_qc_attr
        assert attr._create_scan_pet_session_count() == 1

        # empty
        attr.table['subject.info.derived.scan_pet_dates'] = []
        assert attr._create_scan_pet_session_count() == 0

    def test_create_scan_pet_year_count(self, scan_pet_qc_attr):
        """Tests _create_scan_pet_year_count, which should just count the
        unique years in scan_pet_dates."""
        attr = scan_pet_qc_attr
        assert attr._create_scan_pet_year_count() == 1

        # empty
        attr.table['subject.info.derived.scan_pet_dates'] = []
        assert attr._create_scan_pet_year_count() == 0

    def test_create_scan_pet_amyloid_tracers(self, scan_pet_qc_attr):
        """Tests _create_scan_pet_amyloid_tracers, loop over all options."""
        attr = scan_pet_qc_attr
        for k, v in MQTSCANAttribute.TRACER_MAPPING.items():
            # convert to string just to make sure type conversion is correct
            attr.table['file.info.raw.radiotracer'] = str(k)

            # needs to == amyloid
            if k in [2, 3, 4, 5]:
                assert attr._create_scan_pet_amyloid_tracers() == v
            else:
                assert attr._create_scan_pet_amyloid_tracers() is None

        # None case
        attr.table['file.info.raw.radiotracer'] = None
        assert attr._create_scan_pet_amyloid_tracers() is None

    def test_create_scan_pet_tau_tracers(self, scan_pet_qc_attr):
        """Tests _create_scan_pet_tau_tracers, which just checks if scan_type.

        == tau and returns tracer string if so.
        """
        attr = scan_pet_qc_attr
        assert attr._create_scan_pet_tau_tracers() is None

        # tau scans
        for i in [6, 7, 8, 9]:
            attr.table['file.info.raw.radiotracer'] = i
            assert attr._create_scan_pet_tau_tracers() == attr.TRACER_MAPPING[i]


@pytest.fixture(scope='function')
def scan_mri_sbm() -> MQTSCANAttribute:
    """Create dummy data for a SCAN MRI SBM (analysis)-focused curation."""
    data = {
        'file': {
            'info': {
                'raw': {
                    "cerebrumtcv": "2.5",
                    "wmh": "3.5",
                    "scandt": "2025-01-01"
                }
            }
        }
    }

    return MQTSCANAttribute(SymbolTable(data))


class TestSCANMRISBMAttribute:
    """From ucbmrisbm.csv"""

    def test_create_scan_volume_analysis_indicator(self, scan_mri_sbm):
        """Tests _create_scan_volume_analysis_indicator, which looks at
        cerebrumtcv when series_type == T1w."""
        attr = scan_mri_sbm
        assert attr._create_scan_volume_analysis_indicator()

        # 0 case, is a valid number so should return True
        attr.table['file.info.raw.cerebrumtcv'] = '0'
        assert attr._create_scan_volume_analysis_indicator()

        # empty
        attr.table['file.info.raw.cerebrumtcv'] = None
        assert not attr._create_scan_volume_analysis_indicator()

    def test_create_scan_flair_wmh_indicator(self, scan_mri_sbm):
        """Tests _create_scan_flair_wmh_indicator, which looks at wmh."""
        attr = scan_mri_sbm
        assert attr._create_scan_flair_wmh_indicator()

        # 0 case, is a valid number so should return True
        attr.table['file.info.raw.wmh'] = '0'
        assert attr._create_scan_flair_wmh_indicator()

        # empty
        attr.table['file.info.raw.wmh'] = None
        assert not attr._create_scan_flair_wmh_indicator()


@pytest.fixture(scope='function')
def scan_pet_amyloid_gaain() -> MQTSCANAttribute:
    """Create dummy data for a SCAN PET Amyloid GAAIN (analysis)-focused curation."""
    data = {
        'file': {
            'info': {
                'raw': {
                    "tracer": "1.0",
                    "centiloids": "1.5",
                    "amyloid_status": "1",
                    "scandate": "2025-01-01"
                }
            }
        }
    }

    return MQTSCANAttribute(SymbolTable(data))


class TestSCANAmyloidPETGAAINAttribute:
    """From v_berkeley_amyloid_pet_gaain.csv"""

    def test_create_scan_pet_centaloid(self, scan_pet_amyloid_gaain):
        """Tests _create_scan_pet_centaloid, should just return centaloid as a
        float."""
        attr = scan_pet_amyloid_gaain
        assert attr._create_scan_pet_centaloid() == 1.5

        # empty
        attr.table['file.info.raw.centiloids'] = None
        assert attr._create_scan_pet_centaloid() is None

    def test_create_scan_pet_centaloid_x(self, scan_pet_amyloid_gaain):
        """Tests _create_scan_pet_centaloid_*, should return centerloid as a
        float if the tracer is the given value."""
        attr = scan_pet_amyloid_gaain
        attr.table['file.info.raw.tracer'] = '2'
        assert attr._create_scan_pet_centaloid_pib() == 1.5

        attr.table['file.info.raw.tracer'] = '3.0'
        assert attr._create_scan_pet_centaloid_florbetapir() == 1.5

        attr.table['file.info.raw.tracer'] = '4'
        assert attr._create_scan_pet_centaloid_florbetaben() == 1.5

        attr.table['file.info.raw.tracer'] = '5'
        assert attr._create_scan_pet_centaloid_nav4694() == 1.5

        # 99, should all be None
        attr.table['file.info.raw.tracer'] = '99'
        assert attr._create_scan_pet_centaloid_pib() is None
        assert attr._create_scan_pet_centaloid_florbetapir() is None
        assert attr._create_scan_pet_centaloid_florbetaben() is None
        assert attr._create_scan_pet_centaloid_nav4694() is None

    def test_create_scan_pet_amyloid_positivity_indicator(self, scan_pet_amyloid_gaain):
        """Tests _create_scan_pet_amyloid_positivity_indicator, which just gets
        amyloid_status."""
        attr = scan_pet_amyloid_gaain
        assert attr._create_scan_pet_amyloid_positivity_indicator()

        # string float case
        attr.table['file.info.raw.amyloid_status'] = '1.0'
        assert attr._create_scan_pet_amyloid_positivity_indicator()

        # 0 case, should be False
        attr.table['file.info.raw.amyloid_status'] = '0'
        assert not attr._create_scan_pet_amyloid_positivity_indicator()

        # empty
        attr.table['file.info.raw.amyloid_status'] = None
        assert not attr._create_scan_pet_amyloid_positivity_indicator()
