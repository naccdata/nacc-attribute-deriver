from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class GeneticsDerivedAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__subject_derived = SubjectDerivedNamespace(table)

    def _create_ngdsgwas(self) -> Optional[int]:
        """NIAGADS GWAS investigator availability."""
        return self.__subject_derived.get_int_value("niagads_gwas")

    def _create_ngdsexom(self) -> Optional[int]:
        """NIAGADS ExomeChip investigator availability."""
        return self.__subject_derived.get_int_value("niagads_exome")

    def _create_ngdswgs(self) -> Optional[int]:
        """NIAGADS WGS investigator availability."""
        return self.__subject_derived.get_int_value("niagads_wgs")

    def _create_ngdswes(self) -> Optional[int]:
        """NIAGADS WES investigator availability."""
        return self.__subject_derived.get_int_value("niagads_wes")
