"""Derived variables from form D1b: Etiological Diagnosis and Biomarker
Support.

In V3 and earlier, was part of D1: Clinician Diagnosis.
"""

from typing import List, Optional

from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)

from .form_d1 import UDSFormDxAttribute


class ContributionStatus:
    PRIMARY = 1
    CONTRIBUTING = 2
    NON_CONTRIBUTING = 3

    @classmethod
    def all(cls):
        """Returns all possible statuses."""
        return [cls.PRIMARY, cls.CONTRIBUTING, cls.NON_CONTRIBUTING]


class UDSFormD1bAttribute(UDSFormDxAttribute):
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

    def _create_naccalzp(self) -> int:
        """From d1structrdd.sas.

        Primary, contributing, or non-contributing cause of observed
        cognitive impairment -- Alzheimer's disease (AD)
        """
        if self.normcog == 1:
            return 8

        if self.formver < 4:
            contr_status = self.get_contr_status(["probadif", "possadif", "alzdisif"])
            if contr_status:
                return contr_status

            return 7

        alzdisif = self.uds.get_value("alzdisif", int)
        if alzdisif in [1, 2, 3]:
            return alzdisif

        if self.has_cognitive_impairment():
            return 7

        # TODO: ASKING RT ABOUT THE MBI CASE - FOR NOW RETURN 0
        return 0

    def _create_nacclbde(self) -> int:
        """From d1structrdd.sas.

        Presumptive etilogic diagnosis of the cognitive disorder
        - Lewy body disease (LBD)
        """
        if self.normcog == 1:
            return 8

        if self.formver < 3:
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
        if self.normcog == 1:
            return 8

        contr_status = None
        if self.formver < 3:
            contr_status = self.get_contr_status(["dlbif", "parkif"])
        else:
            contr_status = self.get_contr_status(["lbdif"])

        if contr_status:
            return contr_status

        if self.formver < 4:
            if self._create_nacclbde() == 0:
                return 7
        elif self.has_cognitive_impairment():
            return 7

        # TODO: ASKING RT ABOUT MBI - FOR NOW RETURN 0 (NO)
        return 0

    def _create_naccalzd(self) -> int:
        """Creates NACCALZD - Presumptive etiologic diagnosis of
        the cognitive disorder - Alzheimer's disease.
        """
        if self.normcog == 1:
            return 8

        alzdis = self.uds.get_value("alzdis", int)

        if self.formver < 4:
            probad = self.uds.get_value("probad", int)
            possad = self.uds.get_value("possad", int)

            if any(x == 1 for x in [probad, possad, alzdis]):
                return 1

            if (probad == 0 and possad == 0) or alzdis == 0:
                return 0

        if alzdis is None:
            return 0

        return alzdis

    def _create_naccadmu(self) -> int:
        """Creates NACCADMU - Does the subject have a dominantly
        inherited AD mutation?

        Requires NPCHROM/NPPDXP from NP. Stays at 1 if ever set to 1.
        """
        naccadmu = self.subject_derived.get_cross_sectional_value("naccadmu", int)
        if naccadmu == 1:
            return 1

        if self.formver >= 4:
            return 1 if self.uds.get_value("nppdxp", int) == 1 else 0

        admut = self.uds.get_value("admut", int)
        npchrom = self.working.get_cross_sectional_value("npchrom", int)
        nppdxp = self.working.get_cross_sectional_value("nppdxp", int)

        if admut == 1 or npchrom in [1, 2, 3] or nppdxp == 1:
            return 1

        return 0

    def _create_naccftdm(self) -> int:
        """Creates NACCFTDM - Does the subject have an hereditary
        FTLD mutation?

        Requires NPCHROM/NPPDXQ from NP. Stays at 1 if ever set to 1.
        """
        naccftdm = self.subject_derived.get_cross_sectional_value("naccftdm", int)
        if naccftdm == 1:
            return 1

        if self.formver >= 4:
            return 1 if self.uds.get_value("nppdxq", int) == 1 else 0

        ftldmut = self.uds.get_value("ftldmut", int)
        npchrom = self.working.get_cross_sectional_value("npchrom", int)
        nppdxq = self.working.get_cross_sectional_value("nppdxq", int)

        if ftldmut == 1 or npchrom == 4 or nppdxq == 1:
            return 1

        return 0

    def _create_naccwmhsev(self) -> Optional[int]:
        """Creates NACCWMHSEV - White-matter hyperintensity severity.
        Only in V3+
        """
        if self.formver < 3:
            return INFORMED_MISSINGNESS

        imagmwmh = self.uds.get_value("imagmwmh", int)  # V3
        imagewmh = self.uds.get_value("imagewmh", int)  # V3
        imagwmhsev = self.uds.get_value("imagwmhsev", int)  # V4
        if imagwmhsev == 1 or imagmwmh == 1:
            return 1
        if imagwmhsev == 2 or imagewmh == 1:
            return 2

        imagwmh = self.uds.get_value("imagwmh", int)  # V4
        if imagwmh == 0 or (imagmwmh == 0 and imagewmh == 0):
            return 7
        if imagwmh == 8 or (imagmwmh == 8 and imagewmh == 8):
            return 8
        if imagwmh == 9:
            return 9

        return INFORMED_MISSINGNESS

    def has_primary_d1b(self) -> bool:
        """Check if primary in D1b."""
        all_attributes = self.uds.group_attributes(
            [
                "alzdisif",
                "lbdif",
                "msaif",
                "pspif",
                "cortif",
                "ftldmoif",
                "ftldnoif",
                "cvdif",
                "downsif",
                "huntif",
                "prionif",
                "othcogif",
                "cteif",
                "caaif",
                "lateif",
            ],
            int,
        )

        return not all(x == 0 or x is None for x in all_attributes)

    def has_primary(self, attributes: List[str], check_primary: bool = False) -> bool:
        """Returns true if any of the attributes == 1 (Primary).

        False otherwise.
        """

        # For V4, some rules require PRIMDXD1B = False
        if self.formver >= 4 and self.has_primary_d1b():
            return False

        overall_status = self.get_contr_status(attributes)
        return overall_status == ContributionStatus.PRIMARY

    def _create_naccetpr(self) -> int:  # noqa: C901
        """From Create NACCETPR, PRIMDX, SYNMULT.R which in turn comes from
        getd1all.sas.

        Primary etiologic diagnosis (MCI), impaired, not MCI, or
        dementia
        """

        if self.normcog == 1:
            return 88

        # assuming normcog == 0 after this point
        # get all statuses in a list, evaluate each group in order

        if self.has_primary(["probadif", "possadif", "alzdisif"]):
            return 1
        if self.formver < 3 and self.has_primary(["dlbif", "parkif"]):
            return 2
        if self.formver >= 3 and self.has_primary(["lbdif"]):
            return 2
        if self.has_primary(["msaif"]):
            return 3
        if self.has_primary(["pspif"]):
            return 4
        if self.has_primary(["cortif"]):
            return 5
        if self.has_primary(["ftldmoif"]):
            return 6
        if self.has_primary(["ftdif", "ppaphif", "ftldnoif"]):
            return 7
        if self.has_primary(["cvdif", "vascif", "vascpsif", "strokif"]):
            return 8
        if self.formver < 4 and self.has_primary(["esstreif"]):
            return 9
        if self.has_primary(["downsif"]):
            return 10
        if self.has_primary(["huntif"]):
            return 11
        if self.has_primary(["prionif"]):
            return 12
        if self.formver < 4 and self.has_primary(["brninjif"]):
            return 13
        if self.formver >= 4 and self.has_primary(["tbidxif"], check_primary=True):
            return 13
        if self.has_primary(["hycephif"], check_primary=True):
            return 14
        if self.has_primary(["epilepif"], check_primary=True):
            return 15
        if self.has_primary(["neopif"], check_primary=True):
            return 16
        if self.has_primary(["hivif"], check_primary=True):
            return 17
        if self.has_primary(["othcogif", "othcillif"], check_primary=True):
            return 18
        if self.has_primary(["depif"], check_primary=True):
            return 19
        if self.has_primary(["bipoldif"], check_primary=True):
            return 20
        if self.has_primary(["schizoif"], check_primary=True):
            return 21
        if self.has_primary(["anxietif"], check_primary=True):
            return 22
        if self.has_primary(["delirif"], check_primary=True):
            return 23
        if self.has_primary(["ptsddxif"], check_primary=True):
            return 24
        if self.has_primary(["othpsyif"], check_primary=True):
            return 25
        if self.has_primary(["alcdemif"], check_primary=True):
            return 26
        if self.has_primary(["impsubif"], check_primary=True):
            return 27
        if self.has_primary(["dysillif"], check_primary=True):
            return 28
        if self.has_primary(["medsif"], check_primary=True):
            return 29
        if self.has_primary(["cogothif", "cogoth2f", "cogoth3f"], check_primary=True):
            return 30
        if self.has_primary(["ndevdisif"], check_primary=True):
            return 31
        if self.has_primary(["cteif"]):
            return 32
        if self.has_primary(["caaif"]):
            return 33
        if self.has_primary(["lateif"]):
            return 34

        return 99
