"""UDS Attribute collection."""

import datetime
from typing import List, Optional, Type

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    PreviousRecordNamespace,
)
from nacc_attribute_deriver.attributes.namespace.namespace import T, WorkingNamespace
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
        attribute: str,
        attr_type: Type[T],
        default: Optional[T] = None,
        working: Optional[WorkingNamespace] = None,
    ) -> Optional[T]:
        """Get the previous value.

        REGRESSION: It seems in some cases (namely on B9), the 777/prev code
        can actually pull across several visits. So it needs to actually
        consider the last time the value was set at all, not necessarily the
        previous visit.

        Basically, if this is passed a working namespace, try to grab from
        there first. Then try to pull from the previous record. Especially
        because previous record might resolve to a missingness value that
        we don't necessarily want.

        (TODO: maybe conflating that too much. Those looking at working want
        the RAW value whereas all others want the RESOLVED value, which is
        after missingness is applied).
        """
        if working:
            result = working.get_cross_sectional_value(
                attribute, attr_type, default=default
            )
            if result is not None:
                return result

        if self.__prev_record is not None:
            return self.__prev_record.get_resolved_value(
                attribute, attr_type, default=default
            )

        return None


class UDSMissingness(UDSAttributeCollection):
    """Class to handle UDS missingness values."""

    def generic_missingness(
        self, attribute: str, attr_type: Type[T], default: Optional[T] = None
    ) -> Optional[T]:
        """Generic missingness:

        If FIELD is None, FIELD = -4 / -4.4 / blank
        """
        if self.uds.get_value(attribute, str) is None:
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
        self, gate: str, attribute: str, values: List[int], include_none: bool = False
    ) -> Optional[str]:
        """Handles generic write-in logic in the form:

        If GATE is in GATE_VALUES, then FIELD should be blank
        """
        gate_value = self.uds.get_value(gate, int)
        if gate_value in values or (include_none and gate_value is None):
            return INFORMED_BLANK

        return self.generic_missingness(attribute, str)

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
        gate_value = self.uds.get_value(gate, int)
        if gate_value in check_values:
            return gate_value

        return None

    def handle_prev_visit(
        self,
        attribute: str,
        attr_type: Type[T],
        prev_code: Optional[T] = None,
        default: Optional[T] = None,
        working: Optional[WorkingNamespace] = None,
    ) -> Optional[T]:
        """Handle when the value could be provided by the previous visit.

        If VAR == PREV_CODE, VAR = PREV_VISIT.
        ELIF VAR is not blank, return None (do not override)
        ELSE generic missingness
        """
        # no prev record expected if true initial packet (I4 does not count)
        if not self.uds.is_initial() or self.uds.is_i4():
            value = self.uds.get_value(attribute, attr_type)

            if value == prev_code:
                prev_value = self.get_prev_value(
                    attribute, attr_type, default=default, working=working
                )
                if prev_value is not None:
                    return prev_value

        return self.generic_missingness(attribute, attr_type, default=default)
