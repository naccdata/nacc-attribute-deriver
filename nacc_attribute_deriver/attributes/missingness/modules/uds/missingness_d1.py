"""Class to handle D1-specific missingness values.

These are variables that only exist in V3 and earlier for D1; others
will now be found in either D1a or D1b.
"""

from typing import List, Optional

from nacc_attribute_deriver.symbol_table import SymbolTable

from .missingness_uds import UDSMissingness


class UDSFormD1Missingness(UDSMissingness):
    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table)

        # variables a majority of these missingness values rely on
        self.normcog = self.uds.get_value("normcog", int)
        self.demented = self.uds.get_value("demented", int)
        self.impnomci = self.uds.get_value("impnomci", int)
        self.mci = self.generate_mci()

    def check_applicable(self, versions: Optional[List[float]] = None) -> bool:
        """Called by each variable; returns True if this variable is applicable
        to the specified versions.

        In general, a lot of variables are only calculated for version
        3.0, 3.2, and 4.0.
        """
        if versions is None:
            versions = [3.0, 3.2, 4.0]

        raw_formver = self.uds.get_required("formver", float)
        return raw_formver in versions

    def generate_mci(self) -> int:
        """(This is copied from the derived variable code; should probably
        figure out a better pattern to avoid duplication."""
        if self.formver >= 4:
            mci = self.uds.get_value("mci", int)
            return 1 if mci == 1 else 0

        # all of these fields can be null, 0, or 1
        mci_vars = self.uds.group_attributes(
            ["mciamem", "mciaplus", "mcinon1", "mcinon2"], int
        )

        return 1 if any(x == 1 for x in mci_vars) else 0

    def has_cognitive_impairment(self) -> bool:
        """Check DEMENTED, MCI, and IMPNOMCI for cognitive impairment."""
        impnomci = self.uds.get_value("impnomci", int)
        return self.demented == 1 or self.generate_mci() == 1 or impnomci == 1
