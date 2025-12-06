"""UDS Attribute collection."""

import datetime
from typing import List, Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace,
)
from nacc_attribute_deriver.attributes.namespace.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
)
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
)


class UDSAttributeCollection(AttributeCollection):
    def __init__(
        self, table: SymbolTable, required: frozenset[str] = frozenset()
    ) -> None:
        self.__uds = UDSNamespace(table, required=required)
        self.__formver = self.uds.normalized_formver()
        self.__prev_record = PreviousRecordNamespace(table=table)

    @property
    def prev_record(self) -> PreviousRecordNamespace:
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


class UDSMissingness(FormMissingnessCollection):
    """Class to handle UDS missingness values."""

    def __init__(
        self, table: SymbolTable, required: frozenset[str] = frozenset()
    ) -> None:
        super().__init__(table=table, namespace=UDSNamespace, required=required)
        self.__formver = self.uds.normalized_formver()

    @property
    def uds(self) -> UDSNamespace:
        return self.form  # type: ignore

    @property
    def formver(self) -> int:
        return self.__formver

    def handle_gated_writein(
        self, gate: str, attribute: str, values: List[int], include_none: bool = False
    ) -> str:
        """Handles generic write-in logic in the form:

        If GATE is in GATE_VALUES, then FIELD should be blank
        """
        gate_value = self.uds.get_value(gate, int)
        if gate_value in values or (include_none and gate_value is None):
            return INFORMED_BLANK

        return self.generic_missingness(attribute, str)

    def handle_forbidden_gated_writein(self, gate: str, value: int, field: str) -> str:
        """Handles write-in blanks that rely on a gate variable in the form: If
        GATE is NOT VALUE then FIELD should be blank.

        Args:
            gate: The gate variable
            value: The value the gate must NOT equal to trigger the condition
            field: If condition not passed, field to perform generic missingness for
        """
        if self.uds.get_value(gate, int) != value:
            return INFORMED_BLANK

        return self.generic_missingness(field, str)

    def handle_set_to_gate(self, gate: str, check_values: List[int]) -> Optional[int]:
        """Generically handle:

        If GATE is in CHECK_VALUES, then FIELD should = GATE.
        """
        gate_value = self.uds.get_value(gate, int)
        if gate_value in check_values:
            return gate_value

        return None
