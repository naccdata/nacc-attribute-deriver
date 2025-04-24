from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.uds_namespace import UDSNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class APOEDerivedAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)

    def _create_naccapoe(self) -> int:
        return self.__uds.get_cross_sectional_value("naccapoe")
