"""All SCAN MQT derived variables.

Assumes NACC-derived variables are already set
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.attributes.base.scan_namespace import (
    SCANNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import get_unique_years
from nacc_attribute_deriver.utils.scope import (
    SCANPETScope,
)


class PETAnalysisTypes:
    AMYLOID_GAAIN = "amyloid_gaain_centiloid_suvr"
    AMYLOID_NPDKA = "amyloid_npdka_suvr"
    FDG_NPDKA = "fdg_npdka_suvr"
    TAU_NPDKA = "tau_npdka_suvr"


class SCANPETQCAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__scan = SCANNamespace(table=table, scope=SCANPETScope.PET_QC)

    def _create_scan_pet_scan_types(self) -> Optional[str]:
        """SCAN PET types available Access radiotracer (scan_petdashboard) and
        map to {amyloid, tau, fdg}"""
        return self.__scan.get_scan_type("radiotracer")

    def _create_scan_pet_amyloid_tracers(self) -> Optional[str]:
        """SCAN Amyloid tracers available Access radiotracer
        (scan_petdashboard) and map to names of tracers."""
        if self.__scan.get_scan_type("radiotracer") == "amyloid":
            return self.__scan.get_tracer("radiotracer")

        return None

    def _create_scan_pet_tau_tracers(self) -> Optional[str]:
        """SCAN tau tracers available Access radiotracer (scan_petdashboard)
        and map to names of tracers."""
        if self.__scan.get_scan_type("radiotracer") == "tau":
            return self.__scan.get_tracer("radiotracer")

        return None


class SCANPETAmyloidGAAINAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__scan = SCANNamespace(table=table, scope=SCANPETScope.AMYLOID_PET_GAAIN)

    def get_centiloid(self) -> Optional[float]:
        """Get the centiloid value."""
        return self.__scan.get_float("centiloids")

    def _create_scan_pet_amyloid_gaain_analysis_type(self) -> Optional[str]:
        """Returns the Amyloid GAAIN Centiloid/SUVR analysis type."""
        centiloid = self.get_centiloid()
        suvr = self.__scan.get_float("gaain_summary_suvr")
        return PETAnalysisTypes.AMYLOID_GAAIN if centiloid and suvr else None

    def _create_scan_pet_centaloid(self) -> Optional[float]:
        """SCAN Amyloid PET scans centiloid min Access CENTILOIDS in UC
        Berkeley GAAIN analysis."""
        return self.get_centiloid()

    def _create_scan_pet_centaloid_pib(self) -> Optional[float]:
        """SCAN Amyloid PET scans with PIB centiloid min Access CENTILOIDS in
        UC Berkeley GAAIN analysis."""
        if self.__scan.get_tracer("tracer") == "pib":
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_florbetapir(self) -> Optional[float]:
        """SCAN Amyloid PET scans with Florbetapir centiloid min Access
        CENTILOIDS in UC Berkeley GAAIN analysis."""
        if self.__scan.get_tracer("tracer") == "florbetapir":
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_florbetaben(self) -> Optional[float]:
        """SCAN Amyloid PET scans with Florbetaben centiloid min Access
        CENTILOIDS in UC Berkeley GAAIN analysis."""
        if self.__scan.get_tracer("tracer") == "florbetaben":
            return self.get_centiloid()

        return None

    def _create_scan_pet_centaloid_nav4694(self) -> Optional[float]:
        """SCAN Amyloid PET scans with NAV4694 centiloid min Access CENTILOIDS
        in UC Berkeley GAAIN analysis."""
        if self.__scan.get_tracer("tracer") == "nav4694":
            return self.get_centiloid()

        return None

    def _create_scan_pet_amyloid_positivity_indicator(self) -> Optional[bool]:
        """SCAN Amyloid positive scans available Access AMYLOID_STATUS in UC
        Berkeley GAAIN analysis.

        Is given as an int so check int boolean.
        """
        attribute_value = self.__scan.get_value("amyloid_status")
        if attribute_value is None:
            return None

        try:
            status = float(attribute_value)
        except (TypeError, ValueError):
            return False

        return bool(status)


class SCANPETAmyloidNPDKAAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__scan = SCANNamespace(table=table, scope=SCANPETScope.AMYLOID_PET_NPDKA)

    def _create_scan_pet_amyloid_npdka_analysis_type(self) -> Optional[str]:
        """Returns the Amyloid NPDKA SUVR analysis type."""
        suvr = self.__scan.get_float("npdka_summary_suvr")
        return PETAnalysisTypes.AMYLOID_NPDKA if suvr else None


class SCANPETFDGNPDKAAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__scan = SCANNamespace(table=table, scope=SCANPETScope.FDG_PET_NPDKA)

    def _create_scan_pet_fdg_npdka_analysis_type(self) -> Optional[str]:
        """Returns the FDG NPDKA SUVR analysis type."""
        suvr = self.__scan.get_float("fdg_metaroi_suvr")
        return PETAnalysisTypes.FDG_NPDKA if suvr else None


class SCANPETTAUNPDKAAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__scan = SCANNamespace(table=table, scope=SCANPETScope.TAU_PET_NPDKA)

    def _create_scan_pet_tau_npdka_analysis_type(self) -> Optional[str]:
        """Returns the Tau NPDKA SUVR analysis type."""
        suvr = self.__scan.get_float("meta_temporal_suvr")
        return PETAnalysisTypes.TAU_NPDKA if suvr else None


class SubjectSCANPETAttributeCollection(AttributeCollection):
    """Class to collect MQT SCAN attributes."""

    def __init__(self, table: SymbolTable):
        self.__subject_derived = SubjectDerivedNamespace(
            table=table, required=frozenset(["scan-pet-dates"])
        )

    def _create_scan_pet_session_count(self) -> Optional[int]:
        """Number of SCAN PET sessions available.

        Counts the unique session dates.
        """
        return self.__subject_derived.get_count("scan-pet-dates")

    def _create_scan_pet_year_count(self) -> Optional[int]:
        """Years of SCAN PET scans available."""
        attribute_value = self.__subject_derived.get_value("scan-pet-dates")
        if attribute_value is None:
            return None

        return len(get_unique_years(attribute_value))
