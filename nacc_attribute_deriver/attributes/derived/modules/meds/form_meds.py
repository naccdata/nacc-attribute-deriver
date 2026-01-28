"""Handles the MEDS form.

This is mainly used to inform UDS A4 NACC derived variables.
"""

import csv
import datetime
from importlib import resources
from typing import Dict, List

from nacc_attribute_deriver import config
from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    BaseNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import date_from_form_date
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)


# drug IDs that need to be substituted to another
# TODO: need a way to handle all our different drug references
# for now just hardcoding because its easiest
DRUG_ID_SUBSTITUTIONS = {
    "s10008": "d04523",
    "s10136": "d04523"
}


def load_normalized_drugs_list() -> Dict[str, str | None]:
    """Load the normalized drugs list. Done globally so it's only done once per
    execution.

    In UDS V1 all the drugs were written in. Uses normalized_drug_ids_v1.csv,
    which was manually generated with the following steps:
        1. Use Claude AI to "spellcheck" all misspelled/abbreviated entries
            - pulled from drugs.txt file found on server
        2. Lookup the drug in UDSMEDS, which is a NACC-specific database
            of brand/drug names and map to the listed drug ID
            - not all drugs matched - not sure how they were handled in SAS code
            - UDSMEDS does have name clashes - just used first one found
        3. Manually map any stragglers as needed - mostly focused on those
            that caused failures in regression testing, but ideally need
            a good way to map all of them properly. ~1.9k unmatched

    TODO: I'm not sure normalized_drug_ids.csv is actually comprehensive - there are far
    more entries in UDSMEDS. Since this is only relevant to V1, trying to load the
    smallest subset, but if regression tests still fail a bunch probably best to also
    include the UDSMEDS csv.
    """
    normalized_drugs_file = resources.files(config).joinpath(
        "normalized_drug_ids_v1.csv"
    )
    drugs: Dict[str, str | None] = {}

    with normalized_drugs_file.open("r") as fh:
        reader = csv.DictReader(fh)
        # map every possible name (both raw and normalized) to its drug ID
        for row in reader:
            drug_id = row["drug_id"]

            for field in ["raw_drug", "normalized_drug"]:
                name = row[field].strip().lower()
                if name not in drugs or drugs[name] is None:
                    drugs[name] = drug_id if drug_id != "NO_DRUG_ID" else None

    return drugs


# load this globally so it's only done once per execution
NORMALIZED_DRUGS = load_normalized_drugs_list()


class MEDSFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        """Initializer."""
        self.__meds = BaseNamespace(
            table=table,
            attribute_prefix="file.info.forms.json",
            required=frozenset(["module", "formver"]),
        )
        module = self.__meds.get_required("module", str)
        if module.upper() != "MEDS":
            raise InvalidFieldError(
                f"Current file is not a MEDS form: found {module}",
            )

        self.__formver = self.__meds.get_value("formver", float)

    def get_date(self) -> datetime.date:
        """Get MEDS date; depends on version."""
        date_attribute = (
            "frmdatea4" if (self.__formver and self.__formver < 2) else "frmdatea4g"
        )
        formdate = self.__meds.get_value(date_attribute, str)
        date = date_from_form_date(formdate)

        if not date:
            raise AttributeDeriverError("Cannot determine MEDS form date")

        return date

    def _create_drugs_list(self) -> List[str]:
        """Returns list of drugs for this visit."""
        # in V1, each prescription medication is specified by variables
        # PMA - PMT, need to extract
        if self.__formver == 1:
            return self.__get_v1_drugs()

        drugs_str = self.__meds.get_value("drugs_list", str)
        return sorted(
            [x.strip().lower() for x in drugs_str.split(",")] if drugs_str else []
        )

    def __get_v1_drugs(self) -> List[str]:
        """Gets V1 drugs by mapping write-ins to normalized DB."""
        # if not in drugs_db, use drug_name
        drugs_list = []
        for i in range(ord("a"), ord("t") + 1):
            drug_name = self.__meds.get_value(f"pm{chr(i)}", str)
            if not drug_name:
                continue

            drug_name = drug_name.strip().lower()
            drug_id = NORMALIZED_DRUGS.get(drug_name, drug_name)
            drugs_list.append(drug_id if drug_id is not None else drug_name)

        return sorted(drugs_list)
