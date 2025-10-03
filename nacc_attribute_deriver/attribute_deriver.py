"""Defines the AttributeDeriver class.

Gear needs to iterate over all subjects, and for each subject, call this
AttributeDeriver (deriver.curate(file)) for all (relevant) files in the
subject. File must correspond to the curation schema.
"""

import csv
from importlib import resources
from typing import Dict, List, Optional

from pydantic import ValidationError

from . import config
from .attributes.attribute_collection import AttributeCollectionRegistry
from .schema.errors import AttributeDeriverError, OperationError
from .schema.rule_types import DateTaggedValue
from .schema.schema import AttributeAssignment, CurationRule, RuleFileModel
from .symbol_table import SymbolTable
from .utils.scope import ScopeLiterals


class AttributeDeriver:
    def __init__(self):
        """Initializer.

        Args:
            rules_file: Path to raw CSV containing the list of
                rules to execute.
        """
        self.__rule_map = self.__load_rules()
        # collect all attributes beforehand so they're easily hashable
        self.__instance_collections = (
            AttributeCollectionRegistry.get_attribute_methods()
        )

    def __load_rules(self) -> Dict[str, List[CurationRule]]:
        """Load rules from the given path. All forms called through curate will
        have these rules applied to them.

        Args:
            rules_file: Path to load rules from
        """

        attributes: Dict[str, Dict[str, List[AttributeAssignment]]] = {}
        rules_file = resources.files(config).joinpath("curation_rules.csv")
        with rules_file.open("r") as file_stream:
            reader = csv.DictReader(file_stream)
            if not reader.fieldnames:
                raise AttributeDeriverError("No CSV headers found in derive rules file")

            for row in reader:
                try:
                    rule_schema = RuleFileModel.model_validate(row)
                except ValidationError as error:
                    raise AttributeDeriverError(
                        f"error loading curation rule row: {error}"
                    ) from error

                attribute_map = attributes.get(rule_schema.scope, {})
                attribute_list = attribute_map.get(rule_schema.function, [])
                attribute_list.append(rule_schema.assignment)
                attribute_map[rule_schema.function] = attribute_list
                attributes[rule_schema.scope] = attribute_map

        # create rule for each attribute
        rule_map: Dict[str, List[CurationRule]] = {}
        for scope, attribute_map in attributes.items():
            for attribute_function, assignments in attribute_map.items():
                rules = rule_map.get(scope, [])
                rules.append(
                    CurationRule(
                        function=f"create_{attribute_function}", assignments=assignments
                    )
                )
                rule_map[scope] = rules

        return rule_map

    def curate(self, table: SymbolTable, scope: ScopeLiterals) -> None:
        """Curate the symbol table with the rules of this deriver.

        Assumes has all the FW metadata required to curate with the schema rules.
        Derived attributes are added to the same table.

        Args:
            table: symbol table with subject and file data to curate
            scope: The curation scope
        """
        # derive the variables, if no rules for this scope, return
        rules = self.__rule_map.get(scope)
        if not rules:
            return

        for rule in rules:
            method = self.__instance_collections.get(rule.function, None)
            if not method:
                raise AttributeDeriverError(
                    f"Unknown attribute function: {rule.function}"
                )

            try:
                raw_value, date = method.apply(table)
            except Exception as e:
                raise AttributeDeriverError(
                    f"Failed to derive rule {rule.function}: {e}"
                ) from e

            if raw_value is None:
                continue

            for assignment in rule.assignments:
                value = raw_value
                operation = assignment.operation
                if assignment.dated:
                    if not date:
                        raise OperationError(
                            f"Cannot compute date for dated operation on rule {rule}"
                        )

                    if not isinstance(value, DateTaggedValue):
                        value = DateTaggedValue(value=value, date=date)

                operation.evaluate(
                    table=table, value=value, attribute=assignment.attribute
                )

    def get_curation_rules(self, scope: ScopeLiterals) -> Optional[List[CurationRule]]:
        """Grabs all curation rules associated with the given scope.

        Args:
            scope: the curation scope
        Returns:
            The list of CurationRules
        """
        return self.__rule_map.get(scope)
