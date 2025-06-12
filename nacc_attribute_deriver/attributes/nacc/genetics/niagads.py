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
        self.__niagads = RawNamespace(
            table,
            required=frozenset(
                [
                    "niagads_gwas",
                    "niagads_exomechip",
                    "niagads_wgs",
                    "niagads_wes",
                ]
            ),
        )

    def _evaluate_investigator(self, attribute: str) -> int:
        """Evaluate investigator. If null/missing (set to None or "0") then
        return 0, else return 1.

        Args:
            attribute: name of attribute
        """
        value = self.__niagads.get_required(attribute, str)
        return 1 if value and str(value) != "0" else 0

    def _create_ngdsgwas(self) -> int:
        """NIAGADS GWAS investigator availability."""
        return self._evaluate_investigator("niagads_gwas")

    def _create_ngdsexome(self) -> int:
        """NIAGADS ExomeChip investigator availability."""
        return self._evaluate_investigator("niagads_exomechip")

    def _create_ngdswgs(self) -> int:
        """NIAGADS WGS investigator availability."""
        return self._evaluate_investigator("niagads_wgs")

    def _create_ngdswes(self) -> int:
        """NIAGADS WES investigator availability."""
        return self._evaluate_investigator("niagads_wes")
