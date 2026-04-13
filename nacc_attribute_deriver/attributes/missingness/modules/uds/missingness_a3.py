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

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)


class UDSFormA3Missingness(UDSMissingness):
    def __handle_str_prev_missingness_code_v4(
        self, nwinf_field: str, field: str, prev_code: str = '66') -> str:
        """Handles "provided at previous visit" missingness for *ETPR and
        *ETSEC variables, which are int-like strings.

        Set default to -4 instead of blanks since even though these
        are strings, they're not write-ins.
        """
        # only in V4
        if self.formver < 4:
            return str(INFORMED_MISSINGNESS)

        if not self.uds.is_initial() and self.uds.get_value(nwinf_field, int) == 0:
            ignore_current_value = True
        else:
            ignore_current_value = False

        return self.handle_prev_visit(
            field,
            str,
            prev_code="66",
            default=str(INFORMED_MISSINGNESS),
            ignore_current_value=ignore_current_value,
        )

    def _missingness_mometpr(self) -> str:
        """Handles missingness for MOMETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfpar", "mometpr")

    def _missingness_dadetpr(self) -> str:
        """Handles missingness for DADETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfpar", "dadetpr")

    def _missingness_sib1etpr(self) -> str:
        """Handles missingness for SIB1ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib1etpr")

    def _missingness_sib2etpr(self) -> str:
        """Handles missingness for SIB2ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib2etpr")

    def _missingness_sib3etpr(self) -> str:
        """Handles missingness for SIB3ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib3etpr")

    def _missingness_sib4etpr(self) -> str:
        """Handles missingness for SIB4ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib4etpr")

    def _missingness_sib5etpr(self) -> str:
        """Handles missingness for SIB5ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib5etpr")

    def _missingness_sib6etpr(self) -> str:
        """Handles missingness for SIB6ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib6etpr")

    def _missingness_sib7etpr(self) -> str:
        """Handles missingness for SIB7ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib7etpr")

    def _missingness_sib8etpr(self) -> str:
        """Handles missingness for SIB8ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib8etpr")

    def _missingness_sib9etpr(self) -> str:
        """Handles missingness for SIB9ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib9etpr")

    def _missingness_sib10etpr(self) -> str:
        """Handles missingness for SIB10ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib10etpr")

    def _missingness_sib11etpr(self) -> str:
        """Handles missingness for SIB11ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib11etpr")

    def _missingness_sib12etpr(self) -> str:
        """Handles missingness for SIB12ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib12etpr")

    def _missingness_sib13etpr(self) -> str:
        """Handles missingness for SIB13ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib13etpr")

    def _missingness_sib14etpr(self) -> str:
        """Handles missingness for SIB14ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib14etpr")

    def _missingness_sib15etpr(self) -> str:
        """Handles missingness for SIB15ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib15etpr")

    def _missingness_sib16etpr(self) -> str:
        """Handles missingness for SIB16ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib16etpr")

    def _missingness_sib17etpr(self) -> str:
        """Handles missingness for SIB17ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib17etpr")

    def _missingness_sib18etpr(self) -> str:
        """Handles missingness for SIB18ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib18etpr")

    def _missingness_sib19etpr(self) -> str:
        """Handles missingness for SIB19ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib19etpr")

    def _missingness_sib20etpr(self) -> str:
        """Handles missingness for SIB20ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib20etpr")

    def _missingness_kid1etpr(self) -> str:
        """Handles missingness for KID1ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid1etpr")

    def _missingness_kid2etpr(self) -> str:
        """Handles missingness for KID2ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid2etpr")

    def _missingness_kid3etpr(self) -> str:
        """Handles missingness for KID3ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid3etpr")

    def _missingness_kid4etpr(self) -> str:
        """Handles missingness for KID4ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid4etpr")

    def _missingness_kid5etpr(self) -> str:
        """Handles missingness for KID5ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid5etpr")

    def _missingness_kid6etpr(self) -> str:
        """Handles missingness for KID6ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid6etpr")

    def _missingness_kid7etpr(self) -> str:
        """Handles missingness for KID7ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid7etpr")

    def _missingness_kid8etpr(self) -> str:
        """Handles missingness for KID8ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid8etpr")

    def _missingness_kid9etpr(self) -> str:
        """Handles missingness for KID9ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid9etpr")

    def _missingness_kid10etpr(self) -> str:
        """Handles missingness for KID10ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid10etpr")

    def _missingness_kid11etpr(self) -> str:
        """Handles missingness for KID11ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid11etpr")

    def _missingness_kid12etpr(self) -> str:
        """Handles missingness for KID12ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid12etpr")

    def _missingness_kid13etpr(self) -> str:
        """Handles missingness for KID13ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid13etpr")

    def _missingness_kid14etpr(self) -> str:
        """Handles missingness for KID14ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid14etpr")

    def _missingness_kid15etpr(self) -> str:
        """Handles missingness for KID15ETPR."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid15etpr")

    def _missingness_mometsec(self) -> str:
        """Handles missingness for MOMETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfpar", "mometsec")

    def _missingness_dadetsec(self) -> str:
        """Handles missingness for DADETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfpar", "dadetsec")

    def _missingness_sib1etsec(self) -> str:
        """Handles missingness for SIB1ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib1etsec")

    def _missingness_sib2etsec(self) -> str:
        """Handles missingness for SIB2ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib2etsec")

    def _missingness_sib3etsec(self) -> str:
        """Handles missingness for SIB3ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib3etsec")

    def _missingness_sib4etsec(self) -> str:
        """Handles missingness for SIB4ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib4etsec")

    def _missingness_sib5etsec(self) -> str:
        """Handles missingness for SIB5ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib5etsec")

    def _missingness_sib6etsec(self) -> str:
        """Handles missingness for SIB6ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib6etsec")

    def _missingness_sib7etsec(self) -> str:
        """Handles missingness for SIB7ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib7etsec")

    def _missingness_sib8etsec(self) -> str:
        """Handles missingness for SIB8ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib8etsec")

    def _missingness_sib9etsec(self) -> str:
        """Handles missingness for SIB9ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib9etsec")

    def _missingness_sib10etsec(self) -> str:
        """Handles missingness for SIB10ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib10etsec")

    def _missingness_sib11etsec(self) -> str:
        """Handles missingness for SIB11ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib11etsec")

    def _missingness_sib12etsec(self) -> str:
        """Handles missingness for SIB12ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib12etsec")

    def _missingness_sib13etsec(self) -> str:
        """Handles missingness for SIB13ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib13etsec")

    def _missingness_sib14etsec(self) -> str:
        """Handles missingness for SIB14ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib14etsec")

    def _missingness_sib15etsec(self) -> str:
        """Handles missingness for SIB15ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib15etsec")

    def _missingness_sib16etsec(self) -> str:
        """Handles missingness for SIB16ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib16etsec")

    def _missingness_sib17etsec(self) -> str:
        """Handles missingness for SIB17ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib17etsec")

    def _missingness_sib18etsec(self) -> str:
        """Handles missingness for SIB18ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib18etsec")

    def _missingness_sib19etsec(self) -> str:
        """Handles missingness for SIB19ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib19etsec")

    def _missingness_sib20etsec(self) -> str:
        """Handles missingness for SIB20ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfsib", "sib20etsec")

    def _missingness_kid1etsec(self) -> str:
        """Handles missingness for KID1ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid1etsec")

    def _missingness_kid2etsec(self) -> str:
        """Handles missingness for KID2ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid2etsec")

    def _missingness_kid3etsec(self) -> str:
        """Handles missingness for KID3ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid3etsec")

    def _missingness_kid4etsec(self) -> str:
        """Handles missingness for KID4ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid4etsec")

    def _missingness_kid5etsec(self) -> str:
        """Handles missingness for KID5ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid5etsec")

    def _missingness_kid6etsec(self) -> str:
        """Handles missingness for KID6ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid6etsec")

    def _missingness_kid7etsec(self) -> str:
        """Handles missingness for KID7ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid7etsec")

    def _missingness_kid8etsec(self) -> str:
        """Handles missingness for KID8ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid8etsec")

    def _missingness_kid9etsec(self) -> str:
        """Handles missingness for KID9ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid9etsec")

    def _missingness_kid10etsec(self) -> str:
        """Handles missingness for KID10ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid10etsec")

    def _missingness_kid11etsec(self) -> str:
        """Handles missingness for KID11ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid11etsec")

    def _missingness_kid12etsec(self) -> str:
        """Handles missingness for KID12ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid12etsec")

    def _missingness_kid13etsec(self) -> str:
        """Handles missingness for KID13ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid13etsec")

    def _missingness_kid14etsec(self) -> str:
        """Handles missingness for KID14ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid14etsec")

    def _missingness_kid15etsec(self) -> str:
        """Handles missingness for KID15ETSEC."""
        return self.__handle_str_prev_missingness_code_v4("nwinfkid", "kid15etsec")
