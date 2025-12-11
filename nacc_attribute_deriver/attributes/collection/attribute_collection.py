"""Implements a plugin infrastructure where each "plugin" is a collection of
attributes.

Heavily based off of
    https://eli.thegreenplace.net/2012/08/07/fundamental-concepts-of-plugin-infrastructures
"""

import datetime
import logging
from inspect import isfunction
from types import FunctionType
from typing import Any, Callable, ClassVar, Dict, List, Optional, Tuple, Type

from pydantic import BaseModel, ConfigDict

from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import CURATION_TYPE
from nacc_attribute_deriver.utils.errors import AttributeDeriverError

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

    def apply(self, table: SymbolTable) -> Tuple[Any, datetime.date | None]:
        """Calls the function on the instance.

        Returns:
          the value returned by the function applied to the instance and
          corresponding date, if applicable
        Raises:
            MissingRequiredError if the attribute class cannot be instantiated
            on the table
        """
        instance = self.attribute_class(table)
        return self.function(instance), instance.get_date()

    def apply_with_field(
        self,
        table: SymbolTable,
        field: str,
        attr_type: Type,
    ) -> Tuple[Any, datetime.date | None]:
        """Apply the function on the instance with the field passed as a
        parameter.

        Returns:
          the value returned by the function applied to the instance and
          corresponding date, if applicable
        Raises:
            MissingRequiredError if the attribute class cannot be instantiated
            on the table
        """
        instance = self.attribute_class(table)
        return self.function(instance, field, attr_type), instance.get_date()


class AttributeCollectionRegistry(type):
    collection_types: ClassVar[List[type]] = []

    def __init__(
        cls, name: str, bases: Tuple[type], attrs: Dict[str, str | FunctionType]
    ):
        """Registers the class in the registry when the class has this class as
        a metaclass."""
        if (
            name != "AttributeCollection"
            and name not in AttributeCollectionRegistry.collection_types  # type: ignore
        ):
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
        methods: Dict[str, AttributeExpression] = {}
        for collection_type in cls.collection_types:
            for name, function in collection_type.get_all_hooks().items():  # type: ignore
                if name in methods:
                    raise AttributeDeriverError(f"Attribute {name} already defined")

                methods[name] = AttributeExpression(
                    function=function,  # type: ignore
                    attribute_class=collection_type,
                )

        return methods


class AttributeCollection(object, metaclass=AttributeCollectionRegistry):
    def __init__(self, table: SymbolTable) -> None:
        pass

    @classmethod
    def get_all_hooks(cls) -> Dict[str, FunctionType]:
        """Grab all available _create_ and _missingness_ functions."""
        result: Dict[str, FunctionType] = {}
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isfunction(attr) and any(
                attr_name.startswith(f"_{derive_type}_")
                for derive_type in CURATION_TYPE
            ):
                hook = attr_name.lstrip("_")
                if hook in result:
                    raise AttributeDeriverError(
                        f"Attribute {attr_name} already defined"
                    )
                result[hook] = attr

        return result

    @classmethod
    def get_derive_hook(cls, derive_name: str) -> Optional[Callable[[], Any]]:
        """Aggregates all _create  and _missingness_functions and returns the
        function if derive_name matches. Throws error otherwise.

        Args:
            derive_name: Derive function name to search for
        Returns:
            _create_ or _missingness_ function, if defined for this class
        """
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if (
                isfunction(attr)
                and any(
                    attr_name.startswith(f"_{derive_type}_")
                    for derive_type in CURATION_TYPE
                )
                and attr_name.lstrip("_") == derive_name
            ):
                return attr

        return None

    def get_date(self) -> Optional[datetime.date]:
        """Get date corresponding to this attribute collection from a specific
        namespace, if applicable.

        May return None for collections where dates do not make sense
        (genetics, derived) or those with multiple dated namespaces
        (cross-module).
        """
        return None
