"""All study-parameter MQT derived variables.

Assumes NACC-derived variables are already set
"""
from typing import List

from nacc_attribute_deriver.attributes.base.base_attribute import MQTAttribute


class StudyParametersAttribute(MQTAttribute):
    """Class to collect study-parameter attributes."""

    def _create_uds_versions_available(self) -> List[str]:
        """Keeps track of available UDS versions.

        Location:
            subject.info.study-parameters.uds.versions
        Operation:
            set
        Type:
            mqt-longitudinal
        Description:
            Number of years of UDS visits available
        """
        formver = self.get_value('formver')
        versions = self.table.get('subject.info.study-parameters.uds.versions',
                                  [])
        versions = set(versions) if versions else set()

        if formver:
            versions.add(formver)

        return versions
