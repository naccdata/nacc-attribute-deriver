"""All genetics MQT derived variables.

Assumes NACC-derived variables are already set
"""

from nacc_attribute_deriver.attributes.base.base_attribute import RawAttribute
from nacc_attribute_deriver.schema.errors import MissingRequiredError


class GeneticAttribute(RawAttribute):
    """Class to collect genetic attributes."""

    def _create_apoe(self) -> str:
        """Mapped from NACCAPOE."""
        # need to search required field since we're pulling raw data
        # this is duplicate with the NCRAD initializer - better options?
        # might need to do something similar to how SCAN is doing it and/or
        # explicitly split by ncrad/niagads
        for field in ["a1", "a2"]:
            if f"{self.attribute_prefix}{field}" not in self.table:
                raise MissingRequiredError(f"{field} required to curate APOE")

        a1 = self.get_value("a1")
        a2 = self.get_value("a2")

        if not a1 or not a2:
            return "Missing/unknown/not assessed"

        return f"{a1},{a2}".lower()

    def _create_ngdsgwas_mqt(self) -> bool:
        """Mapped from NGDSGWAS."""
        result = self.assert_required(["ngdsgwas"], prefix="file.info.derived.")
        return bool(result["ngdsgwas"])

    def _create_ngdsexom_mqt(self) -> bool:
        """Mapped from NGDSEXOM."""
        result = self.assert_required(["ngdsexom"], prefix="file.info.derived.")
        return bool(result["ngdsexom"])

    def _create_ngdswgs_mqt(self) -> bool:
        """Mapped from NGDSWGS."""
        result = self.assert_required(["ngdswgs"], prefix="file.info.derived.")
        return bool(result["ngdswgs"])

    def _create_ngdswes_mqt(self) -> bool:
        """Mapped from NGDSWES."""
        result = self.assert_required(["ngdswes"], prefix="file.info.derived.")
        return bool(result["ngdswes"])
