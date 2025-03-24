"""All genetics MQT derived variables.

Assumes NACC-derived variables are already set
"""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.base_attribute import (
    DerivedAttribute,
    RawAttribute,
)


class GeneticAttributeCollection(AttributeCollection):
    """Class to collect genetic attributes."""

    def __init__(self, table):
        self.__raw = RawAttribute(table)
        self.__derived = DerivedAttribute(table)

    def _create_apoe(self) -> str:
        """Mapped from NACCAPOE."""
        # need to search required field since we're pulling raw data
        # this is duplicate with the NCRAD initializer - better options?
        # might need to do something similar to how SCAN is doing it and/or
        # explicitly split by ncrad/niagads
        self.__raw.assert_required(["a1", "a2"])
        # for field in ["a1", "a2"]:
        #     if f"{self.attribute_prefix}{field}" not in self.table:
        #         raise MissingRequiredError(f"{field} required to curate APOE")

        a1 = self.__raw.get_value("a1")
        a2 = self.__raw.get_value("a2")

        if not a1 or not a2:
            return "Missing/unknown/not assessed"

        return f"{a1},{a2}".lower()

    def _create_ngdsgwas_mqt(self) -> bool:
        """Mapped from NGDSGWAS."""
        result = self.__derived.assert_required(["ngdsgwas"])
        return bool(result["ngdsgwas"])

    def _create_ngdsexom_mqt(self) -> bool:
        """Mapped from NGDSEXOM."""
        result = self.__derived.assert_required(["ngdsexom"])
        return bool(result["ngdsexom"])

    def _create_ngdswgs_mqt(self) -> bool:
        """Mapped from NGDSWGS."""
        result = self.__derived.assert_required(["ngdswgs"])
        return bool(result["ngdswgs"])

    def _create_ngdswes_mqt(self) -> bool:
        """Mapped from NGDSWES."""
        result = self.__derived.assert_required(["ngdswes"])
        return bool(result["ngdswes"])
