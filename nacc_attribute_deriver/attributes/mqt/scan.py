"""All SCAN MQT derived variables.

Assumes NACC-derived variables are already set
"""

from typing import List, Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.attributes.base.scan_namespace import (
    SCANMRINamespace,
    SCANPETNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import get_unique_years
from nacc_attribute_deriver.utils.scope import (
    SCANMRIScope,
    SCANPETScope,
)


class MRIAnalysisTypes:
    T1_VOLUME = "t1_volume"
    FLAIR_WMH = "flair_wmh"


class PETAnalysisTypes:
    AMYLOID_GAAIN = "amyloid_gaain_centiloid_suvr"
    AMYLOID_NPDKA = "amyloid_npdka_suvr"
    FDG_NPDKA = "fdg_npdka_suvr"
    TAU_NPDKA = "tau_npdka_suvr"


class SCANMRIQCAttributeCollection(AttributeCollection):
    """Class to collect SCAN MRI QC attributes (scan_mridashboard.csv)"""

    def __init__(self, table: SymbolTable):
        self.__mri_qc = SCANMRINamespace(table, scope=SCANMRIScope.MRI_QC)
        self.__subject_derived = SubjectDerivedNamespace(
            table=table, required=frozenset(["scan-mri-dates"])
        )

    def _create_scan_mri_scan_types(self) -> Optional[str]:
        """SCAN MRI scan types available Access series_type (scan_mridashboard
        file)"""
        return self.__mri_qc.get_value("series_type", str)

    def _create_scan_mri_session_count(self) -> int:
        """Number of SCAN MRI session available.

        Counts the unique session dates.
        """
        dates = self.__subject_derived.get_required("scan-mri-dates", list)
        return len(dates)

    def _create_scan_mri_year_count(self) -> int:
        """Years of SCAN MRI scans available.

        Does this similar to years of UDS where it keeps track of a
        "NACC" derived variable scan_years which is a list of all years
        a participant has SCAN data in. This create method then just
        counts the distinct years.
        """
        dates = self.__subject_derived.get_required("scan-mri-dates", list)
        return len(get_unique_years(dates))


class SCANMRISBMAttributeCollection(AttributeCollection):
    """Class to collect SCAN MRI SBM attributes (ucdmrisbm.csv)"""

    def __init__(self, table: SymbolTable):
        self.__mri_sbm = SCANMRINamespace(table, scope=SCANMRIScope.MRI_SBM)

    def _is_mri_indicator(self, target: str) -> bool:
        """Returns whether or not the given target is an MRI.

        indicator - checks by seeing if the target can be
        converted to a float.

        Args:
            target: The target field
        Returns:
            Whether or not this is an indicator
        """
        value = self.__mri_sbm.get_value(target, str)
        if value is not None:
            try:
                float(value)
                return True
            except (ValueError, TypeError):
                pass

        return False

    def _create_scan_volume_analysis_indicator(self) -> bool:
        """SCAN T1 brain volume analysis results available Check if cerebrumtcv
        (ucdmrisbm file) exists."""
        return self._is_mri_indicator("cerebrumtcv")

    def _create_scan_flair_wmh_indicator(self) -> bool:
        """SCAN FLAIR WMH analysis available available Check if wmh (ucdmrisbm
        file) exists."""
        return self._is_mri_indicator("wmh")

    def _create_mri_scan_analysis_types(self) -> Optional[List[str]]:
        """SCAN MRI analysis types available, which is based on the above two
        indicators."""
        result = []
        if self._create_scan_volume_analysis_indicator():
            result.append(MRIAnalysisTypes.T1_VOLUME)
        if self._create_scan_flair_wmh_indicator():
            result.append(MRIAnalysisTypes.FLAIR_WMH)

        return result if result else None


class SCANPETQCAttributeCollection(AttributeCollection):
    """Class to collect SCAN PET QC attributes (scan_petdashboard.csv)"""

    def __init__(self, table: SymbolTable):
        self.__pet_qc = SCANPETNamespace(table, scope=SCANPETScope.PET_QC)
        self.__subject_derived = SubjectDerivedNamespace(
            table=table, required=frozenset(["scan-pet-dates"])
        )

    def _create_scan_pet_scan_types(self) -> Optional[str]:
        """SCAN PET types available Access radiotracer (scan_petdashboard) and
        map to {amyloid, tau, fdg}"""
        return self.__pet_qc.get_scan_type("radiotracer")

    def _create_scan_pet_amyloid_tracers(self) -> Optional[str]:
        """SCAN Amyloid tracers available Access radiotracer
        (scan_petdashboard) and map to names of tracers."""
        if self.__pet_qc.get_scan_type("radiotracer") == "amyloid":
            return self.__pet_qc.get_tracer("radiotracer")

        return None

    def _create_scan_pet_tau_tracers(self) -> Optional[str]:
        """SCAN tau tracers available Access radiotracer (scan_petdashboard)
        and map to names of tracers."""
        if self.__pet_qc.get_scan_type("radiotracer") == "tau":
            return self.__pet_qc.get_tracer("radiotracer")

        return None

    def _create_scan_pet_session_count(self) -> int:
        """Number of SCAN PET sessions available.

        Counts the unique session dates.
        """
        dates = self.__subject_derived.get_required("scan-pet-dates", list)
        return len(dates)

    def _create_scan_pet_year_count(self) -> int:
        """Years of SCAN PET scans available."""
        dates = self.__subject_derived.get_required("scan-pet-dates", list)
        return len(get_unique_years(dates))


class SCANPETAmyloidGAAINAttributeCollection(AttributeCollection):
    """Class to collect SCAN PET Amyloid GAAIN attributes
    (v_ucberkeley_amyloid_mrifree_gaain.csv)"""

    def __init__(self, table: SymbolTable):
        self.__amyloid_gaain = SCANPETNamespace(
            table, scope=SCANPETScope.AMYLOID_PET_GAAIN
        )

    def get_centiloid(self) -> Optional[float]:
        """Get the centiloid value."""
        return self.__amyloid_gaain.get_value("centiloids", float)

    def _create_scan_pet_centaloid(self) -> Optional[float]:
        """SCAN Amyloid PET scans centiloid min Access CENTILOIDS in UC
        Berkeley GAAIN analysis."""
        return self.get_centiloid()

    def _create_scan_pet_centaloid_pib(self) -> Optional[float]:
        """SCAN Amyloid PET scans with PIB centiloid min Access CENTILOIDS in
        UC Berkeley GAAIN analysis."""
        if self.__amyloid_gaain.get_tracer("tracer") == "pib":
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_florbetapir(self) -> Optional[float]:
        """SCAN Amyloid PET scans with Florbetapir centiloid min Access
        CENTILOIDS in UC Berkeley GAAIN analysis."""
        if self.__amyloid_gaain.get_tracer("tracer") == "florbetapir":
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_florbetaben(self) -> Optional[float]:
        """SCAN Amyloid PET scans with Florbetaben centiloid min Access
        CENTILOIDS in UC Berkeley GAAIN analysis."""
        if self.__amyloid_gaain.get_tracer("tracer") == "florbetaben":
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_nav4694(self) -> Optional[float]:
        """SCAN Amyloid PET scans with NAV4694 centiloid min Access CENTILOIDS
        in UC Berkeley GAAIN analysis."""
        if self.__amyloid_gaain.get_tracer("tracer") == "nav4694":
            return self.get_centiloid()

        return None

    def _create_scan_pet_amyloid_positivity_indicator(self) -> bool:
        """SCAN Amyloid positive scans available Access AMYLOID_STATUS in UC
        Berkeley GAAIN analysis.

        Is given as an int so check int boolean.
        """
        raw_value = self.__amyloid_gaain.get_required("amyloid_status", float)
        return raw_value == 1

    def _create_scan_pet_amyloid_gaain_analysis_type(self) -> Optional[str]:
        """Returns the Amyloid GAAIN Centiloid/SUVR analysis type."""
        centiloid = self.get_centiloid()
        suvr = self.__amyloid_gaain.get_value("gaain_summary_suvr", float)
        return PETAnalysisTypes.AMYLOID_GAAIN if centiloid and suvr else None


class SCANPETAmyloidNPDKAAttributeCollection(AttributeCollection):
    """Class to collect SCAN PET Amyloid NPDKA attributes
    (v_ucberkeley_amyloid_mrifree_npdka.csv)"""

    def __init__(self, table: SymbolTable):
        self.__amyloid_npdka = SCANPETNamespace(
            table, scope=SCANPETScope.AMYLOID_PET_NPDKA
        )

    def _create_scan_pet_amyloid_npdka_analysis_type(self) -> Optional[str]:
        """Returns the Amyloid NPDKA SUVR analysis type."""
        suvr = self.__amyloid_npdka.get_value("npdka_summary_suvr", float)
        return PETAnalysisTypes.AMYLOID_NPDKA if suvr else None


class SCANPETFTDNPDKAAttributeCollection(AttributeCollection):
    """Class to collect SCAN PET FDG NPDKA attributes
    (v_ucberkeley_fdg_metaroi_npdka.csv)"""

    def __init__(self, table: SymbolTable):
        self.__fdg_npdka = SCANPETNamespace(table, scope=SCANPETScope.FDG_PET_NPDKA)

    def _create_scan_pet_fdg_npdka_analysis_type(self) -> Optional[str]:
        """Returns the FDG NPDKA SUVR analysis type."""
        suvr = self.__fdg_npdka.get_value("fdg_metaroi_suvr", float)
        return PETAnalysisTypes.FDG_NPDKA if suvr else None


class SCANPETTAUNPDKAAttributeCollection(AttributeCollection):
    """Class to collect SCAN PET TAU NPDKA attributes
    (v_ucberkeley_tau_mrifree_npdka.csv)"""

    def __init__(self, table: SymbolTable):
        self.__tau_npdka = SCANPETNamespace(table, scope=SCANPETScope.TAU_PET_NPDKA)

    def _create_scan_pet_tau_npdka_analysis_type(self) -> Optional[str]:
        """Returns the Tau NPDKA SUVR analysis type."""
        suvr = self.__tau_npdka.get_value("meta_temporal_suvr", float)
        return PETAnalysisTypes.TAU_NPDKA if suvr else None
