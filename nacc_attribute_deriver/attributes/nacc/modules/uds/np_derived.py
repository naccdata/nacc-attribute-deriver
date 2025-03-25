from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace


class NPDerivedAttributeCollection(AttributeCollection):
    def __init__(self, table):
        self.__subject_derived = SubjectDerivedNamespace(table)

    def _create_naccbraa(self) -> int:
        """Copy subject level attribute."""
        return self.__subject_derived.get_value("np_braa")

    def _create_naccneur(self) -> int:
        """Copy subject level attribute."""
        return self.__subject_derived.get_value("np_neur")

    def _create_naccmicr(self) -> int:
        """Copy subject level attribute."""
        return self.__subject_derived.get_value("np_micr")

    def _create_nacchem(self) -> Optional[int]:
        """Copy subject level attribute."""
        return self.__subject_derived.get_value("np_hem")

    def _create_naccarte(self) -> Optional[int]:
        """Copy subject level attribute."""
        return self.__subject_derived.get_value("np_arte")

    def _create_nacclewy(self) -> Optional[int]:
        """Copy subject level attribute."""
        return self.__subject_derived.get_value("np_lewy")
