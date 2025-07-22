"""Derived variables from form D1: Clinician Diagnosis.

The original SAS code has a lot of recode logic that basically bulk-
handles recoding variables (usually to handle null values). It is very
unintuitive so that was effectively ignored in this rewrite, and their
function was "redone" per-variable based on the RDD description and
regression testing.
"""

from typing import List, Optional

from nacc_attribute_deriver.attributes.base.namespace import (
    SubjectDerivedNamespace,
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable

from .uds_attribute_collection import UDSAttributeCollection


class ContributionStatus:
    PRIMARY = 1
    CONTRIBUTING = 2
    NON_CONTRIBUTING = 3

    @classmethod
    def all(cls):
        """Returns all possible statuses."""
        return [cls.PRIMARY, cls.CONTRIBUTING, cls.NON_CONTRIBUTING]


class UDSFormD1Attribute(UDSAttributeCollection):
    def __init__(self, table: SymbolTable):
        super().__init__(table, uds_required=frozenset(["normcog"]))
        self.__subject_derived = SubjectDerivedNamespace(table=table)
        self.__working = WorkingDerivedNamespace(table=table)
        self.__normcog = self.uds.get_required("normcog", int)
        self.__demented = self.uds.get_value("demented", int)

    def get_contr_status(self, fields: List[str]) -> Optional[int]:
        """Gets the overall contributing status based on the given list.
        Assumes all fields have values null or 1, 2, or 3 (primary,
        contributing, or non-contributing)

        Args:
            fields: Fields to get overall status from
        Returns:
            The overall contributed status, None if none satisfy
        """
        all_statuses = self.uds.group_attributes(fields, int)

        for status in ContributionStatus.all():
            if any([x == status for x in all_statuses]):
                return status

        return None

    def generate_mci(self) -> int:
        """Mild cognitive impairment MCI, which is not a derived variable
        itself but is used to calculate other derived variables."""

        # all of these fields are null, 0, or 1
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

    def _create_naccalzp(self) -> int:
        """From d1structrdd.sas.

        Primary, contributing, or non-contributing cause of observed
        cognitive impairment -- Alzheimer's disease (AD)
        """
        if self.__normcog == 1:
            return 8

        contr_status = self.get_contr_status(["probadif", "possadif", "alzdisif"])
        if contr_status:
            return contr_status

        return 7

    def _create_nacclbde(self) -> int:
        """From d1structrdd.sas.

        Presumptive etilogic diagnosis of the cognitive disorder
        - Lewy body disease (LBD)
        """
        if self.__normcog == 1:
            return 8

        if self.formver != 3:
            dlb = self.uds.get_value("dlb", int)
            park = self.uds.get_value("park", int)

            if dlb == 1 or park == 1:
                return 1
            if dlb == 0 and park == 0:
                return 0

        lbdis = self.uds.get_value("lbdis", int)
        if lbdis in [0, 1]:
            return lbdis

        return 0

    def _create_nacclbdp(self) -> int:
        """From d1structrdd.sas. Also relies on another derived variable
        nacclbde.

        Primary, contributing, or non-contributing cause of cognitive
        impairment -- Lewy body disease (LBD)
        """
        if self.__normcog == 1:
            return 8

        contr_status = None
        if self.formver != 3:
            contr_status = self.get_contr_status(["dlbif", "parkif"])
        else:
            contr_status = self.get_contr_status(["lbdif"])

        if contr_status:
            return contr_status

        if self._create_nacclbde() == 0:
            return 7

        # TODO: raising error instead of returning None
        # I think in theory it seems it shouldn't ever get here
        # and nacclbdp should always be set to something
        # (maybe use 7 as a default otherwise)
        raise ValueError("Unable to determine nacclbdp")

    def _create_naccudsd(self) -> int:
        """From Create NACCUDSD.R which in turn is from derive.sas.

        Cognitive status at UDS visit
        """
        if self.generate_mci() == 1:
            return 3
        if self.__demented == 1:
            return 4
        if self.__normcog == 1:
            return 1
        if self.uds.get_value("impnomci", int) == 1:
            return 2

        # TODO: risk throwing an error here, same situation as nacclbdp.
        # not really sure what a proper default would be in this case
        raise ValueError("Unable to determine naccudsd")

    def _create_naccetpr(self) -> int:
        """From Create NACCETPR, PRIMDX, SYNMULT.R which in turn comes from
        getd1all.sas.

        Primary etiologic diagnosis (MCI), impaired, not MCI, or
        dementia
        """

        if self.__normcog == 1:
            return 88

        # assuming normcog == 0 != 1 after this point
        # get all statuses in a list, then return the first one that == 1 (Primary)
        # result maps to position in list (start index 1)
        all_status = [
            self.get_contr_status(["probadif", "possadif", "alzdisif"]),
            self.get_contr_status(["dlbif", "parkif"])
            if self.formver != 3
            else self.get_contr_status(["lbdif"]),
            # could just grab directly for those with only 1 but this is more readable
            self.get_contr_status(["msaif"]),
            self.get_contr_status(["pspif"]),
            self.get_contr_status(["cortif"]),
            self.get_contr_status(["ftldmoif"]),
            self.get_contr_status(["ftdif", "ppaphif", "ftldnoif"]),
            self.get_contr_status(["cvdif", "vascif", "vascpsif", "strokif"]),
            self.get_contr_status(["esstreif"]),
            self.get_contr_status(["downsif"]),
            self.get_contr_status(["huntif"]),
            self.get_contr_status(["prionif"]),
            self.get_contr_status(["brninjif"]),
            self.get_contr_status(["hycephif"]),
            self.get_contr_status(["epilepif"]),
            self.get_contr_status(["neopif"]),
            self.get_contr_status(["hivif"]),
            self.get_contr_status(["othcogif"]),
            self.get_contr_status(["depif"]),
            self.get_contr_status(["bipoldif"]),
            self.get_contr_status(["schizoif"]),
            self.get_contr_status(["anxietif"]),
            self.get_contr_status(["delirif"]),
            self.get_contr_status(["ptsddxif"]),
            self.get_contr_status(["othpsyif"]),
            self.get_contr_status(["alcdemif"]),
            self.get_contr_status(["impsubif"]),
            self.get_contr_status(["dysillif"]),
            self.get_contr_status(["medsif"]),
            self.get_contr_status(["cogothif", "cogoth2f", "cogoth3f"]),
        ]

        assert len(all_status) == 30
        for i, status in enumerate(all_status):
            if status and self.is_target_int(status, ContributionStatus.PRIMARY):
                return i + 1

        return 99

    def _create_naccppa(self) -> int:
        """From d1structdd.sas.

        Primary progressive aphasia (PPA) with cognitive impairment
        """
        ppaph = self.uds.get_value("ppaph", int)
        ppasyn = self.uds.get_value("ppasyn", int)

        if self.__demented == 1:
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

    def _create_naccbvft(self) -> int:
        """From d1structdd.sas.

        Dementia syndrome -- behavioral variant FTD syndrome (bvFTD)
        """
        if self.__demented != 1:
            return 8

        # assuming demented == 1 after this point
        ftd = self.uds.get_value("ftd", int)
        ftdsyn = self.uds.get_value("ftdsyn", int)

        if ftd in [0, 1]:
            return ftd
        if ftdsyn in [0, 1]:
            return ftdsyn

        # return self.uds.check_default("naccbvft", 8)
        return 8

    def _create_nacclbds(self) -> int:
        """From d1structdd.sas.

        Dementia syndrome -- Lewy body dementia syndrome
        """
        if self.__demented != 1:
            return 8

        # assuming demented == 1 after this point
        dlb = self.uds.get_value("dlb", int)
        lbdsyn = self.uds.get_value("lbdsyn", int)

        if dlb in [0, 1]:
            return dlb
        if lbdsyn in [0, 1]:
            return lbdsyn

        return 8

    def _create_naccalzd(self) -> int:
        """Creates NACCALZD - Presumptive etiologic diagnosis of
        the cognitive disorder - Alzheimer's disease.
        """
        if self.__normcog == 1:
            return 8

        probad = self.uds.get_value("probad", int)
        possad = self.uds.get_value("possad", int)
        alzdis = self.uds.get_value("alzdis", int)

        if any(x == 1 for x in [probad, possad, alzdis]):
            return 1

        if (probad == 0 and possad == 0) or alzdis == 0:
            return 0

        # the above are expected to always be defined, so throw
        # error if we cannot determine it
        raise AttributeDeriverError("Cannot determine NACCALZD")

    def _create_naccnorm(self) -> int:
        """Comes from derive.sas and derivenew.sas (same code)

        Normal cognition at all visits to date
        """
        naccnorm = self.__subject_derived.get_cross_sectional_value("naccnorm", int)
        if naccnorm == 0:
            return 0

        return self.__normcog

    def _create_notdemin(self) -> Optional[int]:
        """Creates NOTDEMIN, which is a helper variable for whether someone is
        demented at the initial visit.

        Used for NACCIDEM.
        """
        if not self.uds.is_initial():
            return None

        impnomci = self.uds.get_value("impnomci", int)
        mci = self.generate_mci()
        if self.__normcog == 1 or impnomci == 1 or mci == 1:
            return 1

        return 0

    def _create_naccidem(self) -> Optional[int]:
        """Creates NACCIDEM - Incident dementia during UDS follow-up"""
        naccidem = self.__subject_derived.get_cross_sectional_value("naccidem", int)
        if naccidem == 1:
            return 1

        # requires followup visit, so if initial return 0/9 - visits
        # should be curated in order anyways
        if self.uds.is_initial():
            if self.__demented == 1:
                return 8

            return 0

        notdemin = self.__working.get_cross_sectional_value("notdemin", int)
        if notdemin == 1 and self.__demented == 1:
            return 1

        # in general should be set, but sometimes we don't receive an initial visit
        return naccidem

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
        if self.__demented == 1 and naccppa == 0:
            return 7

        return 8

    def _create_naccppme(self) -> Optional[int]:
        """Creates NACCPPME - Primary progressive aphasia (PPA) subtype according to
        older criteria outlined by Mesulam et al. (2001 and 2003)

        Not assessed this way in v3+
        """
        if self.formver >= 3:
            return None

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
        if (self.__demented == 1 or impnomci == 1 or mci == 1) and naccppa != 1:
            return 7

        if impnomci != 1 and mci != 1 and self.__demented != 1:
            return 8

        # TODO: SAS sets default to -9, but -9 is not valid per RDD. not sure
        # if it's translated to -4 or something else elsewhere
        return -9

    def _create_nacctmci(self) -> int:
        """Creates NACCTMCI - Mild cognitive impairment (MCI) type"""
        if self.uds.get_value("mciamem", int) == 1:
            return 1
        if self.uds.get_value("mciaplus", int) == 1:
            return 2
        if self.uds.get_value("mcinon1", int) == 1:
            return 3
        if self.uds.get_value("mcinon2", int) == 1:
            return 4

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

    def _create_naccmcii(self) -> int:
        """Creates NACCMCII - Incident MCI during USD follow-up

        Requires working variables FVMCI.
        """
        naccmcii = self.__subject_derived.get_cross_sectional_value("naccmcii", int)
        fvmci = self.__working.get_cross_sectional_value("fvmci", int)

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
        if self.__normcog == 1 or impnomci == 1:
            return 1

        return 0

    def _create_fvmci(self) -> Optional[int]:
        """Creates FVMCI - helper variable for NACCMCII. Only defined
        in follow-up visits."""
        if self.uds.is_initial():
            return None

        mci = self.generate_mci()
        fvmci = self.__working.get_cross_sectional_value("fvmci", int)
        ivcstat = self.__working.get_cross_sectional_value("ivcstat", int)

        if mci == 1 and fvmci is None:
            return 1

        if mci != 1 and fvmci != 1 and ivcstat == 1 and self.__demented == 1:
            return 2

        return fvmci

    """
    The following require NP variables.
    """

    def _create_naccadmu(self) -> int:
        """Creates NACCADMU - Does the subject have a dominantly
        inherited AD mutation?

        Requires NPCHROM/NPPDXP from NP.
        """
        naccadmu = self.__subject_derived.get_cross_sectional_value("naccadmu", int)
        if naccadmu == 1:
            return 1

        admut = self.uds.get_value("admut", int)
        npchrom = self.__working.get_cross_sectional_value("npchrom", int)
        nppdxp = self.__working.get_cross_sectional_value("nppdxp", int)

        if admut == 1 or npchrom in [1, 2, 3] or nppdxp == 1:
            return 1

        return 0

    def _create_naccftdm(self) -> int:
        """Creates NACCFTDM - Does the subject have an hereditary
        FTLD mutation?

        Requires NPCHROM/NPPDXQ from NP.
        """
        naccftdm = self.__subject_derived.get_cross_sectional_value("naccftdm", int)
        if naccftdm == 1:
            return 1

        ftldmut = self.uds.get_value("ftldmut", int)
        npchrom = self.__working.get_cross_sectional_value("npchrom", int)
        nppdxq = self.__working.get_cross_sectional_value("nppdxq", int)

        if ftldmut == 1 or npchrom == 4 or nppdxq == 1:
            return 1

        return 0
