"""Defines the AttributeDeriver class.

Gear needs to iterate over all subjects, and for each subject, call this
AttributeDeriver (deriver.curate(file)) for all (relevant) files in the
subject. File must correspond to the curation schema.
"""
from typing import Any, Dict

from .attributes.attribute_map import (
    discover_collections,
    generate_attribute_schema,
)
from .schema.schema import CurationSchema
from .symbol_table import SymbolTable


class AttributeDeriver:

    def __init__(self, schema: Dict[str, Any] = None):
        """Initiailzer.

        Args:
            schema: Raw curation schema; if not provided,
                generates the all-attribute schema
        """
        # get all available collections
        self.__collections = discover_collections()

        if not schema:
            schema = generate_attribute_schema(collections=self.__collections)

        self.__schema = CurationSchema(**schema)
        self.__date_key = self.__schema.date_key

    def curate(self, table: SymbolTable) -> None:
        """Curate the given file. Assumes has all the FW metadata required to
        curate the schema. Derived attributes will be added to the same table.

        Args:
            table: Table with file data to curate
        """
        # make sure date_key is in metadata
        if self.__date_key not in table or not table[self.__date_key]:
            raise ValueError(
                f"Table does not have specified date key: {self.__date_key}")

        collections = [c(table) for c in self.__collections]
        instance_collections = {}

        # collect all attributes beforehand so they're easily hashable
        for instance in [c(table) for c in self.__collections]:
            instance_collections.update({
                k: {
                    'func': v,
                    'instance': instance
                }
                for k, v in instance.get_all_hooks().items()
            })

        # derive NACC first, then MQT
        for attr in self.__schema.curation_order():
            hook = instance_collections.get(attr.function, None)
            if not hook:
                raise ValueError(
                    f"Unknown attribute function: {attr.function}")

            value = hook['func'](hook['instance'])

            for event in attr.events:
                event.operation.evaluate(table,
                                         value,
                                         event.location,
                                         date_key=self.__date_key)
