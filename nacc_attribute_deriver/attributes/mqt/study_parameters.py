"""All study-parameter MQT derived variables.

Assumes NACC-derived variables are already set
"""

import re
from typing import List

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectInfoNamespace
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class StudyParametersAttributeCollection(AttributeCollection):
    """Class to collect study-parameter attributes."""

    def __init__(self, table: SymbolTable):
        self.__file = UDSNamespace(table)
        self.__subject_info = SubjectInfoNamespace(table)

    def _create_uds_versions_available(self) -> List[str]:
        """Keeps track of available UDS versions."""
        formver = self.__file.normalized_formver()
        versions = self.__subject_info.get_value("study-parameters.uds.versions", [])
        assert versions is not None
        versions = {
            version
            for version in versions
            if isinstance(version, str) and re.match(r"UDSv[1-4]", version)
        }
        if formver:
            versions.add(f"UDSv{formver}")

        return list(versions)
