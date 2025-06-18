"""Derived variables from form C1: Neuropsychological Battery Summary Scores.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_days,
    datetime_from_form_date,
)


class UDSFormC1Attribute(AttributeCollection):
    """Class to collect UDS C1 attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)
        self.__submitted = self.__uds.get_value("frmdatec1", str) is not None
        self.__formver = self.__uds.normalized_formver()

    def _create_naccc1(self) -> Optional[int]:
        """Creates NACCC1, form data discrepancy between UDS Form A1
        and Form C1.
        """
        if not self.__submitted:
            return None

        frmdate_a1 = datetime_from_form_date(
            self.__uds.get_value("frmdatea1", str))
        frmdate_c1 = datetime_from_form_date(
            self.__uds.get_value("frmdatec1", str))

        if not frmdate_a1 or not frmdate_c1:
            raise AttributeDeriverError(
                "Cannot determine date from FRMDATEA1 or FRMDATEC2")

        interval = calculate_days(frmdate_c1, frmdate_a1)
        if interval is None:
            raise AttributeDeriverError(
                "Cannot determine days between FRMDATEA1 or FRMDATEC2")

        # 0 if C1 completed within 90 days of A1, 1 otherwise
        return 0 if interval <= 90 else 1

    def _create_naccmmse(self) -> Optional[int]:
        """Creates NACCMMSE, Total MMSE score (using D-L-R-O-W)"""
        if not self.__submitted:
            return None

        mmse = self.__uds.get_value('mmse', int)
        mmsereas = self.__uds.get_value('mmsereas', int)

        if mmse is None and mmsereas is not None:
            return mmsereas

        return mmse

    def _create_naccmoca(self) -> Optional[int]:
        """(V3+ only) Creates NACCMOCA

        MoCA Total Score -- corrected for education
        """
        if self.__formver < 3:
            return None

        precise_formver = self.__uds.get_required('formver', float)
        packet = self.__uds.get_value('packet', str)

        if precise_formver == 3 and packet != 'IT':
            mocatots = self.__uds.get_value('mocatots', int)
            educ = self.__uds.get_value('educ', int)
            if mocatots is None or mocatots == 88:
                return 88
            if educ is None or educ == 99:
                return 99
            if educ <= 12 and mocatots < 30:
                return mocatots + 1

            return mocatots

        return None

    def _create_naccmocb(self) -> Optional[int]:
        """(V3+ only) Creates NACCMOCB

        MoCA-Blind Total Score -- corrected for education
        """
        if self.__formver < 3:
            return None

        precise_formver = self.__uds.get_required('formver', float)
        packet = self.__uds.get_value('packet', str)

        if precise_formver == 3.2 or (precise_formver == 3 and packet == 'IT'):
            mocbtots = self.__uds.get_value('mocbtots', int)
            mocacomp = self.__uds.get_value('mocacomp', int)
            educ = self.__uds.get_value('educ', int)
            if mocbtots is None or mocbtots == 88 or mocacomp == 0:
                return 88
            if educ is None or educ == 99:
                return 99
            if educ >= 0 and educ <= 12 and mocbtots >= 0 and mocbtots < 22:
                return mocbtots + 1

            return mocbtots

        return None
