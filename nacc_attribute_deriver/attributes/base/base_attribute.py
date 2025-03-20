"""Base attributes, derive directly from AttributeCollection."""

from inspect import stack
from typing import Any, Dict, List

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.schema.errors import MissingRequiredException


class NACCAttribute(AttributeCollection):
    """Currently doesn't have anything specific going on, but may be useful
    later."""


class MQTAttribute(AttributeCollection):
    """MQT-specific attribute collection.

    The main difference is that MQT variables often require that a
    derived NACC variable has already been set.
    """

    def assert_required(
        self, required: List[str], prefix: str = "file.info.derived."
    ) -> Dict[str, Any]:
        """Asserts that the given fields in required are in the table for the
        source.

        Args:
            required: The required fields
            prefix: Key prefix the required field is expected to be under
        Returns:
            The found required variables, flattened out from the table
        """
        found = {}
        for r in required:
            full_field = f"{prefix}{r}"
            # TODO: maybe can implicitly derive even if schema didn't define it?
            if full_field not in self.table:
                source = stack()[
                    1
                ].function  # not great but preferable to passing the name every time
                raise MissingRequiredException(
                    f"{full_field} must be derived before {source} can run"
                )

            found[r] = self.table[full_field]

        return found
