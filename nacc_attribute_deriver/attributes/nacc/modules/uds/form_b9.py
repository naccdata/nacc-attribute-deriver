# ruff: noqa: SIM114
"""For now ignore SIM114 which is complaining about the complicated if/else
branches derived from SAS. Eventually want to clean up.

Derived variables from form B9: Clinician Judgement of Symptoms.

Form B9 is required and expected to have been filled out.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormB9Attribute(AttributeCollection):
    """Class to collect UDS B9 attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)
        self.__formver = self.__uds.normalized_formver()
        self.__subject_derived = SubjectDerivedNamespace(table=table)

        # if b9chg == 1 was selected in version 1.2 of UDS (no meaningful changes),
        # indicates NACC has brought forward data from previous visit
        self.__b9_changes = self.__uds.get_value("b9chg", int) in [1, 3]

    def grab_prev(self, field: str) -> Optional[int]:
        """Grabs the previous recorded field - assumes longitudinal integer
        field.

        Args:
            field: The field to grab the previous longitudinal records for
        """
        prev_records = self.__subject_derived.get_longitudinal_value(field, int)
        return prev_records[-1] if prev_records else None

    def _create_naccbehf(self) -> int:
        """Create NACCBEHF, indicate the predominant symptom that was first
        recognized as a decline in the subject's behavior.

        the p-vars (p_decclin, p_befrst, p_befpred)
        """
        befrst = self.__uds.get_value("befrst", int)  # v1, v2
        befpred = self.__uds.get_value("befpred", int)  # v3+
        naccbehf = befpred if befpred is not None else befrst

        p_decclin = self.grab_prev("decclin")
        p_befrst = self.grab_prev("befrst")

        if befrst == 88 or (self.__b9_changes and p_decclin == 0):
            naccbehf = 0
        elif self.__b9_changes and p_decclin == 1:
            if p_befrst == 88:
                naccbehf = 0
            if p_befrst is not None:
                naccbehf = p_befrst

        if self.__formver >= 3:
            p_befpred = self.grab_prev("befpred")
            if befpred == 0:
                if p_befpred is not None and p_befpred != 0:
                    naccbehf = p_befpred
                elif p_befpred == 0:
                    naccbehf = 99

        return naccbehf if naccbehf is not None else 99

    def _create_naccbefx(self) -> Optional[str]:
        """Create NACCBEFX, specification of other predominant symptom that was
        first recognized as a decline in the subject's behavior."""
        if self._create_naccbehf() != 10:
            return None

        if self.__formver < 3:
            return self.__uds.get_value("befrstx", str)

        return self.__uds.get_value("befpredx", str)

    def _create_nacccgfx(self) -> Optional[str]:
        """Creates NACCCGFX, specification for other predominant symptom first
        recognized as a decline in the subject's cognition."""
        cogfprex = self.__uds.get_value("cogfprex", str)
        cogfrstx = self.__uds.get_value("cogfrstx", str)

        return cogfprex if cogfprex is not None else cogfrstx

    def _create_nacccogf(self) -> int:
        """Creates NACCCOGF, Indicate the predominant symptom that was first
        recognized as a decline in the subject's cognition."""
        cogfrst = self.__uds.get_value("cogfrst", int)
        cogfpred = self.__uds.get_value("cogfpred", int)
        p_decclin = self.grab_prev("decclin")
        p_cogfrst = self.grab_prev("cogfrst")
        p_cogfpred = self.grab_prev("cogfpred")

        nacccogf = 99

        if cogfrst == 88 or (self.__b9_changes and p_decclin == 0):
            nacccogf = 0
        elif cogfrst == 88 or (
            self.__b9_changes and p_decclin == 1 and p_cogfrst == 88
        ):
            nacccogf = 0
        elif self.__b9_changes and p_decclin == 1 and p_cogfrst is not None:
            nacccogf = p_cogfrst
        elif cogfrst is not None and cogfrst > 0 and cogfrst < 9:
            nacccogf = cogfrst
        elif cogfpred and cogfpred > 0 and cogfpred < 9:
            nacccogf = cogfpred
        elif cogfpred == 0 and p_cogfpred is not None:
            nacccogf = p_cogfpred

        if self.__formver >= 3 and nacccogf == 88:
            nacccogf = 0

        return nacccogf if nacccogf is not None else 99

    def _create_naccmotf(self) -> int:
        """Creates NACCMOTF, Indicate the predominant symptom that was first
        recognized as a decline in the subject's motor function."""
        mofrst = self.__uds.get_value("mofrst", int)
        naccmotf = mofrst if mofrst and mofrst not in [0, 88] else None

        p_decclin = self.grab_prev("decclin")
        p_mofrst = self.grab_prev("mofrst")

        if mofrst == 88 or (self.__b9_changes and p_decclin == 0 and naccmotf is None):
            naccmotf = 0
        elif (
            self.__b9_changes and p_decclin == 1 and p_mofrst == 88 and naccmotf is None
        ):
            naccmotf = 0
        elif self.__b9_changes and p_decclin == 1 and p_mofrst is not None:
            naccmotf = p_mofrst

        # SAS code had rmofrst - likely typo?
        elif self.__formver >= 3 and p_mofrst == 0 and naccmotf is None:
            naccmotf = p_mofrst

        if self.__formver >= 3 and naccmotf == 88:
            naccmotf = 0

        return naccmotf if naccmotf is not None else 99

    #########################################
    # Carryover form variables              #
    # These must be curated AFTER the above #
    #########################################

    def _create_decclin(self) -> Optional[int]:
        """Carries over DECCLIN (V1, V2)."""
        return self.__uds.get_value("decclin", int)

    def _create_befrst(self) -> Optional[int]:
        """Carries over BEFRST (V1, V2)."""
        return self.__uds.get_value("befrst", int)

    def _create_cogfrst(self) -> Optional[int]:
        """Carries over COGFRST (V1, V2)."""
        return self.__uds.get_value("cogfrst", int)

    def _create_mofrst(self) -> Optional[int]:
        """Carries over MOFRST (V1, V2)."""
        return self.__uds.get_value("mofrst", int)

    def _create_befpred(self) -> Optional[int]:
        """Carries over BEFPRED (V3+)."""
        return self.__uds.get_value("befpred", int)

    def _create_cogfpred(self) -> Optional[int]:
        """Carries over COGFPRED (V3+)."""
        return self.__uds.get_value("cogfpred", int)
