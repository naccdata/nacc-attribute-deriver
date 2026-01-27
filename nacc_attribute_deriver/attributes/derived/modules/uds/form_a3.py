"""Derived variables from form A3: Family History."""

from typing import Callable, Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)

from .helpers.family_handler import FamilyHandler, LegacyFamilyHandler
from .helpers.family_member_handler import FamilyMemberHandler


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

    def __handle_parents(self, derived_var: str, parent: FamilyMemberHandler) -> int:
        """Handles NACCDAD and NACCMOM."""
        known_value = self.__subject_derived.get_cross_sectional_value(derived_var, int)
        # REGRESSION: we are now allowing these values to flip/flop, but
        # to match regression make it stay 1 if its ever 1
        # if known_value == 1:
        #     return known_value

        if not self.submitted:
            return known_value if known_value is not None else INFORMED_MISSINGNESS

        return self.__family.determine_naccparent(
            parent,  # type: ignore
            known_value if known_value is not None else 9,
        )

    def _create_naccdad(self) -> int:
        """Creates NACCDAD - Indicator of father with cognitive
        impariment.
        """
        return self.__handle_parents("naccdad", self.__family.dad)  # type: ignore

    def _create_naccmom(self) -> int:
        """Creates NACCMOM - Indicator of mother with cognitive
        impairment.
        """
        return self.__handle_parents("naccmom", self.__family.mom)  # type: ignore

    def _create_naccfam(self) -> int:
        """Creates NACCFAM - Indicator of first-degree family
        member with cognitive impariment.
        """
        known_value = self.__subject_derived.get_cross_sectional_value("naccfam", int)

        # REGRESSION: we are now allowing these values to flip/flop, but
        # to match regression make it stay 1 if its ever 1
        # if known_value == 1:
        #     return known_value

        if not self.submitted:
            return known_value if known_value is not None else INFORMED_MISSINGNESS

        return self.__family.determine_naccfam(  # type: ignore
            known_value if known_value is not None else 9
        )

    ###########
    # V3 ONLY #
    ###########

    def __handle_a3_derived_logic(
        self,
        logic: Callable,
        derived_var: str,
        default: int = 9,
        missingness_value: int = INFORMED_MISSINGNESS,
    ) -> int:
        """All of these legacy A3 derived variables work the same:

        - Get the known derived value.
        - If the form was not submitted, or isn't in V3, return the
          known value if it was already set, else -4/missingness value
        - Execute core logic
        - If none of the core logic is satisfied, return the known
          value if it was already set (not None and not the missingness value),
          otherwise the default, usually 0 or 9
        """
        known_value = self.__subject_derived.get_cross_sectional_value(derived_var, int)

        if not self.submitted or self.formver != 3:
            return known_value if known_value is not None else missingness_value

        result = logic(self, known_value)
        if result is not None:
            return result

        if known_value is not None and known_value != missingness_value:
            return known_value

        return default

    def _create_naccfadm(self) -> int:
        """Creates NACCFADM - In this family, is there evidence
        of dominantly inherited AD?

        Only really defined for V3. Explicitly removed in V4, but
        if had been defined before then carry forward.
        """

        def __naccfadm_logic(self, known_value: int) -> Optional[int]:
            if self.uds.get_value("fadmut", int) in [1, 2, 3, 8]:
                return 1

            return None

        # TODO: for whatever reason, the missingness value was 0 and not
        # -4 in older versions. should it be changed to -4?
        return self.__handle_a3_derived_logic(
            __naccfadm_logic,
            "naccfadm",
            default=0,
            missingness_value=0 if self.formver != 4 else INFORMED_MISSINGNESS,
        )

    def _create_naccfftd(self) -> int:
        """Creates NACCFFTD - In this family, is there evidence for
        an FTLD mutation?

        Only in V3.
        """

        def __naccfftd_logic(self, known_value: int) -> Optional[int]:
            if (
                self.uds.get_value("fftdmut", int) in [1, 2, 3, 4, 8]
                or self.uds.get_value("ftdmutat", int) == 1
            ):
                return 1

            return None

        # TODO: for whatever reason, the missingness value was 0 and not
        # -4 in older versions. should it be changed to -4?
        return self.__handle_a3_derived_logic(
            __naccfftd_logic,
            "naccfftd",
            default=0,
            missingness_value=0 if self.formver != 4 else INFORMED_MISSINGNESS,
        )

    def _create_naccam(self) -> int:
        """Creates NACCAM - In this family, is there evidence
        of an AD mutation?

        Only in V3+. This seems to assume at most the same
        code will be noted in all visits, but it could theoretically
        be overwritten (e.g. change from 2 -> 8 -> 3 -> etc.) so
        will ultimately report the last one since its cross-sectional.
        """

        def __naccam_logic(self, known_value: int) -> Optional[int]:
            fadmut = self.uds.get_value("fadmut", int)
            if fadmut in [1, 2, 3, 8]:
                return fadmut
            if fadmut == 0:
                # a non-zero known value should supersede
                if known_value in [1, 2, 3, 8]:
                    return known_value
                return fadmut

            return None

        return self.__handle_a3_derived_logic(__naccam_logic, "naccam")

    def _create_naccams(self) -> int:
        """Creates NACCAMS - Source of evidence for AD
        mutation.

        Only in V3, and None if NACCAM (FADMUT) is 0. Same
        assumption as NACCAM. Also, if the source of evidence
        is unknown at all visits (all == 9) then NACCAMS is 9.
        If not reported at any (NACCAM == 0) than -4.
        """

        def __naccams_logic(self, known_value: int) -> Optional[int]:
            if self._create_naccam() == 0:
                return INFORMED_MISSINGNESS

            fadmuso = self.uds.get_value("fadmuso", int)
            if fadmuso in [1, 2, 3, 8]:
                return fadmuso

            # for NACCAMS to be 9, it must be 9 at ALL visits, return None otherwise
            if fadmuso == 9 and (self.uds.is_initial() or known_value == 9):
                return 9

            return None

        return self.__handle_a3_derived_logic(__naccams_logic, "naccams")

    def _create_naccfm(self) -> int:
        """Creates NACCFM - In this family, is there evidence for an
        FTLD mutation (from a list of specific mutations)?

        Only in V3.
        """

        def __naccfm_logic(self, known_value: int) -> Optional[int]:
            fftdmut = self.uds.get_value("fftdmut", int)
            if fftdmut in [1, 2, 3, 4, 8]:
                return fftdmut

            if fftdmut == 0:
                # a non-zero known value should supersede
                if known_value in [1, 2, 3, 4, 8]:
                    return known_value
                return fftdmut

            return None

        return self.__handle_a3_derived_logic(__naccfm_logic, "naccfm")

    def _create_naccfms(self) -> int:
        """Creates NACCFMS - Source of evidence for FTLD
        mutation.

        Only in V3.
        """

        def __naccfms_logic(self, known_value: int) -> Optional[int]:
            if self._create_naccfm() == 0:
                return INFORMED_MISSINGNESS

            fftdmusu = self.uds.get_value("fftdmuso", int)
            if fftdmusu in [0, 1, 2, 3, 8]:
                return fftdmusu

            # for NACCFMS to be 9, it must be 9 at ALL visits, return None otherwise
            if fftdmusu == 9 and (self.uds.is_initial() or known_value == 9):
                return 9

            return None

        return self.__handle_a3_derived_logic(__naccfms_logic, "naccfms")

    def _create_naccom(self) -> int:
        """Creates NACCOM - In this family, is there evidence for
        a mutation other than an AD or FTLD mutation?

        Only in V3
        """

        def __naccom_logic(self, known_value: int) -> Optional[int]:
            # known value 1 always supersedes
            if known_value == 1:
                return 1

            fothmut = self.uds.get_value("fothmut", int)
            if fothmut in [0, 1]:
                return fothmut

            return None

        return self.__handle_a3_derived_logic(__naccom_logic, "naccom")

    def _create_naccoms(self) -> int:
        """Creates NACCOMS - Source of evidence for other
        mutation.

        Only in V3.
        """

        def __naccoms_logic(self, known_value: int) -> Optional[int]:
            if self._create_naccom() == 0:
                return INFORMED_MISSINGNESS

            fothmuso = self.uds.get_value("fothmuso", int)
            if fothmuso in [0, 1, 2, 3, 8]:
                return fothmuso

            # for NACCOMS to be 9, it must be 9 at ALL visits, return None otherwise
            if fothmuso == 9 and (self.uds.is_initial() or known_value == 9):
                return 9

            return None

        return self.__handle_a3_derived_logic(__naccoms_logic, "naccoms")

    #############
    # Write-ins #
    #############

    def __handle_writein(self, field: str, derived: str) -> str:
        """Handle write-in derived variables, which all work the same."""
        # grab the current write-in, and return if not updated
        value = self.__subject_derived.get_cross_sectional_value(derived, str)
        value = value if value else INFORMED_BLANK

        if not self.submitted or self.formver != 3:
            return value

        result = self.uds.get_value(field, str)
        if result:
            return result

        return value

    def _create_naccamx(self) -> str:
        """Creates NACCAMX - If an AD mutation other than
        APP, PSEN-1, or PSEN-2 is reported.

        Only in V3.
        """
        return self.__handle_writein("fadmutx", "naccamx")

    def _create_naccamsx(self) -> str:
        """Creates NACCAMSX - Other source of AD.

        Only in V3.
        """
        return self.__handle_writein("fadmusox", "naccamsx")

    def _create_naccfmsx(self) -> str:
        """Creates NACCFMSX - If other source of FTLD mutation,
        report here.

        Only in V3
        """
        return self.__handle_writein("fftdmusx", "naccfmsx")

    def _create_naccfmx(self) -> str:
        """Creates NACCFMX - If an FTLD mutation other than
        provided list, report here.

        Only in V3.
        """
        return self.__handle_writein("fftdmutx", "naccfmx")

    def _create_naccomsx(self) -> str:
        """Creates NACCOMSX - If mutation is reported at any
        visit (NACCOMS == 8), report here.

        Only in V3.
        """
        return self.__handle_writein("fothmusx", "naccomsx")

    def _create_naccomx(self) -> str:
        """Creates NACCOMX - If any other mutation is reported at
        any visit, reported here.

        Only in V3.
        """
        return self.__handle_writein("fothmutx", "naccomx")
