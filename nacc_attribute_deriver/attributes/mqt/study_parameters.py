"""All study-parameter MQT derived variables.

Assumes NACC-derived variables are already set
"""

from typing import List

from nacc_attribute_deriver.attributes.base.base_attribute import MQTAttribute
from nacc_attribute_deriver.schema.errors import AttributeDeriverException


class StudyParametersAttribute(MQTAttribute):
    """Class to collect study-parameter attributes."""

    def _create_uds_versions_available(self) -> List[str]:
        """Keeps track of available UDS versions."""
        formver = self.get_value("formver")
        versions = self.table.get("subject.info.study-parameters.uds.versions", [])
        versions = set(versions) if versions else set()

        if formver:
            try:
                versions.add(int(formver))
            except (ValueError, TypeError):
                raise AttributeDeriverException("UDS form version must be an integer")

        return list(versions)
