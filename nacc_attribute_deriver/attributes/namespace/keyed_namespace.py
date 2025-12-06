"""Namespaces for working/intermediate data, namely those stored under special
keys in the passed SymbolTable."""

from typing import List, Optional, Type

from nacc_attribute_deriver.attributes.namespace.namespace import (
    BaseNamespace,
    T,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class PreviousRecordNamespace(BaseNamespace):
    """Namespace for attributes from the previous record, namely under.

    _prev_record.info.forms.json and _prev_record.info.forms.missingness
    """

    def __init__(
        self,
        *,
        table: SymbolTable,
        attribute_prefix: str = "_prev_record.info.",
        required: frozenset[str] = frozenset(),
        # date_attribute: str = "forms.json.visitdate",
    ) -> None:
        super().__init__(
            table=table,
            attribute_prefix=attribute_prefix,
            required=required,
        )

    def is_initial(self) -> bool:
        """Returns whether or not the previous record was an initial packet."""
        packet = self.get_resolved_value("packet", str)
        return packet is not None and packet.upper().startswith("I")

    def get_resolved_value(
        self,
        attribute: str,
        attr_type: Type[T],
        default: Optional[T] = None,
        working: Optional[WorkingNamespace] = None,
    ) -> Optional[T]:
        """Returns the value of the resolved attribute key in the table.

        Looks for the working value first, then resolved value, then raw value.

        Args:
          attribute: the attribute name
          attr_type: the attribute type; an error is thrown if the
            non-null grabbed value cannot be casted to it
          default: the default value
          working: working namespace to check in first, if provided
        Returns:
          the value for the attribute in the table


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

        resolved = self.get_value(f"resolved.{attribute}", attr_type, default)
        if resolved is None:
            return self.get_value(f"forms.json.{attribute}", attr_type, default)

        return resolved

    def get_derived_value(
        self,
        attribute: str,
        attr_type: Type[T],
        default: Optional[T] = None,
    ) -> Optional[T]:
        """Returns the derived variable of the previous record."""
        return self.get_value(f"derived.{attribute}", attr_type, default)


class RxClassNamespace(BaseNamespace):
    """Namespace for RxClass members.

    This is honestly of a hack, but done to avoid directly calling the RxClass API
        https://lhncbc.nlm.nih.gov/RxNav/APIs/api-RxClass.getClassMembers.html

    within the deriver, it expects the caller (curator gear) to store the mapping
    of RxClasss to RxCUI members in the table under a special _rxnorm field.

    Expects a mapping of ClassID to RxCUI members, e.g.
    "_rxnorm": {
            "C02L": [
                197959,
                237192,
                ...
            ],
            ...
        }
    }
    """

    def __init__(
        self,
        *,
        table: SymbolTable,
        attribute_prefix: str = "_rxclass.",
        required: frozenset[str] = frozenset(),
        date_attribute: Optional[str] = None,
    ) -> None:
        super().__init__(
            table=table,
            attribute_prefix=attribute_prefix,
            required=required,
            date_attribute=date_attribute,
        )

    def get_members(self, rxclass: str) -> List[str]:
        """Get members for associated RxClass.

        Args:
            rxclass: Name of the RxClass
        Returns:
            List of RxCUIs associated with the RxClass
        """
        members = self.get_value(rxclass, list)
        if not members:
            return []

        return [x.strip() for x in members]
