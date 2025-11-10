"""Class to handle UDS missingness variables.

In general, returns -4 unless otherwise specified.
"""

from typing import Optional, Type

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSMissingness,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    T,
)


class GenericUDSMissingness(UDSMissingness):
    """Defines generic missingness rule in its own subclass otherwise it gets
    inherited by all subclasses and imported multiple times."""

    def _missingness_uds(self, field: str, attr_type: Type[T]) -> Optional[T]:
        """Defines general missingness for UDS; -4 if missing."""
        return self.generic_missingness(field, attr_type)
