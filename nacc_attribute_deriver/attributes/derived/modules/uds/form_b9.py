# ruff: noqa: SIM114
"""For now ignore SIM114 which is complaining about the complicated if/else
branches derived from SAS. Eventually want to clean up.

Derived variables from form B9: Clinician Judgement of Symptoms.

Form B9 is required and expected to have been filled out.

There is a lot of carrying over of previous values and recoding in the original
SAS, resulting in pretty confusing logic, which may not be super clear here
either. It could definitely be updated and take better advantage of the how
the new system handles longitudinal values, but for now leaving as-is.

REGRESSION: A lot of these variables are supposed to be cross-sectional,
but they're actually being treated as longitudinal.
"""

from typing import Optional, Tuple

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)


class UDSFormB9Attribute(UDSAttributeCollection):
    """Class to collect UDS B9 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)
        self.__working = WorkingNamespace(table=table)

        # if b9chg == 1 was selected in version 1.2 of UDS (no meaningful changes),
        # indicates NACC has brought forward data from previous visit
        self.__b9_changes = self.uds.get_value("b9chg", int) in [1, 3]
        self.__decclin = self.uds.get_value("decclin", int)

    def __get_last_set(self, field: str) -> Optional[int]:
        """B9 potentially pulls across multiple visits to get the last time the
        field was ever set, so need to pass the working namespace."""
        result = self.prev_record.get_resolved_value(field, int, working=self.__working)

        # treat -4 as None
        if result == INFORMED_MISSINGNESS:
            return None

        return result

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
        if value == 777:
            value = self.__get_last_set(target_var)

        if value is None:
            return INFORMED_MISSINGNESS

        # enforce range is 9 - 110
        if value not in [777, 888, 999]:
            value = max(9, min(110, value))

        return value

    def __naccbehf_logic(self) -> Tuple[int, str]:  # noqa: C901
        """Helps create NACCBEHF and NACCBEFX. NACCBEFX is strongly
        dependent on NACCBEHF and should only be set/carried forward
        depending on the results of NACCBEHF. Namely, NACCBEFX can only
        be set if NACCBEHF = 10 and the visit that sets it defined the
        variables needed for NACCBEFX, otherwise it should be None.

        Logic also depends on previous vars (p_decclin, p_befrst, p_befpred)

        Returns:
            Computed NACCBHEF and NACCBEFX
        """
        known_naccbehf = self.__subject_derived.get_prev_longitudinal_value(
            "naccbehf", int
        )
        known_naccbefx = self.__subject_derived.get_prev_longitudinal_value(
            "naccbefx", str
        )

        if known_naccbefx is None:
            known_naccbefx = INFORMED_BLANK

        # not defined in V4; -4 instead of 99 if no known value
        if self.formver == 4:
            if known_naccbehf is not None:
                return (known_naccbehf, known_naccbefx)

            return (INFORMED_MISSINGNESS, INFORMED_BLANK)

        if known_naccbehf is None:
            known_naccbehf = 99

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
                return (0, INFORMED_BLANK)
            elif self.__decclin == 0:
                return (0, INFORMED_BLANK)

        p_decclin = self.__get_last_set("decclin")
        p_befrst = self.__get_last_set("befrst")
        p_befpred = self.__get_last_set("befpred")

        if befrst == 88 or (self.__b9_changes and p_decclin == 0):
            naccbehf = 0
        elif self.__b9_changes and p_decclin == 1:
            if p_befrst == 88:
                naccbehf = 0
            elif p_befrst is not None:
                naccbehf = p_befrst

        if self.formver >= 3:
            if befpred == 0:  # noqa: SIM102
                if p_befpred is not None and p_befpred != 0:
                    naccbehf = p_befpred

            if naccbehf == 88:
                naccbehf = 0

        # now see if naccbefx should be set
        naccbefx = None
        if naccbehf == 10:
            if self.formver < 3:
                naccbefx = self.uds.get_value("befrstx", str)
            else:
                naccbefx = self.uds.get_value("befpredx", str)

        if naccbefx is None:
            naccbefx = INFORMED_BLANK

        return (
            (naccbehf, naccbefx)
            if naccbehf is not None
            else (known_naccbehf, known_naccbefx)
        )

    def _create_naccbehf(self) -> int:
        """Create NACCBEHF, indicate the predominant symptom that was first
        recognized as a decline in the subject's behavior."""
        naccbehf, _ = self.__naccbehf_logic()
        return naccbehf

    def _create_naccbefx(self) -> str:
        """Create NACCBEFX, specification of other predominant symptom that was
        first recognized as a decline in the subject's behavior.

        This value should only be set if NACCBHEF = 10, and may
        carry through with it as a pair.
        """
        _, naccbefx = self.__naccbehf_logic()
        return naccbefx

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

    def __nacccogf_logic(self) -> Tuple[int, str]:  # noqa: C901
        """Helps create NACCCOGF and NACCCGFX. NACCCGFX is strongly
        dependent on NACCCOGF and should only be set/carried forward
        depending on the results of NACCCOGF. Namely, NACCCGFX can only
        be set if NACCCOGF = 8 and the visit that sets it defined the
        variables needed for NACCCGFX, otherwise it should be None.

        Logic also depends on previous vars (p_decclin, p_cogfrst, p_cogfpred)

        Returns:
            Computed NACCCOGF and NACCCGFX
        """
        known_nacccogf = self.__subject_derived.get_prev_longitudinal_value(
            "nacccogf", int
        )
        known_nacccgfx = self.__subject_derived.get_prev_longitudinal_value(
            "nacccgfx", str
        )
        if known_nacccgfx is None:
            known_nacccgfx = INFORMED_BLANK

        # not defined in V4; -4 instead of 99 if no known value
        if self.formver == 4:
            if known_nacccogf is not None:
                return (known_nacccogf, known_nacccgfx)

            return (INFORMED_MISSINGNESS, INFORMED_BLANK)

        if known_nacccogf is None:
            known_nacccogf = 99

        cogfrst = self.harmonize_cogfrst()
        cogfpred = self.uds.get_value("cogfpred", int)
        nacccogf = None

        p_decclin = self.__get_last_set("decclin")
        p_cogfrst = self.__get_last_set("cogfrst")
        p_cogfpred = self.__get_last_set("cogfpred")

        if cogfrst is None and cogfpred is None:
            if self.formver >= 3:
                return (0, INFORMED_BLANK)
            elif self.__decclin == 0:
                return (0, INFORMED_BLANK)

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

        if self.formver >= 3 and nacccogf == 88:
            nacccogf = 0

        # now, see if NACCCGFX should be set
        nacccgfx = None
        if nacccogf == 8:
            cogfprex = self.uds.get_value("cogfprex", str)
            cogfrstx = self.uds.get_value("cogfrstx", str)

            nacccgfx = cogfprex if cogfprex is not None else cogfrstx

        if nacccgfx is None:
            nacccgfx = INFORMED_BLANK

        return (
            (nacccogf, nacccgfx)
            if nacccogf is not None
            else (known_nacccogf, known_nacccgfx)
        )

    def _create_nacccogf(self) -> int:
        """Creates NACCCOGF, Indicate the predominant symptom that was first
        recognized as a decline in the subject's cognition."""
        nacccogf, _ = self.__nacccogf_logic()
        return nacccogf

    def _create_nacccgfx(self) -> str:
        """Creates NACCCGFX, specification for other predominant symptom first
        recognized as a decline in the subject's cognition.

        This value should only be set if NACCCOGF = 8, and may
        carry through with it as a pair.
        """
        _, nacccgfx = self.__nacccogf_logic()
        return nacccgfx

    def _create_naccmotf(self) -> int:  # noqa: C901
        """Creates NACCMOTF, Indicate the predominant symptom that was first
        recognized as a decline in the subject's motor function."""
        known_value = self.__subject_derived.get_prev_longitudinal_value(
            "naccmotf", int
        )

        # not defined in V4; -4 instead of 99 if no known value
        if self.formver == 4:
            return known_value if known_value is not None else INFORMED_MISSINGNESS

        if known_value is None:
            known_value = 99

        mofrst = self.uds.get_value("mofrst", int)

        if mofrst is None:
            if self.formver >= 3:
                return 0
            elif self.__decclin == 0:
                return 0

        naccmotf = None
        p_decclin = self.__get_last_set("decclin")
        p_mofrst = self.__get_last_set("mofrst")

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

        return naccmotf if naccmotf is not None else known_value
