"""NCRAD Biomarker derived variables."""

import datetime

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    ProvenanceNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


class NCRADBiomarkerAttributeCollection(AttributeCollection):
    """Class to collect NCRAD biomarker attributes."""

    def __init__(self, table: SymbolTable) -> None:
        """Initializer."""
        self.__provenance = ProvenanceNamespace(table=table)

    def _create_past_ncrad_embargo(self) -> int:
        """Creates past_ncrad_embargo.

        Determines whether biomarker data is ready to release.
        """
        # date this data was released to ADRCs
        provenance_date = self.__provenance.get_value("modified_date", str)
        if not provenance_date:
            raise AttributeDeriverError(
                "modified_date not found in biomarker provenance data"
            )

        try:
            release_dt = datetime.datetime.fromisoformat(provenance_date)
            now = datetime.datetime.now(datetime.timezone.utc)
        except (ValueError, TypeError) as e:
            raise AttributeDeriverError("Failed to calculate embargo date") from e

        # check if this data was distributed over 90 days ago
        return 1 if (now - release_dt) > datetime.timedelta(days=90) else 0
