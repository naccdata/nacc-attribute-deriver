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

    def generic_missingness(self, field: str, attr_type: Type[T]) -> T:
        """Generic missingness:

        If FIELD is None, FIELD = -4 / -4.4 / blank
        """
        # NOTE: because V4 saves all metadata as strings, we need to
        # force the typing here for missingness. the intended behavior
        # was to return None (no update) if the value exists, but
        # because of the typing issue we do need to set it.
        # ideally this gets fixed further upstream at some point

        value = self.__form.get_value(field, attr_type)
        if value is None:
            if attr_type == int:  # noqa: E721
                return INFORMED_MISSINGNESS  # type: ignore
            if attr_type == str:  # noqa: E721
                return INFORMED_BLANK  # type: ignore
            if attr_type == float:  # noqa: E721
                return INFORMED_MISSINGNESS_FLOAT  # type: ignore

            raise AttributeDeriverError(
                f"Unknown missingness attribute type: {attr_type}"
            )

        return value


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
        """Handle missing values at the subject level. Assuming all ints."""
        value = self.__derived.get_cross_sectional_value(attribute, int)
        if value is None:
            return default

        # Unlike the file-level, subject-level metadata is ensured to be
        # the correct type, so we could still return None. However,
        # also making it return the value so its consistent. shouldn't
        # affect dated values as not relevant to this context
        return value
