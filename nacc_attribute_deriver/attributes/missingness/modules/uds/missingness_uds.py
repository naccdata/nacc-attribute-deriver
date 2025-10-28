"""Class to handle UDS missingness variables.

In general, returns -4 unless otherwise specified.
"""

from typing import List, Optional

from nacc_attribute_deriver.attributes.collection.uds_attribute import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace
)
from nacc_attribute_deriver.schema.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSMissingness(UDSAttributeCollection):
    """Class to handle UDS missingness values."""

    def __init__(self, table: SymbolTable) -> None:
        super().__init__(table)
        self.__prev_record = None

        # prev record should exist for non-initial visits, and contain:
        #   raw form info under info.forms.json.x
        #   missingness info under info.forms.missingness.x
        if not self.uds.is_initial():
            self.__prev_record = PreviousRecordNamespace(table=table)

    @property
    def prev_record(self) -> Optional[PreviousRecordNamespace]:
        return self.__prev_record

    def _missingness_uds(self, field: str) -> Optional[int]:
        """Defines general missingness for UDS; -4 if missing."""
        if self.uds.get_value(field, str) is None:
            return INFORMED_MISSINGNESS

        return None

    def generic_missingness(self, field: str) -> Optional[int]:
        """Generic missingness for internal calls."""
        return self._missingness_uds(field)

    def generic_writein(self, field: str) -> Optional[str]:
        """Generic blankness (write-ins) for internal calls."""
        # if value exists, return None so we don't override
        value = self.uds.get_value(field, str)
        if value is not None:
            return None

        return INFORMED_BLANK

    def handle_gated_writein(self, gate: str, value: int) -> Optional[str]:
        """Handles write-in blanks that rely on a gate variable.

        Args:
            gate: The gate variable
            value: The value the gate must NOT equal to trigger the condition
        """
        if self.uds.get_value(gate, int) != value:
            return INFORMED_BLANK

        return None

    def handle_set_to_gate(self, gate: str, check_values: List[int]) -> Optional[int]:
        """Generically handle:

        If GATE is in CHECK_VALUES, then FIELD should = GATE.
        """
        value = self.uds.get_value(gate, int)
        if value in check_values:
            return value

        return None

    def handle_prev_visit(self, field: str, prev_code: int = 777) -> Optional[int]:
        """Handle when the value is provided by the previous visit.

        If VAR == PREV_CODE, VAR must be equal to PREV_VISIT. ELIF VAR
        is not blank and not PREV_CODE, return None (do not override)
        ELSE generic missingness
        """
        value = self.uds.get_value(field, int)
        if value == prev_code and self.__prev_record is not None:
            prev_value = self.__prev_record.get_resolved_value(
                field, int, prev_code=prev_code
            )
            if prev_value is not None:
                return prev_value

        elif value is not None:
            return None

        return self.generic_missingness(field)


class VersionedUDSMissingness(UDSMissingness):
    """Class to handle UDS missingness values that rely heavily on the form
    version."""

    def handle_formver_missingness(
        self,
        field: str,
        missing_value: int = 0,
        gate_version: int = 4,
    ) -> Optional[int]:
        """Handles generic formver-gated missingness, which follows the logic:

        If FORMVER=4 and VAR is blank, VAR should = MISSING_VALUE
        else if FORMVER < 4, VAR should be -4

        Args:
            field: The field to check and set missingness for
            missing_value: The value to set if the field is missing;
                defaults to 0
        Returns:
            Missingness value if missing, None otherwise (so it isn't
            set)
        """
        if self.formver < gate_version:
            return INFORMED_MISSINGNESS

        # if value exists, return None so we don't override
        value = self.uds.get_value(field, int)
        if value is not None:
            return None

        return missing_value

    def handle_formver_writein(
        self, field: str, gate_version: int = 4
    ) -> Optional[str]:
        """Handles formver-gated writein missingness, which follows the logic:

        If FORMVER < 4 or VAR is blank, VAR should remain blank
        """
        if self.formver < gate_version:
            return INFORMED_BLANK

        return self.generic_writein(field)
