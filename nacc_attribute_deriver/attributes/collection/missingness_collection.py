"""Class to handle form missingness values that check subject-level derived
variables."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class FormMissingnessCollection(AttributeCollection):
    """Class to handle missingness values at the form level."""

    def __init__(self, table: SymbolTable, required=frozenset([])) -> None:
        self.__form = FormNamespace(table=table, required=required)

    def generic_missingness(self, field: str) -> Optional[int]:
        """Generic missingness for internal calls."""
        if self.__form.get_value(field, str) is None:
            return INFORMED_MISSINGNESS

        return None


class SubjectMissingnessCollection(AttributeCollection):
    """Class to handle missingness values at the subject level."""

    def __init__(self, table: SymbolTable):
        self.__derived = SubjectDerivedNamespace(table=table)

    @property
    def derived(self) -> SubjectDerivedNamespace:
        return self.__derived

    def handle_subject_missing(
        self, attribute: str, default: Optional[int] = INFORMED_MISSINGNESS
    ) -> Optional[int]:
        """Handle missing values at the subject level."""
        value = self.__derived.get_cross_sectional_value(attribute, str)
        if value is None:
            return default

        # the reason we don't return the value itself is because in this
        # context returning None means "don't replace what's already there"
        # whereas returning the value would say "replace what's there with
        # itself" and could potentially cause ordering/date issues
        return None
