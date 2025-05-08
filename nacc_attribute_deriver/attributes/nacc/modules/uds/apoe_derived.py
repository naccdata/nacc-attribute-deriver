from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class APOEDerivedAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__subject_derived = SubjectDerivedNamespace(table)

    def _create_naccapoe(self) -> int:
        return self.__subject_derived.get_cross_sectional_value("naccapoe")
