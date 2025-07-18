"""Handles the MEDS form.

This is mainly used to inform UDS A4 NACC derived variables.
"""

import csv
import re
from importlib import resources
from typing import Dict, List

from nacc_attribute_deriver import config
from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    BaseNamespace,
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.schema.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


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

        # TODO: V1 does not have drugs_list and instead lists everything
        # explicitly - do not see it in pulled SAS code, will need to investigate
        self.__formver = self.__meds.get_value("formver", float)
        date_attribute = (
            "frmdatea4" if (self.__formver and self.__formver < 2) else "frmdatea4g"
        )
        self.__formdate = self.__meds.get_value(date_attribute, str)

        if not self.__formdate:
            raise AttributeDeriverError("Cannot determine MEDS form date")

        self.__working = WorkingDerivedNamespace(table=table)

    def _create_drugs_list(self) -> Dict[str, List[str]]:
        """Returns list of drugs for this visit, adding to overall mapping."""
        all_drugs = self.__working.get_cross_sectional_value("drugs-list", dict)
        if all_drugs is None:
            all_drugs = {}

        if self.__formdate in all_drugs:
            raise AttributeDeriverError(
                f"Drugs list for frmdatea4g {self.__formdate} already exists"
            )

        # in V1, each prescription medication is specified by variables
        # PMA - PMT, need to extract
        if self.__formver == 1:
            all_drugs[self.__formdate] = self.__load_from_normalized_drugs_list()
        else:
            drugs_str = self.__meds.get_value("drugs_list", str)
            all_drugs[self.__formdate] = sorted(
                [x.strip().lower() for x in drugs_str.split(",")] if drugs_str else []
            )

        return all_drugs

    def __load_from_normalized_drugs_list(self) -> List[str]:
        """V1.

        In this version all the drugs were written in. Uses normalized_drug_ids.csv,
        which was manually generated with the following steps:
            1. Use Claude AI to "spellcheck" all misspelled/abbreviated entries
            2. Lookup the drug in UDSMEDS, which is a NACC-specific database
                of brand/drug names and map to the listed drug ID
                - drug ID seems to be NACC-specific, e.g. not related to RxCUI or similar
                - not all drugs matched - not sure how they were handled in SAS code
                - UDSMEDS does have name clashes - just used first one found
            3. Manually map any stragglers as needed - mostly focused on those
                that caused failures in regression testing, but ideally need
                a good way to map all of them properly. ~1.9k unmatched
        """
        normalized_drugs_file = resources.files(config).joinpath("normalized_drug_ids.csv")
        drugs_db: Dict[str, str] = {}

        with normalized_drugs_file.open("r") as fh:
            reader = csv.DictReader(fh)
            # map every possible name to its drug ID
            for row in reader:
                drug_name = row['normalized_drug']
                drug_id = row['drug_id']

                drugs_db[drug_name] = drug_id if drug_id != 'NO_DRUG_ID' else drug_name

        # now look at every drug name in MEDS drugs_list; if not in
        # drugs_db, use drug_name
        drugs_list = []
        for i in range(ord("a"), ord("t") + 1):
            drug_name = self.__meds.get_value(f"pm{chr(i)}", str)
            if not drug_name:
                continue

            drugs_list.append(drugs_db.get(drug_name, drug_name))

        return sorted(drugs_list)
