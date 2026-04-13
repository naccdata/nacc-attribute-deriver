"""Class to handle A3-specific missingness values.

For V4:
Many variables in this form have the "provided at previous visit" code 66 or 666.

If indicated we must pull forward the value from the previous visit.

Similarly if no new info is provided (assured blank when NWINF variables = 0), then we also need
to pull through the previous visit. If NWINFx is set, enforce ignoring the current value even
if they set something (shouldn't happen due to error checks but done as a safeguard.)

In short, if we see the prev visit code or NWINFx = 0, then pull through the
previous value. 

V3 and earlier:
Not handled.
"""
from typing import Type

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    T,
)
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)


class UDSFormA3V4Missingness(UDSMissingness):
    """Handles V4-specific missingness variables."""

    def __handle_a3_prev_visit_missingness(
        self,
        nwinf_field: str,
        field: str,
        attr_type: Type[T],
        prev_code: int
    ) -> T:
        """Handles "provided at previous visit" missingness for V4 variables.
        Checks the gate NWINF* variable to determine whether or not we ignore
        the current value or not (so if they erraneously set something).

        *ETPR and *ETSEC variables are effectively int-like strings, so can use
        same logic just type casted to str at the end.
        """
        # only in V4
        if self.formver < 4:
            return attr_type(INFORMED_MISSINGNESS)

        if not self.uds.is_initial() and self.uds.get_value(nwinf_field, int) == 0:
            ignore_current_value = True
        else:
            ignore_current_value = False

        return self.handle_prev_visit(
            field,
            attr_type,
            prev_code=attr_type(prev_code),
            default=attr_type(INFORMED_MISSINGNESS),
            ignore_current_value=ignore_current_value,
        )

    ###########################
    # Year of birth variables #
    ###########################

    def _missingness_momyob(self) -> int:
        """Handles missingness for MOMYOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "momyob", int, prev_code=6666)

    def _missingness_dadyob(self) -> int:
        """Handles missingness for DADYOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "dadyob", int, prev_code=6666)

    def _missingness_sib1yob(self) -> int:
        """Handles missingness for SIB1YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib1yob", int, prev_code=6666)

    def _missingness_sib2yob(self) -> int:
        """Handles missingness for SIB2YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib2yob", int, prev_code=6666)

    def _missingness_sib3yob(self) -> int:
        """Handles missingness for SIB3YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib3yob", int, prev_code=6666)

    def _missingness_sib4yob(self) -> int:
        """Handles missingness for SIB4YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib4yob", int, prev_code=6666)

    def _missingness_sib5yob(self) -> int:
        """Handles missingness for SIB5YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib5yob", int, prev_code=6666)

    def _missingness_sib6yob(self) -> int:
        """Handles missingness for SIB6YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib6yob", int, prev_code=6666)

    def _missingness_sib7yob(self) -> int:
        """Handles missingness for SIB7YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib7yob", int, prev_code=6666)

    def _missingness_sib8yob(self) -> int:
        """Handles missingness for SIB8YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib8yob", int, prev_code=6666)

    def _missingness_sib9yob(self) -> int:
        """Handles missingness for SIB9YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib9yob", int, prev_code=6666)

    def _missingness_sib10yob(self) -> int:
        """Handles missingness for SIB10YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib10yob", int, prev_code=6666)

    def _missingness_sib11yob(self) -> int:
        """Handles missingness for SIB11YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib11yob", int, prev_code=6666)

    def _missingness_sib12yob(self) -> int:
        """Handles missingness for SIB12YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib12yob", int, prev_code=6666)

    def _missingness_sib13yob(self) -> int:
        """Handles missingness for SIB13YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib13yob", int, prev_code=6666)

    def _missingness_sib14yob(self) -> int:
        """Handles missingness for SIB14YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib14yob", int, prev_code=6666)

    def _missingness_sib15yob(self) -> int:
        """Handles missingness for SIB15YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib15yob", int, prev_code=6666)

    def _missingness_sib16yob(self) -> int:
        """Handles missingness for SIB16YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib16yob", int, prev_code=6666)

    def _missingness_sib17yob(self) -> int:
        """Handles missingness for SIB17YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib17yob", int, prev_code=6666)

    def _missingness_sib18yob(self) -> int:
        """Handles missingness for SIB18YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib18yob", int, prev_code=6666)

    def _missingness_sib19yob(self) -> int:
        """Handles missingness for SIB19YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib19yob", int, prev_code=6666)

    def _missingness_sib20yob(self) -> int:
        """Handles missingness for SIB20YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib20yob", int, prev_code=6666)

    def _missingness_kid1yob(self) -> int:
        """Handles missingness for KID1YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid1yob", int, prev_code=6666)

    def _missingness_kid2yob(self) -> int:
        """Handles missingness for KID2YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid2yob", int, prev_code=6666)

    def _missingness_kid3yob(self) -> int:
        """Handles missingness for KID3YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid3yob", int, prev_code=6666)

    def _missingness_kid4yob(self) -> int:
        """Handles missingness for KID4YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid4yob", int, prev_code=6666)

    def _missingness_kid5yob(self) -> int:
        """Handles missingness for KID5YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid5yob", int, prev_code=6666)

    def _missingness_kid6yob(self) -> int:
        """Handles missingness for KID6YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid6yob", int, prev_code=6666)

    def _missingness_kid7yob(self) -> int:
        """Handles missingness for KID7YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid7yob", int, prev_code=6666)

    def _missingness_kid8yob(self) -> int:
        """Handles missingness for KID8YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid8yob", int, prev_code=6666)

    def _missingness_kid9yob(self) -> int:
        """Handles missingness for KID9YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid9yob", int, prev_code=6666)

    def _missingness_kid10yob(self) -> int:
        """Handles missingness for KID10YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid10yob", int, prev_code=6666)

    def _missingness_kid11yob(self) -> int:
        """Handles missingness for KID11YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid11yob", int, prev_code=6666)

    def _missingness_kid12yob(self) -> int:
        """Handles missingness for KID12YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid12yob", int, prev_code=6666)

    def _missingness_kid13yob(self) -> int:
        """Handles missingness for KID13YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid13yob", int, prev_code=6666)

    def _missingness_kid14yob(self) -> int:
        """Handles missingness for KID14YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid14yob", int, prev_code=6666)

    def _missingness_kid15yob(self) -> int:
        """Handles missingness for KID15YOB."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid15yob", int, prev_code=6666)

    ##########################
    # Age of death variables #
    ##########################

    def _missingness_momdage(self) -> int:
        """Handles missingness for MOMDAGE."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "momdage", int, prev_code=666)

    def _missingness_daddage(self) -> int:
        """Handles missingness for DADDAGE."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "daddage", int, prev_code=666)

    def _missingness_sib1agd(self) -> int:
        """Handles missingness for SIB1AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib1agd", int, prev_code=666)

    def _missingness_sib2agd(self) -> int:
        """Handles missingness for SIB2AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib2agd", int, prev_code=666)

    def _missingness_sib3agd(self) -> int:
        """Handles missingness for SIB3AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib3agd", int, prev_code=666)

    def _missingness_sib4agd(self) -> int:
        """Handles missingness for SIB4AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib4agd", int, prev_code=666)

    def _missingness_sib5agd(self) -> int:
        """Handles missingness for SIB5AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib5agd", int, prev_code=666)

    def _missingness_sib6agd(self) -> int:
        """Handles missingness for SIB6AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib6agd", int, prev_code=666)

    def _missingness_sib7agd(self) -> int:
        """Handles missingness for SIB7AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib7agd", int, prev_code=666)

    def _missingness_sib8agd(self) -> int:
        """Handles missingness for SIB8AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib8agd", int, prev_code=666)

    def _missingness_sib9agd(self) -> int:
        """Handles missingness for SIB9AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib9agd", int, prev_code=666)

    def _missingness_sib10agd(self) -> int:
        """Handles missingness for SIB10AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib10agd", int, prev_code=666)

    def _missingness_sib11agd(self) -> int:
        """Handles missingness for SIB11AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib11agd", int, prev_code=666)

    def _missingness_sib12agd(self) -> int:
        """Handles missingness for SIB12AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib12agd", int, prev_code=666)

    def _missingness_sib13agd(self) -> int:
        """Handles missingness for SIB13AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib13agd", int, prev_code=666)

    def _missingness_sib14agd(self) -> int:
        """Handles missingness for SIB14AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib14agd", int, prev_code=666)

    def _missingness_sib15agd(self) -> int:
        """Handles missingness for SIB15AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib15agd", int, prev_code=666)

    def _missingness_sib16agd(self) -> int:
        """Handles missingness for SIB16AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib16agd", int, prev_code=666)

    def _missingness_sib17agd(self) -> int:
        """Handles missingness for SIB17AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib17agd", int, prev_code=666)

    def _missingness_sib18agd(self) -> int:
        """Handles missingness for SIB18AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib18agd", int, prev_code=666)

    def _missingness_sib19agd(self) -> int:
        """Handles missingness for SIB19AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib19agd", int, prev_code=666)

    def _missingness_sib20agd(self) -> int:
        """Handles missingness for SIB20AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib20agd", int, prev_code=666)

    def _missingness_kid1agd(self) -> int:
        """Handles missingness for KID1AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid1agd", int, prev_code=666)

    def _missingness_kid2agd(self) -> int:
        """Handles missingness for KID2AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid2agd", int, prev_code=666)

    def _missingness_kid3agd(self) -> int:
        """Handles missingness for KID3AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid3agd", int, prev_code=666)

    def _missingness_kid4agd(self) -> int:
        """Handles missingness for KID4AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid4agd", int, prev_code=666)

    def _missingness_kid5agd(self) -> int:
        """Handles missingness for KID5AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid5agd", int, prev_code=666)

    def _missingness_kid6agd(self) -> int:
        """Handles missingness for KID6AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid6agd", int, prev_code=666)

    def _missingness_kid7agd(self) -> int:
        """Handles missingness for KID7AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid7agd", int, prev_code=666)

    def _missingness_kid8agd(self) -> int:
        """Handles missingness for KID8AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid8agd", int, prev_code=666)

    def _missingness_kid9agd(self) -> int:
        """Handles missingness for KID9AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid9agd", int, prev_code=666)

    def _missingness_kid10agd(self) -> int:
        """Handles missingness for KID10AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid10agd", int, prev_code=666)

    def _missingness_kid11agd(self) -> int:
        """Handles missingness for KID11AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid11agd", int, prev_code=666)

    def _missingness_kid12agd(self) -> int:
        """Handles missingness for KID12AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid12agd", int, prev_code=666)

    def _missingness_kid13agd(self) -> int:
        """Handles missingness for KID13AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid13agd", int, prev_code=666)

    def _missingness_kid14agd(self) -> int:
        """Handles missingness for KID14AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid14agd", int, prev_code=666)

    def _missingness_kid15agd(self) -> int:
        """Handles missingness for KID15AGD."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid15agd", int, prev_code=666)

    ########################
    # Primary dx variables #
    ########################

    def _missingness_mometpr(self) -> str:
        """Handles missingness for MOMETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "mometpr", str, prev_code=66)

    def _missingness_dadetpr(self) -> str:
        """Handles missingness for DADETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "dadetpr", str, prev_code=66)

    def _missingness_sib1etpr(self) -> str:
        """Handles missingness for SIB1ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib1etpr", str, prev_code=66)

    def _missingness_sib2etpr(self) -> str:
        """Handles missingness for SIB2ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib2etpr", str, prev_code=66)

    def _missingness_sib3etpr(self) -> str:
        """Handles missingness for SIB3ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib3etpr", str, prev_code=66)

    def _missingness_sib4etpr(self) -> str:
        """Handles missingness for SIB4ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib4etpr", str, prev_code=66)

    def _missingness_sib5etpr(self) -> str:
        """Handles missingness for SIB5ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib5etpr", str, prev_code=66)

    def _missingness_sib6etpr(self) -> str:
        """Handles missingness for SIB6ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib6etpr", str, prev_code=66)

    def _missingness_sib7etpr(self) -> str:
        """Handles missingness for SIB7ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib7etpr", str, prev_code=66)

    def _missingness_sib8etpr(self) -> str:
        """Handles missingness for SIB8ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib8etpr", str, prev_code=66)

    def _missingness_sib9etpr(self) -> str:
        """Handles missingness for SIB9ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib9etpr", str, prev_code=66)

    def _missingness_sib10etpr(self) -> str:
        """Handles missingness for SIB10ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib10etpr", str, prev_code=66)

    def _missingness_sib11etpr(self) -> str:
        """Handles missingness for SIB11ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib11etpr", str, prev_code=66)

    def _missingness_sib12etpr(self) -> str:
        """Handles missingness for SIB12ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib12etpr", str, prev_code=66)

    def _missingness_sib13etpr(self) -> str:
        """Handles missingness for SIB13ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib13etpr", str, prev_code=66)

    def _missingness_sib14etpr(self) -> str:
        """Handles missingness for SIB14ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib14etpr", str, prev_code=66)

    def _missingness_sib15etpr(self) -> str:
        """Handles missingness for SIB15ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib15etpr", str, prev_code=66)

    def _missingness_sib16etpr(self) -> str:
        """Handles missingness for SIB16ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib16etpr", str, prev_code=66)

    def _missingness_sib17etpr(self) -> str:
        """Handles missingness for SIB17ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib17etpr", str, prev_code=66)

    def _missingness_sib18etpr(self) -> str:
        """Handles missingness for SIB18ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib18etpr", str, prev_code=66)

    def _missingness_sib19etpr(self) -> str:
        """Handles missingness for SIB19ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib19etpr", str, prev_code=66)

    def _missingness_sib20etpr(self) -> str:
        """Handles missingness for SIB20ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib20etpr", str, prev_code=66)

    def _missingness_kid1etpr(self) -> str:
        """Handles missingness for KID1ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid1etpr", str, prev_code=66)

    def _missingness_kid2etpr(self) -> str:
        """Handles missingness for KID2ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid2etpr", str, prev_code=66)

    def _missingness_kid3etpr(self) -> str:
        """Handles missingness for KID3ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid3etpr", str, prev_code=66)

    def _missingness_kid4etpr(self) -> str:
        """Handles missingness for KID4ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid4etpr", str, prev_code=66)

    def _missingness_kid5etpr(self) -> str:
        """Handles missingness for KID5ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid5etpr", str, prev_code=66)

    def _missingness_kid6etpr(self) -> str:
        """Handles missingness for KID6ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid6etpr", str, prev_code=66)

    def _missingness_kid7etpr(self) -> str:
        """Handles missingness for KID7ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid7etpr", str, prev_code=66)

    def _missingness_kid8etpr(self) -> str:
        """Handles missingness for KID8ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid8etpr", str, prev_code=66)

    def _missingness_kid9etpr(self) -> str:
        """Handles missingness for KID9ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid9etpr", str, prev_code=66)

    def _missingness_kid10etpr(self) -> str:
        """Handles missingness for KID10ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid10etpr", str, prev_code=66)

    def _missingness_kid11etpr(self) -> str:
        """Handles missingness for KID11ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid11etpr", str, prev_code=66)

    def _missingness_kid12etpr(self) -> str:
        """Handles missingness for KID12ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid12etpr", str, prev_code=66)

    def _missingness_kid13etpr(self) -> str:
        """Handles missingness for KID13ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid13etpr", str, prev_code=66)

    def _missingness_kid14etpr(self) -> str:
        """Handles missingness for KID14ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid14etpr", str, prev_code=66)

    def _missingness_kid15etpr(self) -> str:
        """Handles missingness for KID15ETPR."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid15etpr", str, prev_code=66)

    ##########################
    # Secondary dx variables #
    ##########################

    def _missingness_mometsec(self) -> str:
        """Handles missingness for MOMETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "mometsec", str, prev_code=66)

    def _missingness_dadetsec(self) -> str:
        """Handles missingness for DADETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "dadetsec", str, prev_code=66)

    def _missingness_sib1etsec(self) -> str:
        """Handles missingness for SIB1ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib1etsec", str, prev_code=66)

    def _missingness_sib2etsec(self) -> str:
        """Handles missingness for SIB2ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib2etsec", str, prev_code=66)

    def _missingness_sib3etsec(self) -> str:
        """Handles missingness for SIB3ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib3etsec", str, prev_code=66)

    def _missingness_sib4etsec(self) -> str:
        """Handles missingness for SIB4ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib4etsec", str, prev_code=66)

    def _missingness_sib5etsec(self) -> str:
        """Handles missingness for SIB5ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib5etsec", str, prev_code=66)

    def _missingness_sib6etsec(self) -> str:
        """Handles missingness for SIB6ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib6etsec", str, prev_code=66)

    def _missingness_sib7etsec(self) -> str:
        """Handles missingness for SIB7ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib7etsec", str, prev_code=66)

    def _missingness_sib8etsec(self) -> str:
        """Handles missingness for SIB8ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib8etsec", str, prev_code=66)

    def _missingness_sib9etsec(self) -> str:
        """Handles missingness for SIB9ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib9etsec", str, prev_code=66)

    def _missingness_sib10etsec(self) -> str:
        """Handles missingness for SIB10ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib10etsec", str, prev_code=66)

    def _missingness_sib11etsec(self) -> str:
        """Handles missingness for SIB11ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib11etsec", str, prev_code=66)

    def _missingness_sib12etsec(self) -> str:
        """Handles missingness for SIB12ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib12etsec", str, prev_code=66)

    def _missingness_sib13etsec(self) -> str:
        """Handles missingness for SIB13ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib13etsec", str, prev_code=66)

    def _missingness_sib14etsec(self) -> str:
        """Handles missingness for SIB14ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib14etsec", str, prev_code=66)

    def _missingness_sib15etsec(self) -> str:
        """Handles missingness for SIB15ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib15etsec", str, prev_code=66)

    def _missingness_sib16etsec(self) -> str:
        """Handles missingness for SIB16ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib16etsec", str, prev_code=66)

    def _missingness_sib17etsec(self) -> str:
        """Handles missingness for SIB17ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib17etsec", str, prev_code=66)

    def _missingness_sib18etsec(self) -> str:
        """Handles missingness for SIB18ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib18etsec", str, prev_code=66)

    def _missingness_sib19etsec(self) -> str:
        """Handles missingness for SIB19ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib19etsec", str, prev_code=66)

    def _missingness_sib20etsec(self) -> str:
        """Handles missingness for SIB20ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib20etsec", str, prev_code=66)

    def _missingness_kid1etsec(self) -> str:
        """Handles missingness for KID1ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid1etsec", str, prev_code=66)

    def _missingness_kid2etsec(self) -> str:
        """Handles missingness for KID2ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid2etsec", str, prev_code=66)

    def _missingness_kid3etsec(self) -> str:
        """Handles missingness for KID3ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid3etsec", str, prev_code=66)

    def _missingness_kid4etsec(self) -> str:
        """Handles missingness for KID4ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid4etsec", str, prev_code=66)

    def _missingness_kid5etsec(self) -> str:
        """Handles missingness for KID5ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid5etsec", str, prev_code=66)

    def _missingness_kid6etsec(self) -> str:
        """Handles missingness for KID6ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid6etsec", str, prev_code=66)

    def _missingness_kid7etsec(self) -> str:
        """Handles missingness for KID7ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid7etsec", str, prev_code=66)

    def _missingness_kid8etsec(self) -> str:
        """Handles missingness for KID8ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid8etsec", str, prev_code=66)

    def _missingness_kid9etsec(self) -> str:
        """Handles missingness for KID9ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid9etsec", str, prev_code=66)

    def _missingness_kid10etsec(self) -> str:
        """Handles missingness for KID10ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid10etsec", str, prev_code=66)

    def _missingness_kid11etsec(self) -> str:
        """Handles missingness for KID11ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid11etsec", str, prev_code=66)

    def _missingness_kid12etsec(self) -> str:
        """Handles missingness for KID12ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid12etsec", str, prev_code=66)

    def _missingness_kid13etsec(self) -> str:
        """Handles missingness for KID13ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid13etsec", str, prev_code=66)

    def _missingness_kid14etsec(self) -> str:
        """Handles missingness for KID14ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid14etsec", str, prev_code=66)

    def _missingness_kid15etsec(self) -> str:
        """Handles missingness for KID15ETSEC."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid15etsec", str, prev_code=66)

    ##################################
    # Method of evaluation variables #
    ##################################

    def _missingness_mommeval(self) -> int:
        """Handles missingness for MOMMEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "mommeval", int, prev_code=6)

    def _missingness_dadmeval(self) -> int:
        """Handles missingness for DADMEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "dadmeval", int, prev_code=6)

    def _missingness_sib1meval(self) -> int:
        """Handles missingness for SIB1MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib1meval", int, prev_code=6)

    def _missingness_sib2meval(self) -> int:
        """Handles missingness for SIB2MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib2meval", int, prev_code=6)

    def _missingness_sib3meval(self) -> int:
        """Handles missingness for SIB3MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib3meval", int, prev_code=6)

    def _missingness_sib4meval(self) -> int:
        """Handles missingness for SIB4MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib4meval", int, prev_code=6)

    def _missingness_sib5meval(self) -> int:
        """Handles missingness for SIB5MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib5meval", int, prev_code=6)

    def _missingness_sib6meval(self) -> int:
        """Handles missingness for SIB6MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib6meval", int, prev_code=6)

    def _missingness_sib7meval(self) -> int:
        """Handles missingness for SIB7MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib7meval", int, prev_code=6)

    def _missingness_sib8meval(self) -> int:
        """Handles missingness for SIB8MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib8meval", int, prev_code=6)

    def _missingness_sib9meval(self) -> int:
        """Handles missingness for SIB9MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib9meval", int, prev_code=6)

    def _missingness_sib10meval(self) -> int:
        """Handles missingness for SIB10MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib10meval", int, prev_code=6)

    def _missingness_sib11meval(self) -> int:
        """Handles missingness for SIB11MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib11meval", int, prev_code=6)

    def _missingness_sib12meval(self) -> int:
        """Handles missingness for SIB12MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib12meval", int, prev_code=6)

    def _missingness_sib13meval(self) -> int:
        """Handles missingness for SIB13MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib13meval", int, prev_code=6)

    def _missingness_sib14meval(self) -> int:
        """Handles missingness for SIB14MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib14meval", int, prev_code=6)

    def _missingness_sib15meval(self) -> int:
        """Handles missingness for SIB15MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib15meval", int, prev_code=6)

    def _missingness_sib16meval(self) -> int:
        """Handles missingness for SIB16MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib16meval", int, prev_code=6)

    def _missingness_sib17meval(self) -> int:
        """Handles missingness for SIB17MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib17meval", int, prev_code=6)

    def _missingness_sib18meval(self) -> int:
        """Handles missingness for SIB18MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib18meval", int, prev_code=6)

    def _missingness_sib19meval(self) -> int:
        """Handles missingness for SIB19MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib19meval", int, prev_code=6)

    def _missingness_sib20meval(self) -> int:
        """Handles missingness for SIB20MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib20meval", int, prev_code=6)

    def _missingness_kid1meval(self) -> int:
        """Handles missingness for KID1MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid1meval", int, prev_code=6)

    def _missingness_kid2meval(self) -> int:
        """Handles missingness for KID2MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid2meval", int, prev_code=6)

    def _missingness_kid3meval(self) -> int:
        """Handles missingness for KID3MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid3meval", int, prev_code=6)

    def _missingness_kid4meval(self) -> int:
        """Handles missingness for KID4MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid4meval", int, prev_code=6)

    def _missingness_kid5meval(self) -> int:
        """Handles missingness for KID5MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid5meval", int, prev_code=6)

    def _missingness_kid6meval(self) -> int:
        """Handles missingness for KID6MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid6meval", int, prev_code=6)

    def _missingness_kid7meval(self) -> int:
        """Handles missingness for KID7MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid7meval", int, prev_code=6)

    def _missingness_kid8meval(self) -> int:
        """Handles missingness for KID8MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid8meval", int, prev_code=6)

    def _missingness_kid9meval(self) -> int:
        """Handles missingness for KID9MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid9meval", int, prev_code=6)

    def _missingness_kid10meval(self) -> int:
        """Handles missingness for KID10MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid10meval", int, prev_code=6)

    def _missingness_kid11meval(self) -> int:
        """Handles missingness for KID11MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid11meval", int, prev_code=6)

    def _missingness_kid12meval(self) -> int:
        """Handles missingness for KID12MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid12meval", int, prev_code=6)

    def _missingness_kid13meval(self) -> int:
        """Handles missingness for KID13MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid13meval", int, prev_code=6)

    def _missingness_kid14meval(self) -> int:
        """Handles missingness for KID14MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid14meval", int, prev_code=6)

    def _missingness_kid15meval(self) -> int:
        """Handles missingness for KID15MEVAL."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid15meval", int, prev_code=6)

    ########################################
    # Age of onset of primary dx variables #
    ########################################

    def _missingness_momageo(self) -> int:
        """Handles missingness for MOMAGEO."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "momageo", int, prev_code=666)

    def _missingness_dadageo(self) -> int:
        """Handles missingness for DADAGEO."""
        return self.__handle_a3_prev_visit_missingness("nwinfpar", "dadageo", int, prev_code=666)

    def _missingness_sib1ago(self) -> int:
        """Handles missingness for SIB1AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib1ago", int, prev_code=666)

    def _missingness_sib2ago(self) -> int:
        """Handles missingness for SIB2AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib2ago", int, prev_code=666)

    def _missingness_sib3ago(self) -> int:
        """Handles missingness for SIB3AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib3ago", int, prev_code=666)

    def _missingness_sib4ago(self) -> int:
        """Handles missingness for SIB4AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib4ago", int, prev_code=666)

    def _missingness_sib5ago(self) -> int:
        """Handles missingness for SIB5AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib5ago", int, prev_code=666)

    def _missingness_sib6ago(self) -> int:
        """Handles missingness for SIB6AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib6ago", int, prev_code=666)

    def _missingness_sib7ago(self) -> int:
        """Handles missingness for SIB7AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib7ago", int, prev_code=666)

    def _missingness_sib8ago(self) -> int:
        """Handles missingness for SIB8AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib8ago", int, prev_code=666)

    def _missingness_sib9ago(self) -> int:
        """Handles missingness for SIB9AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib9ago", int, prev_code=666)

    def _missingness_sib10ago(self) -> int:
        """Handles missingness for SIB10AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib10ago", int, prev_code=666)

    def _missingness_sib11ago(self) -> int:
        """Handles missingness for SIB11AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib11ago", int, prev_code=666)

    def _missingness_sib12ago(self) -> int:
        """Handles missingness for SIB12AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib12ago", int, prev_code=666)

    def _missingness_sib13ago(self) -> int:
        """Handles missingness for SIB13AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib13ago", int, prev_code=666)

    def _missingness_sib14ago(self) -> int:
        """Handles missingness for SIB14AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib14ago", int, prev_code=666)

    def _missingness_sib15ago(self) -> int:
        """Handles missingness for SIB15AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib15ago", int, prev_code=666)

    def _missingness_sib16ago(self) -> int:
        """Handles missingness for SIB16AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib16ago", int, prev_code=666)

    def _missingness_sib17ago(self) -> int:
        """Handles missingness for SIB17AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib17ago", int, prev_code=666)

    def _missingness_sib18ago(self) -> int:
        """Handles missingness for SIB18AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib18ago", int, prev_code=666)

    def _missingness_sib19ago(self) -> int:
        """Handles missingness for SIB19AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib19ago", int, prev_code=666)

    def _missingness_sib20ago(self) -> int:
        """Handles missingness for SIB20AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfsib", "sib20ago", int, prev_code=666)

    def _missingness_kid1ago(self) -> int:
        """Handles missingness for KID1AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid1ago", int, prev_code=666)

    def _missingness_kid2ago(self) -> int:
        """Handles missingness for KID2AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid2ago", int, prev_code=666)

    def _missingness_kid3ago(self) -> int:
        """Handles missingness for KID3AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid3ago", int, prev_code=666)

    def _missingness_kid4ago(self) -> int:
        """Handles missingness for KID4AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid4ago", int, prev_code=666)

    def _missingness_kid5ago(self) -> int:
        """Handles missingness for KID5AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid5ago", int, prev_code=666)

    def _missingness_kid6ago(self) -> int:
        """Handles missingness for KID6AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid6ago", int, prev_code=666)

    def _missingness_kid7ago(self) -> int:
        """Handles missingness for KID7AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid7ago", int, prev_code=666)

    def _missingness_kid8ago(self) -> int:
        """Handles missingness for KID8AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid8ago", int, prev_code=666)

    def _missingness_kid9ago(self) -> int:
        """Handles missingness for KID9AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid9ago", int, prev_code=666)

    def _missingness_kid10ago(self) -> int:
        """Handles missingness for KID10AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid10ago", int, prev_code=666)

    def _missingness_kid11ago(self) -> int:
        """Handles missingness for KID11AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid11ago", int, prev_code=666)

    def _missingness_kid12ago(self) -> int:
        """Handles missingness for KID12AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid12ago", int, prev_code=666)

    def _missingness_kid13ago(self) -> int:
        """Handles missingness for KID13AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid13ago", int, prev_code=666)

    def _missingness_kid14ago(self) -> int:
        """Handles missingness for KID14AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid14ago", int, prev_code=666)

    def _missingness_kid15ago(self) -> int:
        """Handles missingness for KID15AGO."""
        return self.__handle_a3_prev_visit_missingness("nwinfkid", "kid15ago", int, prev_code=666)
