from typing import List

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.attributes.base.scan_namespace import SCANNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import get_unique_years
from nacc_attribute_deriver.utils.scope import SCANMRIScope


class MRIAnalysisTypes:
    T1_VOLUME = "t1_volume"
    FLAIR_WMH = "flair_wmh"


class SCANMRIQCAttributeCollection(AttributeCollection):
    """Class for SCAN MRI QC Attributes."""

    def __init__(self, table: SymbolTable):
        self.__scan = SCANNamespace(table=table, scope=SCANMRIScope.MRI_QC)

    def _create_scan_mri_scan_types(self) -> str:
        """SCAN MRI scan types available Access series_type (scan_mridashboard
        file)"""
        attribute_value = self.__scan.get_value("series_type")
        assert attribute_value

        return attribute_value


class SCANMRISBMAttributeCollection(AttributeCollection):
    """Class for SCAN MRI SBM Attributes."""

    def __init__(self, table: SymbolTable):
        self.__scan = SCANNamespace(table=table, scope=SCANMRIScope.MRI_SBM)

    def _is_mri_indicator(self, target: str) -> bool:
        """Returns whether or not the given target is an MRI.

        indicator - checks by seeing if the target can be
        converted to a float.

        Args:
            target: The target field
            scope: Scope to look in
        Returns:
            Whether or not this is an indicator
        """
        attribute_value = self.__scan.get_value(target)
        if attribute_value is None:
            return False

        try:
            float(attribute_value)
        except (ValueError, TypeError):
            return False

        # true if valid float
        return True

    def _create_scan_volume_analysis_indicator(self) -> bool:
        """SCAN T1 brain volume analysis results available Check if cerebrumtcv
        (ucdmrisbm file) exists."""
        return self._is_mri_indicator("cerebrumtcv")

    def _create_scan_flair_wmh_indicator(self) -> bool:
        """SCAN FLAIR WMH analysis available available Check if wmh (ucdmrisbm
        file) exists."""
        return self._is_mri_indicator("wmh")

    def _create_mri_scan_analysis_types(self) -> List[str]:
        """SCAN MRI analysis types available, which is based on the above two
        indicators."""
        result: List[str] = []
        if self._create_scan_volume_analysis_indicator():
            result.append(MRIAnalysisTypes.T1_VOLUME)
        if self._create_scan_flair_wmh_indicator():
            result.append(MRIAnalysisTypes.FLAIR_WMH)

        return result


class SubjectSCANMRIAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__subject_derived = SubjectDerivedNamespace(
            table=table, required=frozenset(["scan-mri-dates"])
        )

    def _create_scan_mri_session_count(self) -> int:
        """Number of SCAN MRI session available.

        Counts the unique session dates.
        """
        return self.__subject_derived.get_count("scan-mri-dates")

    def _create_scan_mri_year_count(self) -> int:
        """Years of SCAN MRI scans available.

        Does this similar to years of UDS where it keeps track of a
        "NACC" derived variable scan_years which is a list of all years
        a participant has SCAN data in. This create method then just
        counts the distinct years.
        """
        attribute_value = self.__subject_derived.get_value("scan-mri-dates")
        assert attribute_value

        return len(get_unique_years(attribute_value))
