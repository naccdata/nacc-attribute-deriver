"""Derived variables from form A3: Family History."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

from .helpers.family_handler import FamilyHandler, LegacyFamilyHandler


class UDSFormA3Attribute(UDSAttributeCollection):
    """Class to collect UDS A2 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

        handler = LegacyFamilyHandler if self.formver < 4 else FamilyHandler
        self.__family = handler(uds=self.uds, prev_record=self.prev_record)

    @property
    def submitted(self) -> bool:
        """Form A3 is optional in earlier versions.

        Required in V4.
        """
        if self.formver < 4:
            return self.uds.get_value("a3sub", int) == 1

        # required in V4
        return True

    def _create_naccdad(self) -> Optional[int]:
        """Creates NACCDAD - Indicator of father with cognitive
        impariment.
        """
        if not self.submitted:
            return None

        known_value = self.__subject_derived.get_cross_sectional_value(
            "naccdad", int, default=9
        )
        return self.__family.determine_naccparent(  # type: ignore
            self.__family.dad,  # type: ignore
            known_value,
        )

    def _create_naccmom(self) -> Optional[int]:
        """Creates NACCMOM - Indicator of mother with cognitive
        impairment.
        """
        if not self.submitted:
            return None

        known_value = self.__subject_derived.get_cross_sectional_value(
            "naccmom", int, default=9
        )
        return self.__family.determine_naccparent(  # type: ignore
            self.__family.mom,  # type: ignore
            known_value,
        )

    def _create_naccfam(self) -> Optional[int]:
        """Creates NACCFAM - Indicator of first-degree family
        member with cognitive impariment.
        """
        if not self.submitted:
            return None

        known_value = self.__subject_derived.get_cross_sectional_value(
            "naccfam", int, default=9
        )
        return self.__family.determine_naccfam(known_value)  # type: ignore

    #######################
    # V3 AND EARLIER ONLY #
    #######################

    def _create_naccam(self) -> Optional[int]:
        """Creates NACCAM - In this family, is there evidence
        of an AD mutation?

        Only in V3+. This seems to assume at most the same
        code will be noted in all visits, but it could theoretically
        be overwritten (e.g. change from 2 -> 8 -> 3 -> etc.) so
        will ultimately report the last one since its cross-sectional.
        """
        if not self.submitted or self.formver != 3:
            return None

        known_value = self.__subject_derived.get_cross_sectional_value(
            "naccam", int, default=9
        )

        fadmut = self.uds.get_value("fadmut", int)
        if fadmut in [1, 2, 3, 8]:
            return fadmut
        if fadmut == 0:
            # a non-zero known value should supersede
            if known_value in [1, 2, 3, 8]:
                return known_value
            return fadmut

        return known_value

    def _create_naccamx(self) -> Optional[str]:
        """Creates NACCAMX - If an AD mutation other than
        APP, PSEN-1, or PSEN-2 is reported.

        Only in V3.
        """
        if not self.submitted or self.formver != 3:
            return None

        return self.uds.get_value("fadmutx", str)

    def _create_naccams(self) -> Optional[int]:
        """Creates NACCAMS - Source of evidence for AD
        mutation.

        Only in V3, and None if NACCAM (FADMUT) is 0. Same
        assumption as NACCAM. Also, if the source of evidence
        is unknown at all visits (all == 9) then NACCAMS is 9.
        If not reported at any (NACCAM == 0) than -4.
        """
        if not self.submitted or self.formver != 3:
            return None

        if self._create_naccam() == 0:
            return INFORMED_MISSINGNESS

        fadmuso = self.uds.get_value("fadmuso", int)
        if fadmuso in [1, 2, 3, 8]:
            return fadmuso

        # for NACCAMS to be 9, it must be 9 at ALL visits, return None otherwise
        known_value = self.__subject_derived.get_cross_sectional_value("naccams", int)
        if fadmuso == 9 and (self.uds.is_initial() or known_value == 9):
            return 9

        # if fadmuso is None, also return 9 or the known value
        if fadmuso is None:
            return 9 if known_value is None else known_value

        return None

    def _create_naccamsx(self) -> Optional[str]:
        """Creates NACCAMSX - Other source of AD.

        Only in V3.
        """
        if not self.submitted or self.formver != 3:
            return None

        return self.uds.get_value("fadmusox", str)

    def _create_naccfadm(self) -> Optional[int]:
        """Creates NACCFADM - In this family, is there evidence
        of dominantly inherited AD?

        Only really defined for V3. Explicitly removed in V4.
        """
        # removed in V4
        if self.formver >= 4:
            return None

        if not self.submitted or self.formver < 3:
            return 0

        if self.uds.get_value("fadmut", int) in [1, 2, 3, 8]:
            return 1

        return self.__subject_derived.get_cross_sectional_value(  # type: ignore
            "naccfadm", int, default=0
        )

    def _create_naccfftd(self) -> int:
        """Creates NACCFFTD - In this family, is there evidence for
        an FTLD mutation?

        Only in V3.
        """
        if not self.submitted or self.formver != 3:
            return 0

        if (
            self.uds.get_value("fftdmut", int) in [1, 2, 3, 4, 8]
            or self.uds.get_value("ftdmutat", int) == 1
        ):
            return 1

        return self.__subject_derived.get_cross_sectional_value(  # type: ignore
            "naccfftd", int, default=0
        )

    def _create_naccfm(self) -> Optional[int]:
        """Creates NACCFM - In this family, is there evidence for an
        FTLD mutation (from a list of specific mutations)?

        Only in V3.
        """
        if not self.submitted or self.formver != 3:
            return None

        fftdmut = self.uds.get_value("fftdmut", int)
        if fftdmut in [1, 2, 3, 4, 8]:
            return fftdmut

        known_value = self.__subject_derived.get_cross_sectional_value(
            "naccfm", int, default=9
        )
        if fftdmut == 0:
            # a non-zero known value should supersede
            if known_value in [1, 2, 3, 4, 8]:
                return known_value
            return fftdmut

        return known_value

    def _create_naccfms(self) -> Optional[int]:
        """Creates NACCFMS - Source of evidence for FTLD
        mutation.

        Only in V3.
        """
        if not self.submitted or self.formver != 3:
            return None

        if self._create_naccfm() == 0:
            return INFORMED_MISSINGNESS

        fftdmusu = self.uds.get_value("fftdmuso", int)
        if fftdmusu in [0, 1, 2, 3, 8]:
            return fftdmusu

        # for NACCFMS to be 9, it must be 9 at ALL visits, return None otherwise
        known_value = self.__subject_derived.get_cross_sectional_value("naccfms", int)
        if fftdmusu == 9 and (self.uds.is_initial() or known_value == 9):
            return 9

        # if fftdmusu is None, also return 9 or the known value
        if fftdmusu is None:
            return 9 if known_value is None else known_value

        return None

    def _create_naccfmsx(self) -> Optional[str]:
        """Creates NACCFMSX - If other source of FTLD mutation,
        report here.

        Only in V3
        """
        if not self.submitted or self.formver != 3:
            return None

        return self.uds.get_value("fftdmusx", str)

    def _create_naccfmx(self) -> Optional[str]:
        """Creates NACCFMX - If an FTLD mutation other than
        provided list, report here.

        Only in V3.
        """
        if not self.submitted or self.formver != 3:
            return None

        return self.uds.get_value("fftdmutx", str)

    def _create_naccom(self) -> Optional[int]:
        """Creates NACCOM - In this family, is there evidence for
        a mutation other than an AD or FTLD mutation?

        Only in V3
        """
        if not self.submitted or self.formver != 3:
            return None

        # known value 1 always supersedes
        known_value = self.__subject_derived.get_cross_sectional_value(
            "naccom", int, default=9
        )
        if known_value == 1:
            return 1

        fothmut = self.uds.get_value("fothmut", int)
        if fothmut in [0, 1]:
            return fothmut

        return known_value

    def _create_naccoms(self) -> Optional[int]:
        """Creates NACCOMS - Source of evidence for other
        mutation.

        Only in V3.
        """
        if not self.submitted or self.formver != 3:
            return None

        if self._create_naccom() == 0:
            return INFORMED_MISSINGNESS

        fothmuso = self.uds.get_value("fothmuso", int)
        if fothmuso in [0, 1, 2, 3, 8]:
            return fothmuso

        # for NACCOMS to be 9, it must be 9 at ALL visits, return None otherwise
        known_value = self.__subject_derived.get_cross_sectional_value("naccoms", int)
        if fothmuso == 9 and (self.uds.is_initial() or known_value == 9):
            return 9

        # if fothmuso is None, also return 9 or the known value
        if fothmuso is None:
            return 9 if known_value is None else known_value

        return None

    def _create_naccomsx(self) -> Optional[str]:
        """Creates NACCOMSX - If mutation is reported at any
        visit (NACCOMS == 8), report here.

        Only in V3.
        """
        if not self.submitted or self.formver != 3:
            return None

        return self.uds.get_value("fothmusx", str)

    def _create_naccomx(self) -> Optional[str]:
        """Creates NACCOMX - If any other mutation is reported at
        any visit, reported here.

        Only in V3.
        """
        if not self.submitted or self.formver != 3:
            return None

        return self.uds.get_value("fothmutx", str)
