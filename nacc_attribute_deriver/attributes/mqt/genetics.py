"""All genetics MQT derived variables.

Assumes NACC-derived variables are already set
"""

from typing import Any

from nacc_attribute_deriver.attributes.base.base_attribute import MQTAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable


class GeneticAttribute(MQTAttribute):
    """Class to collect genetic attributes."""

    def __init__(
        self,
        table: SymbolTable,
        form_prefix: str = "file.info.raw.",
        ncrad_prefix: str = "file.info.raw.ncrad.",
        niagads_prefix: str = "file.info.raw.niagads.",
    ) -> None:
        """Override initializer to set prefix to SCAN-specific data."""
        super().__init__(table, form_prefix)
        self.__ncrad_prefix = ncrad_prefix
        self.__niagads_prefix = niagads_prefix

    def get_ncrad_value(self, key: str, default: Any = None) -> Any:
        """Get NCRAD-specific value.

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
        """
        return self.get_value(key, default, prefix=self.__ncrad_prefix)

    def get_niagads_value(self, key: str, default: Any = None) -> Any:
        """Get NIAGADS-specific value.

        Args:
            key: Key to grab value for
            default: Default value to return if key is not found
        """
        return self.get_value(key, default, prefix=self.__niagads_prefix)

    def _create_apoe(self) -> str:
        """Mapped from NACCAPOE."""
        a1 = self.get_ncrad_value("a1")
        a2 = self.get_ncrad_value("a2")

        if not a1 or not a2:
            return "Missing/unknown/not assessed"

        return f"{a1},{a2}".lower()

    def _create_ngdsgwas_mqt(self) -> bool:
        """Mapped from NGDSGWAS."""
        result = self.assert_required(["ngdsgwas"])
        return bool(result["ngdsgwas"])

    def _create_ngdsexom_mqt(self) -> bool:
        """Mapped from NGDSEXOM."""
        result = self.assert_required(["ngdsexom"])
        return bool(result["ngdsexom"])

    def _create_ngdswgs_mqt(self) -> bool:
        """Mapped from NGDSWGS."""
        result = self.assert_required(["ngdswgs"])
        return bool(result["ngdswgs"])

    def _create_ngdswes_mqt(self) -> bool:
        """Mapped from NGDSWES."""
        result = self.assert_required(["ngdswes"])
        return bool(result["ngdswes"])
