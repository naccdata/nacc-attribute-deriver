"""Class to handle A3-specific missingness values.

While not explicitly pushed to the QAFs, are necessary to keep track of
for calculationss of derived variables. There are other variables that
specify prev codes to pull through, but are not currently handled at the
moment since nothing is explicitly looking at them.
"""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness


class UDSFormA3Missingness(UDSMissingness):
    def __handle_etpr_missingness(self, field: str) -> str:
        """Handles ETPR missingness.

        66 is the "provided at previous visit code", so if indicated
        we must pull forward the value from the previous visit.
        Similarly if no new info is provided (assured blank when NWINF
        variables = 0), then we need to pull through the previous visit.

        In short, if we see 66 or blank, we pull the previous visit
        through.

        Set default to -4 instead of blanks since even though these
        are strings, they're not write-ins.
        """
        return self.handle_prev_visit(field, str, prev_code="66", default="-4")

    def _missingness_mometpr(self) -> str:
        """Handles missingness for MOMETPR."""
        return self.__handle_etpr_missingness("mometpr")

    def _missingness_dadetpr(self) -> str:
        """Handles missingness for DADETPR."""
        return self.__handle_etpr_missingness("dadetpr")

    def _missingness_sib1etpr(self) -> str:
        """Handles missingness for SIB1ETPR."""
        return self.__handle_etpr_missingness("sib1etpr")

    def _missingness_sib2etpr(self) -> str:
        """Handles missingness for SIB2ETPR."""
        return self.__handle_etpr_missingness("sib2etpr")

    def _missingness_sib3etpr(self) -> str:
        """Handles missingness for SIB3ETPR."""
        return self.__handle_etpr_missingness("sib3etpr")

    def _missingness_sib4etpr(self) -> str:
        """Handles missingness for SIB4ETPR."""
        return self.__handle_etpr_missingness("sib4etpr")

    def _missingness_sib5etpr(self) -> str:
        """Handles missingness for SIB5ETPR."""
        return self.__handle_etpr_missingness("sib5etpr")

    def _missingness_sib6etpr(self) -> str:
        """Handles missingness for SIB6ETPR."""
        return self.__handle_etpr_missingness("sib6etpr")

    def _missingness_sib7etpr(self) -> str:
        """Handles missingness for SIB7ETPR."""
        return self.__handle_etpr_missingness("sib7etpr")

    def _missingness_sib8etpr(self) -> str:
        """Handles missingness for SIB8ETPR."""
        return self.__handle_etpr_missingness("sib8etpr")

    def _missingness_sib9etpr(self) -> str:
        """Handles missingness for SIB9ETPR."""
        return self.__handle_etpr_missingness("sib9etpr")

    def _missingness_sib10etpr(self) -> str:
        """Handles missingness for SIB10ETPR."""
        return self.__handle_etpr_missingness("sib10etpr")

    def _missingness_sib11etpr(self) -> str:
        """Handles missingness for SIB11ETPR."""
        return self.__handle_etpr_missingness("sib11etpr")

    def _missingness_sib12etpr(self) -> str:
        """Handles missingness for SIB12ETPR."""
        return self.__handle_etpr_missingness("sib12etpr")

    def _missingness_sib13etpr(self) -> str:
        """Handles missingness for SIB13ETPR."""
        return self.__handle_etpr_missingness("sib13etpr")

    def _missingness_sib14etpr(self) -> str:
        """Handles missingness for SIB14ETPR."""
        return self.__handle_etpr_missingness("sib14etpr")

    def _missingness_sib15etpr(self) -> str:
        """Handles missingness for SIB15ETPR."""
        return self.__handle_etpr_missingness("sib15etpr")

    def _missingness_sib16etpr(self) -> str:
        """Handles missingness for SIB16ETPR."""
        return self.__handle_etpr_missingness("sib16etpr")

    def _missingness_sib17etpr(self) -> str:
        """Handles missingness for SIB17ETPR."""
        return self.__handle_etpr_missingness("sib17etpr")

    def _missingness_sib18etpr(self) -> str:
        """Handles missingness for SIB18ETPR."""
        return self.__handle_etpr_missingness("sib18etpr")

    def _missingness_sib19etpr(self) -> str:
        """Handles missingness for SIB19ETPR."""
        return self.__handle_etpr_missingness("sib19etpr")

    def _missingness_sib20etpr(self) -> str:
        """Handles missingness for SIB20ETPR."""
        return self.__handle_etpr_missingness("sib20etpr")

    def _missingness_kid1etpr(self) -> str:
        """Handles missingness for KID1ETPR."""
        return self.__handle_etpr_missingness("kid1etpr")

    def _missingness_kid2etpr(self) -> str:
        """Handles missingness for KID2ETPR."""
        return self.__handle_etpr_missingness("kid2etpr")

    def _missingness_kid3etpr(self) -> str:
        """Handles missingness for KID3ETPR."""
        return self.__handle_etpr_missingness("kid3etpr")

    def _missingness_kid4etpr(self) -> str:
        """Handles missingness for KID4ETPR."""
        return self.__handle_etpr_missingness("kid4etpr")

    def _missingness_kid5etpr(self) -> str:
        """Handles missingness for KID5ETPR."""
        return self.__handle_etpr_missingness("kid5etpr")

    def _missingness_kid6etpr(self) -> str:
        """Handles missingness for KID6ETPR."""
        return self.__handle_etpr_missingness("kid6etpr")

    def _missingness_kid7etpr(self) -> str:
        """Handles missingness for KID7ETPR."""
        return self.__handle_etpr_missingness("kid7etpr")

    def _missingness_kid8etpr(self) -> str:
        """Handles missingness for KID8ETPR."""
        return self.__handle_etpr_missingness("kid8etpr")

    def _missingness_kid9etpr(self) -> str:
        """Handles missingness for KID9ETPR."""
        return self.__handle_etpr_missingness("kid9etpr")

    def _missingness_kid10etpr(self) -> str:
        """Handles missingness for KID10ETPR."""
        return self.__handle_etpr_missingness("kid10etpr")

    def _missingness_kid11etpr(self) -> str:
        """Handles missingness for KID11ETPR."""
        return self.__handle_etpr_missingness("kid11etpr")

    def _missingness_kid12etpr(self) -> str:
        """Handles missingness for KID12ETPR."""
        return self.__handle_etpr_missingness("kid12etpr")

    def _missingness_kid13etpr(self) -> str:
        """Handles missingness for KID13ETPR."""
        return self.__handle_etpr_missingness("kid13etpr")

    def _missingness_kid14etpr(self) -> str:
        """Handles missingness for KID14ETPR."""
        return self.__handle_etpr_missingness("kid14etpr")

    def _missingness_kid15etpr(self) -> str:
        """Handles missingness for KID15ETPR."""
        return self.__handle_etpr_missingness("kid15etpr")
