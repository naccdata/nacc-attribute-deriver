"""Class to handle header (general) missingness values, e.g. FORMVER, ADCID,
VISITDATE, etc."""

from typing import Type

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.utils.date import date_from_form_date


class HeaderFormMissingness(FormMissingnessCollection):
    def _missingness_header(self, field: str, attr_type: Type[T]) -> T:
        """Defines general missingness for header form variables."""
        return self.generic_missingness(field.replace("header_", ""), attr_type)

    def _missingness_header_visitdate(self) -> str:
        """Visitdate can come in several formats, so resolve everything to
        YYYY-MM-DD for consistency.

        VISITDATE is required for forms so expected to be there.
        """
        visitdate = date_from_form_date(self.form.get_required("visitdate", str))
        return str(visitdate)
