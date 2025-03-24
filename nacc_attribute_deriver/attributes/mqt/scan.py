"""All SCAN MQT derived variables.

Assumes NACC-derived variables are already set
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.base_attribute import (
    SubjectDerivedAttribute,
)
from nacc_attribute_deriver.attributes.base.scan_attribute import (
    REQUIRED_FIELDS,
    MRIPrefix,
    PETPrefix,
    SCANAttribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import get_unique_years


class MQTSCANAttributeCollection(AttributeCollection):
    """Class to collect MQT SCAN attributes."""

    def __init__(self, table: SymbolTable):
        self.__scan = SCANAttribute(table)
        self.__subject_derived = SubjectDerivedAttribute(table)

    def _create_scan_mri_scan_types(self) -> Optional[str]:
        """SCAN MRI scan types available Access series_type (scan_mridashboard
        file)"""
        self.__scan.assert_required(REQUIRED_FIELDS[MRIPrefix.SCAN_MRI_QC])
        return self.__scan.get_value("series_type")

    def _is_mri_indicator(self, target: str, subprefix: MRIPrefix) -> bool:
        """Returns whether or not the given target is an MRI.

        indicator - checks by seeing if the target can be
        converted to a float.

        Args:
            target: The target field
            subprefix: Subprefix file to look in
        Returns:
            Whether or not this is an indicator
        """
        try:
            self.__scan.assert_required(REQUIRED_FIELDS[subprefix])
            float(self.__scan.get_value(target))
        except (ValueError, TypeError):
            return False

        # true if valid float
        return True

    def _create_scan_volume_analysis_indicator(self) -> bool:
        """SCAN T1 brain volume analysis results available Check if cerebrumtcv
        (ucdmrisbm file) exists."""
        return self._is_mri_indicator("cerebrumtcv", MRIPrefix.MRI_SBM)

    def _create_scan_flair_wmh_indicator(self) -> bool:
        """SCAN FLAIR WMH analysis available available Check if wmh (ucdmrisbm
        file) exists."""
        return self._is_mri_indicator("wmh", MRIPrefix.MRI_SBM)

    # Note: Probably should be "tracer_types"
    def _create_scan_pet_scan_types(self) -> Optional[str]:
        """SCAN PET types available Access radiotracer (scan_petdashboard) and
        map to {amyloid, tau, fdg}"""
        return self.__scan.get_scan_type("radiotracer", PETPrefix.SCAN_PET_QC)

    def _create_scan_pet_amyloid_tracers(self) -> Optional[str]:
        """SCAN Amyloid tracers available Access radiotracer
        (scan_petdashboard) and map to names of tracers."""
        if self.__scan.get_scan_type("radiotracer", PETPrefix.SCAN_PET_QC) == "amyloid":
            return self.__scan.get_tracer("radiotracer", PETPrefix.SCAN_PET_QC)

        return None

    def _create_scan_pet_tau_tracers(self) -> Optional[str]:
        """SCAN tau tracers available Access radiotracer (scan_petdashboard)
        and map to names of tracers."""
        if self.__scan.get_scan_type("radiotracer", PETPrefix.SCAN_PET_QC) == "tau":
            return self.__scan.get_tracer("radiotracer", PETPrefix.SCAN_PET_QC)

        return None

    def get_centiloid(self) -> Optional[float]:
        """Get the centiloid value."""
        centiloid = None
        try:
            self.__scan.assert_required(REQUIRED_FIELDS[PETPrefix.AMYLOID_PET_GAAIN])
            centiloid = float(self.__scan.get_value("centiloids"))
        except (ValueError, TypeError):
            return None

        return centiloid

    # Note: Be careful about the float return type here with the min computation.
    def _create_scan_pet_centaloid(self) -> Optional[float]:
        """SCAN Amyloid PET scans centiloid min Access CENTILOIDS in UC
        Berkeley GAAIN analysis."""
        return self.get_centiloid()

    def _create_scan_pet_centaloid_pib(self) -> Optional[float]:
        """SCAN Amyloid PET scans with PIB centiloid min Access CENTILOIDS in
        UC Berkeley GAAIN analysis."""
        if self.__scan.get_tracer("tracer", PETPrefix.AMYLOID_PET_GAAIN) == "pib":
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_florbetapir(self) -> Optional[float]:
        """SCAN Amyloid PET scans with Florbetapir centiloid min Access
        CENTILOIDS in UC Berkeley GAAIN analysis."""
        if (
            self.__scan.get_tracer("tracer", PETPrefix.AMYLOID_PET_GAAIN)
            == "florbetapir"
        ):
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_florbetaben(self) -> Optional[float]:
        """SCAN Amyloid PET scans with Florbetaben centiloid min Access
        CENTILOIDS in UC Berkeley GAAIN analysis."""
        if (
            self.__scan.get_tracer("tracer", PETPrefix.AMYLOID_PET_GAAIN)
            == "florbetaben"
        ):
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_nav4694(self) -> Optional[float]:
        """SCAN Amyloid PET scans with NAV4694 centiloid min Access CENTILOIDS
        in UC Berkeley GAAIN analysis."""
        if self.__scan.get_tracer("tracer", PETPrefix.AMYLOID_PET_GAAIN) == "nav4694":
            return self.get_centiloid()

        return None

    def _create_scan_pet_amyloid_positivity_indicator(self) -> bool:
        """SCAN Amyloid positive scans available Access AMYLOID_STATUS in UC
        Berkeley GAAIN analysis.

        Is given as an int so check int boolean.
        """
        try:
            self.__scan.assert_required(REQUIRED_FIELDS[PETPrefix.AMYLOID_PET_GAAIN])
            status = float(self.__scan.get_value("amyloid_status"))
        except (TypeError, ValueError):
            return False

        return bool(status)

    def _create_scan_mri_session_count(self):
        """Number of SCAN MRI session available.

        Counts the unique session dates.
        """
        self.__subject_derived.assert_required(["scan-mri-dates"])
        return len(self.__subject_derived.get_value("scan-mri-dates"))

    def _create_scan_pet_session_count(self):
        """Number of SCAN PET sessions available.

        Counts the unique session dates.
        """
        self.__subject_derived.assert_required(["scan-pet-dates"])
        return len(self.__subject_derived.get_value("scan-pet-dates"))

    def _create_scan_mri_year_count(self) -> int:
        """Years of SCAN MRI scans available.

        Does this similar to years of UDS where it keeps track of a
        "NACC" derived variable scan_years which is a list of all years
        a participant has SCAN data in. This create method then just
        counts the distinct years.
        """
        self.__subject_derived.assert_required(["scan-mri-dates"])
        return len(get_unique_years(self.__subject_derived.get_value("scan-mri-dates")))

    def _create_scan_pet_year_count(self) -> int:
        """Years of SCAN PET scans available."""
        self.__subject_derived.assert_required(["scan-pet-dates"])
        return len(get_unique_years(self.__subject_derived.get_value("scan-pet-dates")))
