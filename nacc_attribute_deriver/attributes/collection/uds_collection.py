"""UDS Attribute collection."""

import datetime
from typing import List, Optional, Type

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace,
    T,
)
from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
    INFORMED_MISSINGNESS_FLOAT,
)
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)


class UDSAttributeCollection(AttributeCollection):
    def __init__(
        self, table: SymbolTable, uds_required: Optional[frozenset] = None
    ) -> None:
        self.__uds = UDSNamespace(table, required=uds_required)
        self.__formver = self.uds.normalized_formver()

        module = self.__uds.get_required("module", str)
        if module.upper() != "UDS":
            msg = f"Current file is not a UDS form: found {module}"
            raise InvalidFieldError(msg)

        self.__prev_record = None
        # prev record should exist for non-initial visits
        if not self.uds.is_initial() or self.uds.is_i4():
            self.__prev_record = PreviousRecordNamespace(table=table)

    @property
    def prev_record(self) -> Optional[PreviousRecordNamespace]:
        return self.__prev_record

    @property
    def uds(self) -> UDSNamespace:
        return self.__uds

    @property
    def formver(self) -> int:
        return self.__formver

    @property
    def submitted(self) -> bool:
        return True

    def get_date(self) -> datetime.date:
        """All UDS visits must have a visitdate."""
        visitdate = self.__uds.get_date()
        if not visitdate:
            raise AttributeDeriverError("Cannot determine visitdate for UDS visit")

        return visitdate

    def get_prev_value(
        self,
        field: str,
        attr_type: Type[T],
        default: Optional[T] = None,
    ) -> Optional[T]:
        """Get the previous value."""
        if self.__prev_record is not None:
            return self.__prev_record.get_resolved_value(
                field, attr_type, default=default
            )

        return None


class UDSMissingness(UDSAttributeCollection):
    """Class to handle UDS missingness values."""

    def generic_missingness(
        self, field: str, attr_type: Type[T], default: Optional[T] = None
    ) -> Optional[T]:
        """Generic missingness:

        If FIELD is None, FIELD = -4 / -4.4 / blank
        """
        if self.uds.get_value(field, str) is None:
            if default is not None:
                return default

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

    def handle_gated_writein(
        self, gate: str, field: str, values: List[int], include_none: bool = False
    ) -> Optional[str]:
        """Handles generic write-in logic in the form:

        If GATE is in GATE_VALUES, then FIELD should be blank
        """
        gate_value = self.uds.get_value(gate, int)
        if gate_value in values or (include_none and gate_value is None):
            return INFORMED_BLANK

        return self.generic_missingness(field, str)

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
        self,
        field: str,
        attr_type: Type[T],
        prev_code: Optional[T] = None,
        default: Optional[T] = None,
        cross_sectional: bool = False
    ) -> Optional[T]:
        """Handle when the value could be provided by the previous visit.

        If VAR == PREV_CODE, VAR = PREV_VISIT.
        ELIF VAR is not blank, return None (do not override)
        ELSE generic missingness
        """
        # no prev record expected if true initial packet (I4 does not count)
        if not self.uds.is_initial() or self.uds.is_i4():
            value = self.uds.get_value(field, attr_type)

            if value == prev_code:
                prev_value = self.get_prev_value(
                    field,
                    attr_type,
                    default=default,
                    cross_sectional=cross_sectional)
                if prev_value is not None:
                    return prev_value

        return self.generic_missingness(field, attr_type, default=default)
