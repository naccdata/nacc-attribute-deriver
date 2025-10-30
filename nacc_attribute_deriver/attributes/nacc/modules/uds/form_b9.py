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
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.schema.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormB9Attribute(UDSAttributeCollection):
    """Class to collect UDS B9 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)
        self.__prev_record = None

        if not self.uds.is_initial():
            self.__prev_record = PreviousRecordNamespace(table=table)

        # if b9chg == 1 was selected in version 1.2 of UDS (no meaningful changes),
        # indicates NACC has brought forward data from previous visit
        self.__b9_changes = self.uds.get_value("b9chg", int) in [1, 3]
        self.__decclin = self.uds.get_value("decclin", int)

    def harmonize_befrst(self) -> Optional[int]:
        """Updates BEFRST for NACCBEHF harmonization.

        Returns updated value for BEFRST
        """
        befrst = self.uds.get_value("befrst", int)

        if self.formver < 3:
            if befrst == 8:
                return 10
            if self.formver == 2 and befrst == 9:
                return 8

        return befrst

    def _create_nacccogage(self) -> int:
        """Creates NACCCOGAGE - Age that participant's cognitive impairment began."""
        target_var = "decage" if self.formver < 4 else "cogage"

        value = self.uds.get_value(target_var, int)
        if value == 777 and self.__prev_record:
            value = self.__prev_record.get_resolved_value(target_var, int)

        if value is None:
            return INFORMED_MISSINGNESS

        return value

    def _create_naccbehf(self) -> int:  # noqa: C901
        """Create NACCBEHF, indicate the predominant symptom that was first
        recognized as a decline in the subject's behavior.

        Depends on previous vars (p_decclin, p_befrst, p_befpred)

        TODO: RDD lists this as cross-sectional, but it seems more like
        its longitudinal with carryover from previous forms (e.g. not
        the same for every visit.)
        """
        # not defined in V4
        if self.formver == 4:
            return INFORMED_MISSINGNESS

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

        p_decclin = None
        p_befrst = None
        p_befpred = None

        if self.__prev_record:
            p_decclin = self.__prev_record.get_resolved_value("decclin", int)
            p_befrst = self.__prev_record.get_resolved_value("befrst", int)
            p_befpred = self.__prev_record.get_resolved_value(
                "befpred", int, prev_code=0 if self.formver == 3 else None
            )

        if befrst == 88 or (self.__b9_changes and p_decclin == 0):
            naccbehf = 0
        elif self.__b9_changes and p_decclin == 1:
            if p_befrst == 88:
                naccbehf = 0
            elif p_befrst is not None:
                naccbehf = p_befrst

        if self.formver >= 3:
            if befpred == 0:
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
        # not defined in V4
        if self.formver == 4:
            return INFORMED_BLANK

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
        # not defined in V4
        if self.formver == 4:
            return INFORMED_BLANK

        cogfprex = self.uds.get_value("cogfprex", str)
        cogfrstx = self.uds.get_value("cogfrstx", str)

        return cogfprex if cogfprex is not None else cogfrstx

    def harmonize_cogfrst(self) -> Optional[int]:
        """Updates COGFRST for NACCCOGF harmonization.

        Returns updated value for COGFRST
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
        # not defined in V4
        if self.formver == 4:
            return INFORMED_MISSINGNESS

        cogfrst = self.harmonize_cogfrst()
        cogfpred = self.uds.get_value("cogfpred", int)
        nacccogf = None
        p_decclin = None
        p_cogfrst = None
        p_cogfpred = None

        if self.__prev_record:
            p_decclin = self.__prev_record.get_resolved_value("decclin", int)
            p_cogfrst = self.__prev_record.get_resolved_value("cogfrst", int)
            p_cogfpred = self.__prev_record.get_resolved_value(
                "cogfpred", int, prev_code=0 if self.formver == 3 else None
            )

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

    def _create_naccmotf(self) -> int:  # noqa: C901
        """Creates NACCMOTF, Indicate the predominant symptom that was first
        recognized as a decline in the subject's motor function."""
        # not defined in V4
        if self.formver == 4:
            return INFORMED_MISSINGNESS

        mofrst = self.uds.get_value("mofrst", int)

        # see note in _create_naccbehf; same situation
        if mofrst is None:
            if self.formver >= 3:
                return 0
            elif self.__decclin == 0:
                return 0

        naccmotf = None
        p_decclin = None
        p_mofrst = None
        if self.__prev_record:
            p_decclin = self.__prev_record.get_resolved_value("decclin", int)
            p_mofrst = self.__prev_record.get_resolved_value(
                "mofrst", int, prev_code=0 if self.formver == 3 else None
            )

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
