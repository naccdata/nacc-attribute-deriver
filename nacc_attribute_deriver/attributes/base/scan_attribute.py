"""SCAN attribute, derive directly from AttributeCollection."""
from typing import Any, Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.symbol_table import SymbolTable


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
                 mri_prefix: str = 'file.info.raw.mri.',
                 pet_prefix: str = 'file.info.raw.pet.') -> None:
        """Override initializer to set prefix to SCAN-specific data."""
        super().__init__(table, form_prefix)
        self.__mri_prefix = mri_prefix
        self.__pet_prefix = pet_prefix

    def get_mri_value(self, key: str, default: Any = None) -> Any:
        """Get MRI-specific value.

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
        """
        return self.get_value(key, default, prefix=self.__mri_prefix)

    def get_pet_value(self, key: str, default: Any = None) -> Any:
        """Get PET-specific value.

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
        """
        return self.get_value(key, default, prefix=self.__pet_prefix)

    # get functions for common values
    def get_tracer(self) -> Optional[str]:
        """Get the tracer string."""
        tracer = None
        try:
            tracer = int(self.get_pet_value("radiotracer"))
        except (ValueError, TypeError):
            pass

        return self.TRACER_MAPPING.get(tracer, None)  # type: ignore

    def get_scan_type(self) -> Optional[str]:
        """Get the scan type from the tracer."""
        tracer = None
        try:
            tracer = int(self.get_pet_value("radiotracer"))
        except (ValueError, TypeError):
            pass

        return self.TRACER_SCAN_TYPE_MAPPING.get(tracer, None)  # type: ignore

    def get_centiloid(self) -> Optional[float]:
        """Get the centiloid value."""
        centiloid = None
        try:
            centiloid = float(self.get_pet_value("centiloids"))
        except (ValueError, TypeError):
            pass

        return centiloid
