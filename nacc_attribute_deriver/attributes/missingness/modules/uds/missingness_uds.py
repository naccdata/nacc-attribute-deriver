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
from nacc_attribute_deriver.utils.date import standardize_date


class GenericUDSMissingness(UDSMissingness):
    """Defines generic missingness rule in its own subclass otherwise it gets
    inherited by all subclasses and imported multiple times."""

    def _missingness_uds(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for UDS; -4 if missing."""

        # standardize FRMDATEX variables
        if field.startswith("frmdate") and attr_type == str:  # noqa: E721
            formatted_date = standardize_date(self.uds.get_value(field, str))
            if formatted_date:
                return formatted_date  # type: ignore

        return self.generic_missingness(field, attr_type)
