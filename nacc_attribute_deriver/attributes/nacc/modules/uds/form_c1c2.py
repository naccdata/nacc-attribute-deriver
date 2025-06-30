"""Derived variables from form C1/C2: Neuropsychological Battery Summary
Scores.

One of form C1 or C2 is expected to have been submitted.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.base.namespace import WorkingDerivedNamespace
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_days,
    datetime_from_form_date,
)

from .uds_attribute_collection import UDSAttributeCollection


class UDSFormC1C2Attribute(UDSAttributeCollection):
    """Class to collect UDS C1/C2 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__working_derived = WorkingDerivedNamespace(
            table=table, required=frozenset(["cross-sectional.educ"])
        )
        self.__frmdatec1 = self.uds.get_value("frmdatec1", str)
        self.__frmdatec2 = self.uds.get_value("frmdatec2", str)

    @property
    def submitted(self) -> bool:
        return self.__frmdatec1 is not None or self.__frmdatec2 is not None

    def __calculate_interval_from_a1(self, cmp_date: str) -> Optional[int]:
        """Calculates discrepency between UDS Form A1 and Form C1/C2."""
        frmdate_a1 = datetime_from_form_date(self.uds.get_value("frmdatea1", str))
        frmdate_cx = datetime_from_form_date(cmp_date)

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

    def _create_naccc1(self) -> Optional[int]:
        """Creates NACCC1, form data discrepancy between UDS Form A1 and Form
        C1."""
        if self.__frmdatec1 is None:
            return None

        return self.__calculate_interval_from_a1(self.__frmdatec1)

    def _create_naccc2(self) -> Optional[int]:
        """Creates NACCC2, form data discrepancy between UDS Form A1 and Form
        C2."""
        if self.__frmdatec2 is None:
            return None

        # 2021-10-25
        # 2022-03-22

        return self.__calculate_interval_from_a1(self.__frmdatec2)

    def _create_naccmmse(self) -> Optional[int]:
        """Creates NACCMMSE, Total MMSE score (using D-L-R-O-W)"""
        mmse = self.uds.get_value("mmse", int)
        mmsereas = self.uds.get_value("mmsereas", int)

        if mmse is None and mmsereas is not None:
            return mmsereas

        return mmse

    def _create_naccmoca(self) -> Optional[int]:
        """(V3+ only) Creates NACCMOCA.

        MoCA Total Score -- corrected for education
        """
        if self.formver < 3 or not self.submitted:
            return None

        precise_formver = self.uds.get_required("formver", float)
        packet = self.uds.get_value("packet", str)

        if precise_formver == 3 and packet != "IT":
            mocatots = self.uds.get_value("mocatots", int)
            educ = self.__working_derived.get_cross_sectional_value("educ", int)
            if mocatots is None or mocatots == 88:
                return 88
            if educ is None or educ == 99:
                return 99
            if educ <= 12 and mocatots < 30:
                return mocatots + 1

            return mocatots

        return None

    def _create_naccmocb(self) -> Optional[int]:
        """(V3+ only) Creates NACCMOCB.

        MoCA-Blind Total Score -- corrected for education
        """
        if self.formver < 3 or not self.submitted:
            return None

        precise_formver = self.uds.get_required("formver", float)
        packet = self.uds.get_value("packet", str)

        if precise_formver == 3.2 or (precise_formver == 3 and packet == "IT"):
            mocbtots = self.uds.get_value("mocbtots", int)
            mocacomp = self.uds.get_value("mocacomp", int)
            educ = self.__working_derived.get_cross_sectional_value("educ", int)
            if mocbtots is None or mocbtots == 88 or mocacomp == 0:
                return 88
            if educ is None or educ == 99:
                return 99
            if educ >= 0 and educ <= 12 and mocbtots >= 0 and mocbtots < 22:
                return mocbtots + 1

            return mocbtots

        return None
