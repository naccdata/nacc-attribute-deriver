"""Derived variables from form D1a: Clinical Syndrome.

In V3 and earlier, was part of D1: Clinician Diagnosis.

The original SAS code has a lot of recode logic that basically bulk-
handles recoding variables (usually to handle null values). It is very
unintuitive so that was effectively ignored in this rewrite, and their
function was "redone" per-variable based on the RDD description and
regression testing.
"""

from typing import List, Optional

from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)

from .form_d1 import UDSFormDxAttribute


class UDSFormD1aAttribute(UDSFormDxAttribute):
    def _create_naccudsd(self) -> int:
        """From Create NACCUDSD.R which in turn is from derive.sas.

        Cognitive status at UDS visit
        """
        if self.generate_mci() == 1:
            return 3
        if self.demented == 1:
            return 4
        if self.normcog == 1:
            return 1
        if self.uds.get_value("impnomci", int) == 1:
            return 2

        # TODO: risk throwing an error here, same situation as nacclbdp.
        # not really sure what a proper default would be in this case
        raise ValueError("Unable to determine naccudsd")

    def _create_naccppa(self) -> int:
        """From d1structdd.sas.

        Primary progressive aphasia (PPA) with cognitive impairment
        """
        ppaph = self.uds.get_value("ppaph", int)
        ppasyn = self.uds.get_value("ppasyn", int)

        if self.demented == 1:
            if ppaph == 1 or ppasyn == 1:
                return 1
            if ppaph == 0 or ppasyn == 0:
                return 0

        elif self.uds.get_value("impnomci", int) == 1 or self.generate_mci() == 1:
            if ppaph == 1 or ppasyn == 1:
                return 1
            if ppaph == 0 or ppasyn == 0:
                return 0

            nodx = self.generate_nodx()
            if (self.formver < 3 and nodx == 1) or (self.formver >= 3):
                return 7

        return 8

    def _create_naccppme(self) -> Optional[int]:
        """Creates NACCPPME - Primary progressive aphasia (PPA) subtype according to
        older criteria outlined by Mesulam et al. (2001 and 2003)

        Not assessed this way in v3+
        """
        if self.formver >= 3:
            return INFORMED_MISSINGNESS

        if self.uds.get_value("pnaph", int) == 1:
            return 1
        if self.uds.get_value("semdeman", int) == 1:
            return 2
        if self.uds.get_value("semdemag", int) == 1:
            return 3
        if self.uds.get_value("ppaothr", int) == 1:
            return 4

        impnomci = self.uds.get_value("impnomci", int)
        mci = self.generate_mci()
        nodx = self.generate_nodx()

        if (impnomci == 1 or mci == 1) and nodx == 1:
            return 6

        naccppa = self._create_naccppa()
        if (self.demented == 1 or impnomci == 1 or mci == 1) and naccppa != 1:
            return 7

        if impnomci != 1 and mci != 1 and self.demented != 1:
            return 8

        # SAS returns -9; likely changes to -4 at some point
        return INFORMED_MISSINGNESS

    def _create_naccppag(self) -> Optional[int]:
        """Creates NACCPPAG - Dementia syndrome -- Primary progressive aphasia (PPA)
        subtype according to the criteria outlined by Gorno-Tempini et al. 2011

        Not asessed this way in v1.2 or v2.
        """
        if self.formver < 3:
            return None

        ppasynt = self.uds.get_value("ppasynt", int)
        if ppasynt in [1, 2, 3, 4]:
            return ppasynt

        naccppa = self._create_naccppa()
        if self.demented == 1 and naccppa == 0:
            return 7

        return 8

    def determine_mci_domain_affected(self, mci_domain: List[str]) -> int:
        """Determines if the given MCI domain is affected.

        Expects exactly 3 variables, where
            1. parant variable is MCIAPLUS
            2. parant variable is MCINON1
            3. parant variable is MCINON2

        Args:
            mci_domain: List of strings specifying vars for the MCI domain
        """
        assert len(mci_domain) == 3, "Expected 3 variables for MCI domain"
        mci_vars = self.uds.group_attributes(mci_domain, int)

        # may need to cast nulls to 0s depending on a parent varaible
        # same order as mci_domain
        if self.generate_mci() == 1:
            for i, parent in enumerate(["mciaplus", "mcinon1", "mcinon2"]):
                if self.uds.get_value(parent, int) == 0 and mci_vars[i] is None:
                    mci_vars[i] = 0

        if any(x == 1 for x in mci_vars):
            return 1

        if all(x == 0 for x in mci_vars):
            return 0

        return 8

    def _create_naccmcia(self) -> int:
        """Creates NACCMCIA - MCI domain affected -- attention"""
        return self.determine_mci_domain_affected(["mciapatt", "mcin1att", "mcin2att"])

    def _create_naccmcie(self) -> int:
        """Creates NACCMCIE - MCI domain affected -- executive function"""
        return self.determine_mci_domain_affected(["mciapex", "mcin1ex", "mcin2ex"])

    def _create_naccmcil(self) -> int:
        """Creates NACCMCIL - MCI domain affected -- language"""
        return self.determine_mci_domain_affected(["mciaplan", "mcin1lan", "mcin2lan"])

    def _create_naccmciv(self) -> int:
        """Creates NACCMCIV - MCI domain affected -- visuospatial"""
        return self.determine_mci_domain_affected(["mciapvis", "mcin1vis", "mcin2vis"])

    def _create_naccnorm(self) -> int:
        """Comes from derive.sas and derivenew.sas (same code)

        Normal cognition at all visits to date
        """
        naccnorm = self.subject_derived.get_cross_sectional_value("naccnorm", int)
        if naccnorm == 0:
            return 0

        return self.normcog

    def _create_notdemin(self) -> Optional[int]:
        """Creates NOTDEMIN, which is a helper variable for whether someone is
        demented at the initial visit.

        Used for NACCIDEM.
        """
        if not self.uds.is_initial():
            return None

        impnomci = self.uds.get_value("impnomci", int)
        mci = self.generate_mci()
        if self.normcog == 1 or impnomci == 1 or mci == 1:
            return 1

        return 0

    def _create_naccidem(self) -> Optional[int]:
        """Creates NACCIDEM - Incident dementia during UDS follow-up"""
        naccidem = self.subject_derived.get_cross_sectional_value("naccidem", int)
        if naccidem == 1:
            return 1

        # requires followup visit, so if initial return 0/9 - visits
        # should be curated in order anyways
        if self.uds.is_initial():
            if self.demented == 1:
                return 8

            return 0

        notdemin = self.working.get_cross_sectional_value("notdemin", int)
        if notdemin == 1 and self.demented == 1:
            return 1

        # in general should be set, but sometimes we don't receive an initial visit
        return naccidem

    def _create_naccmcii(self) -> int:
        """Creates NACCMCII - Incident MCI during USD follow-up

        Requires working variables FVMCI.
        """
        # NOTE: despite this initial visit logic being in both SAS/RDD, it doesn't
        # seem to match QAF, as if it is not considering initial visit. This seems
        # like an error, and the below should fix it going forward
        mci = self.generate_mci()
        if self.uds.is_initial():
            if self.demented == 1 or mci == 1:
                return 8
            return 0

        # assuming followup after this point
        naccmcii = self.subject_derived.get_cross_sectional_value("naccmcii", int)
        fvmci = self.working.get_cross_sectional_value("fvmci", int)

        if fvmci == 1 and naccmcii != 8:
            return 1
        if fvmci == 2:
            return 8

        return 0 if naccmcii is None else naccmcii

    """
    The following are working variables (non-NACC derived variables but used
    to help derive other NAC-derived variables.)
    """

    def _create_ivcstat(self) -> Optional[int]:
        """Creates IVCSTAT - helper variable for FVMCI. Only defined
        at initial visit."""
        if not self.uds.is_initial():
            return None

        impnomci = self.uds.get_value("impnomci", int)
        if self.normcog == 1 or impnomci == 1:
            return 1

        return 0

    def _create_fvmci(self) -> Optional[int]:
        """Creates FVMCI - helper variable for NACCMCII. Only defined
        in follow-up visits."""
        if self.uds.is_initial():
            return None

        mci = self.generate_mci()
        fvmci = self.working.get_cross_sectional_value("fvmci", int)
        ivcstat = self.working.get_cross_sectional_value("ivcstat", int)

        if mci == 1 and fvmci is None:
            return 1

        if mci != 1 and fvmci != 1 and ivcstat == 1 and self.demented == 1:
            return 2

        return fvmci
