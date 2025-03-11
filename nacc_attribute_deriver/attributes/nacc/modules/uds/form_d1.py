"""Derived variables from form D1."""
from typing import List, Optional

from .uds_attribute import UDSAttribute


class ContributionStatus:
    PRIMARY = 1
    CONTRIBUTING = 2
    NON_CONTRIBUTING = 3

    @classmethod
    def all(cls):
        """Returns all possible statuses."""
        return [cls.PRIMARY, cls.CONTRIBUTING, cls.NON_CONTRIBUTING]


class UDSFormD1Attribute(UDSAttribute):

    def get_contr_status(self, fields: List[str]) -> Optional[int]:
        """Gets the overall contributing status based on the given list.
        Assumes all fields have values null or 1, 2, or 3 (primary,
        contributing, or non-contributing)

        Args:
            table: Table with all FW metadata
            fields: Fields to get overall status from
        Returns:
            The overall contributed status, None if none satisfy
        """
        all_statuses = []

        for field in fields:
            all_statuses.append(self.get_value(field))

        for i in ContributionStatus.all():
            if any([x == i for x in all_statuses]):
                return i

        return None

    def _create_mci(self) -> int:
        """Create MCI, which is not a derived variable itself but is used to
        calculate other derived variables.

        Location:
            tmp.mci
        Operation:
            update
        Type:
            intermediate
        Description:
            Mild cognitive impairment
        """

        # all of these fields are null, 0, or 1
        return 1 if any([
            self.get_value('mciamem'),
            self.get_value('mciaplus'),
            self.get_value('mcinon1'),
            self.get_value('mcinon2')
        ]) else 0

    def _create_naccalzp(self) -> int:
        """From d1structrdd.sas.

        Location:
            file.info.derived.naccalzp
        Operation:
            update
        Type:
            longitudinal
        Description:
            Primary, contributing, or non-contributing cause of observed
            cognitive impairment -- Alzheimer's disease (AD)
        """
        if self.get_value('normcog') == 1:
            return 8

        contr_status = self.get_contr_status(
            ['probadif', 'possadif', 'alzdisif'])
        if contr_status:
            return contr_status

        # default
        return 7

    def _create_nacclbde(self) -> Optional[int]:
        """From d1structrdd.sas.

        Location:
            file.info.derived.nacclbde
        Operation:
            update
        Type:
            longitudinal
        Description:
            Presumptive etilogic diagnosis of the cognitive disorder
            - Lewy body disease (LBD)
        """
        if self.get_value('normcog') == 1:
            return 8

        if self.get_value('formver') != 3:
            dlb = self.get_value('dlb')
            park = self.get_value('park')

            if dlb == 1 or park == 1:
                return 1
            if dlb == 0 and park == 0:
                return 0

        lbdis = self.get_value('lbdis')
        if lbdis in [0, 1]:
            return lbdis

        return None

    def _create_nacclbdp(self) -> Optional[int]:
        """From d1structrdd.sas. Also relies on another derived variable
        nacclbde.

        Location:
            file.info.derived.nacclbdp
        Operation:
            update
        Type:
            longitudinal
        Description:
            Primary, contributing, or non-contributing cause of
            cognitive impairment -- Lewy body disease (LBD)
        """
        if self.get_value('normcog') == 1:
            return 8

        if self.get_value('formver') != 3:
            contr_status = self.get_contr_status(['dlbif', 'parkif'])
            if contr_status:
                return contr_status

        contr_status = self.get_contr_status(['lbdif'])
        if contr_status:
            return contr_status

        if self._create_nacclbde() == 0:
            return 7

        return None

    def _create_naccudsd(self) -> Optional[int]:
        """From Create NACCUDSD.R which in turn is from derive.sas.

        Location:
            file.info.derived.naccudsd
        Operation:
            update
        Type:
            longitudinal
        Description:
            Cognitive status at UDS visit
        """
        if self._create_mci() == 1:
            return 3
        if self.get_value('demented') == 1:
            return 4
        if self.get_value('normcog') == 1:
            return 1
        if self.get_value('impnomci') == 1:
            return 2

        return None

    def _create_naccetpr(self) -> int:
        """From Create NACCETPR, PRIMDX, SYNMULT.R which in turn comes from
        getd1all.sas.

        Looking for primary status here.

        Location:
            file.info.derived.naccetpr
        Operation:
            update
        Type:
            longitudinal
        Description:
            Primary etiologic diagnosis (MCI), impaired,
            not MCI, or dementia
        """

        if self.get_value('normcog') == 1:
            return 88

        # assuming normcog == 0 != 1 after this point
        # get all statuses in a list, then return the first one that == 1 (Primary)
        # result maps to position in list (start index 1)
        all_status = [
            self.get_contr_status(['probadif', 'possadif', 'alzdisif']),
            self.get_contr_status(['dlbif', 'parkif'])
            if self.get_value('formver') != 3 else self.get_contr_status(
                ['lbdif']),

            # could just grab directly for those with only 1 but this is more readable
            self.get_contr_status(['msaif']),
            self.get_contr_status(['pspif']),
            self.get_contr_status(['cortif']),
            self.get_contr_status(['ftldmoif']),
            self.get_contr_status(['ftdif', 'ppaphif', 'ftldnoif']),
            self.get_contr_status(['cvdif', 'vascif', 'vascpsif', 'strokif']),
            self.get_contr_status(['esstreif']),
            self.get_contr_status(['downsif']),
            self.get_contr_status(['huntif']),
            self.get_contr_status(['prionif']),
            self.get_contr_status(['brninjif']),
            self.get_contr_status(['hycephif']),
            self.get_contr_status(['epilepif']),
            self.get_contr_status(['neopif']),
            self.get_contr_status(['hivif']),
            self.get_contr_status(['othcogif']),
            self.get_contr_status(['depif']),
            self.get_contr_status(['bipoldif']),
            self.get_contr_status(['schizoif']),
            self.get_contr_status(['anxietif']),
            self.get_contr_status(['delirif']),
            self.get_contr_status(['ptsddxif']),
            self.get_contr_status(['othpsyif']),
            self.get_contr_status(['alcdemif']),
            self.get_contr_status(['impsubif']),
            self.get_contr_status(['dysillif']),
            self.get_contr_status(['medsif']),
            self.get_contr_status(['cogothif', 'cogoth2f', 'cogoth3f']),
        ]

        assert len(all_status) == 30
        for i, status in enumerate(all_status):
            if status and self.is_int_value(status,
                                            ContributionStatus.PRIMARY):
                return i + 1

        # default for normcog == 0
        return 99

    def _create_naccppa(self) -> int:
        """From d1structdd.sas.

        Location:
            file.info.derived.naccppa
        Operation:
            update
        Type:
            longitudinal
        Description:
            Primary progressive aphasia (PPA) with
            cognitive impairment
        """
        ppaph = self.get_value('ppaph')
        ppasyn = self.get_value('ppasyn')

        if self.get_value('demented') == 1:
            if ppaph == 1 or ppasyn == 1:
                return 1
            if ppaph == 0 or ppasyn == 0:
                return 0

        nodx = self.get_value('nodx')

        if self.get_value('impnomci') == 1 or self._create_mci() == 1:
            if ppaph == 1 or ppasyn == 1:
                return 1
            if ppaph == 0 or ppasyn == 0:
                return 0
            if (self.get_value('formver') != 3
                    and nodx == 1) or (self.get_value('formver') == 3):
                return 7

        return 8

    def _create_naccbvft(self) -> int:
        """From d1structdd.sas.

        Location:
            file.info.derived.naccbvft
        Operation:
            update
        Type:
            longitudinal
        Description:
            Dementia syndrome -- behavioral variant
            FTD syndrome (bvFTD)
        """
        if self.get_value('demented') != 1:
            return 8

        # assuming demented == 1 after this point
        ftd = self.get_value('ftd')
        ftdsyn = self.get_value('ftdsyn')

        if ftd in [0, 1]:
            return ftd
        if ftdsyn in [0, 1]:
            return ftdsyn

        return 8

    def _create_nacclbds(self) -> int:
        """From d1structdd.sas.

        Location:
            file.info.derived.nacclbds
        Operation:
            update
        Type:
            longitudinal
        Description:
            Dementia syndrome -- Lewy body dementia syndrome
        """
        if self.get_value('demented') != 1:
            return 8

        # assuming demented == 1 after this point
        dlb = self.get_value('dlb')
        lbdsyn = self.get_value('lbdsyn')

        if dlb in [0, 1]:
            return dlb
        if lbdsyn in [0, 1]:
            return lbdsyn

        return 8

    def _create_naccnorm(self) -> int:
        """Comes from derive.sas and derivenew.sas (same code)

        This one is a static variable that needs to know if
        subject.info.derived.naccnorm exists.

        Location:
            file.info.derived.naccnorm
        Operation:
            update
        Type:
            cross-sectional
        Description:
            Normal cognition at all visits to date
        """
        naccnorm = self.table.get('subject.info.derived.naccnorm')
        if naccnorm == 0:
            return naccnorm

        return self.get_value('normcog')
