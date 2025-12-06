"""Derived variables from form D1: Clinician Diagnosis.

In V4 this was split into the following 2 forms:
    D1a: Clinical Syndrome
    D1b: Etiological Diagnosis and Biomarker Support

See corresponding form_d1a.py and form_d1b.py for the variables that
moved to those forms.
"""

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormDxAttribute(UDSAttributeCollection):
    """Base class for all Dx derived variables."""

    def __init__(self, table: SymbolTable):
        super().__init__(table, required=frozenset(["normcog"]))
        self.subject_derived = SubjectDerivedNamespace(table=table)
        self.working = WorkingNamespace(table=table)
        self.normcog = self.uds.get_required("normcog", int)
        self.demented = self.uds.get_value("demented", int)

    def generate_mci(self) -> int:
        """Mild cognitive impairment MCI, which is not a derived variable
        itself but is used to calculate other derived variables.

        In V4, this is just the MCI variable.
        Returns 1 if MCI == 1, else 0 (only option is that or blank, which
        means the same thing for the purpose of deriving variables)

        In V3 and earlier, this is determined from several variables.
        Returns 1 if ANY are 1. Returns 0 if all are 0 or blank.
        """
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
