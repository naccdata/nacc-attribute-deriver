"""NCRAD Biomarker derived variables."""

import datetime
import re

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.keyed_namespace import (
    ProvenanceNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.errors import AttributeDeriverError

BIOMARKER_FILENAME_REGEX = re.compile(
    r"^\d+_ncrad-biomarker.*?-return-(\d+).*?_identifiers\.csv"
)


class NCRADBiomarkerAttributeCollection(AttributeCollection):
    """Class to collect NCRAD biomarker attributes."""

    def __init__(self, table: SymbolTable) -> None:
        """Initializer."""
        self.__provenance = ProvenanceNamespace(
            table=table, required=frozenset(["file_name", "created_date"])
        )

    def _create_past_ncrad_embargo(self) -> int:
        """Creates past_ncrad_embargo.

        Determines whether biomarker data is ready to release. A 90-day
        embargo begins from the FIRST time data is distributed to
        centers, hence usage of the created_date rather than a
        modified_date, as the embargo does not restart if data is
        modified.
        """
        # check parent file name matches
        parent_file = self.__provenance.get_required("file_name", str)
        match = BIOMARKER_FILENAME_REGEX.match(parent_file)
        if match is None:
            raise AttributeDeriverError(
                "Biomarker filename does not match expected regex. "
                + f"Found {parent_file}, expected format {BIOMARKER_FILENAME_REGEX}"
            )

        # Then, check the return round; legacy rounds 1-14 automatically
        # pass embargo since these are legacy rounds that were already
        # returned before Flywheel
        return_round = int(match.group(1))
        if "express" not in parent_file and return_round > 0 and return_round < 15:
            return 1

        # date this data was released to ADRCs
        created_date = self.__provenance.get_required("created_date", str)

        try:
            release_dt = datetime.datetime.fromisoformat(created_date)
            now = datetime.datetime.now(datetime.timezone.utc)
        except (ValueError, TypeError) as e:
            raise AttributeDeriverError(
                "Failed to convert created_date to datetime object"
            ) from e

        # check if this data was distributed over 90 days ago
        return 1 if (now - release_dt) > datetime.timedelta(days=90) else 0
