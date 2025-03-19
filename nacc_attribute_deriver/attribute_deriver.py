"""Defines the AttributeDeriver class.

Gear needs to iterate over all subjects, and for each subject, call this
AttributeDeriver (deriver.curate(file)) for all (relevant) files in the
subject. File must correspond to the curation schema.
"""
import csv
from pathlib import Path
from typing import Dict, List, Optional

from .attributes.attribute_collection import AttributeCollectionRegistry
from .schema.errors import AttributeDeriverException
from .schema.schema import AttributeSchema, DeriveEvent
from .schema.operation import DateOperation
from .symbol_table import SymbolTable


class AttributeDeriver:

    def __init__(self, rules_file: Path, date_key: Optional[str] = None):
        """Initiailzer.

        Args:
            rules_file: Path to raw CSV containing the list of
                rules to execute.
            date_key: Key that determines the order of the forms. Required
                if any date operations are defined
        """
        self.__date_key = date_key
        self.__rules = self.__load_rules(rules_file)

    def __load_rules(self, rules_file: Path) -> List[AttributeSchema]:
        """Load rules from the given path. All forms called through curate will
        have these rules applied to them.

        Args:
            rules_file: Path to load rules from
        """
        # first aggregate all events to their attribute, since some
        # may have multiple events
        attributes: Dict[str, List[DeriveEvent]] = {}
        with rules_file.open('r') as fh:  # type: ignore
            reader = csv.DictReader(fh)
            if not reader.fieldnames:
                raise AttributeDeriverException(
                    "No CSV headers found in derive rules file")

            for exp_header in ['function', 'location', 'operation']:
                if exp_header not in reader.fieldnames:
                    raise AttributeDeriverException(
                        f"Missing expected header: {exp_header}")

            for row in reader:
                func = row.pop('function')
                if func not in attributes:
                    attributes[func] = []

                event = DeriveEvent(**row)  # type: ignore
                if isinstance(event.operation, DateOperation) and not self.__date_key:
                    raise AttributeDeriverException(
                        f"Date operation defined for {func} but no date key defined")

                attributes[func].append(event)

        # create AttributeSchema for each attribute
        rules = []
        for func, events in attributes.items():
            rules.append(
                AttributeSchema(function=f'create_{func}', events=events))

        return rules

    def curate(self, table: SymbolTable) -> None:
        """Curate the given file. Assumes has all the FW metadata required to
        curate the schema. Derived attributes will be added to the same table.

        Args:
            table: Table with file data to curate
        """
        # make sure date_key is in metadata
        if self.__date_key:
            if self.__date_key not in table or not table[self.__date_key]:
                raise AttributeDeriverException(
                    f"Table does not have specified date key: {self.__date_key}")

        # collect all attributes beforehand so they're easily hashable
        collections = {}
        for c in AttributeCollectionRegistry.collections:
            collections.update({
                k: {
                    'func': v,
                    'class': c,
                    'instance': None
                }
                for k, v in c.get_all_hooks().items()
            })

        # derive the variables
        for attr in self.__rules:
            hook = collections.get(attr.function, None)
            if not hook:
                raise AttributeDeriverException(
                    f"Unknown attribute function: {attr.function}")

            # cache an instance if not yet created
            if not hook['instance']:
                hook['instance'] = hook['class'](table)

            value = hook['func'](hook['instance'])

            for event in attr.events:
                event.operation.evaluate(table,
                                         value,
                                         event.location,
                                         date_key=self.__date_key)
