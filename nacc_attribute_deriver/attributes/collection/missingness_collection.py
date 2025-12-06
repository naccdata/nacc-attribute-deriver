"""Class to handle form missingness values that check subject-level derived
variables."""

from typing import Optional, Type

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
    SubjectDerivedNamespace,
    T,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
    INFORMED_MISSINGNESS_FLOAT,
    MISSINGNESS_VALUES,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


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
        self, attribute: str, attr_type: Type[T], default: T
    ) -> T:
        """Handle missing values at the subject level.

        A default is required.
        """
        value = self.__derived.get_cross_sectional_value(attribute, attr_type)

        # Unlike the file-level, subject-level metadata is ensured to be
        # the correct type, so we could still return None. However,
        # also making it return the value so its consistent. shouldn't
        # affect dated values as not relevant to this context
        return value if value is not None else default


class FormMissingnessCollection(AttributeCollection):
    """Class to handle missingness values at the file level.

    These generally expect that the file DOES exist, but may have
    missing values. Things may also need to be pulled across from a
    previous visit
    """

    def __init__(
        self,
        table: SymbolTable,
        namespace: Type[FormNamespace] = FormNamespace,
        required: frozenset[str] = frozenset(),
    ) -> None:
        self.__form = namespace(table=table, required=required)
        self.__prev_record = PreviousRecordNamespace(table=table)

    @property
    def prev_record(self) -> PreviousRecordNamespace:
        return self.__prev_record

    @property
    def form(self) -> FormNamespace:
        return self.__form

    def generic_missingness(
        self, attribute: str, attr_type: Type[T], default: Optional[T] = None
    ) -> T:
        """Generic missingness:

        If FIELD is None, FIELD = -4 / -4.4 / blank
        """
        # NOTE: because V4 saves all metadata as strings, we need to
        # force the typing here for missingness. the intended behavior
        # was to return None (no update) if the value exists, but
        # because of the typing issue we do need to set it.
        # ideally this gets fixed further upstream at some point,
        # especially because forcing the typing makes this take
        # longer (since it needs to perform the operation)

        value = self.__form.get_value(attribute, attr_type)
        if value is None:
            if default is not None:
                return default

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

    def handle_prev_visit(
        self,
        attribute: str,
        attr_type: Type[T],
        prev_code: Optional[T] = None,
        default: Optional[T] = None,
        working: Optional[WorkingNamespace] = None,
    ) -> T:
        """Handle when the value could be provided by the previous visit.

        If VAR == PREV_CODE, VAR = PREV_VISIT.
        ELIF VAR is not blank, return None (do not override)
        ELSE generic missingness
        """
        value = self.__form.get_value(attribute, attr_type)
        if value == prev_code:
            prev_value = self.__prev_record.get_resolved_value(
                attribute, attr_type, default=default, working=working
            )
            if prev_value is not None and prev_value not in MISSINGNESS_VALUES:
                return prev_value

        return self.generic_missingness(attribute, attr_type, default=default)
