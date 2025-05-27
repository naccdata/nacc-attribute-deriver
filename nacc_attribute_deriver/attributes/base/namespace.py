"""Base attributes, derive directly from AttributeCollection."""

import datetime
import logging
from typing import Any, Generic, Iterable, Optional, TypeVar, overload

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
        table: SymbolTable,
        attribute_prefix: str,
        date_attribute: Optional[str] = None,
    ):
        """Initializes an attribute wrapper, setting the prefix for accessing
        attributes.

        Args:
          table: the symbol table
          attribute_prefix: the prefix used to access values
        """
        self.__table = table
        self.__prefix = (
            attribute_prefix if attribute_prefix[-1] == "." else f"{attribute_prefix}."
        )
        self.__date_attribute = date_attribute

    def __contains__(self, key: str) -> bool:
        return f"{self.__prefix}{key}" in self.__table

    @property
    def prefix(self) -> str:
        """Returns the attribute prefix for this object."""
        return self.__prefix

    def get_value(self, attribute: str, default: Optional[Any] = None) -> Optional[Any]:
        """Returns the value of the attribute key in the table.

        Args:
          key: the attribute name
          default: the default value
        Returns:
          the value for the attribute in the table
        """
        return self.__table.get(f"{self.prefix}{attribute}", default)  # type: ignore

    def get_date(self) -> Optional[datetime.date]:
        """Returns the value for the date-attribute if defined.

        Returns:
          the value of the date-attribute if defined. None, otherwise.
        """
        if self.__date_attribute is None:
            return None

        file_date = datetime_from_form_date(self.get_value(self.__date_attribute))
        if not file_date:
            return None

        return file_date.date()

    def create_dated_value(
        self,
        attribute: str,
        date: Optional[datetime.date],
        default: Optional[Any] = None,
    ) -> Optional[DateTaggedValue[Any]]:
        """Create a DateTaggedValue for the value of the attribute from this
        namespace.

        Args:
          attribute: the attribute
          date: the date to tag the value with
          default: value to use if the attribute has no value in this namespace.
        Returns:
          value of the attribute tagged by the date. None if there is no value.
        """
        attribute_value = self.get_value(attribute=attribute, default=default)
        if attribute_value is None:
            return None

        return DateTaggedValue(value=attribute_value, date=date)

    def get_dated_value(
        self, attribute: str, default: Optional[Any] = None
    ) -> Optional[DateTaggedValue[Any]]:
        """Grab value from the table using the key and prefix, if provided.

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
        """
        return self.create_dated_value(attribute, self.get_date(), default)

    def get_int_value(self, attribute: str) -> Optional[int]:
        """Gets the value for an integer attribute.

        Args:
          attribute: the attribute
        Returns:
          the integer value of attribute if exists. None, otherwise.
        Raises:
          TypeError if the value of the attribute is not an integer
        """
        attribute_value = self.get_value(attribute)
        if attribute_value is None:
            return None

        try:
            return int(attribute_value)
        except ValueError as error:
            raise InvalidFieldError(f"{attribute} expected to be an integer") from error

    @overload
    def scope(self, *, name: str) -> "NamespaceScope": ...

    @overload
    def scope(self, *, fields: Iterable[str]) -> "NamespaceScope": ...

    @overload
    def scope(self, *, name: str, fields: Iterable[str]) -> "NamespaceScope": ...

    def scope(
        self,
        *,
        name: Optional[str] = None,
        fields: Optional[Iterable[str]] = None,
    ) -> "NamespaceScope":
        if name is None or fields is None:
            raise ScopeDefinitionError("Scope definition is incomplete")

        return NamespaceScope(namespace=self, name=name, fields=fields)


class ScopeDefinitionError(Exception):
    pass


