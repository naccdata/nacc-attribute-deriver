# ruff: noqa: SIM114
"""For now ignore SIM114 which is complaining about the complicated if/else
branches derived from SAS. Eventually want to clean up.

Derived variables from form B9: Clinician Judgement of Symptoms.

Form B9 is required and expected to have been filled out.
"""

from typing import Optional, Union

from pydantic import ValidationError

from nacc_attribute_deriver.attributes.base.namespace import (
    SubjectDerivedNamespace,
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.schema.rule_types import DateTaggedValue
from nacc_attribute_deriver.symbol_table import SymbolTable

from .uds_attribute_collection import UDSAttributeCollection


class UDSFormB9Attribute(UDSAttributeCollection):
    """Class to collect UDS B9 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__working_derived = WorkingDerivedNamespace(table=table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

        # if b9chg == 1 was selected in version 1.2 of UDS (no meaningful changes),
        # indicates NACC has brought forward data from previous visit
        self.__b9_changes = self.uds.get_value("b9chg", int) in [1, 3]

    def harmonize_befrst(self) -> int:
        """Updates BEFRST for NACCBEHF harmonization.

        Returns
            updated value for BEFRST
        """
        befrst = self.uds.get_value("befrst", int)

        if self.formver < 3:
            if befrst == 8:
                return 10
            if self.formver == 2 and befrst == 9:
                return 8

        return befrst if befrst is not None else 88

    def _create_naccbehf(self) -> int:
        """Create NACCBEHF, indicate the predominant symptom that was first
        recognized as a decline in the subject's behavior.

        Depends on previous vars (p_decclin, p_befrst, p_befpred)

        TODO: RDD lists this as cross-sectional, but it seems more like
        its longitudinal with carryover from previous forms (e.g. not
        the same for every visit.)
        """
        befrst = self.harmonize_befrst()
        befpred = self.uds.get_value("befpred", int)  # v3+
        naccbehf = self.__subject_derived.get_prev_value('naccbehf', int)

        if naccbehf is None:
            naccbehf = befpred if befpred is not None else befrst

        p_decclin = self.__working_derived.get_cross_sectional_dated_value("decclin", int)
        p_befrst = self.__working_derived.get_cross_sectional_dated_value("befrst", int)

        if befrst == 88 or (self.__b9_changes and p_decclin == 0):
            naccbehf = 0
        elif self.__b9_changes and p_decclin == 1:
            if p_befrst == 88:
                naccbehf = 0
            if p_befrst is not None:
                naccbehf = p_befrst

        if self.formver >= 3:
            if befpred == 0:
                p_befpred = self.__working_derived.get_cross_sectional_dated_value("befpred", int)
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

    def harmonize_cogfrst(self) -> int:
        """Updates COGFRST for NACCCOGF harmonization.

        Returns
            updated value for COGFRST
        """
        cogfrst = self.uds.get_value("cogfrst", int)

        if self.formver < 3:
            if cogfrst is not None and cogfrst > 1 and cogfrst < 6:
                return cogfrst + 1
            elif cogfrst == 6:
                return 8

        return cogfrst if cogfrst is not None else 88

    def _create_nacccogf(self) -> int:
        """Creates NACCCOGF, Indicate the predominant symptom that was first
        recognized as a decline in the subject's cognition.

        TODO: RDD lists this as cross-sectional, but it seems more like
        its longitudinal with carryover from previous forms (e.g. not
        the same for every visit.)
        """
        cogfrst = self.harmonize_cogfrst()
        cogfpred = self.uds.get_value("cogfpred", int)
        p_decclin = self.__working_derived.get_cross_sectional_dated_value("decclin", int)
        p_cogfrst = self.__working_derived.get_cross_sectional_dated_value("cogfrst", int)
        p_cogfpred = self.__working_derived.get_cross_sectional_dated_value("cogfpred", int)

        nacccogf = self.__subject_derived.get_prev_value('nacccogf', int)

        if nacccogf is None:
            if cogfrst == 88 or (self.__b9_changes and p_decclin == 0):
                nacccogf = 0
            elif cogfrst == 88 or (
                self.__b9_changes and p_decclin == 1 and p_cogfrst == 88
            ):
                nacccogf = 0
            elif self.__b9_changes and p_decclin == 1 and p_cogfrst is not None:
                nacccogf = p_cogfrst
            elif cogfrst > 0 and cogfrst < 9:
                nacccogf = cogfrst
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
        naccmotf = self.__subject_derived.get_prev_value('naccmotf', int)
        if mofrst not in [0, 88] and naccmotf is None:
            naccmotf = mofrst

        p_decclin = self.__working_derived.get_cross_sectional_dated_value("decclin", int)
        p_mofrst = self.__working_derived.get_cross_sectional_dated_value("mofrst", int)
        r_mofrst = self.__working_derived.get_prev_record("mofrst", int)

        if naccmotf is None:
            if mofrst == 88 or (self.__b9_changes and p_decclin == 0):
                naccmotf = 0
            elif self.__b9_changes and p_decclin == 1 and p_mofrst == 88:
                naccmotf = 0
            elif self.formver >= 3 and r_mofrst == 0 and naccmotf is None:
                naccmotf = p_mofrst

        elif self.__b9_changes and p_decclin == 1 and p_mofrst is not None:
            naccmotf = p_mofrst

        if self.formver >= 3 and naccmotf == 88:
            naccmotf = 0

        return naccmotf if naccmotf is not None else 99

    #########################################
    # Carryover form variables
    # These must be curated AFTER the above
    # Most only care about the initial (set in curation rules as cross-sectional.initial),
    # except MOFRST which also needs the most recent (so also has rule for longitudinal)
    #########################################

    def _create_decclin(self) -> Optional[int]:
        """Carries over DECCLIN (V1, V2)."""
        return self.uds.get_value("decclin", int)

    def _create_befrst(self) -> Optional[int]:
        """Carries over BEFRST (V1, V2)."""
        return self.uds.get_value("befrst", int)

    def _create_cogfrst(self) -> Optional[int]:
        """Carries over COGFRST (V1, V2)."""
        return self.uds.get_value("cogfrst", int)

    def _create_mofrst(self) -> Optional[int]:
        """Carries over MOFRST (V1, V2)."""
        return self.uds.get_value("mofrst", int)

    def _create_befpred(self) -> Optional[int]:
        """Carries over BEFPRED (V3+)."""
        return self.uds.get_value("befpred", int)

    def _create_cogfpred(self) -> Optional[int]:
        """Carries over COGFPRED (V3+)."""
        return self.uds.get_value("cogfpred", int)
