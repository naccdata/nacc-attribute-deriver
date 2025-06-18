"""Derived variables from form B9: Clinician Judgement of Symptoms.

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

    def grab_prev(self, field: str) -> Optional[int]:
        """Grabs the previous recorded field - assumes longitudinal integer
        field.

        Args:
            field: The field to grab the previous longitudinal records for
        """
        prev_records = self.__subject_derived.get_longitudinal_value(field, int)
        return prev_records[-1] if prev_records else None

    def _create_naccbehf(self) -> int:
        """Create NACCBEHF, indicate the predominant symptom that was
        first recognized as a decline in the subject's behavior

        the p-vars (p_decclin, p_befrst, p_befpred)
        """
        befrst = self.__uds.get_value('befrst', int)    # v1, v2
        befpred = self.__uds.get_value('befpred', int)  # v3+
        naccbehf = befpred if befpred is not None else befrst

        b9chg = self.__uds.get_value('b9chg')  # when == 1 means no meaningful changes
        p_decclin = self.grab_prev('decclin')
        p_befrst = self.grab_prev('befrst')

        if befrst == 88 or (b9chg in [1, 3] and p_decclin == 0):
            naccbehf = 0
        elif b9chg in [1, 3] and p_decclin == 1:
            if p_befrst == 88:
                naccbehf = 0
            if p_befrst != None:
                naccbehf = p_befrst

        if self.__formver >= 3:
            p_befpred = self.grab_prev('befpred')
            if befpred == 0:
                if p_befpred is not None and p_befpred != 0:
                    naccbehf = p_befpred
                elif p_befpred == 0:
                    naccbehf = 99

        return naccbehf

    def _create_naccbefx(self) -> Optional[str]:
        """Create NACCBEFX, specification of other predominant symptom
        that was first recognized as a decline in the subject's behavior.
        """
        if self._create_naccbehf() != 10:
            return None

        if self.__formver < 3:
            return self.__uds.get_value('befrstx', str)

        return self.__uds.get_value('befpredx', str)

    ############################
    # Carryover form variables #
    ############################

    def _create_decclin(self) -> Optional[int]:
        """Carries over DECCLIN (V1, V2)."""
        return self.__uds.get_value('decclin', int)

    def _create_befrst(self) -> Optional[int]:
        """Carries over BEFRST (V1, V2)."""
        return self.__uds.get_value('befrst', int)

    def _create_befpred(self) -> Optional[int]:
        """Carries over BEFPRED (V3+)."""
        return self.__uds.get_value('befpred', int)
