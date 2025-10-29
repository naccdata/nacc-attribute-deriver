"""Class to handle A3-specific missingness values.

While not explicitly pushed to the QAFs, are necessary to keep track
of for calculationss of derived variables.
"""

from typing import Optional

from .missingness_uds import UDSMissingness


class UDSFormA3Missingness(UDSMissingness):

    def __handle_etpr_missingness(self, field: str) -> Optional[str]:
        """Handles ETPR missingness.

        66 is the "provided at previous visit code", so if indicated
        we must pull forward the value from the previous visit.
        Similarly if no new info is provided (assured blank when NWINF
        variables = 0), then we need to pull through the previous visit.

        In short, if we see 66 or blank, we pull the previous visit
        through.
        """
        return self.handle_prev_visit(field, attribute_type=str, prev_code='66')

    def _missingness_mometpr(self) -> Optional[str]:
        """Handles missingness for MOMETPR"""
        return self.handle_prev_visit('mometpr')

    def _missingness_dadetpr(self) -> Optional[str]:
        """Handles missingness for DADETPR"""
        return self.handle_prev_visit('dadetpr')

    def _missingness_sib1etpr(self) -> Optional[str]:
        """Handles missingness for SIB1ETPR"""
        return self.handle_prev_visit('sib1etpr')

    def _missingness_sib2etpr(self) -> Optional[str]:
        """Handles missingness for SIB2ETPR"""
        return self.handle_prev_visit('sib2etpr')

    def _missingness_sib3etpr(self) -> Optional[str]:
        """Handles missingness for SIB3ETPR"""
        return self.handle_prev_visit('sib3etpr')

    def _missingness_sib4etpr(self) -> Optional[str]:
        """Handles missingness for SIB4ETPR"""
        return self.handle_prev_visit('sib4etpr')

    def _missingness_sib5etpr(self) -> Optional[str]:
        """Handles missingness for SIB5ETPR"""
        return self.handle_prev_visit('sib5etpr')

    def _missingness_sib6etpr(self) -> Optional[str]:
        """Handles missingness for SIB6ETPR"""
        return self.handle_prev_visit('sib6etpr')

    def _missingness_sib7etpr(self) -> Optional[str]:
        """Handles missingness for SIB7ETPR"""
        return self.handle_prev_visit('sib7etpr')

    def _missingness_sib8etpr(self) -> Optional[str]:
        """Handles missingness for SIB8ETPR"""
        return self.handle_prev_visit('sib8etpr')

    def _missingness_sib9etpr(self) -> Optional[str]:
        """Handles missingness for SIB9ETPR"""
        return self.handle_prev_visit('sib9etpr')

    def _missingness_sib10etpr(self) -> Optional[str]:
        """Handles missingness for SIB10ETPR"""
        return self.handle_prev_visit('sib10etpr')

    def _missingness_sib11etpr(self) -> Optional[str]:
        """Handles missingness for SIB11ETPR"""
        return self.handle_prev_visit('sib11etpr')

    def _missingness_sib12etpr(self) -> Optional[str]:
        """Handles missingness for SIB12ETPR"""
        return self.handle_prev_visit('sib12etpr')

    def _missingness_sib13etpr(self) -> Optional[str]:
        """Handles missingness for SIB13ETPR"""
        return self.handle_prev_visit('sib13etpr')

    def _missingness_sib14etpr(self) -> Optional[str]:
        """Handles missingness for SIB14ETPR"""
        return self.handle_prev_visit('sib14etpr')

    def _missingness_sib15etpr(self) -> Optional[str]:
        """Handles missingness for SIB15ETPR"""
        return self.handle_prev_visit('sib15etpr')

    def _missingness_sib16etpr(self) -> Optional[str]:
        """Handles missingness for SIB16ETPR"""
        return self.handle_prev_visit('sib16etpr')

    def _missingness_sib17etpr(self) -> Optional[str]:
        """Handles missingness for SIB17ETPR"""
        return self.handle_prev_visit('sib17etpr')

    def _missingness_sib18etpr(self) -> Optional[str]:
        """Handles missingness for SIB18ETPR"""
        return self.handle_prev_visit('sib18etpr')

    def _missingness_sib19etpr(self) -> Optional[str]:
        """Handles missingness for SIB19ETPR"""
        return self.handle_prev_visit('sib19etpr')

    def _missingness_sib20etpr(self) -> Optional[str]:
        """Handles missingness for SIB20ETPR"""
        return self.handle_prev_visit('sib20etpr')

    def _missingness_kid1etpr(self) -> Optional[str]:
        """Handles missingness for KID1ETPR"""
        return self.handle_prev_visit('kid1etpr')

    def _missingness_kid2etpr(self) -> Optional[str]:
        """Handles missingness for KID2ETPR"""
        return self.handle_prev_visit('kid2etpr')

    def _missingness_kid3etpr(self) -> Optional[str]:
        """Handles missingness for KID3ETPR"""
        return self.handle_prev_visit('kid3etpr')

    def _missingness_kid4etpr(self) -> Optional[str]:
        """Handles missingness for KID4ETPR"""
        return self.handle_prev_visit('kid4etpr')

    def _missingness_kid5etpr(self) -> Optional[str]:
        """Handles missingness for KID5ETPR"""
        return self.handle_prev_visit('kid5etpr')

    def _missingness_kid6etpr(self) -> Optional[str]:
        """Handles missingness for KID6ETPR"""
        return self.handle_prev_visit('kid6etpr')

    def _missingness_kid7etpr(self) -> Optional[str]:
        """Handles missingness for KID7ETPR"""
        return self.handle_prev_visit('kid7etpr')

    def _missingness_kid8etpr(self) -> Optional[str]:
        """Handles missingness for KID8ETPR"""
        return self.handle_prev_visit('kid8etpr')

    def _missingness_kid9etpr(self) -> Optional[str]:
        """Handles missingness for KID9ETPR"""
        return self.handle_prev_visit('kid9etpr')

    def _missingness_kid10etpr(self) -> Optional[str]:
        """Handles missingness for KID10ETPR"""
        return self.handle_prev_visit('kid10etpr')

    def _missingness_kid11etpr(self) -> Optional[str]:
        """Handles missingness for KID11ETPR"""
        return self.handle_prev_visit('kid11etpr')

    def _missingness_kid12etpr(self) -> Optional[str]:
        """Handles missingness for KID12ETPR"""
        return self.handle_prev_visit('kid12etpr')

    def _missingness_kid13etpr(self) -> Optional[str]:
        """Handles missingness for KID13ETPR"""
        return self.handle_prev_visit('kid13etpr')

    def _missingness_kid14etpr(self) -> Optional[str]:
        """Handles missingness for KID14ETPR"""
        return self.handle_prev_visit('kid14etpr')

    def _missingness_kid15etpr(self) -> Optional[str]:
        """Handles missingness for KID15ETPR"""
        return self.handle_prev_visit('kid15etpr')
