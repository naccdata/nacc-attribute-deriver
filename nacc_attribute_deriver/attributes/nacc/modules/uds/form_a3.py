"""Derived variables from form A3: Family History.

Form A3 is optional, so may not have been submitted.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import SubjectDerivedNamespace
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable

from .helpers.family_handler import FamilyHandler


class UDSFormA3Attribute(AttributeCollection):
    """Class to collect UDS A2 attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

        # TODO - for v4 this will be modea3
        self.__submitted = self.__uds.get_value("a3sub", int) == 1
        self.__formver = self.__uds.normalized_formver()

        self.__mom = FamilyHandler("mom", self.__uds)
        self.__dad = FamilyHandler("dad", self.__uds)
        self.__sib = FamilyHandler("sib", self.__uds)
        self.__kid = FamilyHandler("kid", self.__uds)
        self.__family = [self.__mom, self.__dad, self.__sib, self.__kid]

    def _create_naccam(self) -> Optional[int]:
        """Creates NACCAM - In this family, is there evidence
        of an AD mutation?

        Only in V3+. This seems to assume at most the same
        code will be noted in all visits, but it could theoretically
        be overwritten (e.g. change from 2 -> 8 -> 3 -> etc.) so
        will ultimately report the last one since its cross-sectional.
        """
        if not self.__submitted or self.__formver < 3:
            return None

        fadmut = self.__uds.get_value("fadmut", int)
        if fadmut in [0, 1, 2, 3, 8]:
            return fadmut

        # check if defined in previous form, else return 9
        return self.__subject_derived.get_cross_sectional_value(
            "naccam", int, default=9
        )

    def _create_naccamx(self) -> Optional[str]:
        """Creates NACCAMX - If an AD mutation other than
        APP, PSEN-1, or PSEN-2 is reported.
        """
        if not self.__submitted or self.__formver < 3:
            return None

        return self.__uds.get_value("fadmutx", str)

    def _create_naccams(self) -> Optional[int]:
        """Creates NACCAMS - Source of evidence for AD
        mutation.

        Only in V3+, and None if NACCAM (FADMUT) is 0. Same
        assumption as NACCAM.
        """
        if not self.__submitted or self.__formver < 3 or self._create_naccam() == 0:
            return None

        fadmuso = self.__uds.get_value("fadmuso", int)
        if fadmuso in [1, 2, 3, 4, 8]:
            return fadmuso

        # check if defined in previous form, else return 9
        return self.__subject_derived.get_cross_sectional_value(
            "naccams", int, default=9
        )

    def _create_naccamsx(self) -> Optional[str]:
        """Creates NACCAMSX - Other source of AD."""
        if not self.__submitted or self.__formver < 3:
            return None

        return self.__uds.get_value("fadmusox", str)

    def _create_naccdad(self) -> Optional[int]:
        """Creates NACCDAD - Indicator of father with cognitive
        impariment.
        """
        if not self.__submitted:
            return None

        if self.__dad.xdem():
            return 1
        if self.__dad.xnot():
            return 0

        # check if defined in previous form, else return 9
        return self.__subject_derived.get_cross_sectional_value(
            "naccdad", int, default=9
        )

    def _create_naccfadm(self) -> int:
        """Creates NACCFADM - In this family, is there evidence
        of dominantly inherited AD?
        """
        if not self.__submitted or self.__formver < 3:
            return 0

        if self.__uds.get_value("fadmut", int) in [1, 2, 3, 8]:
            return 1

        return 0

    def _create_naccfam(self) -> Optional[int]:
        """Creates NACCFAM - Indicator of first-degree family
        member with cognitive impariment.
        """
        if not self.__submitted:
            return None

        if any(member.xdem() for member in self.__family):
            return 1
        elif all(member.xnot() for member in self.__family):
            return 0

        # check if defined in previous form, else return 9
        return self.__subject_derived.get_cross_sectional_value(
            "naccfam", int, default=9
        )

    def _create_naccfftd(self) -> int:
        """Creates NACCFFTD - In this family, is there evidence for
        an FTLD mutation?
        """
        if not self.__submitted or self.__formver < 3:
            return 0

        if (
            self.__uds.get_value("fftdmut", int) in [1, 2, 3, 4, 8]
            or self.__uds.get_value("ftdmutat", int) == 1
        ):
            return 1

        return 0

    def _create_naccfm(self) -> Optional[int]:
        """Creates NACCFM - In this family, is there evidence for an
        FTLD mutation (from a list of specific mutations)?
        """
        if not self.__submitted or self.__formver < 3:
            return None

        fftdmut = self.__uds.get_value("fftdmut", int)
        if fftdmut in [0, 1, 2, 3, 4, 8]:
            return fftdmut

        return self.__subject_derived.get_cross_sectional_value(
            "naccfm", int, default=9
        )

    def _create_naccfms(self) -> Optional[int]:
        """Creates NACCFMS - Source of evidence for FTLD
        mutation.
        """
        if not self.__submitted or self.__formver < 3 or self._create_naccfm() == 0:
            return None

        fftdmusu = self.__uds.get_value("fftdmuso", int)
        if fftdmusu in [0, 1, 2, 3, 8]:
            return fftdmusu

        return 9

    def _create_naccfmsx(self) -> Optional[str]:
        """Creates NACCFMSX - If other source of FTLD mutation,
        report here.
        """
        if not self.__submitted or self.__formver < 3:
            return None

        return self.__uds.get_value("fftdmusx", str)

    def _create_naccfmx(self) -> Optional[str]:
        """Creates NACCFMX - If an FTLD mutation other than
        provided list, report here."""
        if not self.__submitted or self.__formver < 3:
            return None

        return self.__uds.get_value("fftdmutx", str)

    def _create_naccmom(self) -> Optional[int]:
        """Creates NACCMOM - Indicator of mother with cognitive
        impairment.
        """
        if not self.__submitted:
            return None

        if self.__mom.xdem():
            return 1
        if self.__mom.xnot():
            return 0

        # check if defined in previous form, else return 9
        return self.__subject_derived.get_cross_sectional_value(
            "naccmom", int, default=9
        )

    def _create_naccom(self) -> Optional[int]:
        """Creates NACCOM - In this family, is there evidence for
        a mutation other than an AD or FTLD mutation?
        """
        if not self.__submitted or self.__formver < 3:
            return None

        fothmut = self.__uds.get_value("fothmut", int)
        if fothmut in [0, 1]:
            return fothmut

        # check if defined in previous form, else return 9
        return self.__subject_derived.get_cross_sectional_value(
            "naccom", int, default=9
        )

    def _create_naccoms(self) -> Optional[int]:
        """Creates NACCOMS - Source of evidence for other
        mutation.
        """
        if not self.__submitted or self.__formver < 3 or self._create_naccom() == 0:
            return None

        fothmuso = self.__uds.get_value("fothmuso", int)
        if fothmuso in [0, 1, 2, 3, 8]:
            return fothmuso

        return 9

    def _create_naccomsx(self) -> Optional[str]:
        """Creates NACCOMSX - If mutation is reported at any
        visit (NACCOMS == 8), report here."""
        if not self.__submitted or self.__formver < 3:
            return None

        return self.__uds.get_value("fothmusx", str)

    def _create_naccomx(self) -> Optional[str]:
        """Creates NACCOMX - If any other mutation is reported at
        any visit, reported here."""
        if not self.__submitted or self.__formver < 3:
            return None

        return self.__uds.get_value("fothmutx", str)
