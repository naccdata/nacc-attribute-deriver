"""SCAN attributes, derive directly from AttributeCollection.

Comes from 7 unique files.
"""

from types import MappingProxyType
from typing import Dict, Iterable, List, Optional

from nacc_attribute_deriver.attributes.base.namespace import (
    NamespaceScope,
    RawNamespace,
    ScopeDefinitionError,
)
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.utils.scope import SCANMRIScope, SCANPETScope

# TODO: make this more elegant
SCAN_REQUIRED_FIELDS: Dict[str, List[str]] = {
    SCANMRIScope.MRI_QC: ["study_date", "series_type"],
    SCANMRIScope.MRI_SBM: ["scandt", "cerebrumtcv", "wmh"],
    SCANPETScope.PET_QC: ["scan_date"],
    SCANPETScope.AMYLOID_PET_GAAIN: ["scandate", "tracer", "amyloid_status"],
    SCANPETScope.AMYLOID_PET_NPDKA: ["scandate"],
    SCANPETScope.FDG_PET_NPDKA: ["scandate"],
    SCANPETScope.TAU_PET_NPDKA: ["scandate"],
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
            7: "mk6240",
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

    def scope(
        self,
        *,
        name: Optional[str] = None,
        fields: Optional[Iterable[str]] = None,
    ) -> NamespaceScope:
        if not name:
            raise ScopeDefinitionError("SCAN scope definition incomplete")

        fields = fields if fields else SCAN_REQUIRED_FIELDS.get(name)
        return super().scope(name=name, fields=fields)

    # get functions for common values
    def get_tracer(self, field: str, scope: SCANPETScope) -> Optional[str]:
        """Get the tracer string."""
        attribute_value = self.get_value(field)
        if not attribute_value:  # no falsey value is valid
            return None

        try:
            tracer = int(float(attribute_value))
        except (ValueError, TypeError) as error:
            raise InvalidFieldError(
                f"Attribute {self.prefix}{field} is expected to have a float value"
            ) from error

        return self.TRACER_MAPPING.get(tracer, None)

    def get_scan_type(
        self, field: str, scope: SCANPETScope | SCANMRIScope
    ) -> Optional[str]:
        """Get the scan type from the tracer."""
        attribute_value = self.get_value(field)
        if not attribute_value:  # no falsey value is valid
            return None

        try:
            tracer = int(float(attribute_value))
        except (ValueError, TypeError) as error:
            raise InvalidFieldError(
                f"Attribute {self.prefix}{field} is expected to have a float value"
            ) from error

        return self.TRACER_SCAN_TYPE_MAPPING.get(tracer, None)
