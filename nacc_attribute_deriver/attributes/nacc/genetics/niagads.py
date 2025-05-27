"""NIAGAD-specific derived variables.

Right now these should all come from the imported GWAS data under
<subject>_niagads_availability.json
"""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import RawNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class NIAGADSAttributeCollection(AttributeCollection):
    """Class to collect NIAGADS attributes."""

    def __init__(self, table: SymbolTable) -> None:
        """Override initializer to set prefix to NIAGADS-specific data."""
        self.__niagads = RawNamespace(table)

    def _evaluate_investigator(self, attribute: str) -> int:
        """Evaluate investigator. If null/missing (set to None or "0") then
        return 0, else return 1.

        Args:
            attribute: The attribute to evaluate.
        """
        attribute_value = self.__niagads.get_value(attribute)
        return 1 if attribute_value and str(attribute_value) != "0" else 0

    def _create_niagads_gwas(self) -> int:
        """NIAGADS GWAS investigator availability."""
        return self._evaluate_investigator("niagads_gwas")

    def _create_niagads_exome(self) -> int:
        """NIAGADS ExomeChip investigator availability."""
        return self._evaluate_investigator("niagads_exomechip")

    def _create_niagads_wgs(self) -> int:
        """NIAGADS WGS investigator availability."""
        return self._evaluate_investigator("niagads_wgs")

    def _create_niagads_wes(self) -> int:
        """NIAGADS WES investigator availability."""
        return self._evaluate_investigator("niagads_wes")
