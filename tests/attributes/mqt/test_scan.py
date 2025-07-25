"""Tests deriving MQT SCAN variables."""

import pytest
from nacc_attribute_deriver.attributes.base.scan_namespace import (
    SCANPETNamespace,
)
from nacc_attribute_deriver.attributes.mqt.scan import (
    SCANMRIQCAttributeCollection,
    SCANMRISBMAttributeCollection,
    SCANPETAmyloidGAAINAttributeCollection,
    SCANPETAmyloidNPDKAAttributeCollection,
    SCANPETFTDNPDKAAttributeCollection,
    SCANPETTAUNPDKAAttributeCollection,
    SCANPETQCAttributeCollection,
    MRIAnalysisTypes,
    PETAnalysisTypes,
)
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def scan_mri_qc_table() -> SymbolTable:
    """Create dummy data for a SCAN MRI QC-focused curation."""
    data = {
        "file": {"info": {"raw": {"series_type": "T1w", "study_date": "2025-01-01"}}},
        "subject": {
            "info": {
                "derived": {
                    "scan-mri-dates": [
                        "1995-01-01",
                        "1996-01-01",
                        "1997-01-01",
                        "1997-02-02",
                        "1997-03-03",
                    ]
                }
            }
        },
    }

    return SymbolTable(data)


class TestSCANMRIQCAttribute:
    """From scan_mridashboard.csv."""

    def test_create_scan_mri_scan_types(self, scan_mri_qc_table):
        """Tests _create_scan_mri_scan_types, which should just return the
        series_type."""
        attr = SCANMRIQCAttributeCollection(scan_mri_qc_table)
        assert attr._create_scan_mri_scan_types() == "T1w"

        # empty
        scan_mri_qc_table["file.info.raw.series_type"] = None
        with pytest.raises(MissingRequiredError):
            SCANMRIQCAttributeCollection(scan_mri_qc_table)

    def test_create_scan_mri_session_count(self, scan_mri_qc_table):
        """Tests _create_scan_mri_session_count, which should just count scan-
        mri-dates."""
        attr = SCANMRIQCAttributeCollection(scan_mri_qc_table)
        assert attr._create_scan_mri_session_count() == 5

        # empty
        scan_mri_qc_table["subject.info.derived.scan-mri-dates"] = []
        attr = SCANMRIQCAttributeCollection(scan_mri_qc_table)
        assert attr._create_scan_mri_session_count() == 0

    def test_create_scan_mri_year_count(self, scan_mri_qc_table):
        """Tests _create_scan_mri_year_count, which should just count the
        unique years in scan-mri-dates."""
        attr = SCANMRIQCAttributeCollection(scan_mri_qc_table)
        assert attr._create_scan_mri_year_count() == 3

        # empty
        scan_mri_qc_table["subject.info.derived.scan-mri-dates"] = []
        attr = SCANMRIQCAttributeCollection(scan_mri_qc_table)
        assert attr._create_scan_mri_year_count() == 0


@pytest.fixture(scope="function")
def scan_pet_qc_table() -> SymbolTable:
    """Create dummy data for a SCAN PET QC-focused curation."""
    data = {
        "file": {"info": {"raw": {"radiotracer": 1, "scan_date": "2025-01-01"}}},
        "subject": {"info": {"derived": {"scan-pet-dates": ["2000-12-12"]}}},
    }

    return SymbolTable(data)


