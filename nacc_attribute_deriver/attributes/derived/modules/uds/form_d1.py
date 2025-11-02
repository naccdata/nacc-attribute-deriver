"""Derived variables from form D1: Clinician Diagnosis.

In V4 this was split into the following 2 forms:
    D1a: Clinical Syndrome
    D1b: Etiological Diagnosis and Biomarker Support

See corresponding form_d1a.py and form_d1b.py for the variables that
moved to those forms. The variables remaining here are either
not applicable to V4 or require variables from both forms.

The original SAS code has a lot of recode logic that basically bulk-
handles recoding variables (usually to handle null values). It is very
unintuitive so that was effectively ignored in this rewrite, and their
function was "redone" per-variable based on the RDD description and
regression testing.
"""

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormDxAttribute(UDSAttributeCollection):
    """Base class for all Dx derived variables."""

    def __init__(self, table: SymbolTable):
        super().__init__(table, uds_required=frozenset(["normcog"]))
        self.subject_derived = SubjectDerivedNamespace(table=table)
        self.working = WorkingDerivedNamespace(table=table)
        self.normcog = self.uds.get_required("normcog", int)
        self.demented = self.uds.get_value("demented", int)

    def generate_mci(self) -> int:
        """Mild cognitive impairment MCI, which is not a derived variable
        itself but is used to calculate other derived variables.

        In V4, this is just the MCI variable.     Returns 1 if MCI == 1,
        else 0 (only option is that or blank, which     means the same
        thing for the purpose of deriving variables) In V3 and earlier,
        this is determined from several variables.     Returns 1 if ANY
        are 1. Returns 0 if all are 0 or blank.
        """
        if self.formver >= 4:
            mci = self.uds.get_value("mci", int)
            return 1 if mci == 1 else 0

        # all of these fields can be null, 0, or 1
        mci_vars = self.uds.group_attributes(
            ["mciamem", "mciaplus", "mcinon1", "mcinon2"], int
        )

        return 1 if any(x == 1 for x in mci_vars) else 0

    def generate_nodx(self) -> int:
        """No diagnosis - used to derive other variables."""

        diagnosis = self.uds.group_attributes(
            [
                "probad",
                "possad",
                "dlb",
                "vasc",
                "vascps",
                "alcdem",
                "demun",
                "ftd",
                "ppaph",
                "psp",
                "cort",
                "hunt",
                "prion",
                "meds",
                "dysill",
                "dep",
                "othpsy",
                "downs",
                "park",
                "stroke",
                "hyceph",
                "brninj",
                "neop",
                "cogoth",
                "cogoth2",
                "cogoth3",
            ],
            int,
        )

        return all(x != 1 for x in diagnosis)


class UDSFormD1Attribute(UDSFormDxAttribute):
    """The following require NP variables."""

    def _create_naccadmu(self) -> int:
        """Creates NACCADMU - Does the subject have a dominantly
        inherited AD mutation?

        Requires NPCHROM/NPPDXP from NP.
        """
        naccadmu = self.subject_derived.get_cross_sectional_value("naccadmu", int)
        if naccadmu == 1:
            return 1

        admut = self.uds.get_value("admut", int)
        npchrom = self.working.get_cross_sectional_value("npchrom", int)
        nppdxp = self.working.get_cross_sectional_value("nppdxp", int)

        if admut == 1 or npchrom in [1, 2, 3] or nppdxp == 1:
            return 1

        return 0

    def _create_naccftdm(self) -> int:
        """Creates NACCFTDM - Does the subject have an hereditary
        FTLD mutation?

        Requires NPCHROM/NPPDXQ from NP.
        """
        naccftdm = self.subject_derived.get_cross_sectional_value("naccftdm", int)
        if naccftdm == 1:
            return 1

        ftldmut = self.uds.get_value("ftldmut", int)
        npchrom = self.working.get_cross_sectional_value("npchrom", int)
        nppdxq = self.working.get_cross_sectional_value("nppdxq", int)

        if ftldmut == 1 or npchrom == 4 or nppdxq == 1:
            return 1

        return 0
