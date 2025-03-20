"""Base attributes, derive directly from AttributeCollection."""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.symbol_table import SymbolTable


class FormAttribute(AttributeCollection):
    """Base class for attributes over file.info.forms."""

    def __init__(
        self, table: SymbolTable, form_prefix: str = "file.info.forms.json."
    ) -> None:
        super().__init__(table, form_prefix)


class RawAttribute(AttributeCollection):
    """Base class for attributes over file.info.raw."""

    def __init__(self, table: SymbolTable, form_prefix: str = "file.info.raw.") -> None:
        super().__init__(table, form_prefix)
