"""NCRAD-specific derived variables.

Right now these should all come from the imported APOE data under
<subject>_apoe_availability.json
"""

from types import MappingProxyType
from typing import Mapping, Tuple

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import RawNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class NCRADAPOEAttributeCollection(AttributeCollection):
    """Class to collect NCRAD APOE attributes."""

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
        """Override initializer to set prefix to APOE-specific data."""
        self.__apoe = RawNamespace(table)
        self.__apoe.assert_required(required=["a1", "a2"])

    def _create_ncrad_apoe(self) -> int:
        """Comes from derive.sas and derivenew.sas (same code)

        Should come from the actual imported APOE data
        <subject>_apoe_availability.json
        """
        a1 = self.__apoe.get_value("a1")
        a2 = self.__apoe.get_value("a2")

        if not a1 or not a2:
            return 9

        return self.APOE_ENCODINGS.get((a1.strip().upper(), a2.strip().upper()), 9)


class NCRADSamplesAttributeCollection(AttributeCollection):
    """Class to collect NCRAD Sample attributes."""

    def __init__(self, table: SymbolTable) -> None:
        """Override initializer to set prefix to NCRAD biosample-specific
        data."""
        self.__samples = RawNamespace(table)
        self.__samples.assert_required(
            required=["date_sample_received", "sample_received"]
        )

    def _create_naccncrd(self) -> int:
        """Creates NACCNCRD.

        Set to 1 if there is any data, which there is assumed to be if
        this class is successfully initialized at all
        """
        return 1
