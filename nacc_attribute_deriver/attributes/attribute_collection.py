"""Implements a plugin infrastructure where each "plugin" is a collection of
attributes.

Heavily based off of
    https://eli.thegreenplace.net/2012/08/07/fundamental-concepts-of-plugin-infrastructures
"""

from inspect import isfunction
from types import FunctionType
from typing import Any, Callable, Dict, List, Optional, Union

from pydantic import BaseModel

from pydantic import BaseModel

from nacc_attribute_deriver.schema.errors import MissingRequiredException
from nacc_attribute_deriver.symbol_table import SymbolTable


class AttributeExpression(BaseModel):
    """An attribute expression is implemented as an application of a create
    function to the symbol table.

    This object holds the function object and the instance of an
    attribute collection instantiate on a symbol table.
    """

    class Config:
        arbitrary_types_allowed = True

    function: FunctionType
    instance: "AttributeCollection"

    def apply(self) -> Any:
        """Calls the function on the instance.

        Returns:
          the value returned by the function applied to the instance
        """
        return self.function(self.instance)


class AttributeCollectionRegistry(type):
    collections: List[type] = []

    def __init__(cls, name, bases, attrs):
        """Registers the class in the registry when the class has this class as
        a metaclass."""
        if name != "AttributeCollection":
            if name not in AttributeCollectionRegistry.collections:
                AttributeCollectionRegistry.collections.append(cls)

    @classmethod
    def get_attribute_methods(
        cls, table: SymbolTable
    ) -> Dict[str, AttributeExpression]:
        """Returns dictionary of the attribute methods in the registered
        collections.

        Args:
          table: the symbol table
        Returns:
          a dictionary mapping a function name to the attribute expression
        """
        methods = {}
        for collection in cls.collections:
            instance = collection(table)
            for name, function in instance.get_all_hooks().items():
                methods[name] = AttributeExpression(
                    function=function, instance=instance
                )

        return methods


class AttributeCollection(object, metaclass=AttributeCollectionRegistry):
    def __init__(
        self, table: SymbolTable, form_prefix: str = "file.info.forms.json."
    ) -> None:
    def __init__(
        self, table: SymbolTable, form_prefix: str = "file.info.forms.json."
    ) -> None:
        """Initializes the collection. Requires a SymbolTable containing all
        the relevant FW metadata necessary to derive the attributes.

        Args:
            table: SymbolTable which contains all necessary
                FW metadata information
            form_prefix: Form key prefix, which is where most variables
                to pull from are expected to live under.
        """
        self.table = table
        self.form_prefix = form_prefix

        raw_prefix = self.form_prefix.rstrip(".")
        if raw_prefix not in self.table:
            raise MissingRequiredException(
                f"Form prefix {raw_prefix} not found in current file"
            )

    @classmethod
    def get_all_hooks(cls) -> Dict[str, FunctionType]:
        """Grab all available _create_ functions."""
        result = {}
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isfunction(attr) and attr_name.startswith("_create_"):
                result[attr_name.lstrip("_")] = attr
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
            if isfunction(attr) and attr_name.startswith("_create_"):
                if attr_name.lstrip("_") == derive_name:
                    return attr

        return None

    def get_value(
        self, key: str, default: Optional[Any] = None, prefix: Optional[str] = None
    ) -> Any:
    def get_value(
        self, key: str, default: Optional[Any] = None, prefix: Optional[str] = None
    ) -> Any:
        """Grab value from the table using the key and prefix, if provided. If
        not specified, prefix will default to self.form_prefix.

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
            prefix: Prefix to attach to key. Use the empty string
                to explicitly not set a prefix.
        """
        if prefix is None:
            prefix = self.form_prefix

        return self.table.get(f"{prefix}{key}", default)

    def set_value(self, key: str, value: Any, prefix: Optional[str] = None) -> None:
        """Set the value from the table using the specified key and prefix.

        Args:
            key: Key to set to the value to
            value: Value to set
            prefix: Prefix to attach to key
        """
        if prefix is None:
            prefix = self.form_prefix

        self.table[f"{prefix}{key}"] = value

    def aggregate_variables(
        self,
        fields: List[str],
        default: Optional[Any] = None,
        prefix: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Aggregates all the specified fields.

        Args:
            fields: Fields to iterate over. Grabs the field and sets it
                     to the found/derived value.
            default: Default value to set aggregation to if not found
            prefix: Prefix key to pull mapped values out of. This prefix
                will be applied to ALL keys in the map.
        Returns:
            The aggregated variables
        """
        result = {}
        for field in fields:
            result[field] = self.get_value(field, default, prefix)

        return result

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

        return False
