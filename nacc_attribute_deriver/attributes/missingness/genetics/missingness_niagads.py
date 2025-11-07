"""Class to handle NIAGADS missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
)


class NIAGADSMissingness(SubjectMissingnessCollection):
    """Class to handle NIAGADS missingness values."""

    def _missingness_ngdsgwas(self) -> Optional[int]:
        """Handles NGDSGWAS."""
        return self.handle_subject_missing("ngdsgwas", 0)

    def _missingness_ngdsexom(self) -> Optional[int]:
        """Handles NGDSEXOM."""
        return self.handle_subject_missing("ngdsexom", 0)

    def _missingness_ngdswgs(self) -> Optional[int]:
        """Handles NGDSWGS."""
        return self.handle_subject_missing("ngdswgs", 0)

    def _missingness_ngdswes(self) -> Optional[int]:
        """Handles NGDSWES."""
        return self.handle_subject_missing("ngdswes", 0)

    def _missingness_ngdsgwac(self) -> Optional[int]:
        """Handles NGDSGWAC."""
        return self.handle_subject_missing("ngdsgwac", 88)

    def _missingness_ngdsexac(self) -> Optional[int]:
        """Handles NGDSEXAC."""
        return self.handle_subject_missing("ngdsexac", 88)

    def _missingness_ngdswgac(self) -> Optional[int]:
        """Handles NGDSWGAC."""
        return self.handle_subject_missing("ngdswgac", 88)

    def _missingness_ngdsweac(self) -> Optional[int]:
        """Handles NGDSWEAC."""
        return self.handle_subject_missing("ngdsweac", 88)

    def _missingness_adgcgwas(self) -> Optional[int]:
        """Handles ADGCGWAS."""
        return self.handle_subject_missing("adgcgwas")

    def _missingness_adgcexom(self) -> Optional[int]:
        """Handles ADGCEXOM."""
        return self.handle_subject_missing("adgcexom")

    def _missingness_adgcrnd(self) -> Optional[str]:
        """Handles ADGCRND."""
        if self.derived.get_cross_sectional_value("adgcrnd", str) is None:
            return "88"

        return None

    def _missingness_adgcexr(self) -> Optional[str]:
        """Handles ADGCEXR."""
        if self.derived.get_cross_sectional_value("adgcexr", str) is None:
            return "88"

        return None
