"""Defines the AttributeDeriver class.

Gear needs to iterate over all subjects, and for each subject, call this
AttributeDeriver (deriver.curate(file)) for all (relevant) files in the
subject. File must correspond to the curation schema.
"""

import csv
import datetime
from abc import ABC, abstractmethod
from importlib import resources
from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import ValidationError

from . import config
from .attributes.collection.attribute_collection import AttributeCollectionRegistry
from .schema.rule_types import DateTaggedValue
from .schema.schema import (
    AttributeAssignment,
    CurationRule,
    MissingnessFileModel,
    RuleFileModel,
)
from .symbol_table import SymbolTable
from .utils.constants import CURATION_TYPE
from .utils.errors import AttributeDeriverError, OperationError
from .utils.scope import ScopeLiterals


class BaseAttributeDeriver(ABC):
    def __init__(self, rules_filename: str, curation_type: str):
        """Initializer.

        Args:
            rules_file: Path to raw CSV containing the list of
                rules to execute.
        """
        if curation_type not in CURATION_TYPE:
            raise AttributeDeriverError(f"Unknown derive type: {curation_type}")

        self._rules_filename = rules_filename
        self._curation_type = curation_type

        self._rule_map = self.__load_rules()
        # collect all attributes beforehand so they're easily hashable
        self._instance_collections = AttributeCollectionRegistry.get_attribute_methods()

    def __load_rules(self) -> Dict[str, List[CurationRule]]:
        """Load rules from the given path. All forms called through curate will
        have these rules applied to them.

        Args:
            rules_file: Path to load rules from
        """

        attributes: Dict[str, Dict[str, List[AttributeAssignment]]] = {}
        rules_file = resources.files(config).joinpath(self._rules_filename)
        with rules_file.open("r") as file_stream:
            reader = csv.DictReader(file_stream)
            if not reader.fieldnames:
                raise AttributeDeriverError("No CSV headers found in rules file")

            for row in reader:
                try:
                    rule_schema = RuleFileModel.model_validate(row)
                except (ValidationError, OperationError) as error:
                    raise AttributeDeriverError(
                        f"error loading rule row: {error}"
                    ) from error

                attribute_function = f"{self._curation_type}_{rule_schema.function}"
                attribute_map = attributes.get(rule_schema.scope, {})
                attribute_list = attribute_map.get(attribute_function, [])

                attribute_list.append(rule_schema.assignment)
                attribute_map[attribute_function] = attribute_list
                attributes[rule_schema.scope] = attribute_map

        # create rule for each attribute
        rule_map: Dict[str, List[CurationRule]] = {}
        for scope, attribute_map in attributes.items():
            for attribute_function, assignments in attribute_map.items():
                rules = rule_map.get(scope, [])
                rules.append(
                    CurationRule(function=attribute_function, assignments=assignments)
                )
                rule_map[scope] = rules

        return rule_map

    @abstractmethod
    def get_curated_value(
        self, table: SymbolTable, rule: CurationRule, scope: str
    ) -> Tuple[Any, Optional[datetime.date]]:
        """Get the curated value and date, if applicable."""
        pass

    def curate(self, table: SymbolTable, scope: ScopeLiterals) -> None:
        """Curate the symbol table with the rules of this deriver.

        Assumes has all the FW metadata required to curate with the schema rules.
        Derived attributes are added to the same table.

        Args:
            table: symbol table with subject and file data to curate
            scope: The curation scope
        """
        # derive the variables, if no rules for this scope, return
        rules = self._rule_map.get(scope)
        if not rules:
            return

        for rule in rules:
            raw_value, date = self.get_curated_value(table, rule, scope)
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
        return self._rule_map.get(scope)


class AttributeDeriver(BaseAttributeDeriver):
    def __init__(self) -> None:
        super().__init__("curation_rules.csv", "create")

    def get_curated_value(
        self, table: SymbolTable, rule: CurationRule, scope: str
    ) -> Tuple[Any, Optional[datetime.date]]:
        """Get the curated value and date, if applicable.

        For derived variables, an exact one to one mapping is expected.
        """
        method = self._instance_collections.get(rule.function, None)
        if not method:
            raise AttributeDeriverError(
                f"Unknown attribute function for scope {scope}: {rule.function}"
            )

        try:
            return method.apply(table)
        except Exception as e:
            raise AttributeDeriverError(
                f"Failed to derive rule {rule.function} for scope {scope}: {e}"
            ) from e


class MissingnessDeriver(BaseAttributeDeriver):
    def __init__(self, missingness_file: str = "missingness_rules.csv") -> None:
        super().__init__(missingness_file, "missingness")
        self.__attribute_types = self.__get_attribute_types()

    def __get_attribute_types(self) -> Dict[str, Type]:
        """Get attribute types for each attribute, e.g.,
            "attribute": int

        If a missingness rule is not defined for this attribute,
        it will infer the default missingness value from this type.
        """
        results = {}
        rules_file = resources.files(config).joinpath(self._rules_filename)
        with rules_file.open("r") as file_stream:
            reader = csv.DictReader(file_stream)

            # we already read this file once, so don't need to redo validation
            for row in reader:
                rule_schema = MissingnessFileModel.model_validate(row)

                # generally consider 1 to 1 mapping so throw error on duplicates
                if rule_schema.function in results:
                    raise AttributeDeriverError(
                        f"Multiple missingness rules defined for {rule_schema.function}"
                    )

                results[rule_schema.function] = rule_schema.attr_type

        return results

    def get_curated_value(
        self, table: SymbolTable, rule: CurationRule, scope: str
    ) -> Tuple[Any, Optional[datetime.date]]:
        """Get the curated value and date, if applicable.

        For missingness variables, if a missingness function is not
        defined for it, use the generic scope missingness definition.
        """
        method = self._instance_collections.get(rule.function, None)
        if method:
            try:
                return method.apply(table)
            except Exception as e:
                raise AttributeDeriverError(
                    f"Failed to derive rule {rule.function}: {e}"
                ) from e

        # use generic scope missingness function
        # we also need to pass the name of the field we are trying to assign a
        # missingness value for since this is a generic function, so strip out
        # the leading missingness_ in the original function name
        method = self._instance_collections.get(f"{self._curation_type}_{scope}", None)
        field = rule.function.removeprefix(f"{self._curation_type}_")

        if not method:
            raise AttributeDeriverError(
                f"Unknown attribute function for scope {scope}: "
                + f"{self._curation_type}_{scope}"
            )

        try:
            return method.apply_with_field(table, field, self.__attribute_types[field])
        except Exception as e:
            raise AttributeDeriverError(
                f"Failed to derive rule {rule.function} with field {field}: {e}"
            ) from e
