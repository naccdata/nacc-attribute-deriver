"""SCAN attribute, derive directly from AttributeCollection.

Raw values are split across 7 files - deriving a variable should be isolated
to a single file as much as possible, otherwise we need to somehow map cross-file
attributes.
"""
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.schema.errors import MissingRequiredException
from nacc_attribute_deriver.symbol_table import SymbolTable


class MRIPrefix(str, Enum):

    SCAN_MRI_QC = 'scan_mri_qc.'
    MRI_SBM = 'mri_sbm.'


class PETPrefix(str, Enum):

    SCAN_PET_QC = 'scan_pet_qc.'
    AMYLOID_PET_GAAIN = 'amyloid_pet_gaain.'
    AMYLOID_PET_NPDKA = 'amyloid_pet_npdka.'
    FDG_PET_NPDKA = 'fdg_pet_npdka.'
    TAU_PET_NPDKA = 'tau_pet_npdka.'

    @classmethod
    def analysis_files(cls):
        """Returns all analysis PET files."""
        return [
            cls.AMYLOID_PET_GAAIN, cls.AMYLOID_PET_NPDKA, cls.FDG_PET_NPDKA,
            cls.TAU_PET_NPDKA
        ]

# TODO: make this more elegant
REQUIRED_FIELDS: Dict[Union[MRIPrefix, PETPrefix], List[str]] = {
    MRIPrefix.SCAN_MRI_QC: ['studydate', 'seriestype'],
    MRIPrefix.MRI_SBM: ['scandt', 'cerebrumtcv', 'wmh'],

    PETPrefix.SCAN_PET_QC: ['scan_date', 'radiotracer'],
    PETPrefix.AMYLOID_PET_GAAIN: ['scandate', 'tracer', 'centiloids', 'amyloid_status'],
    PETPrefix.AMYLOID_PET_NPDKA: ['scandate'],
    PETPrefix.FDG_PET_NPDKA: ['scandate'],
    PETPrefix.TAU_PET_NPDKA: ['scandate']
}


class SCANAttribute(AttributeCollection):

    TRACER_MAPPING = {
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

    TRACER_SCAN_TYPE_MAPPING = {
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

    def __init__(self,
                 table: SymbolTable,
                 form_prefix: str = 'file.info.raw.') -> None:
                 # mri_prefix: str = 'file.info.raw.mri.scan.',
                 # pet_prefix: str = 'file.info.raw.pet.scan.') -> None:
        """Override initializer to set prefix to SCAN-specific data."""
        super().__init__(table, form_prefix)
        # self.__mri_prefix = mri_prefix
        # self.__pet_prefix = pet_prefix

    def __verify_prefix(self, subprefix: Union[MRIPrefix, PETPrefix]) -> None:
        if subprefix not in REQUIRED_FIELDS:
            raise MissingRequiredException(
                f"Unknown SCAN file: {subprefix.value}")

        for field in REQUIRED_FIELDS[subprefix]:
            if field not in self.table[self.form_prefix.rstrip('.')]:
                raise MissingRequiredException(
                    f"Required field {field} for SCAN data " +
                    f"{subprefix.value} not found in current file")

    # TODO: combine these two into one since they're now doing the same thing?
    # although it is nice to have get_mri_value vs get_pet_value distinctions
    def get_mri_value(self,
                      key: str,
                      subprefix: MRIPrefix,
                      default: Any = None) -> Any:
        """Get MRI-specific value.

        Args:
            key: Key to grab value for
            subprefix: The MRI-specific sub-prefix
            default: Default value to return if key is not found
        """
        self.__verify_prefix(subprefix)
        return self.get_value(key, default)

    def get_pet_value(self,
                      key: str,
                      subprefix: PETPrefix,
                      default: Any = None) -> Any:
        """Get PET-specific value.

        Args:
            key: Key to grab value for
            subprefix: The PET-specific sub-prefix
            default: Default value to return if key is not found
        """
        self.__verify_prefix(subprefix)
        return self.get_value(key, default)

    # get functions for common values
    def get_tracer(self, field: str, subprefix: PETPrefix) -> Optional[str]:
        """Get the tracer string."""
        tracer = None
        try:
            tracer = float(self.get_pet_value(field, subprefix))
        except (ValueError, TypeError):
            return None

        return self.TRACER_MAPPING.get(tracer, None)

    def get_scan_type(self, field: str, subprefix: PETPrefix) -> Optional[str]:
        """Get the scan type from the tracer."""
        tracer = None
        try:
            tracer = float(self.get_pet_value(field, subprefix))
        except (ValueError, TypeError):
            return None

        return self.TRACER_SCAN_TYPE_MAPPING.get(tracer, None)
