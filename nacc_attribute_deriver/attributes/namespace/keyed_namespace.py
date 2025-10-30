"""Namespaces for working/intermediate data, namely those stored under special
keys in the passed SymbolTable."""

from typing import List, Optional, Type

from nacc_attribute_deriver.attributes.namespace.namespace import (
    BaseNamespace,
    FormNamespace,
    T,
)
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable


class PreviousRecordNamespace(FormNamespace):
    """Namespace for attributes from the previous record, namely under.

    _prev_record.info.forms.json and _prev_record.info.forms.missingness
    """

    def __init__(
        self,
        *,
        table: SymbolTable,
        attribute_prefix: str = "_prev_record.info.forms.",
        required: frozenset[str] = frozenset(),
        date_attribute: str = "json.visitdate",
    ) -> None:
        super().__init__(
            table=table,
            attribute_prefix=attribute_prefix,
            required=required,
            date_attribute=date_attribute,
        )

    def get_resolved_value(
        self,
        attribute: str,
        attr_type: Type[T],
        prev_code: Optional[T] = None,
        default: Optional[T] = None,
    ) -> Optional[T]:
        """Returns the value of the resolved attribute key in the table. First.

        looks at the raw value - if a prev_visit code (e.g. 777) or None,
        looks at the missingness/resolved value already stored at
        file.info.resolved instead.

        Args:
          attribute: the attribute name
          attr_type: the attribute type; an error is thrown if the
            non-null grabbed value cannot be casted to it
          default: the default value
        Returns:
          the value for the attribute in the table
        """
        raw_value = self.get_value(f"json.{attribute}", attr_type, default)
        if raw_value is None or raw_value == prev_code:
            return self.get_value(f"resolved.{attribute}", attr_type, default)

        return raw_value


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
            raise AttributeDeriverError(f"No RxCUIs associated with RxClass {rxclass}")

        return [x.strip() for x in members]
