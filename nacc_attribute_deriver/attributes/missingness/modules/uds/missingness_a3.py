"""Class to handle A3-specific missingness values.

While not explicitly pushed to the QAFs, are necessary to keep track of
for calculationss of derived variables. There are other variables that
specify prev codes to pull through, but are not currently handled at the
moment since nothing is explicitly looking at them.
"""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.utils.constants import (
    INFORMED_MISSINGNESS,
)


class UDSFormA3Missingness(UDSMissingness):
    def __handle_etpr_missingness(self, nwinf_field: str, field: str) -> str:
        """Handles ETPR missingness.

        66 is the "provided at previous visit code", so if indicated
        we must pull forward the value from the previous visit.
        Similarly if no new info is provided (assured blank when NWINF
        variables = 0), then we also need to pull through the previous
        visit.

        In short, if we see 66 or NWINFx = 0, then pull through the
        previous value.

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
        return self.__handle_etpr_missingness("nwinfpar", "mometpr")

    def _missingness_dadetpr(self) -> str:
        """Handles missingness for DADETPR."""
        return self.__handle_etpr_missingness("nwinfpar", "dadetpr")

    def _missingness_sib1etpr(self) -> str:
        """Handles missingness for SIB1ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib1etpr")

    def _missingness_sib2etpr(self) -> str:
        """Handles missingness for SIB2ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib2etpr")

    def _missingness_sib3etpr(self) -> str:
        """Handles missingness for SIB3ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib3etpr")

    def _missingness_sib4etpr(self) -> str:
        """Handles missingness for SIB4ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib4etpr")

    def _missingness_sib5etpr(self) -> str:
        """Handles missingness for SIB5ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib5etpr")

    def _missingness_sib6etpr(self) -> str:
        """Handles missingness for SIB6ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib6etpr")

    def _missingness_sib7etpr(self) -> str:
        """Handles missingness for SIB7ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib7etpr")

    def _missingness_sib8etpr(self) -> str:
        """Handles missingness for SIB8ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib8etpr")

    def _missingness_sib9etpr(self) -> str:
        """Handles missingness for SIB9ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib9etpr")

    def _missingness_sib10etpr(self) -> str:
        """Handles missingness for SIB10ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib10etpr")

    def _missingness_sib11etpr(self) -> str:
        """Handles missingness for SIB11ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib11etpr")

    def _missingness_sib12etpr(self) -> str:
        """Handles missingness for SIB12ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib12etpr")

    def _missingness_sib13etpr(self) -> str:
        """Handles missingness for SIB13ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib13etpr")

    def _missingness_sib14etpr(self) -> str:
        """Handles missingness for SIB14ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib14etpr")

    def _missingness_sib15etpr(self) -> str:
        """Handles missingness for SIB15ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib15etpr")

    def _missingness_sib16etpr(self) -> str:
        """Handles missingness for SIB16ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib16etpr")

    def _missingness_sib17etpr(self) -> str:
        """Handles missingness for SIB17ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib17etpr")

    def _missingness_sib18etpr(self) -> str:
        """Handles missingness for SIB18ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib18etpr")

    def _missingness_sib19etpr(self) -> str:
        """Handles missingness for SIB19ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib19etpr")

    def _missingness_sib20etpr(self) -> str:
        """Handles missingness for SIB20ETPR."""
        return self.__handle_etpr_missingness("nwinfsib", "sib20etpr")

    def _missingness_kid1etpr(self) -> str:
        """Handles missingness for KID1ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid1etpr")

    def _missingness_kid2etpr(self) -> str:
        """Handles missingness for KID2ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid2etpr")

    def _missingness_kid3etpr(self) -> str:
        """Handles missingness for KID3ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid3etpr")

    def _missingness_kid4etpr(self) -> str:
        """Handles missingness for KID4ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid4etpr")

    def _missingness_kid5etpr(self) -> str:
        """Handles missingness for KID5ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid5etpr")

    def _missingness_kid6etpr(self) -> str:
        """Handles missingness for KID6ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid6etpr")

    def _missingness_kid7etpr(self) -> str:
        """Handles missingness for KID7ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid7etpr")

    def _missingness_kid8etpr(self) -> str:
        """Handles missingness for KID8ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid8etpr")

    def _missingness_kid9etpr(self) -> str:
        """Handles missingness for KID9ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid9etpr")

    def _missingness_kid10etpr(self) -> str:
        """Handles missingness for KID10ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid10etpr")

    def _missingness_kid11etpr(self) -> str:
        """Handles missingness for KID11ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid11etpr")

    def _missingness_kid12etpr(self) -> str:
        """Handles missingness for KID12ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid12etpr")

    def _missingness_kid13etpr(self) -> str:
        """Handles missingness for KID13ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid13etpr")

    def _missingness_kid14etpr(self) -> str:
        """Handles missingness for KID14ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid14etpr")

    def _missingness_kid15etpr(self) -> str:
        """Handles missingness for KID15ETPR."""
        return self.__handle_etpr_missingness("nwinfkid", "kid15etpr")
