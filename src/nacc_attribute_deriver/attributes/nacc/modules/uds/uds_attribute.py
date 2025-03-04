"""
Class to define UDS-specific attributes.
"""
from datetime import datetime
from nacc_attribute_deriver.attributes.attribute_collection import (
    NACCAttribute,
)


class UDSAttribute(NACCAttribute):

    def generate_uds_dob(self) -> datetime:
        """Creates UDS DOB, which is used to calculate ages.
        """
        birthmo = self.get_value('birthmo')
        birthyr = self.get_value('birthyr')
        formdate = self.get_value('visitdate')
        if None in [birthmo, birthyr, formdate]:
            return None

        return datetime(int(birthyr), int(birthmo), 1)