class TestSCANPETQCAttribute:
    """From scan_petdashboard.csv."""

    def test_create_scan_pet_scan_types(self, scan_pet_qc_table):
        """Tests _create_scan_pet_scan_types, loop over all options."""
        for k, v in SCANPETNamespace.TRACER_SCAN_TYPE_MAPPING.items():
            # convert to string just to make sure type conversion is correct
            scan_pet_qc_table["file.info.raw.radiotracer"] = str(k)
            attr = SCANPETQCAttributeCollection(scan_pet_qc_table)
            assert attr._create_scan_pet_scan_types() == v

            # string float case
            scan_pet_qc_table["file.info.raw.radiotracer"] = str(float(k))
            attr = SCANPETQCAttributeCollection(scan_pet_qc_table)
            assert attr._create_scan_pet_scan_types() == v

        # None case
        scan_pet_qc_table["file.info.raw.radiotracer"] = ""
        attr = SCANPETQCAttributeCollection(scan_pet_qc_table)
        assert attr._create_scan_pet_scan_types() is None

    def test_create_scan_pet_session_count(self, scan_pet_qc_table):
        """Tests _create_scan_pet_session_count, which should just count scan-
        pet-dates."""
        attr = SCANPETQCAttributeCollection(scan_pet_qc_table)
        assert attr._create_scan_pet_session_count() == 1

        # empty
        scan_pet_qc_table["subject.info.derived.scan-pet-dates"] = []
        attr = SCANPETQCAttributeCollection(scan_pet_qc_table)
        assert attr._create_scan_pet_session_count() == 0

    def test_create_scan_pet_year_count(self, scan_pet_qc_table):
        """Tests _create_scan_pet_year_count, which should just count the
        unique years in scan-pet-dates."""
        attr = SCANPETQCAttributeCollection(scan_pet_qc_table)
        assert attr._create_scan_pet_year_count() == 1

        # empty
        scan_pet_qc_table["subject.info.derived.scan-pet-dates"] = []
        assert attr._create_scan_pet_year_count() == 0

    def test_create_scan_pet_amyloid_tracers(self, scan_pet_qc_table):
        """Tests _create_scan_pet_amyloid_tracers, loop over all options."""
        attr = scan_pet_qc_table
        for k, v in SCANPETNamespace.TRACER_MAPPING.items():
            # convert to string just to make sure type conversion is correct
            scan_pet_qc_table["file.info.raw.radiotracer"] = str(k)
            attr = SCANPETQCAttributeCollection(scan_pet_qc_table)

            # needs to == amyloid
            if k in [2, 3, 4, 5]:
                assert attr._create_scan_pet_amyloid_tracers() == v
            else:
                assert attr._create_scan_pet_amyloid_tracers() is None

        # None case
        scan_pet_qc_table["file.info.raw.radiotracer"] = None
        attr = SCANPETQCAttributeCollection(scan_pet_qc_table)
        assert attr._create_scan_pet_amyloid_tracers() is None

    def test_create_scan_pet_tau_tracers(self, scan_pet_qc_table):
        """Tests _create_scan_pet_tau_tracers, which just checks if scan_type.

        == tau and returns tracer string if so.
        """
        attr = SCANPETQCAttributeCollection(scan_pet_qc_table)
        assert attr._create_scan_pet_tau_tracers() is None

        # tau scans
        for i in [6, 7, 8, 9]:
            scan_pet_qc_table["file.info.raw.radiotracer"] = i
            attr = SCANPETQCAttributeCollection(scan_pet_qc_table)
            assert (
                attr._create_scan_pet_tau_tracers()
                == SCANPETNamespace.TRACER_MAPPING[i]
            )


@pytest.fixture(scope="function")
def scan_mri_sbm() -> SymbolTable:
    """Create dummy data for a SCAN MRI SBM (analysis)-focused curation."""
    data = {
        "file": {
            "info": {
                "raw": {"cerebrumtcv": "2.5", "wmh": "3.5", "scandt": "2025-01-01"}
            }
        }
    }

    return SymbolTable(data)


class TestSCANMRISBMAttribute:
    """From ucbmrisbm.csv."""

    def test_create_scan_volume_analysis_indicator(self, scan_mri_sbm):
        """Tests _create_scan_volume_analysis_indicator, which looks at
        cerebrumtcv when series_type == T1w."""
        attr = SCANMRISBMAttributeCollection(scan_mri_sbm)
        assert attr._create_scan_volume_analysis_indicator()

        # 0 case, is a valid number so should return True
        scan_mri_sbm["file.info.raw.cerebrumtcv"] = "0"
        attr = SCANMRISBMAttributeCollection(scan_mri_sbm)
        assert attr._create_scan_volume_analysis_indicator()

        # empty
        scan_mri_sbm["file.info.raw.cerebrumtcv"] = None
        with pytest.raises(MissingRequiredError):
            SCANMRISBMAttributeCollection(scan_mri_sbm)

    def test_create_scan_flair_wmh_indicator(self, scan_mri_sbm):
        """Tests _create_scan_flair_wmh_indicator, which looks at wmh."""
        attr = SCANMRISBMAttributeCollection(scan_mri_sbm)
        assert attr._create_scan_flair_wmh_indicator()

        # 0 case, is a valid number so should return True
        scan_mri_sbm["file.info.raw.wmh"] = "0"
        attr = SCANMRISBMAttributeCollection(scan_mri_sbm)
        assert attr._create_scan_flair_wmh_indicator()

        # empty
        scan_mri_sbm["file.info.raw.wmh"] = None
        attr = SCANMRISBMAttributeCollection(scan_mri_sbm)
        assert not attr._create_scan_flair_wmh_indicator()

    def test_create_mri_scan_analysis_types(self, scan_mri_sbm):
        """Tests _create_mri_scan_analysis_types."""
        attr = SCANMRISBMAttributeCollection(scan_mri_sbm)
        assert attr._create_mri_scan_analysis_types() == [
            MRIAnalysisTypes.T1_VOLUME,
            MRIAnalysisTypes.FLAIR_WMH,
        ]

        # t1 volume is missing
        scan_mri_sbm["file.info.raw.cerebrumtcv"] = None
        assert attr._create_mri_scan_analysis_types() == [MRIAnalysisTypes.FLAIR_WMH]

        # both are missing
        scan_mri_sbm["file.info.raw.wmh"] = None
        assert attr._create_mri_scan_analysis_types() is None


