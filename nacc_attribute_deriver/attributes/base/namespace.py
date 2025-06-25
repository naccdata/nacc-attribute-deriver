"""Base attributes, derive directly from AttributeCollection."""

import datetime
import logging
from typing import (
    Any,
    Generic,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar,
)

from pydantic import BaseModel, ConfigDict, field_serializer

from nacc_attribute_deriver.schema.errors import InvalidFieldError, MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import datetime_from_form_date

log = logging.getLogger(__name__)


T = TypeVar("T")


class DateTaggedValue(BaseModel, Generic[T]):
    """Model for a date-tagged attribute value."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    date: Optional[datetime.date]
    value: T

    @field_serializer("date")
    def serialize_date_as_str(self, date: Optional[datetime.date]):
        return str(date)


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
            # treat empty string as None
            if value == "":
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
        assert self.is_required(attribute)
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

        file_date = datetime_from_form_date(self.get_value(self.__date_attribute, str))
        if not file_date:
            return None

        return file_date.date()


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

    def get_cross_sectional_value(
        self, attribute: str, attr_type: Type[T], default: Optional[Any] = None
    ) -> Any:
        """Returns a cross-sectional value.

        Args:
          key: the attribute name
          default: the default value
        Returns:
          the value for the attribute in the table
        """
        return self.get_value(f"cross-sectional.{attribute}", attr_type, default)

    def get_longitudinal_value(
        self, attribute: str, attr_type: Type[T], default: Optional[Any] = None
    ) -> Any:
        """Returns a longitudinal value.

        Args:
          key: the attribute name
          default: the default value
        Returns:
          the value for the attribute in the table
        """
        return self.get_value(f"longitudinal.{attribute}", attr_type, default)
