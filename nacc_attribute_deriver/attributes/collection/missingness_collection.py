"""Class to handle form missingness values that check subject-level derived
variables."""

from typing import Optional, Type

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
    SubjectDerivedNamespace,
    T,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
    INFORMED_MISSINGNESS_FLOAT,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


class FormMissingnessCollection(AttributeCollection):
    """Class to handle missingness values at the form level.

    These generally expect that the form DOES exist, but may have
    missing values.
    """

    def __init__(self, table: SymbolTable, required=frozenset([])) -> None:
        self.__form = FormNamespace(table=table, required=required)

    @property
    def form(self) -> FormNamespace:
        return self.__form

    def generic_missingness(self, field: str, attr_type: Type[T]) -> Optional[T]:
        """Generic missingness:

        If FIELD is None, FIELD = -4 / -4.4 / blank
        """
        if self.__form.get_value(field, str) is None:
            if attr_type == int:  # noqa: E721
                return INFORMED_MISSINGNESS  # type: ignore
            if attr_type == str:  # noqa: E721
                return INFORMED_BLANK  # type: ignore
            if attr_type == float:  # noqa: E721
                return INFORMED_MISSINGNESS_FLOAT  # type: ignore

            raise AttributeDeriverError(
                f"Unknown missingness attribute type: {attr_type}"
            )

        return None


class SubjectMissingnessCollection(AttributeCollection):
    """Class to handle missingness values at the subject level.

    These generally expect that the form/data does not exist at all, so
    can only write things to the subject level.
    """

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
