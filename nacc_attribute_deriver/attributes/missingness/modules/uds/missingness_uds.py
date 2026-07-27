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

    def handle_optional_header_variables(
        self, prefix: str, form: str,
    ) -> int:
        """
        Sometimes invalid data is entered for header variables
        on optional forms since they're not enforced to be empty;
        clean up as needed.

        FRMDATEX already handled in _missingness_uds, and allowed
        if is a valid date. Rest should be of type integer.

        Args:
            Prefix for the variable, will be combined with the form
                to get the full thing, e.g. lang + a1a = langa1a
            form: Form this header variable belongs to
            attr_type: The attribute type
        Returns:
            Resolved missingness for the optional header variable
        """
        # Determine if this is an optional form
        mode_field = self.uds.get_value(f'mode{form}')
        if self.uds.get_value(f'mode{form}', int) != 0:
            return self.generic_missingness(field, int)

        # this is an optional form, data should not be filled
        return INFORMED_MISSINGNESS
