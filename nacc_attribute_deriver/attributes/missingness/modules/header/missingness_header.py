"""Class to handle header (general) missingness values, e.g. FORMVER, ADCID,
VISITDATE, etc."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.utils.date import standardize_date
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


class HeaderFormMissingness(FormMissingnessCollection):
    def _missingness_header(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for header form variables."""
        return self.generic_missingness(field.replace("header_", ""), attr_type)

    def _missingness_header_visitdate(self) -> str:
        """Visitdate can come in several formats, so resolve everything to
        YYYY-MM-DD for consistency.

        VISITDATE is required for forms so expected to be there.
        """
        raw_visitdate = self.form.get_required("visitdate", str)
        visitdate = standardize_date(raw_visitdate)
        if not visitdate:
            raise AttributeDeriverError(
                f"Unable to standardize visitdate: {raw_visitdate}"
            )

        return visitdate
