"""NCRAD-specific derived variables.

Right now these should all come from the imported APOE data under
<subject>_apoe_availability.json
"""

from types import MappingProxyType
from typing import Mapping, Tuple

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import RawNamespace
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable


class NCRADAttributeCollection(AttributeCollection):
    """Class to collect NCRAD attributes."""

    # NCRAD (a1, a2) to NACC encoding
    APOE_ENCODINGS: Mapping[Tuple[str, str], int] = MappingProxyType(
        {
            ("E3", "E3"): 1,
            ("E3", "E4"): 2,
            ("E4", "E3"): 2,
            ("E3", "E2"): 3,
            ("E2", "E3"): 3,
            ("E4", "E4"): 4,
            ("E4", "E2"): 5,
            ("E2", "E4"): 5,
            ("E2", "E2"): 6,
        }
    )

    def __init__(self, table: SymbolTable) -> None:
        """Override initializer to set prefix to NCRAD-specific data."""
        self.__apoe = RawNamespace(table)

    def _create_ncrad_apoe(self) -> int:
        """Comes from derive.sas and derivenew.sas (same code)

        Should come from the actual imported APOE data
        <subject>_apoe_genotype.json
        """
        a1 = self.__apoe.get_value("a1")
        a2 = self.__apoe.get_value("a2")

        if not a1 or not a2:
            return 9

        return self.APOE_ENCODINGS.get((a1.strip().upper(), a2.strip().upper()), 9)


class HistoricalNCRADAttributeCollection(AttributeCollection):
    """Class to collect historical NCRAD attributes."""

    def __init__(self, table: SymbolTable) -> None:
        """Override initializer to set prefix to NCRAD-specific data."""
        self.__apoe = RawNamespace(table)

    def _create_historic_apoe(self) -> int:
        """For APOE values provided from sources other than the NCRAD APOE
        file.

        <subject>_historic_apoe_genotype.json
        """
        apoe = self.__apoe.get_int_value("apoe")

        # while sas code handles consistency, just do a sanity check
        # to make sure entire rows lines up, else there's an issue
        if apoe is not None:
            for field in ["apoecenter", "apoenp", "apoeadgc", "adcapoe", "apoecomm"]:
                source_apoe = self.__apoe.get_int_value(field)
                if source_apoe is None:
                    continue

                if source_apoe != apoe:
                    raise InvalidFieldError(
                        f"Source {field} with value {source_apoe} does not match "
                        + f"expected apoe value {apoe}"
                    )

        return apoe if apoe and apoe >= 1 and apoe <= 6 else 9
