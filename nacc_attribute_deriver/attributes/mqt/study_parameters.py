"""All study-parameter MQT derived variables.

Assumes NACC-derived variables are already set
"""

import re
from typing import List

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import SubjectInfoNamespace
from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class StudyParametersAttributeCollection(AttributeCollection):
    """Class to collect study-parameter attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)
        self.__subject_info = SubjectInfoNamespace(table=table)

    def _create_uds_versions_available(self) -> List[str]:
        """Keeps track of available UDS versions."""
        formver = self.__uds.normalized_formver()
        versions = set([f"UDSv{formver}"])

        prev_versions = self.__subject_info.get_value(
            "study-parameters.uds.versions", list, default=[]
        )

        if prev_versions:
            for v in prev_versions:
                if isinstance(v, str) and re.match(r"UDSv[1-4]", v):
                    versions.add(v)

        return sorted(list(versions))
