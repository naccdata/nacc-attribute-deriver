"""Class to handle UDS missingness variables.

In general, returns -4 unless otherwise specified.
"""

from typing import List, Optional, Type

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
    INFORMED_MISSINGNESS_FLOAT,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


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

    def generic_missingness(self, field: str, attr_type: Type[T]) -> Optional[T]:
        """Generic missingness:

        If FIELD is None, FIELD = -4 / -4.4 / blank
        """
        if self.uds.get_value(field, str) is None:
            if attr_type == int:  # noqa: E721
                return INFORMED_MISSINGNESS  # type: ignore
            if attr_type == str:  # noqa: E721
                return INFORMED_BLANK  # type: ignore
            if attr_type == float:  # noqa: E721
                return INFORMED_MISSINGNESS_FLOAT  # type: ignore

            raise AttributeDeriverError(
                f"Unknown missingness attribute type: {attr_type}"
            )

        return None

    def handle_gated_writein(self, gate: str, values: List[int]) -> Optional[str]:
        """Handles generic write-in logic in the form:

        If GATE is in GATE_VALUES, then FIELD should be blank
        """
        gate_value = self.uds.get_value(gate, int)
        if gate_value is None or gate_value in values:
            return INFORMED_BLANK

        return None

    def handle_forbidden_gated_writein(self, gate: str, value: int) -> Optional[str]:
        """Handles write-in blanks that rely on a gate variable in the form: If
        GATE is NOT VALUE then FIELD should be blank.

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

    def handle_prev_visit(
        self, field: str, attr_type: Type[T], prev_code: Optional[T] = None
    ) -> Optional[T]:
        """Handle when the value is provided by the previous visit.

        If VAR == PREV_CODE, VAR = PREV_VISIT.
        ELIF VAR is not blank, return None (do not override)
        ELSE generic missingness
        """
        value = self.uds.get_value(field, attr_type)
        if value == prev_code and self.__prev_record is not None:
            prev_value = self.__prev_record.get_resolved_value(
                field, attr_type, prev_code=prev_code
            )
            if prev_value is not None:
                return prev_value

        elif value is not None:
            return None

        result = self.generic_missingness(field, attr_type)
        if result is not None:
            return result  # type: ignore

        return None

    def check_applicable_version(self, versions: List[float]) -> bool:
        """Returns True if this variable is applicable to the specified
        versions."""
        raw_formver = self.uds.get_required("formver", float)
        return raw_formver in versions

    def check_applicable(self) -> bool:
        """Check if applicable to V3+ (3.0, 3.2, 4.0+) and where 3.1 treated as
        a separate case."""
        return self.check_applicable_version([3.0, 3.2, 4.0])

    def check_applicable_legacy(self) -> bool:
        """Check if applicable to an old version or 3.1 (1.0, 2.0, 3.1)"""
        return self.check_applicable_version([1.0, 2.0, 3.1])


class GenericUDSMissingness(UDSMissingness):
    """Defines generic missingness rule in its own subclass otherwise it gets
    inherited by all subclasses and imported multiple times."""

    def _missingness_uds(self, field: str, attr_type: Type[T]) -> Optional[T]:
        """Defines general missingness for UDS; -4 if missing."""
        return self.generic_missingness(field, attr_type)
