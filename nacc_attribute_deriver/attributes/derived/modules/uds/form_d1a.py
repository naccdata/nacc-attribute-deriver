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
from nacc_attribute_deriver.utils.errors import AttributeDeriverError

from .form_d1 import UDSFormDxAttribute


class UDSFormD1aAttribute(UDSFormDxAttribute):
    def _create_naccmcim(self) -> int:
        """Creates NACCMCIM - MCI domain affected - memory.

        Newly introduced in V4, but applies to all versions.
        """
        # V1 - V3
        if self.formver < 4:
            mciamem = self.uds.get_value("mciamem", int)
            mciaplus = self.uds.get_value("mciaplus", int)
            if mciamem == 1 or mciaplus == 1:
                return 1
            if mciamem == 0 and mciaplus == 0:
                return 0

            if self.generate_mci() == 0:
                return 8

            return INFORMED_MISSINGNESS

        # V4
        cdommem = self.uds.get_value("cdommem", int)
        if self.generate_mci() == 1:
            if cdommem == 1:
                return 1
            if cdommem is None:
                return 0

        # only other case is MCI is 0 or None, so return 8 = Not diagnosed with MCI
        return 8

    def _create_naccmciapx(self) -> int:
        """Creates NACCMCIAPX - MCI domain affected - apraxia.

        Newly introduceed in V4 and only applicable to V4.
        """
        if self.formver < 4:
            return INFORMED_MISSINGNESS

        cdomaprax = self.uds.get_value("cdomaprax", int)
        if self.generate_mci() == 1:
            if cdomaprax == 1:
                return 1
            if cdomaprax is None:
                return 0

        # only other case is MCI is 0 or None, so return 8 = Not diagnosed with MCI
        return 8

    def _create_naccdepd(self) -> int:
        """Creates NACCDEPD - Non-neurodegenerative or non-CVD conditions affecting
        cognitive impairment - Depression (v1-4)

        Newly introduceed in V4 but applies to all versions.
        """
        if self.normcog == 1:
            return 8

        if self.formver < 4:
            dep = self.uds.get_value("dep", int)
            if dep == 1:
                return 1
            if dep == 0 or dep is None:
                return 0
        else:
            majdepdx = self.uds.get_value("majdepdx", int)
            othdepdx = self.uds.get_value("othdepdx", int)
            if majdepdx == 1 or othdepdx == 1:
                return 1
            if majdepdx is None and othdepdx is None:
                return 0

        # shouldn't really reach this case, but fallback
        return INFORMED_MISSINGNESS

    def _create_naccdepdif(self) -> int:
        """Creates NACCDEPDIF - Primary, contributing, or non-contributing cause of
        cognitive impairment - Depression (v1-4)

        Newly introduced in V4, but applies to all versions.
        """
        if self.normcog == 1:
            return 8

        if self.formver < 4:
            depif = self.uds.get_value("depif", int)
            dep = self.uds.get_value("dep", int)

            if depif in [1, 2, 3]:
                return depif
            if dep == 0 or dep is None:
                return 7
        else:
            majdepdxif = self.uds.get_value("majdepdxif", int)
            othdepdif = self.uds.get_value("othdepdif", int)
            othdepdx = self.uds.get_value("othdepdx", int)
            majdepdx = self.uds.get_value("majdepdx", int)

            if majdepdxif in [1, 2, 3] and othdepdif in [1, 2, 3]:
                return max(majdepdxif, othdepdif)
            if majdepdx is None and othdepdx is None:
                return 7

        # shouldn't really reach this case, but fallback
        return INFORMED_MISSINGNESS

    def _create_nacctbidx(self) -> int:
        """Creates NACCTBIDX - Non-neurodegenerative or non-CVD conditions affecting
        cognitive impairment - Traumatic brain injury (TBI) (v1-4)

        Newly introduced in V4, but applies to all versions.
        """
        if self.normcog == 1:
            return 8

        if self.formver < 4:
            brninj = self.uds.get_value("brninj", int)
            if brninj == 1:
                return 1
            if brninj == 0 or brninj is None:
                return 0
        else:
            tbidx = self.uds.get_value("tbidx", int)
            if tbidx == 1:
                return 1
            if tbidx is None:
                return 0

        # shouldn't really reach this case, but fallback
        return INFORMED_MISSINGNESS

    def _create_nacctbidxif(self) -> int:
        """Creates NACCTBIDXIF - Primary, contributing, or non-contributing cause of
        cognitive impairment - Traumatic brain injury (TBI) (v1-4)

        Newly introduced in V4, but applies to all versions.
        """
        if self.normcog == 1:
            return 8

        if self.formver < 4:
            brninjif = self.uds.get_value("brninjif", int)
            brninj = self.uds.get_value("brninj", int)
            if brninjif in [1, 2, 3]:
                return brninjif
            if brninj == 0 or brninj is None:
                return 7
        else:
            tbidxif = self.uds.get_value("tbidxif", int)
            tbidx = self.uds.get_value("tbidx", int)
            if tbidxif in [1, 2, 3]:
                return 1
            if tbidx is None:
                return 7

        # shouldn't really reach this case, but fallback
        return INFORMED_MISSINGNESS

    def _create_naccudsd(self) -> int:
        """From Create NACCUDSD.R which in turn is from derive.sas.

        Cognitive status at UDS visit

        V1 - V4 logic is the same, only difference is where MCI comes from
        """
        if self.normcog == 1:
            return 1
        if self.uds.get_value("impnomci", int) == 1:
            return 2
        if self.generate_mci() == 1:
            return 3
        if self.demented == 1:
            return 4

        return INFORMED_MISSINGNESS

    def __determine_predominant_syndrome(self, field: str) -> int:
        """V4; determine predominant syndrome, used for NACCAPPA, NACCBVFT, and
        NACCLBDS.

        If NORMCOG == 1, DERIVED = 8
        If FIELD == 1, DERIVED = 1
        If PREDOMSYN == 1 and FIELD is blank, return 0
        if PREDOMSYN == 0 and FIELD is blank, return 7
        """
        if self.normcog == 1:
            return 8

        value = self.uds.get_value(field, int)
        predomsyn = self.uds.get_value("predomsyn", int)
        if value == 1:
            return 8
        if predomsyn == 1 and value is None:
            return 0
        if predomsyn == 0 and value is None:
            return 7

        return INFORMED_MISSINGNESS

    def _create_naccppa(self) -> int:
        """From d1structdd.sas.

        Primary progressive aphasia (PPA) with cognitive impairment
        """
        if self.formver >= 4:
            return self.__determine_predominant_syndrome("ppasyn")

        # V3 and earlier
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

    def _create_naccppag(self) -> int:
        """Creates NACCPPAG - Dementia syndrome -- Primary progressive aphasia (PPA)
        subtype according to the criteria outlined by Gorno-Tempini et al. 2011

        Not asessed this way in v1.2 or v2.
        """
        if self.formver < 3:
            return INFORMED_MISSINGNESS

        # V3
        if self.formver < 4:
            ppasynt = self.uds.get_value("ppasynt", int)
            if ppasynt in [1, 2, 3, 4]:
                return ppasynt

            naccppa = self._create_naccppa()
            if self.demented == 1 and naccppa == 0:
                return 7

            return 8

        # V4
        ppasyn = self.uds.get_value("ppasyn", int)
        predomsyn = self.uds.get_value("predomsyn", int)
        if self.normcog == 0 and predomsyn == 1 and ppasyn is None:
            return 7
        if self.normcog == 1 and ppasyn is None:
            return 8

        ppasynt = self.uds.get_value("ppasynt", int)
        return ppasynt if ppasynt is not None else INFORMED_MISSINGNESS

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

    def _create_naccbvft(self) -> int:
        """From d1structdd.sas.

        Dementia syndrome -- behavioral variant FTD syndrome (bvFTD)
        """
        if self.formver >= 4:
            return self.__determine_predominant_syndrome("ftdsyn")

        # V3 and earlier
        if self.demented != 1:
            return 8

        # assuming demented == 1 after this point
        ftd = self.uds.get_value("ftd", int)
        ftdsyn = self.uds.get_value("ftdsyn", int)

        if ftd in [0, 1]:
            return ftd
        if ftdsyn in [0, 1]:
            return ftdsyn

        return 8

    def _create_nacclbds(self) -> int:
        """From d1structdd.sas.

        Dementia syndrome -- Lewy body dementia syndrome
        """
        if self.formver >= 4:
            return self.__determine_predominant_syndrome("lbdsyn")

        # V3 and earlier
        if self.demented != 1:
            return 8

        # assuming demented == 1 after this point
        dlb = self.uds.get_value("dlb", int)
        lbdsyn = self.uds.get_value("lbdsyn", int)

        if dlb in [0, 1]:
            return dlb
        if lbdsyn in [0, 1]:
            return lbdsyn

        return 8

    def _create_nacctmci(self) -> int:  # noqa: C901
        """Creates NACCTMCI - Mild cognitive impairment (MCI) type"""
        # V3 and earlier
        if self.formver < 4:
            if self.uds.get_value("mciamem", int) == 1:
                return 1
            if self.uds.get_value("mciaplus", int) == 1:
                return 2
            if self.uds.get_value("mcinon1", int) == 1:
                return 3
            if self.uds.get_value("mcinon2", int) == 1:
                return 4

            return 8

        # V4
        cdommem = self.uds.get_value("cdommem", int)
        cdom_regions = self.uds.group_attributes(
            ["cdomlang", "cdomattn", "cdomexec", "cdomvisu", "cdomaprax"], int
        )

        if cdommem == 1:
            if all(x is None for x in cdom_regions):
                return 1
            if any(x == 1 for x in cdom_regions):
                return 2
        elif cdommem == 0:
            num_regions = cdom_regions.count(1)
            if num_regions == 1:
                return 3
            if num_regions > 1:
                return 4

        if self.generate_mci() == 0:
            return 8

        return INFORMED_MISSINGNESS

    def determine_mci_domain_affected_v3(self, mci_domain: List[str]) -> int:
        """V3 and earlier. Determines if the given MCI domain is affected.

        Expects exactly 3 variables, where
            1. parant variable is MCIAPLUS
            2. parant variable is MCINON1
            3. parant variable is MCINON2

        Args:
            mci_domain: List of strings specifying vars for the MCI domain
        """
        if self.formver >= 4:
            raise AttributeDeriverError("Called V1-V3 method on non-V1-V3 data")

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

    def determine_mci_domain_affected_v4(self, mci_domain: str) -> int:
        """V4.

        Determines if the given MCI domain is affected.
        """
        if self.formver < 4:
            raise AttributeDeriverError("Called V4 method on non-V4 data")

        if self.generate_mci() == 1:
            value = self.uds.get_value(mci_domain, int)
            if value == 1:
                return 1
            if value is None:
                return 0

        return 8

    def _create_naccmcil(self) -> int:
        """Creates NACCMCIL - MCI domain affected -- language"""
        if self.formver >= 4:
            return self.determine_mci_domain_affected_v4("cdomlang")

        return self.determine_mci_domain_affected_v3(
            ["mciaplan", "mcin1lan", "mcin2lan"]
        )

    def _create_naccmcia(self) -> int:
        """Creates NACCMCIA - MCI domain affected -- attention"""
        if self.formver >= 4:
            return self.determine_mci_domain_affected_v4("cdomattn")

        return self.determine_mci_domain_affected_v3(
            ["mciapatt", "mcin1att", "mcin2att"]
        )

    def _create_naccmcie(self) -> int:
        """Creates NACCMCIE - MCI domain affected -- executive function"""
        if self.formver >= 4:
            return self.determine_mci_domain_affected_v4("cdomexec")

        return self.determine_mci_domain_affected_v3(["mciapex", "mcin1ex", "mcin2ex"])

    def _create_naccmciv(self) -> int:
        """Creates NACCMCIV - MCI domain affected -- visuospatial"""
        if self.formver >= 4:
            return self.determine_mci_domain_affected_v4("cdomvisu")

        return self.determine_mci_domain_affected_v3(
            ["mciapvis", "mcin1vis", "mcin2vis"]
        )

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
