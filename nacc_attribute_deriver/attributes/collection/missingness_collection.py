"""Class to handle form missingness values that check subject-level derived
variables."""

from typing import Optional, Tuple, Type

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
    RawNamespace,
    SubjectDerivedNamespace,
    T,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
    INVALID_TEXT,
    MISSINGNESS_VALUES,
)
from nacc_attribute_deriver.utils.date import (
    find_closest_date,
    standardize_date,
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
        namespace: Type[FormNamespace] | Type[RawNamespace] = FormNamespace,
        required: frozenset[str] = frozenset(),
        date_attribute: str | None = "visitdate",
    ) -> None:
        self.__form = namespace(
            table=table, required=required, date_attribute=date_attribute
        )
        self.__prev_record = PreviousRecordNamespace(table=table)

    @property
    def prev_record(self) -> PreviousRecordNamespace:
        return self.__prev_record

    @property
    def form(self) -> FormNamespace | RawNamespace:
        return self.__form

    def get_visitdate(self) -> Optional[str]:
        """Visitdate can come in several formats, so resolve everything to
        YYYY-MM-DD for consistency.

        Returns:
            visitdate as a string, if found, None otherwise
        """
        date_attribute = self.__form.date_attribute
        if not date_attribute:
            return None

        raw_visitdate = self.form.get_value(date_attribute, str)
        if not raw_visitdate:
            raise AttributeDeriverError(
                f"Unable to find date attribute {date_attribute}"
            )

        visitdate = standardize_date(raw_visitdate)
        if not visitdate:
            raise AttributeDeriverError(
                f"Unable to standardize {date_attribute} from {raw_visitdate}"
            )

        return visitdate

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
        if value is None or (attr_type == str and value in INVALID_TEXT):  # noqa: E721
            if default is not None:
                return default

            if attr_type == int:  # noqa: E721
                return INFORMED_MISSINGNESS  # type: ignore
            if attr_type == str:  # noqa: E721
                return INFORMED_BLANK  # type: ignore
            if attr_type == float:  # noqa: E721
                return float(INFORMED_MISSINGNESS)  # type: ignore

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

        If VAR == PREV_CODE, VAR = PREV_VISIT
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


class UDSCorrelatedFormMissingnessCollection(FormMissingnessCollection):
    """Class to handle missingness values at the file level for standalone
    forms that need to be correlated with an UDS visit.

    As such, the date attribute is required.
    """

    def __init__(
        self,
        table: SymbolTable,
        namespace: Type[FormNamespace] | Type[RawNamespace] = FormNamespace,
        required: frozenset[str] = frozenset(),
        date_attribute: str = "visitdate",
    ) -> None:
        """Initializer."""
        if not date_attribute:
            raise AttributeDeriverError("date_attribute required")

        required = required.union([date_attribute])
        super().__init__(table, namespace, required, date_attribute)

        self.__date_attribute = date_attribute
        self.__working = WorkingNamespace(table=table)

    def find_closest_uds_visit(self) -> Tuple[str, int]:
        """Find the closest UDS visit to this form. By calling this, the caller
        assumes that the UDS forms have already been curated, and that we can
        find UDS visitdates under subject.working.uds-visitdates.

        Returns:
            The most recent UDS visit's date and its NACCVNUM (which
                corresponds to its index in uds-visidates)
        """
        visitdate = self.get_visitdate()
        if not visitdate:
            raise AttributeDeriverError("Missing visitdate from form header")

        uds_visitdates = self.__working.get_cross_sectional_value(
            "uds-visitdates", list
        )

        # this shouldn't happen; assuming at least one UDS visit exists
        if not uds_visitdates:
            raise AttributeDeriverError("No UDS visits found to correlate")

        # index + 1 is effectively NACCVNUM
        uds_visit, index = find_closest_date(uds_visitdates, visitdate)
        return str(uds_visit), index + 1
