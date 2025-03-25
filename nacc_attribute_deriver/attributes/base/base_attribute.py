"""Base attributes, derive directly from AttributeCollection."""

import datetime
import logging
from abc import ABC
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, field_serializer

from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import datetime_from_form_date

log = logging.getLogger(__name__)


class AttributeValue(BaseModel):
    """Model for a date-tagged attribute value."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    date: Optional[datetime.date]
    value: Any

    @field_serializer("date")
    def serialize_date_as_str(self, date: Optional[datetime.date]):
        return str(date)


class BaseNamespace(ABC):
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

    def get_value(self, attribute: str, default: Optional[Any] = None) -> Any:
        """Returns the value of the attribute key in the table.

        Args:
          key: the attribute name
          default: the default value
        Returns:
          the value for the attribute in the table
        """
        return self.__table.get(f"{self.prefix}{attribute}", default)

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

    def get_dated_value(
        self, attribute: str, default: Optional[Any] = None
    ) -> AttributeValue:
        """Grab value from the table using the key and prefix, if provided.

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
        """
        return AttributeValue(
            value=self.get_value(attribute=attribute, default=default),
            date=self.get_date(),
        )

    def assert_required(self, required: List[str]) -> bool:
        """Asserts that the given fields in required are in the table for the
        source.

        Args:
            required: The list of required fields
        Returns:
          True if all required fields are present
        Raises:
          MissingRequiredError if a required field is missing
        """
        for attribute in required:
            full_field = f"{self.prefix}{attribute}"
            if full_field not in self.__table:
                raise MissingRequiredError(field=full_field)

        return True


class FormNamespace(BaseNamespace):
    """Base class for attributes over file.info.forms."""

    def __init__(
        self,
        table: SymbolTable,
        attribute_prefix: str = "file.info.forms.json.",
        date_attribute="visitdate",
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


class DerivedNamespace(BaseNamespace):
    """Base class for attributes over file.info.derived."""

    def __init__(
        self,
        table: SymbolTable,
        attribute_prefix="file.info.derived.",
        date_attribute: Optional[str] = None,
    ) -> None:
        super().__init__(table, attribute_prefix, date_attribute)


class SubjectDerivedNamespace(BaseNamespace):
    def __init__(
        self,
        table: SymbolTable,
        attribute_prefix: str = "subject.info.derived.",
        date_attribute: Optional[str] = None,
    ) -> None:
        super().__init__(table, attribute_prefix, date_attribute)


class SubjectInfoNamespace(BaseNamespace):
    def __init__(
        self,
        table: SymbolTable,
        attribute_prefix: str = "subject.info.",
        date_attribute: Optional[str] = None,
    ):
        super().__init__(table, attribute_prefix, date_attribute)
