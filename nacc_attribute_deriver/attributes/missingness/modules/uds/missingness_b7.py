"""Class to handle B7-specific missingness values."""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness


class UDSFormB7Missingness(UDSMissingness):
    def _missingness_langb7(self) -> int:
        """Handle missingness for LANGB7."""
        return self.handle_optional_header_variables("lang", "b7", [1, 2])
