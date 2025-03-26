from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class GeneticsDerivedAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__subject_derived = SubjectDerivedNamespace(table)

    def _create_ngdsgwas(self) -> int:
        """NIAGADS GWAS investigator availability."""
        return self.__subject_derived.get_value("niagads_gwas")

    def _create_ngdsexom(self) -> int:
        """NIAGADS ExomeChip investigator availability."""
        return self.__subject_derived.get_value("niagads_exome")

    def _create_ngdswgs(self) -> int:
        """NIAGADS WGS investigator availability."""
        return self.__subject_derived.get_value("niagads_wgs")

    def _create_ngdswes(self) -> int:
        """NIAGADS WES investigator availability."""
        return self.__subject_derived.get_value("niagads_wes")
