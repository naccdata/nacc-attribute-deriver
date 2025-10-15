"""Tests Mixed Protocol attributes."""

import copy
import pytest
from nacc_attribute_deriver.attributes.nacc.imaging.mp import (
    MPAttributeCollection,
    MPMRIAttributeCollection,
    MPPETAttributeCollection,
)
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable

from tests.conftest import set_attribute


@pytest.fixture(scope="function")
def nifti_table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        'file': {
            'info': {
                'header': {
                    'dicom': {
                        "StudyDate": "20060816",
                    }
                }
            }
        },
        'subject': {
            'info': {
                'working': {
                    'cross-sectional': {
                        'uds-date-of-birth': "1950-05-01",
                        'uds-visitdates': [
                            '1800-12-01',
                            '2020-06-01'
                        ],
                        'mri-sessions': [
                            "2001-03-12",
                            "2006-08-16"
                        ]
                    },
                    # will be filled out later for testing
                    'longitudinal': {
                        'naccdico': [],
                        'naccnift': []
                    }
                }
            }
        }
    }
    return SymbolTable(data)

@pytest.fixture(scope="function")
def dicom_table(nifti_table) -> SymbolTable:
    """Add dummy metadata to show this is a dicom file."""
    data = copy.deepcopy(nifti_table.to_dict())
    data['file']['info']['header'].update({
        'derived': {
            "dummy": "1.2",
        },
        'dicom_array': {
            'dummy': [
                1,
                2
            ]
        }
    })

    return SymbolTable(data)


class TestMPAttributeCollection:
    """Test creating general values, used by both MRI and PET."""

    def test_calculate_age_at_scan(self, dicom_table):
        """Tests calculating age at scan."""
        attr = MPAttributeCollection(dicom_table)
        assert attr.calculate_age_at_scan() == 56

        # test min/max is enforced
        dicom_table['subject.info.working.cross-sectional.uds-date-of-birth'] \
            = '2005-04-03'
        assert attr.calculate_age_at_scan() == 18
        dicom_table['subject.info.working.cross-sectional.uds-date-of-birth'] \
            = '1800-02-17'
        assert attr.calculate_age_at_scan() == 120

        # test missing
        dicom_table['subject.info.working.cross-sectional.uds-date-of-birth'] \
            = None
        assert attr.calculate_age_at_scan() == 888

    def test_calculate_days_from_closest_uds_visit(self, dicom_table):
        """test calculating days since closest UDS visit."""
        attr = MPAttributeCollection(dicom_table)

        # using default values should be from 2020-06-01, so negative
        # since it came before
        assert attr.calculate_days_from_closest_uds_visit() == -5038

        # from 2000-12-01, so positive since it came after
        dicom_table['subject.info.working.cross-sectional.uds-visitdates'] = [
            '1900-01-01',
            '2000-12-01',
            '2100-01-01'
        ]
        assert attr.calculate_days_from_closest_uds_visit() == 2084

        # same, so 0
        dicom_table['subject.info.working.cross-sectional.uds-visitdates'] = [
            '2006-08-16'
        ]
        assert attr.calculate_days_from_closest_uds_visit() == 0

        # test no UDS dates
        dicom_table['subject.info.working.cross-sectional.uds-visitdates'] = None
        assert attr.calculate_days_from_closest_uds_visit() == 8888

    def test_get_num_sessions(self, dicom_table):
        """Test getting number of sessions."""
        attr = MPAttributeCollection(dicom_table)
        assert attr.get_num_sessions('mri-sessions') == 2

        # test min/max is enforced; really just max
        dicom_table['subject.info.working.cross-sectional.mri-sessions'] = [
            f'2000-01-{i:2d}' for i in range(1, 51)
        ]
        assert len(dicom_table['subject.info.working.cross-sectional.mri-sessions']) \
            == 50
        assert attr.get_num_sessions('mri-sessions') == 20

        # test no sessions; shouldn't happen if this namespace is never called,
        # e.g. no sessions, but sanity check
        dicom_table['subject.info.working.cross-sectional.mri-sessions'] = []
        assert attr.get_num_sessions('mri-sessions') == 88
        dicom_table['subject.info.working.cross-sectional.mri-sessions'] = \
            None
        assert attr.get_num_sessions('mri-sessions') == 88


class TestMRIMPAttributeCollection:
    """Test MRI-specific attributes, mainly related to dicoms."""

    def test_create_naccdico(self, dicom_table, nifti_table):
        """Test create NACCDICO."""
        # nothing derived yet, so should just check if the
        # current image is a dicom or not
        attr = MPMRIAttributeCollection(dicom_table)
        assert attr._create_naccdico() == 1

        attr = MPMRIAttributeCollection(nifti_table)
        assert attr._create_naccdico() == 0

        # if already set, should not be set in the nifti case
        nifti_table['subject.info.working.longitudinal.naccdico'] = [
            {
                'date': '2001-03-12',
                'value': 0
            },
            {
                'date': '2006-08-16',
                'value': 1
            }
        ]

        attr = MPMRIAttributeCollection(nifti_table)
        assert attr._create_naccdico() == 1

    def test_create_naccnift(self, dicom_table, nifti_table):
        """Test create NACCNIFT."""
        # nothing derived yet, so should just check if the
        # current image is a nifti or not
        attr = MPMRIAttributeCollection(dicom_table)
        assert attr._create_naccnift() == 0

        attr = MPMRIAttributeCollection(nifti_table)
        assert attr._create_naccnift() == 1

        # if already set, should not be set in the dicom case
        dicom_table['subject.info.working.longitudinal.naccnift'] = [
            {
                'date': '2001-03-12',
                'value': 0
            },
            {
                'date': '2006-08-16',
                'value': 1
            }
        ]

        attr = MPMRIAttributeCollection(dicom_table)
        assert attr._create_naccnift() == 1
