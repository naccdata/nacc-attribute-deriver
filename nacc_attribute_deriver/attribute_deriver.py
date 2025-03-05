"""
Defines the AttributeDeriver class.

Gear needs to iterate over all subjects, and for each subject,
call this AttributeDeriver (deriver.curate(file)) for all
(relevant) files in the subject. File must correspond to the
curation schema.
"""
from typing import Any, Dict
from pathlib import Path

from .attributes.attribute_map import (
    discover_collections,
    generate_attribute_schema,
)
from .attributes.utils.date import datetime_from_form_date
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
            schema = generate_attribute_schema(
                collections=self.__collections)

        self.__schema = CurationSchema(**schema)
        self.__date_key = self.__schema.date_key


    def curate(self, table: SymbolTable) -> None:
        """Curate the given file. Assumes has all the FW metadata required to
        curate the schema. Derived attributes will be added to the same table.

        Args:
            file: File to curate
        """
        # make sure date_key is in metadata
        if self.__date_key not in table or not table[self.__date_key]:
            raise ValueError(f"Table does not have specified date key: {self.__date_key}")

        collections = [c(table) for c in self.__collections]

        # derive NACC first, then MQT
        for attr in self.__schema.curation_order():
            found_hook = False
            for c in collections:
                hook = c.get_derive_hook(attr.function)
                if hook:
                    found_hook = True
                    value = hook(c)

                    for event in attr.events:
                        event.operation.evaluate(table, value, event.location,
                                                 date_key=self.__date_key)
                    break

            if not found_hook:
                raise ValueError(f"Unknown attribute function: {attr}")
