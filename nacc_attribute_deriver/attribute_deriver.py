"""Defines the AttributeDeriver class.

Gear needs to iterate over all subjects, and for each subject, call this
AttributeDeriver (deriver.curate(file)) for all (relevant) files in the
subject. File must correspond to the curation schema.
"""
import csv
from importlib.resources import files
from pathlib import Path
from typing import Any, Dict, List, Optional

from .attributes.attribute_collection import AttributeCollectionRegistry
from .schema.schema import AttributeSchema
from .symbol_table import SymbolTable


class AttributeDeriver:

    def __init__(self,
                 date_key: str,
                 rules_file: Optional[Path] = None):
        """Initiailzer.

        Args:
            date_key: Key that determines the order of the forms
            rules_file: Path to raw CSV containing the list of
                rules to execute. If not provided will use the
                default derive_rules.csv
        """
        self.__date_key = date_key

        if not rules_file:
            rules_file = files("nacc_attribute_deriver")\
                .joinpath("bin/derive_rules.csv")

        self.__rules = self.__load_rules(rules_file)

    def __load_rules(self, rules_file: Path) -> List[AttributeSchema]:
        """Load rules from the given path. All forms called through curate
        will have these rules applied to them.

        Args:
            rules_file: Path to load rules from
        """
        # first aggregate all events to their attribute, since some
        # may have multiple events
        attributes = {}
        with rules_file.open('r') as fh:
            reader = csv.DictReader(fh)
            for exp_header in ['function', 'location', 'operation']:
                if exp_header not in reader.fieldnames:
                    raise ValueError(f"Missing expected header: {exp_header}")

            for row in reader:
                func = row.pop('function')
                if func not in attributes:
                    attributes[func] = []
                attributes[func].append({
                    'location': row['location'],
                    'operation': row['operation']
                })

        # create AttributeSchema for each attribute
        rules = []
        for func, events in attributes.items():
            rules.append(AttributeSchema(function=f'create_{func}', events=events))

        return rules

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

        # collect all attributes beforehand so they're easily hashable
        instance_collections = {}
        for instance in [c(table) for c in AttributeCollectionRegistry.collections]:
            instance_collections.update({
                k: {
                    'func': v,
                    'instance': instance
                }
                for k, v in instance.get_all_hooks().items()
            })

        # derive the variables
        for attr in self.__rules:
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
