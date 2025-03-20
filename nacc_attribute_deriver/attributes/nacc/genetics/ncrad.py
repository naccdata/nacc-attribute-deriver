"""NCRAD-specific derived variables.

Right now these should all come from the imported APOE data under
<subject>_apoe_availability.json
"""

from typing import Dict, Tuple

from nacc_attribute_deriver.attributes.base.base_attribute import NACCAttribute
from nacc_attribute_deriver.schema.errors import MissingRequiredException
from nacc_attribute_deriver.symbol_table import SymbolTable


class NCRADAttribute(NACCAttribute):
    """Class to collect NCRAD attributes."""

    # NCRAD (a1, a2) to NACC encoding
    APOE_ENCODINGS: Dict[Tuple[str, str], int] = {
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

    def __init__(self, table: SymbolTable, form_prefix: str = "file.info.raw.") -> None:
        """Override initializer to set prefix to NCRAD-specific data."""
        super().__init__(table, form_prefix)
        for field in ["a1", "a2"]:
            if f"{self.form_prefix}{field}" not in self.table:
                raise MissingRequiredException(f"{field} required to curate NCRAD data")

    def _create_naccapoe(self) -> int:
        """Comes from derive.sas and derivenew.sas (same code)

        Should come from the actual imported APOE data
        <subject>_apoe_availability.json
        """
        a1 = self.get_value("a1")
        a2 = self.get_value("a2")

        if not a1 or not a2:
            return 9

        return self.APOE_ENCODINGS.get((a1.strip().upper(), a2.strip().upper()), 9)
