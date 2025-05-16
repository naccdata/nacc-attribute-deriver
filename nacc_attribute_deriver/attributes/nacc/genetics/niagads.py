"""NIAGAD-specific derived variables.

Right now these should all come from the imported GWAS data under
<subject>_niagads_availability.json
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import RawNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class NIAGADSAttributeCollection(AttributeCollection):
    """Class to collect NIAGADS attributes."""

    def __init__(self, table: SymbolTable) -> None:
        """Override initializer to set prefix to NIAGADS-specific data."""
        self.__niagads = RawNamespace(table)
        self.__niagads.assert_required(
            required=[
                "niagads_gwas",
                "niagads_exomechip",
                "niagads_wgs",
                "niagads_wes",
            ]
        )

    def _evaluate_investigator(self, attribute: str) -> Optional[int]:
        """Evaluate investigator. If null/missing (set to None or "0") then
        return 0, else return 1.

        Args:
            value: The value to evaluate.
        """
        attribute_value = self.__niagads.get_value(attribute)
        if attribute_value is None:
            return None

        return 1 if attribute_value and str(attribute_value) != "0" else 0

    def _create_niagads_gwas(self) -> Optional[int]:
        """NIAGADS GWAS investigator availability."""
        return self._evaluate_investigator("niagads_gwas")

    def _create_niagads_exome(self) -> Optional[int]:
        """NIAGADS ExomeChip investigator availability."""
        return self._evaluate_investigator("niagads_exomechip")

    def _create_niagads_wgs(self) -> Optional[int]:
        """NIAGADS WGS investigator availability."""
        return self._evaluate_investigator("niagads_wgs")

    def _create_niagads_wes(self) -> Optional[int]:
        """NIAGADS WES investigator availability."""
        return self._evaluate_investigator("niagads_wes")
