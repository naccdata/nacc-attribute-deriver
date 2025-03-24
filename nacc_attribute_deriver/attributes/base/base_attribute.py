"""Base attributes, derive directly from AttributeCollection."""

import logging
from abc import ABC
from typing import Any, List, Optional

from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable

log = logging.getLogger(__name__)


class BaseAttribute(ABC):
    """Abstract base class for wrapping a symbol table to enable accessing
    attribute values by name, without the full prefix."""

    def __init__(self, table: SymbolTable, attribute_prefix: str):
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

    def __contains__(self, key: str) -> bool:
        return f"{self.__prefix}{key}" in self.__table

    @property
    def prefix(self) -> str:
        """Returns the attribute prefix for this object."""
        return self.__prefix

    def get_value(self, key: str, default: Optional[Any] = None) -> Any:
        """Grab value from the table using the key and prefix, if provided. If
        not specified, prefix will default to self.form_prefix.

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
            prefix: Prefix to attach to key. Use the empty string
                to explicitly not set a prefix.
        """
        return self.__table.get(f"{self.prefix}{key}", default)

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


class FormAttribute(BaseAttribute):
    """Base class for attributes over file.info.forms."""

    def __init__(
        self, table: SymbolTable, attribute_prefix: str = "file.info.forms.json."
    ) -> None:
        super().__init__(table, attribute_prefix)


class RawAttribute(BaseAttribute):
    """Base class for attributes over file.info.raw."""

    def __init__(
        self, table: SymbolTable, attribute_prefix: str = "file.info.raw."
    ) -> None:
        super().__init__(table, attribute_prefix)


class DerivedAttribute(BaseAttribute):
    """Base class for attributes over file.info.derived."""

    def __init__(
        self, table: SymbolTable, attribute_prefix="file.info.derived."
    ) -> None:
        super().__init__(table, attribute_prefix)


class SubjectDerivedAttribute(BaseAttribute):
    def __init__(
        self, table: SymbolTable, attribute_prefix: str = "subject.info.derived."
    ) -> None:
        super().__init__(table, attribute_prefix)


class SubjectInfoAttribute(BaseAttribute):
    def __init__(self, table: SymbolTable, attribute_prefix: str = "subject.info."):
        super().__init__(table, attribute_prefix)
