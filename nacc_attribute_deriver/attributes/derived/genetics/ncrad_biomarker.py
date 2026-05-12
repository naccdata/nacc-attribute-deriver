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

        Determines whether biomarker data is ready to release. A 90-day
        embargo begins from the FIRST time data is distributed to centers,
        hence usage of the created_date rather than a modified_date, as the
        embargo does not restart if data is modified.
        """
        # date this data was released to ADRCs
        created_date = self.__provenance.get_value("created_date", str)
        if not created_date:
            raise AttributeDeriverError(
                "created_date not found in biomarker provenance data"
            )

        try:
            release_dt = datetime.datetime.fromisoformat(created_date)
            now = datetime.datetime.now(datetime.timezone.utc)
        except (ValueError, TypeError) as e:
            raise AttributeDeriverError(
                "Failed to convert created_date to datetime object"
            ) from e

        # check if this data was distributed over 90 days ago
        return 1 if (now - release_dt) > datetime.timedelta(days=90) else 0
