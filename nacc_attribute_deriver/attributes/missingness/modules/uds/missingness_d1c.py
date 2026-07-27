"""Class to handle D1c-specific missingness values."""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness


class UDSFormD1cMissingness(UDSMissingness):
    def _missingness_langd1c(self) -> int:
        """Handle missingness for LANGD1C."""
        return self.handle_optional_header_variables("lang", "d1c")
