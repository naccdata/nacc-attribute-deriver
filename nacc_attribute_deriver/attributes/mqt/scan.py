"""All SCAN MQT derived variables.

Assumes NACC-derived variables are already set
"""

from typing import List, Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.attributes.base.scan_namespace import (
    SCAN_REQUIRED_FIELDS,
    SCANNamespace,
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


class MQTSCANAttributeCollection(AttributeCollection):
    """Class to collect MQT SCAN attributes."""

    def __init__(self, table: SymbolTable):
        self.__scan = SCANNamespace(table)
        self.__subject_derived = SubjectDerivedNamespace(table)

    def _create_scan_mri_scan_types(self) -> Optional[str]:
        """SCAN MRI scan types available Access series_type (scan_mridashboard
        file)"""
        self.__scan.assert_required(SCAN_REQUIRED_FIELDS[SCANMRIScope.MRI_QC])
        return self.__scan.get_value("series_type")

    def _is_mri_indicator(self, target: str, scope: SCANMRIScope) -> Optional[bool]:
        """Returns whether or not the given target is an MRI.

        indicator - checks by seeing if the target can be
        converted to a float.

        Args:
            target: The target field
            scope: Scope to look in
        Returns:
            Whether or not this is an indicator
        """
        self.__scan.assert_required(SCAN_REQUIRED_FIELDS[scope])
        attribute_value = self.__scan.get_value(target)
        if attribute_value is None:
            return None

        try:
            float(attribute_value)
        except (ValueError, TypeError):
            return False

        # true if valid float
        return True

    def _create_scan_volume_analysis_indicator(self) -> Optional[bool]:
        """SCAN T1 brain volume analysis results available Check if cerebrumtcv
        (ucdmrisbm file) exists."""
        return self._is_mri_indicator("cerebrumtcv", SCANMRIScope.MRI_SBM)

    def _create_scan_flair_wmh_indicator(self) -> Optional[bool]:
        """SCAN FLAIR WMH analysis available available Check if wmh (ucdmrisbm
        file) exists."""
        return self._is_mri_indicator("wmh", SCANMRIScope.MRI_SBM)

    def _create_mri_scan_analysis_types(self) -> Optional[List[str]]:
        """SCAN MRI analysis types available, which is based on the above two
        indicators."""
        result: List[str] = []
        if self._create_scan_volume_analysis_indicator():
            result.append(MRIAnalysisTypes.T1_VOLUME)
        if self._create_scan_flair_wmh_indicator():
            result.append(MRIAnalysisTypes.FLAIR_WMH)

        return result if result else None

    def _create_scan_pet_scan_types(self) -> Optional[str]:
        """SCAN PET types available Access radiotracer (scan_petdashboard) and
        map to {amyloid, tau, fdg}"""
        return self.__scan.get_scan_type("radiotracer", SCANPETScope.PET_QC)

    def _create_scan_pet_amyloid_tracers(self) -> Optional[str]:
        """SCAN Amyloid tracers available Access radiotracer
        (scan_petdashboard) and map to names of tracers."""
        if self.__scan.get_scan_type("radiotracer", SCANPETScope.PET_QC) == "amyloid":
            return self.__scan.get_tracer("radiotracer", SCANPETScope.PET_QC)

        return None

    def _create_scan_pet_tau_tracers(self) -> Optional[str]:
        """SCAN tau tracers available Access radiotracer (scan_petdashboard)
        and map to names of tracers."""
        if self.__scan.get_scan_type("radiotracer", SCANPETScope.PET_QC) == "tau":
            return self.__scan.get_tracer("radiotracer", SCANPETScope.PET_QC)

        return None

    def get_pet_float(self, attribute: str, scope: SCANPETScope) -> Optional[float]:
        """Get PET float value."""
        self.__scan.assert_required(SCAN_REQUIRED_FIELDS[scope])
        attribute_value = self.__scan.get_value(attribute)
        if attribute_value is None:
            return None

        try:
            return float(attribute_value)
        except (ValueError, TypeError):
            # TODO: this should raise an exception
            pass

        return None

    def get_centiloid(self) -> Optional[float]:
        """Get the centiloid value."""
        return self.get_pet_float("centiloids", SCANPETScope.AMYLOID_PET_GAAIN)

    def _create_scan_pet_centaloid(self) -> Optional[float]:
        """SCAN Amyloid PET scans centiloid min Access CENTILOIDS in UC
        Berkeley GAAIN analysis."""
        return self.get_centiloid()

    def _create_scan_pet_centaloid_pib(self) -> Optional[float]:
        """SCAN Amyloid PET scans with PIB centiloid min Access CENTILOIDS in
        UC Berkeley GAAIN analysis."""
        if self.__scan.get_tracer("tracer", SCANPETScope.AMYLOID_PET_GAAIN) == "pib":
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_florbetapir(self) -> Optional[float]:
        """SCAN Amyloid PET scans with Florbetapir centiloid min Access
        CENTILOIDS in UC Berkeley GAAIN analysis."""
        if (
            self.__scan.get_tracer("tracer", SCANPETScope.AMYLOID_PET_GAAIN)
            == "florbetapir"
        ):
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_florbetaben(self) -> Optional[float]:
        """SCAN Amyloid PET scans with Florbetaben centiloid min Access
        CENTILOIDS in UC Berkeley GAAIN analysis."""
        if (
            self.__scan.get_tracer("tracer", SCANPETScope.AMYLOID_PET_GAAIN)
            == "florbetaben"
        ):
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_nav4694(self) -> Optional[float]:
        """SCAN Amyloid PET scans with NAV4694 centiloid min Access CENTILOIDS
        in UC Berkeley GAAIN analysis."""
        if (
            self.__scan.get_tracer("tracer", SCANPETScope.AMYLOID_PET_GAAIN)
            == "nav4694"
        ):
            return self.get_centiloid()

        return None

    def _create_scan_pet_amyloid_positivity_indicator(self) -> Optional[bool]:
        """SCAN Amyloid positive scans available Access AMYLOID_STATUS in UC
        Berkeley GAAIN analysis.

        Is given as an int so check int boolean.
        """
        self.__scan.assert_required(
            SCAN_REQUIRED_FIELDS[SCANPETScope.AMYLOID_PET_GAAIN]
        )
        attribute_value = self.__scan.get_value("amyloid_status")
        if attribute_value is None:
            return None

        try:
            status = float(attribute_value)
        except (TypeError, ValueError):
            return False

        return bool(status)

    def __get_count(self, attribute: str) -> Optional[int]:
        """Returns the length of the attribute value.

        Args:
          attribute: the attribute
        Returns:
          the length of the attribute value. None if there is no attribute
        """
        attribute_value = self.__subject_derived.get_value(attribute)
        if attribute_value is None:
            return None

        return len(attribute_value)

    def _create_scan_mri_session_count(self) -> Optional[int]:
        """Number of SCAN MRI session available.

        Counts the unique session dates.
        """
        self.__subject_derived.assert_required(["scan-mri-dates"])
        return self.__get_count("scan-mri-dates")

    def _create_scan_pet_session_count(self) -> Optional[int]:
        """Number of SCAN PET sessions available.

        Counts the unique session dates.
        """
        self.__subject_derived.assert_required(["scan-pet-dates"])
        return self.__get_count("scan-pet-dates")

    def _create_scan_mri_year_count(self) -> Optional[int]:
        """Years of SCAN MRI scans available.

        Does this similar to years of UDS where it keeps track of a
        "NACC" derived variable scan_years which is a list of all years
        a participant has SCAN data in. This create method then just
        counts the distinct years.
        """
        self.__subject_derived.assert_required(["scan-mri-dates"])
        attribute_value = self.__subject_derived.get_value("scan-mri-dates")
        if attribute_value is None:
            return None

        return len(get_unique_years(attribute_value))

    def _create_scan_pet_year_count(self) -> Optional[int]:
        """Years of SCAN PET scans available."""
        self.__subject_derived.assert_required(["scan-pet-dates"])
        attribute_value = self.__subject_derived.get_value("scan-pet-dates")
        if attribute_value is None:
            return None

        return len(get_unique_years(attribute_value))

    def _create_scan_pet_amyloid_gaain_analysis_type(self) -> Optional[str]:
        """Returns the Amyloid GAAIN Centiloid/SUVR analysis type."""
        centiloid = self.get_centiloid()
        suvr = self.get_pet_float("gaain_summary_suvr", SCANPETScope.AMYLOID_PET_GAAIN)
        return PETAnalysisTypes.AMYLOID_GAAIN if centiloid and suvr else None

    def _create_scan_pet_amyloid_npdka_analysis_type(self) -> Optional[str]:
        """Returns the Amyloid NPDKA SUVR analysis type."""
        suvr = self.get_pet_float("npdka_summary_suvr", SCANPETScope.AMYLOID_PET_NPDKA)
        return PETAnalysisTypes.AMYLOID_NPDKA if suvr else None

    def _create_scan_pet_fdg_npdka_analysis_type(self) -> Optional[str]:
        """Returns the FDG NPDKA SUVR analysis type."""
        suvr = self.get_pet_float("fdg_metaroi_suvr", SCANPETScope.FDG_PET_NPDKA)
        return PETAnalysisTypes.FDG_NPDKA if suvr else None

    def _create_scan_pet_tau_npdka_analysis_type(self) -> Optional[str]:
        """Returns the Tau NPDKA SUVR analysis type."""
        suvr = self.get_pet_float("meta_temporal_suvr", SCANPETScope.TAU_PET_NPDKA)
        return PETAnalysisTypes.TAU_NPDKA if suvr else None
