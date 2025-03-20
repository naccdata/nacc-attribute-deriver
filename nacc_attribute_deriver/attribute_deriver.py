"""Defines the AttributeDeriver class.

Gear needs to iterate over all subjects, and for each subject, call this
AttributeDeriver (deriver.curate(file)) for all (relevant) files in the
subject. File must correspond to the curation schema.
"""

import csv
from collections import defaultdict
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import ValidationError

from .attributes.attribute_collection import AttributeCollectionRegistry
from .schema.errors import AttributeDeriverError
from .schema.schema import AttributeAssignment, CurationRule, RuleFileModel
from .symbol_table import SymbolTable


class AttributeDeriver:
    def __init__(self, rules_file: Traversable | Path, date_key: Optional[str] = None):
        """Initiailzer.

        Args:
            rules_file: Path to raw CSV containing the list of
                rules to execute.
            date_key: Key that determines the order of the forms. Required
                if any date operations are defined
        """
        self.__date_key = date_key
        self.__rules = self.__load_rules(rules_file)

    def __load_rules(self, rules_file: Traversable | Path) -> List[CurationRule]:
        """Load rules from the given path. All forms called through curate will
        have these rules applied to them.

        Args:
            rules_file: Path to load rules from
        """

        # aggregate all assignments to their attribute function
        attributes: Dict[str, List[AttributeAssignment]] = defaultdict(list)
        with rules_file.open("r") as fh:  # type: ignore
            reader = csv.DictReader(fh)
            if not reader.fieldnames:
                raise AttributeDeriverError("No CSV headers found in derive rules file")

            for row in reader:
                try:
                    rule_schema = RuleFileModel.model_validate(row)
                except ValidationError as error:
                    raise AttributeDeriverError(
                        f"error loading curation rule row: {error}"
                    )

                if (
                    rule_schema.operation in ["initial", "latest"]
                    and not self.__date_key
                ):
                    raise AttributeDeriverError(
                        f"Date operation defined for {rule_schema.function} "
                        "but no date key defined"
                    )

                attributes[rule_schema.function].append(rule_schema.assignment)

        # create rule for each attribute
        rules: List[CurationRule] = []
        for attribute_function, assignments in attributes.items():
            rules.append(
                CurationRule(
                    function=f"create_{attribute_function}", assignments=assignments
                )
            )

        return rules

    def curate(self, table: SymbolTable) -> None:
        """Curate the symbol table with the rules of this deriver.

        Assumes has all the FW metadata required to curate with the schema rules.
        Derived attributes are added to the same table.

        Args:
            table: symbol table with subject and file data to curate
        """
        if self.__date_key:
            if self.__date_key not in table or not table[self.__date_key]:
                raise AttributeDeriverError(
                    f"Table does not have specified date key: {self.__date_key}"
                )

        # collect all attributes beforehand so they're easily hashable
        instance_collections = AttributeCollectionRegistry.get_attribute_methods(table)

        # derive the variables
        for rule in self.__rules:
            method = instance_collections.get(rule.function, None)
            if not method:
                raise AttributeDeriverError(
                    f"Unknown attribute function: {rule.function}"
                )

            value = method.apply(table)

            for assignment in rule.assignments:
                assignment.operation.evaluate(
                    table=table,
                    value=value,
                    attribute=assignment.attribute,
                    date_key=self.__date_key,
                )
