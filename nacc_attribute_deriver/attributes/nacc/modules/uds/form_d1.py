"""Derived variables from form D1."""

from typing import List, Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class ContributionStatus:
    PRIMARY = 1
    CONTRIBUTING = 2
    NON_CONTRIBUTING = 3

    @classmethod
    def all(cls):
        """Returns all possible statuses."""
        return [cls.PRIMARY, cls.CONTRIBUTING, cls.NON_CONTRIBUTING]


class UDSFormD1Attribute(AttributeCollection):
    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)
        self.__subject_derived = SubjectDerivedNamespace(table)

    def get_contr_status(self, fields: List[str]) -> Optional[int]:
        """Gets the overall contributing status based on the given list.
        Assumes all fields have values null or 1, 2, or 3 (primary,
        contributing, or non-contributing)

        Args:
            fields: Fields to get overall status from
        Returns:
            The overall contributed status, None if none satisfy
        """
        # TODO: seems like this could be a set
        all_statuses = []

        for field in fields:
            all_statuses.append(self.__uds.get_value(field))

        for status in ContributionStatus.all():
            if any([x == status for x in all_statuses]):
                return status

        return None

    def _create_mci(self) -> int:
        """Mild cognitive impairment Create MCI, which is not a derived
        variable itself but is used to calculate other derived variables."""

        # all of these fields are null, 0, or 1
        return (
            1
            if any(
                [
                    self.__uds.get_value("mciamem"),
                    self.__uds.get_value("mciaplus"),
                    self.__uds.get_value("mcinon1"),
                    self.__uds.get_value("mcinon2"),
                ]
            )
            else 0
        )

    def _create_naccalzp(self) -> int:
        """From d1structrdd.sas.

        Primary, contributing, or non-contributing cause of observed
        cognitive impairment -- Alzheimer's disease (AD)
        """
        if self.__uds.get_value("normcog") == 1:
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
        if self.__uds.get_value("normcog") == 1:
            return 8

        if self.__uds.normalized_formver() != 3:
            dlb = self.__uds.get_value("dlb")
            park = self.__uds.get_value("park")

            if dlb == 1 or park == 1:
                return 1
            if dlb == 0 and park == 0:
                return 0

        lbdis = self.__uds.get_value("lbdis")
        if lbdis in [0, 1]:
            return lbdis

        return 0

    def _create_nacclbdp(self) -> int:
        """From d1structrdd.sas. Also relies on another derived variable
        nacclbde.

        Primary, contributing, or non-contributing cause of cognitive
        impairment -- Lewy body disease (LBD)
        """
        if self.__uds.get_value("normcog") == 1:
            return 8

        contr_status = None
        if self.__uds.normalized_formver() != 3:
            contr_status = self.get_contr_status(["dlbif", "parkif"])
        else:
            contr_status = self.get_contr_status(["lbdif"])

        if contr_status:
            return contr_status

        if self._create_nacclbde() == 0:
            return 7

        # return self.__uds.check_default("nacclbdp", None)
        # TODO: raising error instead of returning None
        # I think in theory it seems it shouldn't ever get here
        # and nacclbdp should always be set to something
        # (maybe use 7 as a default otherwise)
        raise ValueError("Unable to determine nacclbdp")

    def _create_naccudsd(self) -> int:
        """From Create NACCUDSD.R which in turn is from derive.sas.

        Cognitive status at UDS visit
        """
        if self._create_mci() == 1:
            return 3
        if self.__uds.get_value("demented") == 1:
            return 4
        if self.__uds.get_value("normcog") == 1:
            return 1
        if self.__uds.get_value("impnomci") == 1:
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

        if self.__uds.get_value("normcog") == 1:
            return 88

        # assuming normcog == 0 != 1 after this point
        # get all statuses in a list, then return the first one that == 1 (Primary)
        # result maps to position in list (start index 1)
        all_status = [
            self.get_contr_status(["probadif", "possadif", "alzdisif"]),
            self.get_contr_status(["dlbif", "parkif"])
            if self.__uds.normalized_formver() != 3
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
        ppaph = self.__uds.get_value("ppaph")
        ppasyn = self.__uds.get_value("ppasyn")

        if self.__uds.get_value("demented") == 1:
            if ppaph == 1 or ppasyn == 1:
                return 1
            if ppaph == 0 or ppasyn == 0:
                return 0

        elif self.__uds.get_value("impnomci") == 1 or self._create_mci() == 1:
            if ppaph == 1 or ppasyn == 1:
                return 1
            if ppaph == 0 or ppasyn == 0:
                return 0

            formver = self.__uds.normalized_formver()
            nodx = self.__uds.get_value("nodx")
            if (formver != 3 and nodx == 1) or (formver == 3):
                return 7

        return 8

    def _create_naccbvft(self) -> int:
        """From d1structdd.sas.

        Dementia syndrome -- behavioral variant FTD syndrome (bvFTD)
        """
        if self.__uds.get_value("demented") != 1:
            return 8

        # assuming demented == 1 after this point
        ftd = self.__uds.get_value("ftd")
        ftdsyn = self.__uds.get_value("ftdsyn")

        if ftd in [0, 1]:
            return ftd
        if ftdsyn in [0, 1]:
            return ftdsyn

        # return self.__uds.check_default("naccbvft", 8)
        return 8

    def _create_nacclbds(self) -> int:
        """From d1structdd.sas.

        Dementia syndrome -- Lewy body dementia syndrome
        """
        if self.__uds.get_value("demented") != 1:
            return 8

        # assuming demented == 1 after this point
        dlb = self.__uds.get_value("dlb")
        lbdsyn = self.__uds.get_value("lbdsyn")

        if dlb in [0, 1]:
            return dlb
        if lbdsyn in [0, 1]:
            return lbdsyn

        return 8

    def _create_naccnorm(self) -> int:
        """Comes from derive.sas and derivenew.sas (same code)

        Normal cognition at all visits to date
        """
        naccnorm = self.__subject_derived.get_cross_sectional_value("naccnorm")

        try:
            if naccnorm is not None and int(naccnorm) == 0:
                return 0

            return int(self.__uds.get_value("normcog"))
        except (ValueError, TypeError):
            pass

        return 1
