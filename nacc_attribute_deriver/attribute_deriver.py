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
from .schema.schema import (
    CurationSchema,
    DeriveEvent,
    EventType,
)
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

    def handle_event(self,
                     value: Any,
                     event: DeriveEvent,
                     table: SymbolTable) -> None:
        """Calculate the appropriate value given the event and set it
        in the table.

        Args:
            value: Value to act on
            event_type: Event to evaluate
            table: Table with all the required metadata to evaluate
        """
        # TODO: do we allow null values to go through? might depend on event type
        # if not value:
        #     return

        event_type = event.event
        if event_type == EventType.UPDATE:
            table[event.location] = value

        # assumes location has a date attached to it for these
        elif event_type in [EventType.INITIAL, EventType.LATEST]:
            cur_date = datetime_from_form_date(table[self.__date_key])
            dest_date = datetime_from_form_date(table.get(f'{event.location}.date'))

            if (not dest_date or
                (event_type == EventType.INITIAL and cur_date < dest_date) or
                (event_type == EventType.LATEST and cur_date > dest_date)):
                table[event.location] = {
                    'date': str(cur_date.date()),
                    'value': value
                }

        elif event_type == EventType.COUNT:
            cur_count = table.get(event.location, 0)
            table[event.location] = cur_count + 1

        elif event_type in [EventType.MIN, EventType.MAX]:
            dest_value = table.get(event.location, None)
            if (not dest_value or
                (event_type == EventType.MIN and value < dest_value) or
                (event_type == EventType.MAX and value > dest_value)):

                table[event.location] = value

        elif event_type == EventType.SET:
            cur_set = table.get(event.location)
            cur_set = set(cur_set) if cur_set else set()

            if isinstance(value, (list, set)):
                cur_set.union(set(value))
            elif value is not None:
                cur_set.add(value)

            table[event.location] = list(cur_set)
        elif event_type == EventType.BOOL:
            if not table.get(event.location, False):
                table[event.location] = value
        else:
            raise ValueError(f"Cannot handle event type: {event_type}")

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
                        self.handle_event(value, event, table)
                    break

            if not found_hook:
                raise ValueError(f"Unknown attribute function: {attr}")
