"""Raw form values from form A1: Participant Demographics.

Many of these are required for cross-module derived variables, so must
be saved at the subject level.
"""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    SubjectDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormA1RawAttribute(UDSAttributeCollection):
    """Class to collect raw UDS A1 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__subject_derived = SubjectDerivedNamespace(table=table)

    def _create_educ(self) -> Optional[int]:
        """UDS education level - this rule is used by MQT, since it
        needs to know the latest at the global level. Other derived variables
        looking for educ should use the get_prev_value method instead."""
        return self.uds.get_value("educ", int)

    def _create_uds_date_of_birth(self) -> date:
        """UDS date of birth."""
        return self.uds.generate_uds_dob()

    def _create_prespart(self) -> Optional[int]:
        """Saves PRESPART, which is needed for cross-module derived variables.

        Only expected at initial visit.
        """
        if not self.uds.is_initial():
            return None

        return self.uds.get_value("prespart", int)

    def _create_residenc(self) -> Optional[int]:
        """Saves RESIDENC, which is needed for cross-module derived
        variables."""
        return self.uds.get_value("residenc", int)
