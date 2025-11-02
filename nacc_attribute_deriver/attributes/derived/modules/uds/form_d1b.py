"""Derived variables from form D1b: Etiological Diagnosis and Biomarker
Support.

In V3 and earlier, was part of D1: Clinician Diagnosis.
"""

from typing import List, Optional

from nacc_attribute_deriver.utils.errors import AttributeDeriverError

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

        contr_status = self.get_contr_status(["probadif", "possadif", "alzdisif"])
        if contr_status:
            return contr_status

        return 7

    def _create_nacclbde(self) -> int:
        """From d1structrdd.sas.

        Presumptive etilogic diagnosis of the cognitive disorder
        - Lewy body disease (LBD)
        """
        if self.normcog == 1:
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
        if self.normcog == 1:
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

    def _create_naccetpr(self) -> int:
        """From Create NACCETPR, PRIMDX, SYNMULT.R which in turn comes from
        getd1all.sas.

        Primary etiologic diagnosis (MCI), impaired, not MCI, or
        dementia
        """

        if self.normcog == 1:
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

    def _create_naccalzd(self) -> int:
        """Creates NACCALZD - Presumptive etiologic diagnosis of
        the cognitive disorder - Alzheimer's disease.
        """
        if self.normcog == 1:
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