class NamespaceScope:
    def __init__(
        self, namespace: BaseNamespace, name: str, fields: Iterable[str]
    ) -> None:
        self.__namespace = namespace
        self.__scope_name = name
        self.__fields = fields

    @property
    def namespace(self):
        return self.__namespace

    def __filter_value(self, attribute: str, value: Any) -> Any:
        if value is not None:
            return value

        if attribute not in self.__fields:
            return None

        field = f"{self.namespace.prefix}{attribute}"
        raise MissingRequiredError(
            message=f"Missing required field: {field} for scope {self.__scope_name}",
            field=field,
        )

    def get_value(self, attribute: str) -> Optional[Any]:
        """Returns the value of the attribute key in the table if it is in
        scope.

        Otherwise, raises exception
        """
        return self.__filter_value(
            attribute=attribute, value=self.__namespace.get_value(attribute)
        )

    def create_dated_value(
        self,
        attribute: str,
        date: Optional[datetime.date],
        default: Optional[Any] = None,
    ) -> Optional[DateTaggedValue[Any]]:
        return self.__filter_value(
            attribute=attribute,
            value=self.__namespace.create_dated_value(
                attribute=attribute, date=date, default=default
            ),
        )

    def get_int_value(self, attribute: str) -> Optional[int]:
        return self.__filter_value(
            attribute=attribute,
            value=self.__namespace.get_int_value(attribute=attribute),
        )


class FormNamespace(BaseNamespace):
    """Base class for attributes over file.info.forms."""

    def __init__(
        self,
        table: SymbolTable,
        attribute_prefix: str = "file.info.forms.json.",
        date_attribute: str = "visitdate",
    ) -> None:
        super().__init__(table, attribute_prefix, date_attribute)


class RawNamespace(BaseNamespace):
    """Base class for attributes over file.info.raw."""

    def __init__(
        self,
        table: SymbolTable,
        attribute_prefix: str = "file.info.raw.",
        date_attribute: Optional[str] = None,
    ) -> None:
        super().__init__(table, attribute_prefix, date_attribute)

    def scope(
        self,
        *,
        name: Optional[str] = None,
        fields: Optional[Iterable[str]] = None,
    ) -> NamespaceScope:
        if not fields:
            raise ScopeDefinitionError("File raw scope definition incomplete")

        return super().scope(name="file-raw", fields=fields)


class DerivedNamespace(BaseNamespace):
    """Base class for attributes over file.info.derived."""

    def __init__(
        self,
        table: SymbolTable,
        attribute_prefix: str = "file.info.derived.",
        date_attribute: Optional[str] = None,
    ) -> None:
        super().__init__(table, attribute_prefix, date_attribute)

    def scope(
        self,
        *,
        name: Optional[str] = None,
        fields: Optional[Iterable[str]] = None,
    ) -> NamespaceScope:
        if not fields:
            raise ScopeDefinitionError("File-derived scope definition incomplete")

        return super().scope(name="file-derived", fields=fields)


class SubjectInfoNamespace(BaseNamespace):
    def __init__(
        self,
        table: SymbolTable,
        attribute_prefix: str = "subject.info.",
        date_attribute: Optional[str] = None,
    ):
        super().__init__(table, attribute_prefix, date_attribute)


class SubjectDerivedNamespace(BaseNamespace):
    def __init__(
        self,
        table: SymbolTable,
        attribute_prefix: str = "subject.info.derived.",
        date_attribute: Optional[str] = None,
    ) -> None:
        super().__init__(table, attribute_prefix, date_attribute)

    def get_cross_sectional_value(
        self, attribute: str, default: Optional[Any] = None
    ) -> Any:
        """Returns a cross-sectional value.

        Args:
          key: the attribute name
          default: the default value
        Returns:
          the value for the attribute in the table
        """
        return self.get_value(f"cross-sectional.{attribute}", default)

    def get_longitudinal_value(
        self, attribute: str, default: Optional[Any] = None
    ) -> Any:
        """Returns a longitudinal value.

        Args:
          key: the attribute name
          default: the default value
        Returns:
          the value for the attribute in the table
        """
        return self.get_value(f"longitudinal.{attribute}", default)

    def scope(
        self,
        *,
        name: Optional[str] = None,
        fields: Optional[Iterable[str]] = None,
    ) -> NamespaceScope:
        if not fields:
            raise ScopeDefinitionError("Subject-derived scope definition incomplete")

        return super().scope(
            name="subject-derived",
            fields=fields,
        )
