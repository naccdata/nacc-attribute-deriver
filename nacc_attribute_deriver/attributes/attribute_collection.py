"""Implements a plugin infrastructure where each "plugin" is a collection of
attributes.

Heavily based off of
    https://eli.thegreenplace.net/2012/08/07/fundamental-concepts-of-plugin-infrastructures
"""

import logging
from inspect import isfunction
from types import FunctionType
from typing import Any, Callable, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict

from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable

log = logging.getLogger(__name__)


class AttributeExpression(BaseModel):
    """An attribute expression is implemented as an application of a create
    function to the symbol table.

    This object holds the function object and the instance of an
    attribute collection instantiate on a symbol table.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    function: FunctionType
    attribute_class: type

    def apply(self, table: SymbolTable) -> Any:
        """Calls the function on the instance.

        Returns:
          the value returned by the function applied to the instance
        Raises:
            MissingRequiredError if the attribute class cannot be instantiated
            on the table
        """
        try:
            return self.function(self.attribute_class(table))
        except MissingRequiredError as error:
            log.warning(f"Unable to apply {self.function}: missing field {error.field}")

        return None


class AttributeCollectionRegistry(type):
    collection_types: List[type] = []

    def __init__(cls, name, bases, attrs):
        """Registers the class in the registry when the class has this class as
        a metaclass."""
        if name != "AttributeCollection":
            if name not in AttributeCollectionRegistry.collection_types:
                AttributeCollectionRegistry.collection_types.append(cls)

    @classmethod
    def get_attribute_methods(cls) -> Dict[str, AttributeExpression]:
        """Returns dictionary of the attribute methods in the registered
        collections.

        Args:
          table: the symbol table
        Returns:
          a dictionary mapping a function name to the attribute expression
        """
        methods = {}
        for collection_type in cls.collection_types:
            for name, function in collection_type.get_all_hooks().items():  # type: ignore
                methods[name] = AttributeExpression(
                    function=function, attribute_class=collection_type
                )

        return methods


class AttributeCollection(object, metaclass=AttributeCollectionRegistry):
    def __init__(self, table: SymbolTable) -> None:
        pass

    @classmethod
    def create(cls, table: SymbolTable) -> Optional["AttributeCollection"]:
        """Creates an attribute collection for the symbol table.

        Will return None if the collection is not applicable to the table.

        Args:
          table: the symbol table
        Returns:
          the attribute collection if it can use the table. None otherwise.
        """
        try:
            return cls(table)
        except MissingRequiredError as error:
            log.warning(error)
            return None

    @classmethod
    def get_all_hooks(cls) -> Dict[str, FunctionType]:
        """Grab all available _create_ functions."""
        result = {}
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isfunction(attr) and attr_name.startswith("_create_"):
                result[attr_name.lstrip("_")] = attr

        return result

    @classmethod
    def get_derive_hook(cls, derive_name: str) -> Optional[Callable]:
        """Aggregates all _create functions and returns the function if
        derive_name matches. Throws error otherwise.

        Args:
            derive_name: Derive function name to search for
        Returns:
            _create_ function, if defined for this class
        """
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isfunction(attr) and attr_name.startswith("_create_"):
                if attr_name.lstrip("_") == derive_name:
                    return attr

        return None

    @staticmethod
    def is_int_value(value: Union[int, str], target: int) -> bool:
        """Check whether the value is the specified target int. This might be
        overkill but wanted it to handle str/int comparisons.

        Args:
            value: Field to check
            target: Target to check against
        """
        if not value:
            return False

        try:
            return int(value) == target
        except ValueError:
            return False
