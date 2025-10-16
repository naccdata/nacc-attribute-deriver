"""Class to handle form missingness values that check subject-level derived
variables."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class SubjectMissingnessCollection(AttributeCollection):
    """Class to handle Milestone missingness values."""

    def __init__(self, table: SymbolTable):
        # TODO - may or may not be the actual subject data depending on
        # where this is run, so namespace may change
        self.__derived = SubjectDerivedNamespace(table=table)

    def handle_missing(self, attribute: str, default: int) -> Optional[int]:
        """Handle missing values."""
        value = self.__derived.get_cross_sectional_value(attribute, str)
        if value is None:
            return default

        # the reason we don't return the value itself is because in this
        # context returning None means "don't replace what's already there"
        # whereas returning the value would say "replace what's there with
        # itself" and could potentially cause ordering/date issues
        return None
