"""Class to handle UDS missingness variables.

In general, returns -4 unless otherwise specified.
"""

from typing import Type

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSMissingness,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    T,
)


class GenericUDSMissingness(UDSMissingness):
    """Defines generic missingness rule in its own subclass otherwise it gets
    inherited by all subclasses and imported multiple times."""

    def _missingness_uds(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for UDS; -4 if missing."""
        return self.generic_missingness(field, attr_type)

    def _missingness_uds_formver(self) -> float:
        """Handles missingness for UDS FORMVER."""
        return self.generic_missingness("formver", float)

    def _missingness_uds_adcid(self) -> int:
        """Handles missingness for UDS ADCID."""
        return self.generic_missingness("adcid", int)
