"""Base attributes, derive directly from AttributeCollection."""
from inspect import stack
from typing import Any, Dict, List, Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.symbol_table import SymbolTable


class NACCAttribute(AttributeCollection):
    """Currently doesn't have anything specific going on, but may be useful
    later."""


class MQTAttribute(AttributeCollection):
    """MQT-specific attribute collection.

    The main difference is that MQT variables often require that a
    derived NACC variable has already been set.
    """

    def assert_required(self,
                        required: List[str],
                        prefix: str = 'file.info.derived.') -> Dict[str, Any]:
        """Asserts that the given fields in required are in the table for the
        source.

        Args:
            required: The required fields
            prefix: Key prefix the required field is expected to be under
        Returns:
            The found required variables, flattened out from the table
        """
        found = {}
        for r in required:
            full_field = f'{prefix}{r}'
            # TODO: maybe can implicitly derive even if schema didn't define it?
            if full_field not in self.table:
                source = stack(
                )[1].function  # not great but preferable to passing the name every time
                raise ValueError(
                    f"{full_field} must be derived before {source} can run")

            found[r] = self.table[full_field]

        return found


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
                 form_prefix: str = 'file.info.scan.',
                 mri_prefix: str = 'file.info.scan.mri.',
                 pet_prefix: str = 'file.info.scan.pet.') -> None:
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
