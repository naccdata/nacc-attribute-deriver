"""SCAN attribute, derive directly from AttributeCollection.

Raw values are split across 7 files - deriving a variable should be isolated
to a single file as much as possible, otherwise we need to somehow map cross-file
attributes.
"""
from enum import Enum
from typing import Any, Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
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
                 form_prefix: str = 'file.info.raw.',
                 mri_prefix: str = 'file.info.raw.mri.scan.',
                 pet_prefix: str = 'file.info.raw.pet.scan.') -> None:
        """Override initializer to set prefix to SCAN-specific data."""
        super().__init__(table, form_prefix)
        self.__mri_prefix = mri_prefix
        self.__pet_prefix = pet_prefix

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
        return self.get_value(key,
                              default,
                              prefix=f'{self.__mri_prefix}{subprefix.value}')

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
        return self.get_value(key,
                              default,
                              prefix=f'{self.__pet_prefix}{subprefix.value}')

    # get functions for common values
    def get_tracer(self, field: str, subprefix: PETPrefix) -> Optional[str]:
        """Get the tracer string."""
        tracer = None
        try:
            tracer = float(self.get_pet_value(field, subprefix))
        except (ValueError, TypeError):
            return None

        return self.TRACER_MAPPING.get(tracer, None)  # type: ignore

    def get_scan_type(self, field: str, subprefix: PETPrefix) -> Optional[str]:
        """Get the scan type from the tracer."""
        tracer = None
        try:
            tracer = float(self.get_pet_value(field, subprefix))
        except (ValueError, TypeError):
            return None

        return self.TRACER_SCAN_TYPE_MAPPING.get(tracer, None)  # type: ignore
