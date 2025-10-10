"""Base attributes, derive directly from AttributeCollection."""

import datetime
import logging
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar,
)

from pydantic import ValidationError

from nacc_attribute_deriver.schema.constants import INVALID_TEXT
from nacc_attribute_deriver.schema.errors import InvalidFieldError, MissingRequiredError
from nacc_attribute_deriver.schema.rule_types import DateTaggedValue
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import date_from_form_date

log = logging.getLogger(__name__)


T = TypeVar("T")


class BaseNamespace:
    """Abstract base class for wrapping a symbol table to enable accessing
    attribute values by name, without the full prefix."""

    def __init__(
        self,
        *,
        table: SymbolTable,
        attribute_prefix: str,
        required: frozenset[str] = frozenset(),
        date_attribute: Optional[str] = None,
    ):
        """Initializes an attribute wrapper, setting the prefix for accessing
        attributes.

        Args:
          table: the symbol table
          attribute_prefix: the prefix used to access values

        Raises:
          MissingRequiredError if any required attributes are missing
        """
        self.__table = table
        self.__prefix = (
            attribute_prefix if attribute_prefix[-1] == "." else f"{attribute_prefix}."
        )
        self.__date_attribute = date_attribute
        self.__required = (
            required.union([date_attribute]) if date_attribute else required
        )

        self.__check_required()

    def __check_required(self) -> None:
        """Check that required attributes have a value in the table.

        Raises:
          MissingRequiredError if any required attributes are missing
        """
        missing: List[str] = []
        for attribute in self.__required:
            value = self.get_value(attribute, str)
            if value is not None:
                continue

            missing.append(self.__symbol(attribute))

        if missing:
            raise MissingRequiredError(missing)

    @property
    def prefix(self) -> str:
        """Returns the attribute prefix for this object."""
        return self.__prefix

    def __symbol(self, attribute: str) -> str:
        """Returns the symbol table path for the attribute."""
        return f"{self.prefix}{attribute}"

    def __contains__(self, attribute: str) -> bool:
        """Indicates whether the attribute occurs in the table."""
        return self.__symbol(attribute) in self.__table

    def is_required(self, attribute: str) -> bool:
        """Indicates whether the attribute is required in this namespace.

        Args:
          attribute: the attribute name
        Returns:
          True if the attribute is required. False, otherwise.
        """
        return attribute in self.__required

    @property
    def required_fields(self) -> Iterable[str]:
        """Returns the required fields for this namespace."""
        return self.__required

    def get_value(
        self, attribute: str, attr_type: Type[T], default: Optional[T] = None
    ) -> Optional[T]:
        """Returns the value of the attribute key in the table.

        Args:
          attribute: the attribute name
          attr_type: the attribute type; an error is thrown if the
            non-null grabbed value cannot be casted to it
          default: the default value
        Returns:
          the value for the attribute in the table
        """
        value = self.__table.get(self.__symbol(attribute), default)  # type: ignore
        if value is None:
            return value

        # strip whitespace
        if isinstance(value, str):
            value = value.strip()

            # treat empty/invalid strings as None
            if value in INVALID_TEXT:
                return None

        try:
            return attr_type(value)  # type: ignore
        except TypeError as e:
            raise InvalidFieldError(
                f"{self.__symbol(attribute)} must be of type {attr_type}"
            ) from e

    def get_required(self, attribute: str, attr_type: Type[T]) -> T:
        """Get required value with given type. Throws an error if the attribute
        is missing, None, or the empty string, or cannot be casted to the
        expected type.

        Args:
            attribute: The attribute to grab
            attr_type: The expected attribute type
        Returns:
            The attribute value with the given type
        """
        assert self.is_required(attribute), f"{attribute} must be set as required"
        value = self.get_value(attribute, attr_type)
        if value is None:
            raise InvalidFieldError(f"{self.__symbol(attribute)} cannot be missing")

        return value

    def get_date(self) -> Optional[datetime.date]:
        """Returns the value for the date-attribute if defined.

        Returns:
          the value of the date-attribute if defined. None, otherwise.
        """
        if self.__date_attribute is None:
            return None

        return date_from_form_date(self.get_value(self.__date_attribute, str))

    def group_attributes(
        self, attributes: List[str], attr_type: Type[T]
    ) -> List[T | None]:
        """Group attributes into a list. Assumes all are the same type.

        Args:
            attributes: List of attributes to grab
            attr_type: Expected attribute type for all attributes in list
        """
        return [self.get_value(x, attr_type) for x in attributes]


class FormNamespace(BaseNamespace):
    """Base class for attributes over file.info.forms."""

    def __init__(
        self,
        *,
        table: SymbolTable,
        attribute_prefix: str = "file.info.forms.json.",
        required: frozenset[str] = frozenset(),
        date_attribute: str = "visitdate",
    ) -> None:
        super().__init__(
            table=table,
            attribute_prefix=attribute_prefix,
            required=required,
            date_attribute=date_attribute,
        )


class RawNamespace(BaseNamespace):
    """Base class for attributes over file.info.raw."""

    def __init__(
        self,
        table: SymbolTable,
        attribute_prefix: str = "file.info.raw.",
        required: frozenset[str] = frozenset(),
        date_attribute: Optional[str] = None,
    ) -> None:
        super().__init__(
            table=table,
            attribute_prefix=attribute_prefix,
            required=required,
            date_attribute=date_attribute,
        )


class DerivedNamespace(BaseNamespace):
    """Base class for attributes over file.info.derived."""

    def __init__(
        self,
        *,
        table: SymbolTable,
        attribute_prefix: str = "file.info.derived.",
        required: frozenset[str] = frozenset(),
        date_attribute: Optional[str] = None,
    ) -> None:
        super().__init__(
            table=table,
            attribute_prefix=attribute_prefix,
            required=required,
            date_attribute=date_attribute,
        )


