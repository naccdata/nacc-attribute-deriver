"""
Base class to define a collection of attributes.
"""
from inspect import isfunction
from typing import Any, Callable, Dict, List, Union

from nacc_attribute_deriver.deriver.symbol_table import SymbolTable


class AttributeCollection:
    """Class to define a collection of attributes.

    All derived variables should be part of an attribute class.
    """

    def __init__(self,
                 table: SymbolTable,
                 form_prefix: str = 'file.info.forms.json.') -> None:
        """Initializer.

        Args:
            table: SymbolTable which contains all necessary
                FW metadata information
        """
        self.table = table
        self.__form_prefix = form_prefix

    def get_value(self,
                  key: str,
                  default: Any = None,
                  prefix: str = None) -> Any:
        """Grab value from the table using the key and prefix,
        if provided. If not specified, prefix will default to
        self.form_prefix

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
            prefix: Prefix to attach to key. Use the empty string
                to explicitly not set a prefix.
        """
        if prefix is None:
            prefix = self.__form_prefix

        return self.table.get(f'{prefix}{key}', default)

    def set_value(self, key: str, value: Any, prefix: str = None) -> None:
        """Set the value from the table using the specified key
        and prefix.

        Args:
            key: Key to set to the value to
            value: Value to set
            prefix: Prefix to attach to key
        """
        if prefix is None:
            prefix = self.__form_prefix

        self.table[f'{prefix}{key}'] = value

    def aggregate_variables(self,
                            mapping: Dict[str, Any],
                            default: Any = None,
                            prefix: str = None) -> Dict[str, Any]:
        """Aggregates all the variables defined in the mapping.

        Args:
            mapping: Mapping to iterate over. Grabs the field and sets it
                     to the found/derived value.
            default: Default value to set aggregation to if not found
            prefix: Prefix key to pull mapped values out of. This prefix
                will be applied to ALL keys in the map.
        Returns:
            The aggregated variables
        """
        result = {}
        for field, label in mapping.items():
            result[field] = self.get_value(field, default, prefix)

        return result

    @staticmethod
    def is_int_value(value: Union[int, str], target: int) -> bool:
        """Check whether the value is the specified target int.
        This might be overkill but wanted it to handle str/int comparisons.

        Args:
            value: Field to check
            target: Target to check against
        """
        if not value:
            return False

        try:
            return int(value) == target
        except ValueError as e:
            return False

        return False

    @classmethod
    def collect_attributes(cls) -> Dict[str, Dict[str, Callable]]:
        """Aggregates all _create functions and returns a mapping from
        function name to the class and callable.
        """
        result = {}
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isfunction(attr) and attr_name.startswith('_create_'):
                result[attr_name.lstrip('_')] = {
                    'class': cls,
                    'function': attr
                }

        return result


class NACCAttribute(AttributeCollection):
    """Currently doesn't have anything specific going on, but
    may be useful later."""


class MQTAttribute(AttributeCollection):
    """MQT-specific attribute collection.

    The main difference is that MQT variables often require that a
    derived NACC variable has already been set.
    """

    def assert_required(self,
                        required: List[str],
                        prefix: str = 'file.info.derived.') -> Dict[str, Any]:
        """Asserts that the given fields in required are in the
        table for the source

        Args:
            required: The required fields
            prefix: Key prefix the required field is expected to be under
        Returns:
            The found required variables, flattened out from the table
        """
        found = {}
        for r in required:
            full_field = f'{prefix}{r}'
            if full_field not in self.table:          # TODO: maybe can implicitly derive even if schema didn't define it?
                source = inspect.stack()[1].function  # not great but preferable to passing the name every time
                raise ValueError(f"{full_field} must be derived before {source} can run")

            found[r] = self.table[full_field]

        return found
