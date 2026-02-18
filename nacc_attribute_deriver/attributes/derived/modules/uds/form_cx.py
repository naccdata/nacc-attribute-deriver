"""Derived variables from form C1/C2: Neuropsychological Battery Summary
Scores. In V4 these are the C2/C2T forms.

One of form (C1 or C2)/(C2 or C2T) is expected to have been submitted.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)
from nacc_attribute_deriver.utils.date import (
    calculate_days,
    date_from_form_date,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


class UDSFormCXAttribute(UDSAttributeCollection):
    """Class to collect UDS C1/C2 or C2/C2T attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        # V3 and earlier, used to differentiate which version was used
        self.__frmdatec1 = self.uds.get_value("frmdatec1", str)
        self.__frmdatec2 = self.uds.get_value("frmdatec2", str)
        self.__formverc1 = self.uds.get_value("formverc1", float)
        self.__formverc2 = self.uds.get_value("formverc2", float)

        # V4. If C2T is submitted, RMMODEC2C2T must be 1, so used as
        # an indicator of whether or not this is a C2T form
        self.__frmdatec2c2t = self.uds.get_value("frmdatec2c2t", str)
        self.__is_c2t = self.uds.get_value("rmmodec2c2t", int) == 1

    def __calculate_interval_from_a1(self, cmp_date: str) -> int:
        """Calculates discrepency between UDS Form A1 and Form C1/C2."""
        frmdate_a1 = date_from_form_date(self.uds.get_value("frmdatea1", str))
        frmdate_cx = date_from_form_date(cmp_date)

        if not frmdate_a1 or not frmdate_cx:
            raise AttributeDeriverError(
                "Cannot determine date for FRMDATEA1 or FRMDATECX"
            )

        interval = calculate_days(frmdate_cx, frmdate_a1)
        if interval is None:
            raise AttributeDeriverError(
                "Cannot determine days between FRMDATEA1 and FRMDATECX"
            )

        # 0 if CX completed within 90 days of A1, 1 otherwise
        return 0 if interval <= 90 else 1

    def _create_naccc1(self) -> int:
        """Creates NACCC1, form data discrepancy between UDS Form A1 and Form
        C1.

        Only runs in V3 and earlier for form C1.
        """
        if self.__frmdatec1 is None:
            return INFORMED_MISSINGNESS

        return self.__calculate_interval_from_a1(self.__frmdatec1)

    def _create_naccc2(self) -> int:
        """Creates NACCC2, form data discrepancy between UDS Form A1 and Form
        C2.

        Always runs in V4, and for V3 and earlier, when the C2 form is
        submitted.
        """
        if self.formver < 4 and self.__frmdatec2 is None:
            return INFORMED_MISSINGNESS

        cmp_date = self.__frmdatec2 if self.formver < 4 else self.__frmdatec2c2t
        if not cmp_date:
            raise AttributeDeriverError(
                "Expected one of frmdatec2 or frmdatec2c2t to derive NACCC2"
            )

        return self.__calculate_interval_from_a1(cmp_date)

    def _create_naccmmse(self) -> int:
        """Creates NACCMMSE, Total MMSE score (using D-L-R-O-W).

        Only in V3 and earlier, but implicitly handled by these
        variables just not existing in V4.
        """
        mmse = self.uds.get_value("mmse", int)
        mmsereas = self.uds.get_value("mmsereas", int)

        if mmse is None and mmsereas is not None:
            return mmsereas

        return mmse if (mmse is not None and mmse != 99) else INFORMED_MISSINGNESS

    def __get_educ(self) -> Optional[int]:
        """Educ only explicitly provided at initial visit."""
        if self.uds.is_initial():
            return self.uds.get_value("educ", int)

        return self.prev_record.get_resolved_value("educ", int)

    def _create_naccmoca(self) -> int:
        """(V3+ only) Creates NACCMOCA.

        MoCA Total Score -- corrected for education
        """
        # In V4 only run for C2, -4 otherwise
        if self.formver >= 4:
            if self.__is_c2t:
                return INFORMED_MISSINGNESS

        # In V3 and earlier, only run
        # if formverc2 = 3 and packet != IT
        else:
            packet = self.uds.get_value("packet", str)
            if not (self.__formverc2 == 3 and packet != "IT"):
                return INFORMED_MISSINGNESS

        mocatots = self.uds.get_value("mocatots", int)
        if mocatots is None:
            return INFORMED_MISSINGNESS
        if mocatots == 88:
            return 88

        educ = self.__get_educ()
        if educ is None or educ == 99:
            return 99
        if educ <= 12 and mocatots < 30:
            return mocatots + 1

        return mocatots

    def _create_naccmocb(self) -> int:
        """(V3+ only) Creates NACCMOCB.

        MoCA-Blind Total Score -- corrected for education
        """
        # In V4 only run for C2T, -4 otherwise
        if self.formver >= 4:
            if not self.__is_c2t:
                return INFORMED_MISSINGNESS

        # In V3, only run
        #   if formverc2 = 3.2 OR
        #   if formverc2 = 3.0 and packet = IT
        else:
            packet = self.uds.get_value("packet", str)
            if self.__formverc2 != 3.2 and not (
                self.__formverc2 == 3 and packet == "IT"
            ):
                return INFORMED_MISSINGNESS

        mocbtots = self.uds.get_value("mocbtots", int)
        mocacomp = self.uds.get_value("mocacomp", int)

        if mocbtots is None:
            return INFORMED_MISSINGNESS
        if mocbtots == 88 or mocacomp == 0:
            return 88

        educ = self.__get_educ()
        if educ is None or educ == 99:
            return 99
        if educ >= 0 and educ <= 12 and mocbtots >= 0 and mocbtots < 22:
            return mocbtots + 1

        return mocbtots
