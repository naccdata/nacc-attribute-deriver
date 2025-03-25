"""SCAN attribute, derive directly from AttributeCollection.

Raw values are split across 7 files - deriving a variable should be isolated
to a single file as much as possible, otherwise we need to somehow map cross-file
attributes.
"""

from enum import Enum
from types import MappingProxyType
from typing import Dict, List, Optional, Union

from nacc_attribute_deriver.attributes.base.base_attribute import RawNamespace


class MRIPrefix(str, Enum):
    """File name prefixes for SCAN MR-specific files."""

    SCAN_MRI_QC = "scan_mri_qc."
    MRI_SBM = "mri_sbm."


class PETPrefix(str, Enum):
    """File name prefixes for SCAN PET-specific files."""

    SCAN_PET_QC = "scan_pet_qc."
    AMYLOID_PET_GAAIN = "amyloid_pet_gaain."
    AMYLOID_PET_NPDKA = "amyloid_pet_npdka."
    FDG_PET_NPDKA = "fdg_pet_npdka."
    TAU_PET_NPDKA = "tau_pet_npdka."

    @classmethod
    def analysis_files(cls):
        """Returns the names of all analysis PET files."""
        return [
            cls.AMYLOID_PET_GAAIN,
            cls.AMYLOID_PET_NPDKA,
            cls.FDG_PET_NPDKA,
            cls.TAU_PET_NPDKA,
        ]


# TODO: make this more elegant
REQUIRED_FIELDS: Dict[Union[MRIPrefix, PETPrefix], List[str]] = {
    MRIPrefix.SCAN_MRI_QC: ["study_date", "series_type"],
    MRIPrefix.MRI_SBM: ["scandt", "cerebrumtcv", "wmh"],
    PETPrefix.SCAN_PET_QC: ["scan_date"],
    PETPrefix.AMYLOID_PET_GAAIN: ["scandate", "tracer", "amyloid_status"],
    PETPrefix.AMYLOID_PET_NPDKA: ["scandate"],
    PETPrefix.FDG_PET_NPDKA: ["scandate"],
    PETPrefix.TAU_PET_NPDKA: ["scandate"],
}


class SCANNamespace(RawNamespace):
    TRACER_MAPPING = MappingProxyType(
        {
            1: "fdg",
            2: "pib",
            3: "florbetapir",
            4: "florbetaben",
            5: "nav4694",
            6: "flortaucipir",
            7: "MK6240",
            8: "pi2620",
            9: "gtp1",
            99: "unknown",
        }
    )

    TRACER_SCAN_TYPE_MAPPING = MappingProxyType(
        {
            1: "fdg",
            2: "amyloid",
            3: "amyloid",
            4: "amyloid",
            5: "amyloid",
            6: "tau",
            7: "tau",
            8: "tau",
            9: "tau",
        }
    )

    # get functions for common values
    def get_tracer(self, field: str, subprefix: PETPrefix) -> Optional[str]:
        """Get the tracer string."""
        tracer = None
        try:
            self.assert_required(REQUIRED_FIELDS[subprefix])
            tracer = float(self.get_value(field))
            tracer = int(tracer)  # can't call int directly on string-float
        except (ValueError, TypeError):
            return None

        return self.TRACER_MAPPING.get(tracer, None)

    def get_scan_type(self, field: str, subprefix: PETPrefix) -> Optional[str]:
        """Get the scan type from the tracer."""
        tracer = None
        try:
            self.assert_required(REQUIRED_FIELDS[subprefix])
            tracer = float(self.get_value(field))
            tracer = int(tracer)
        except (ValueError, TypeError):
            return None

        return self.TRACER_SCAN_TYPE_MAPPING.get(tracer, None)
