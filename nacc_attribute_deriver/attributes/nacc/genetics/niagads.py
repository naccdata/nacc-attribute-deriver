"""NIAGAD-specific derived variables.

Right now these should all come from the imported GWAS data under
<subject>_niagads_availability.json
"""

from nacc_attribute_deriver.attributes.base.base_attribute import NACCAttribute
from nacc_attribute_deriver.schema.errors import MissingRequiredException
from nacc_attribute_deriver.symbol_table import SymbolTable


class NIAGADSAttribute(NACCAttribute):
    """Class to collect NIAGADS attributes."""

    def __init__(self, table: SymbolTable, form_prefix: str = "file.info.raw.") -> None:
        """Override initializer to set prefix to NIAGADS-specific data."""
        super().__init__(table, form_prefix)
        for field in [
            "niagads_gwas",
            "niagads_exomechip",
            "niagads_wgs",
            "niagads_wes",
        ]:
            if f"{self.form_prefix}{field}" not in self.table:
                raise MissingRequiredException(
                    f"{field} required to curate NIAGADS data"
                )

    def _evaluate_investigator(self, value: str) -> int:
        """Evaluate investigator. If null/missing (set to None or "0") then
        return 0, else return 1.

        Args:
            value: The value to evaluate.
        """
        return 1 if value and str(value) != "0" else 0

    def _create_ngdsgwas(self) -> int:
        """NIAGADS GWAS investigator availability."""
        return self._evaluate_investigator(self.get_value("niagads_gwas"))

    def _create_ngdsexom(self) -> int:
        """NIAGADS ExomeChip investigator availability."""
        return self._evaluate_investigator(self.get_value("niagads_exomechip"))

    def _create_ngdswgs(self) -> int:
        """NIAGADS WGS investigator availability."""
        return self._evaluate_investigator(self.get_value("niagads_wgs"))

    def _create_ngdswes(self) -> int:
        """NIAGADS WES investigator availability."""
        return self._evaluate_investigator(self.get_value("niagads_wes"))