class SubjectInfoNamespace(BaseNamespace):
    def __init__(
        self,
        *,
        table: SymbolTable,
        attribute_prefix: str = "subject.info.",
        required: frozenset[str] = frozenset(),
        date_attribute: Optional[str] = None,
    ):
        super().__init__(
            table=table,
            attribute_prefix=attribute_prefix,
            required=required,
            date_attribute=date_attribute,
        )


class SubjectDerivedNamespace(BaseNamespace):
    """For NACC derived cross-sectional and longitudinal variables."""

    def __init__(
        self,
        *,
        table: SymbolTable,
        attribute_prefix: str = "subject.info.derived.",
        required: frozenset[str] = frozenset(),
        date_attribute: Optional[str] = None,
    ) -> None:
        super().__init__(
            table=table,
            attribute_prefix=attribute_prefix,
            required=required,
            date_attribute=date_attribute,
        )

    def cast_to_dated_tagged_value(
        self, attribute: str, raw_value: Dict[str, Any], attr_type: Type[T]
    ) -> DateTaggedValue:
        """Cast given value to DateTaggedValue."""
        if not isinstance(raw_value, dict):
            raise InvalidFieldError("Cannot cast non-dict to DateTaggedValue")

        try:
            value = DateTaggedValue(**raw_value)
        except ValidationError as e:
            raise InvalidFieldError(
                f"Cannot cast cross-sectional value for {attribute} to "
                + f"DateTaggedValue from {raw_value}: {e}"
            ) from e

        try:
            if value.value is not None:
                value.value = attr_type(value.value)  # type: ignore
        except TypeError as e:
            raise InvalidFieldError(
                f"{attribute}.value must be of type {attr_type}"
            ) from e

        return value

    def get_cross_sectional_value(
        self, attribute: str, attr_type: Type[T], default: Optional[Any] = None
    ) -> Optional[T]:
        """Returns a cross-sectional value.

        Args:
            attribute: The field to grab cross-sectional value for
            attr_type: Attribute type
            default: default value
        Returns:
          the value for the attribute in the table
        """
        return self.get_value(f"cross-sectional.{attribute}", attr_type, default)

    def get_cross_sectional_dated_value(
        self, attribute: str, attr_type: Type[T]
    ) -> Optional[DateTaggedValue]:
        """Returns the value of a cross-sectional dated value.

        Args:
            attribute: The field to grab cross-sectional value for
            attr_type: Attribute type
            default: default value
        Returns:
          the value for the dated attribute in the table
        """
        raw_value = self.get_cross_sectional_value(attribute, dict)
        if not raw_value:
            return None

        return self.cast_to_dated_tagged_value(attribute, raw_value, attr_type)

    def get_longitudinal_value(
        self, attribute: str, attr_type: Type[T]
    ) -> Optional[List[DateTaggedValue]]:
        """Returns a longitudinal value. Will be a list of DatedTaggedValues.
        This does not support default values.

        Args:
            attribute: The field to grab longitudinal values for
            attr_type: Attribute type
        Returns:
          the list of DateTaggedValues for the attribute in the table
        """
        records = self.get_value(f"longitudinal.{attribute}", list)
        if not records:
            return None

        # cast to DateTaggedValues
        for i, record in enumerate(records):
            records[i] = self.cast_to_dated_tagged_value(attribute, record, attr_type)

        return records

    def get_corresponding_longitudinal_value(
        self, target_date: str, attribute: str, attr_type: Type[T]
    ) -> Optional[T]:
        """Returns the longitudinal value corresponding to the given date. This
        does not support default values.

        Args:
            attribute: The field to grab longitudinal values for
            attr_type: Attribute type
        Returns:
          the value for the attribute in the table
        """
        records = self.get_longitudinal_value(attribute, attr_type)
        if not records:
            return None

        for record in reversed(records):
            if str(record.date) == target_date:
                return record.value

        return None

    def get_prev(self, attribute: str, attr_type: Type[T]) -> Optional[DateTaggedValue]:
        """Gets the previous record - pulls from longitudinal records.

        Args:
            attribute: The field to grab the previous longitudinal record for
            attr_type: Attribute type
        Returns:
            The previous DateTaggedValue
        """
        records = self.get_longitudinal_value(attribute, attr_type)
        if records is None:
            return None

        prev_record = None

        # sanity check make sure we are not grabbing this form's values;
        # e.g. break for loop as soon as we get the most recent record
        # that isn't this form's
        for record in reversed(records):
            if record.date != self.get_date():
                prev_record = record
                break

        # even for non-initial visits sometimes we simply don't
        # have the previous visit in Flywheel
        if not prev_record:
            return None

        return prev_record

    def get_prev_value(self, attribute: str, attr_type: Type[T]) -> Optional[T]:
        """Get prev value, if we don't necessarily care about date.

        Args:
            attribute: The field to grab the previous longitudinal record for
            attr_type: Attribute type
        Returns:
            The previous value
        """
        prev_record = self.get_prev(attribute, attr_type)
        return None if prev_record is None else prev_record.value


class WorkingDerivedNamespace(SubjectDerivedNamespace):
    """Similar to SubjectDerivedNamespace but specifically for
    working/temporary variables."""

    def __init__(
        self,
        *,
        table: SymbolTable,
        attribute_prefix: str = "subject.info.working.",
        required: frozenset[str] = frozenset(),
        date_attribute: Optional[str] = None,
    ) -> None:
        super().__init__(
            table=table,
            attribute_prefix=attribute_prefix,
            required=required,
            date_attribute=date_attribute,
        )