@pytest.fixture(scope="function")
def scan_pet_amyloid_gaain() -> SymbolTable:
    """Create dummy data for a SCAN PET Amyloid GAAIN (analysis)-focused
    curation."""
    data = {
        "file": {
            "info": {
                "raw": {
                    "tracer": "1.0",
                    "centiloids": "1.5",
                    "gaain_summary_suvr": "2.703",
                    "amyloid_status": "1",
                    "scandate": "2025-01-01",
                }
            }
        }
    }

    return SymbolTable(data)


class TestSCANAmyloidPETGAAINAttribute:
    """From v_berkeley_amyloid_pet_gaain.csv."""

    def test_create_scan_pet_centiloid(self, scan_pet_amyloid_gaain):
        """Tests _create_scan_pet_centiloid, should just return centiloid as a
        float."""
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_centiloid() == 1.5

        # empty
        scan_pet_amyloid_gaain["file.info.raw.centiloids"] = None
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_centiloid() is None

    def test_create_scan_pet_centiloid_x(self, scan_pet_amyloid_gaain):
        """Tests _create_scan_pet_centiloid_*, should return centerloid as a
        float if the tracer is the given value."""
        attr = scan_pet_amyloid_gaain
        scan_pet_amyloid_gaain["file.info.raw.tracer"] = "2"
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_centiloid_pib() == 1.5

        scan_pet_amyloid_gaain["file.info.raw.tracer"] = "3.0"
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_centiloid_florbetapir() == 1.5

        scan_pet_amyloid_gaain["file.info.raw.tracer"] = "4"
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_centiloid_florbetaben() == 1.5

        scan_pet_amyloid_gaain["file.info.raw.tracer"] = "5"
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_centiloid_nav4694() == 1.5

        # 99, should all be None
        scan_pet_amyloid_gaain["file.info.raw.tracer"] = "99"
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_centiloid_pib() is None
        assert attr._create_scan_pet_centiloid_florbetapir() is None
        assert attr._create_scan_pet_centiloid_florbetaben() is None
        assert attr._create_scan_pet_centiloid_nav4694() is None

    def test_create_scan_pet_amyloid_positivity_indicator(self, scan_pet_amyloid_gaain):
        """Tests _create_scan_pet_amyloid_positivity_indicator, which just gets
        amyloid_status."""
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_amyloid_positivity_indicator()

        # string float case
        scan_pet_amyloid_gaain["file.info.raw.amyloid_status"] = "1.0"
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_amyloid_positivity_indicator()

        # 0 case, should be False
        scan_pet_amyloid_gaain["file.info.raw.amyloid_status"] = "0"
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert not attr._create_scan_pet_amyloid_positivity_indicator()

        # empty
        scan_pet_amyloid_gaain["file.info.raw.amyloid_status"] = None
        with pytest.raises(MissingRequiredError):
            SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)

    def test_create_scan_pet_amyloid_gaain_analysis_type(self, scan_pet_amyloid_gaain):
        """Tests _create_scan_pet_amyloid_gaain_analysis_type."""
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert (
            attr._create_scan_pet_amyloid_gaain_analysis_type()
            == PETAnalysisTypes.AMYLOID_GAAIN
        )

        # missing centiloid
        scan_pet_amyloid_gaain["file.info.raw.centiloids"] = None
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_amyloid_gaain_analysis_type() is None

        # missing gaain_summary_suvr
        scan_pet_amyloid_gaain["file.info.raw.centiloids"] = "1.234"
        scan_pet_amyloid_gaain["file.info.raw.gaain_summary_suvr"] = None
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_amyloid_gaain_analysis_type() is None

        # empty
        scan_pet_amyloid_gaain["file.info.raw.centiloids"] = None
        attr = SCANPETAmyloidGAAINAttributeCollection(scan_pet_amyloid_gaain)
        assert attr._create_scan_pet_amyloid_gaain_analysis_type() is None


