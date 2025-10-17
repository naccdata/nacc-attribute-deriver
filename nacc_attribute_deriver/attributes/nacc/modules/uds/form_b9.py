# ruff: noqa: SIM114
"""For now ignore SIM114 which is complaining about the complicated if/else
branches derived from SAS. Eventually want to clean up.

Derived variables from form B9: Clinician Judgement of Symptoms.

Form B9 is required and expected to have been filled out.

There is a lot of carrying over of previous values and recoding in the original
SAS, resulting in pretty confusing logic, which may not be super clear here
either.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_attribute import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormB9Attribute(UDSAttributeCollection):
    """Class to collect UDS B9 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__working = WorkingDerivedNamespace(table=table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

        # if b9chg == 1 was selected in version 1.2 of UDS (no meaningful changes),
        # indicates NACC has brought forward data from previous visit
        self.__b9_changes = self.uds.get_value("b9chg", int) in [1, 3]
        self.__decclin = self.uds.get_value("decclin", int)

    def harmonize_befrst(self) -> Optional[int]:
        """Updates BEFRST for NACCBEHF harmonization.

        Returns     updated value for BEFRST
        """
        befrst = self.uds.get_value("befrst", int)

        if self.formver < 3:
            if befrst == 8:
                return 10
            if self.formver == 2 and befrst == 9:
                return 8

        return befrst

    def _create_naccbehf(self) -> int:  # noqa: C901
        """Create NACCBEHF, indicate the predominant symptom that was first
        recognized as a decline in the subject's behavior.

        Depends on previous vars (p_decclin, p_befrst, p_befpred)

        TODO: RDD lists this as cross-sectional, but it seems more like
        its longitudinal with carryover from previous forms (e.g. not
        the same for every visit.)
        """
        befrst = self.harmonize_befrst()
        befpred = self.uds.get_value("befpred", int)  # v3+
        naccbehf = befpred if befpred is not None else befrst

        """
        None can mean one of the following:
            1. For all versions, this may indicate a gate variable (e.g.
                DECCLIN in V2 and earlier or DECCLBE in V3+) was 0
                for no decline in subject behavior. If so, we return 0 (no decline)
                In general this means we always return 0 in V3, since otherwise
                they should explicitly set befpred to 0 to grab previous value
            2. For V2 and earlier, if the gate variable is none or 1, then
                that means we need to grab the value from the previous form,
                so we do not return early (continue function)
        """
        if naccbehf is None:
            if self.formver >= 3:
                return 0
            elif self.__decclin == 0:
                return 0

        p_decclin = self.__working.get_prev_value("decclin", int)
        p_befrst = self.__working.get_prev_value("befrst", int)

        if befrst == 88 or (self.__b9_changes and p_decclin == 0):
            naccbehf = 0
        elif self.__b9_changes and p_decclin == 1:
            if p_befrst == 88:
                naccbehf = 0
            elif p_befrst is not None:
                naccbehf = p_befrst

        if self.formver >= 3:
            if befpred == 0:
                p_befpred = self.__working.get_prev_value("befpred", int)
                if p_befpred is not None and p_befpred != 0:
                    naccbehf = p_befpred
                elif p_befpred == 0:
                    naccbehf = 99

            if naccbehf == 88:
                naccbehf = 0

        return naccbehf if naccbehf is not None else 99

    def _create_naccbefx(self) -> Optional[str]:
        """Create NACCBEFX, specification of other predominant symptom that was
        first recognized as a decline in the subject's behavior.

        TODO: RDD lists this as cross-sectional, but it seems more like
        its longitudinal,
        """
        if self._create_naccbehf() != 10:
            return None

        if self.formver < 3:
            return self.uds.get_value("befrstx", str)

        return self.uds.get_value("befpredx", str)

    def _create_nacccgfx(self) -> Optional[str]:
        """Creates NACCCGFX, specification for other predominant symptom first
        recognized as a decline in the subject's cognition.

        TODO: RDD lists this as cross-sectional, but it seems more like
        its longitudinal.
        """
        cogfprex = self.uds.get_value("cogfprex", str)
        cogfrstx = self.uds.get_value("cogfrstx", str)

        return cogfprex if cogfprex is not None else cogfrstx

    def harmonize_cogfrst(self) -> Optional[int]:
        """Updates COGFRST for NACCCOGF harmonization.

        Returns     updated value for COGFRST
        """
        cogfrst = self.uds.get_value("cogfrst", int)

        if self.formver < 3:
            if cogfrst is not None and cogfrst > 1 and cogfrst < 6:
                return cogfrst + 1
            elif cogfrst == 6:
                return 8

        return cogfrst

    def _create_nacccogf(self) -> int:  # noqa: C901
        """Creates NACCCOGF, Indicate the predominant symptom that was first
        recognized as a decline in the subject's cognition.

        TODO: RDD lists this as cross-sectional, but it seems more like
        its longitudinal with carryover from previous forms (e.g. not
        the same for every visit.)
        """
        cogfrst = self.harmonize_cogfrst()
        cogfpred = self.uds.get_value("cogfpred", int)
        p_decclin = self.__working.get_prev_value("decclin", int)
        p_cogfrst = self.__working.get_prev_value("cogfrst", int)
        p_cogfpred = self.__working.get_prev_value("cogfpred", int)
        nacccogf = None

        # see note in _create_naccbehf; same situation
        if cogfrst is None and cogfpred is None:
            if self.formver >= 3:
                return 0
            elif self.__decclin == 0:
                return 0

        # V2 and earlier
        if cogfrst == 88 or (self.__b9_changes and p_decclin == 0):
            nacccogf = 0
        elif self.__b9_changes and p_decclin == 1 and p_cogfrst == 88:
            nacccogf = 0
        elif self.__b9_changes and p_decclin == 1 and p_cogfrst is not None:
            nacccogf = p_cogfrst
        elif cogfrst is not None and cogfrst > 0 and cogfrst < 9:
            nacccogf = cogfrst

        # V3+
        elif cogfpred is not None and cogfpred > 0 and cogfpred < 9:
            nacccogf = cogfpred
        elif cogfpred == 0 and p_cogfpred is not None and p_cogfpred != 0:
            nacccogf = p_cogfpred
        else:
            nacccogf = 99

        if self.formver >= 3 and nacccogf == 88:
            nacccogf = 0

        return nacccogf if nacccogf is not None else 99

    def _create_naccmotf(self) -> int:
        """Creates NACCMOTF, Indicate the predominant symptom that was first
        recognized as a decline in the subject's motor function."""
        mofrst = self.uds.get_value("mofrst", int)

        # see note in _create_naccbehf; same situation
        if mofrst is None:
            if self.formver >= 3:
                return 0
            elif self.__decclin == 0:
                return 0

        naccmotf = None
        p_decclin = self.__working.get_prev_value("decclin", int)
        p_mofrst = self.__working.get_prev_value("mofrst", int)

        if mofrst and mofrst not in [0, 88]:
            naccmotf = mofrst
        elif mofrst == 88 or (self.__b9_changes and p_decclin == 0):
            naccmotf = 0
        elif self.__b9_changes and p_decclin == 1 and p_mofrst == 88:
            naccmotf = 0
        elif self.__b9_changes and p_decclin == 1 and p_mofrst is not None:
            naccmotf = p_mofrst

        elif self.formver >= 3 and mofrst == 0:
            naccmotf = p_mofrst

        if self.formver >= 3 and naccmotf == 88:
            naccmotf = 0

        return naccmotf if naccmotf is not None else 99

    #######################################################################
    # Carryover form variables - needed for above curation
    # These should be curated AFTER the above
    # We do check dates though so it shouldn't matter too much
    #######################################################################

    def determine_carryover(self, attribute: str) -> Optional[int]:
        """In many followup visits, 0 == assessed at previous visit.

        Need to pull in that case.
        """
        raw_value = self.uds.get_value(attribute, int)

        # see note in _create_naccbehf; same situation
        if not self.uds.is_initial():  # noqa: SIM102
            if raw_value == 0 or (
                raw_value is None and self.formver < 3 and self.__decclin is None
            ):
                prev_value = self.__working.get_prev_value(attribute, int)
                if prev_value is not None:
                    return prev_value

        return raw_value

    def _create_mofrst(self) -> Optional[int]:
        """Carries over MOFRST (V3+ and V1, V2)."""
        return self.determine_carryover("mofrst")

    def _create_befpred(self) -> Optional[int]:
        """Carries over BEFPRED (V3+)."""
        return self.determine_carryover("befpred")

    def _create_cogfpred(self) -> Optional[int]:
        """Carries over COGFPRED (V3+)."""
        return self.determine_carryover("cogfpred")

    def _create_decclin(self) -> Optional[int]:
        """Carries over DECCLIN (V1, V2)."""
        return self.determine_carryover("decclin")

    def _create_befrst(self) -> Optional[int]:
        """Carries over BEFRST (V1, V2)."""
        return self.determine_carryover("befrst")

    def _create_cogfrst(self) -> Optional[int]:
        """Carries over COGFRST (V1, V2)."""
        return self.determine_carryover("cogfrst")

    ###############################################################
    # Tracked form variables - needed for missingness
    # Curation order does not matter for these, just keeping track
    # of what they are at each visit
    ###############################################################

    def _create_behage(self) -> Optional[int]:
        """Keeps track of BEHAGE."""
        return self.uds.get_value("behage", int)

    def _create_psychage(self) -> Optional[int]:
        """Keeps track of PSYCHAGE."""
        return self.uds.get_value("psychage", int)

    def _create_perchage(self) -> Optional[int]:
        """Keeps track of PERCHAGE."""
        return self.uds.get_value("perchage", int)

    def _create_beremago(self) -> Optional[int]:
        """Keeps track of BEREMAGO."""
        return self.uds.get_value("beremago", int)

    def _create_motorage(self) -> Optional[int]:
        """Keeps track of MOTORAGE."""
        return self.uds.get_value("motorage", int)

    def _create_frstchg(self) -> Optional[int]:
        """Keeps track of FRSTCHG."""
        return self.uds.get_value("frstchg", int)
