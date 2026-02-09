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
from nacc_attribute_deriver.utils.constants import INFORMED_BLANK
from nacc_attribute_deriver.utils.date import standardize_date
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


class GenericUDSMissingness(UDSMissingness):
    """Defines generic missingness rule in its own subclass otherwise it gets
    inherited by all subclasses and imported multiple times."""

    def _missingness_uds(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for UDS; -4 if missing."""

        # standardize FRMDATEX variables
        # not all FRMDATEX variables required (optional forms), and some centers
        # enter something like "NA" instead, so catch and set to blank if not a date
        if field.startswith("frmdate") and attr_type == str:  # noqa: E721
            try:
                frmdate = standardize_date(self.uds.get_value(field, str))
            except AttributeDeriverError:
                return INFORMED_BLANK  # type: ignore

            return frmdate if frmdate else INFORMED_BLANK  # type: ignore

        return self.generic_missingness(field, attr_type)