@pytest.fixture(scope="function")
def scan_pet_amyloid_npdka() -> SymbolTable:
    """Create dummy data for a SCAN PET Amyloid NPDKA (analysis)-focused
    curation."""
    data = {
        "file": {
            "info": {"raw": {"npdka_summary_suvr": "2.411", "scandate": "2021-04-06"}}
        }
    }

    return SymbolTable(data)


class TestSCANAmyloidPETNPDKAAttribute:
    """From v_ucberkeley_amyloid_mrifree_npdka.csv."""

    def test_create_scan_pet_amyloid_npdka_analysis_type(self, scan_pet_amyloid_npdka):
        """Tests _create_scan_pet_amyloid_npdka_analysis_type."""
        attr = SCANPETAmyloidNPDKAAttributeCollection(scan_pet_amyloid_npdka)
        assert (
            attr._create_scan_pet_amyloid_npdka_analysis_type()
            == PETAnalysisTypes.AMYLOID_NPDKA
        )

        # missing
        scan_pet_amyloid_npdka["file.info.raw.npdka_summary_suvr"] = None
        attr = SCANPETAmyloidNPDKAAttributeCollection(scan_pet_amyloid_npdka)
        assert attr._create_scan_pet_amyloid_npdka_analysis_type() is None


@pytest.fixture(scope="function")
def scan_pet_fdg_npdka() -> SymbolTable:
    """Create dummy data for a SCAN PET FDG NPDKA (analysis)-focused
    curation."""
    data = {
        "file": {
            "info": {"raw": {"fdg_metaroi_suvr": "1.139", "scandate": "2024-03-08"}}
        }
    }

    return SymbolTable(data)


class TestSCANFDGPETNPDKAAttribute:
    """From v_ucberkeley_fdg_metaroi_npdka.csv."""

    def test_create_scan_pet_fdg_npdka_analysis_type(self, scan_pet_fdg_npdka):
        """Tests _create_scan_pet_fdg_npdka_analysis_type."""
        attr = SCANPETFTDNPDKAAttributeCollection(scan_pet_fdg_npdka)
        assert (
            attr._create_scan_pet_fdg_npdka_analysis_type()
            == PETAnalysisTypes.FDG_NPDKA
        )

        # missing
        scan_pet_fdg_npdka["file.info.raw.fdg_metaroi_suvr"] = None
        attr = SCANPETFTDNPDKAAttributeCollection(scan_pet_fdg_npdka)
        assert attr._create_scan_pet_fdg_npdka_analysis_type() is None


@pytest.fixture(scope="function")
def scan_pet_tau_npdka() -> SymbolTable:
    """Create dummy data for a SCAN PET Tau NPDKA (analysis)-focused
    curation."""
    data = {
        "file": {
            "info": {
                "raw": {
                    "meta_temporal_suvr": "1.276",
                    "scandate": "2023-05-17",
                }
            }
        }
    }

    return SymbolTable(data)


class TestSCANTauPETNPDKAAttribute:
    """From v_ucberkeley_tau_mrifree_npdka.csv."""

    def test_create_scan_pet_tau_npdka_analysis_type(self, scan_pet_tau_npdka):
        """Tests _create_scan_pet_tau_npdka_analysis_type."""
        attr = SCANPETTAUNPDKAAttributeCollection(scan_pet_tau_npdka)
        assert (
            attr._create_scan_pet_tau_npdka_analysis_type()
            == PETAnalysisTypes.TAU_NPDKA
        )

        # missing
        scan_pet_tau_npdka["file.info.raw.meta_temporal_suvr"] = None
        attr = SCANPETTAUNPDKAAttributeCollection(scan_pet_tau_npdka)
        assert attr._create_scan_pet_tau_npdka_analysis_type() is None
