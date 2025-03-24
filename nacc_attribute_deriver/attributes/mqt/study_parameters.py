"""All study-parameter MQT derived variables.

Assumes NACC-derived variables are already set
"""

from typing import List

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.base_attribute import SubjectInfoAttribute
from nacc_attribute_deriver.attributes.nacc.modules.uds.uds_attribute import (
    UDSAttribute,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable


class StudyParametersAttributeCollection(AttributeCollection):
    """Class to collect study-parameter attributes."""

    def __init__(self, table: SymbolTable):
        self.__file = UDSAttribute(table)
        self.__subject_info = SubjectInfoAttribute(table)

    def _create_uds_versions_available(self) -> List[str]:
        """Keeps track of available UDS versions."""
        formver = self.__file.get_value("formver")
        versions = self.__subject_info.get_value("study-parameters.uds.versions", [])
        versions = set(versions) if versions else set()

        if formver:
            try:
                versions.add(int(formver))
            except (ValueError, TypeError):
                raise AttributeDeriverError("UDS form version must be an integer")

        return list(versions)
