"""Class to handle NIAGADS missingness values."""

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    SubjectMissingnessCollection,
)


class NIAGADSMissingness(SubjectMissingnessCollection):
    """Class to handle NIAGADS missingness values."""

    def _missingness_adgcgwas(self) -> int:
        """Handles ADGCGWAS."""
        return self.handle_subject_missing("adgcgwas", int, 0)

    def _missingness_adgcexom(self) -> int:
        """Handles ADGCEXOM."""
        return self.handle_subject_missing("adgcexom", int, 0)

    def _missingness_adgcrnd(self) -> str:
        """Handles ADGCRND."""
        return self.handle_subject_missing("adgcrnd", str, "88")

    def _missingness_adgcexr(self) -> str:
        """Handles ADGCEXR."""
        return self.handle_subject_missing("adgcexr", str, "88")

    def _missingness_ngdsgwas(self) -> int:
        """Handles NGDSGWAS."""
        return self.handle_subject_missing("ngdsgwas", int, 0)

    def _missingness_ngdsexom(self) -> int:
        """Handles NGDSEXOM."""
        return self.handle_subject_missing("ngdsexom", int, 0)

    def _missingness_ngdswgs(self) -> int:
        """Handles NGDSWGS."""
        return self.handle_subject_missing("ngdswgs", int, 0)

    def _missingness_ngdswes(self) -> int:
        """Handles NGDSWES."""
        return self.handle_subject_missing("ngdswes", int, 0)

    def _missingness_ngdsgwac(self) -> str:
        """Handles NGDSGWAC."""
        return self.handle_subject_missing("ngdsgwac", str, "88")

    def _missingness_ngdsexac(self) -> str:
        """Handles NGDSEXAC."""
        return self.handle_subject_missing("ngdsexac", str, "88")

    def _missingness_ngdswgac(self) -> str:
        """Handles NGDSWGAC."""
        return self.handle_subject_missing("ngdswgac", str, "88")

    def _missingness_ngdsweac(self) -> str:
        """Handles NGDSWEAC."""
        return self.handle_subject_missing("ngdsweac", str, "88")
