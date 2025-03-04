"""
All study-parameter MQT derived variables.
Assumes NACC-derived variables are already set
"""
from typing import List

from nacc_attribute_deriver.symbol_table import SymbolTable

def _create_uds_versions_available(table: SymbolTable) -> List[str]:
    """Keeps track of available UDS versions

	Location:
		subject.info.study-parameters.uds.versions
	Event:
		set
    Type:
        mqt-longitudinal
    Description:
        Number of years of UDS visits available
    """
    formver = table.get('file.info.forms.json.formver')
    versions = table.get('subject.info.study-parameters.uds.versions', [])
    versions = set(versions) if versions else set()

    if formver:
        versions.add(formver)

    return versions
