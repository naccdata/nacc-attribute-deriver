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

from .prefix_tree import PrefixTree

ALPHA_NUMERIC = re.compile(r"[^a-zA-Z0-9]")


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

        self.__working_derived = WorkingDerivedNamespace(table=table)

    def _create_drugs_list(self) -> Dict[str, List[str]]:
        """Returns list of drugs for this visit, adding to overall mapping."""
        all_drugs = self.__working_derived.get_cross_sectional_value("drugs-list", dict)
        if all_drugs is None:
            all_drugs = {}

        if self.__formdate in all_drugs:
            raise AttributeDeriverError(
                f"Drugs list for frmdatea4g {self.__formdate} already exists"
            )

        # in V1, each prescription medication is specified by variables
        # PMA - PMT, need to extract
        if self.__formver == 1:
            # all_drugs[self.__formdate] = self.__load_from_udsmeds_table()
            all_drugs[self.__formdate] = []
        else:
            drugs_str = self.__meds.get_value("drugs_list", str)
            all_drugs[self.__formdate] = sorted(
                [x.strip().lower() for x in drugs_str.split(",")] if drugs_str else []
            )

        return all_drugs

    def __load_from_udsmeds_table(self) -> List[str]:
        """V1.

        In this version all the drugs were written in. Need to use
        UDSMEDS CSV (combination of UDSMEDS table from Oracle DB +
        drugs.sas which translated typos/alternative spellings) and map
        each possible drug variable to its ID.
        """
        udsmeds_table_file = resources.files(config).joinpath("UDSMEDS_combined.csv")
        udsmeds: Dict[str, str] = {}
        prefix_tree = PrefixTree()  # prefix tree for searching

        with udsmeds_table_file.open("r") as fh:
            reader = csv.DictReader(fh)

            # map every possible name to its drug ID
            # TODO: unfortunately UDSMEDS does have name clashes. for now,
            # just keep the first one and ignore the others
            for row in reader:
                drug_id = row["drug_id"]
                for field in ["brand_name", "drug_name", "alternative_name"]:
                    name = row[field]

                    # CSV is already lowercased/stripped, but also
                    # remove all non-alphanumeric characters
                    name = ALPHA_NUMERIC.sub("", name) if name else None
                    if not name or name in udsmeds:
                        continue
                    udsmeds[name] = drug_id
                    prefix_tree.insert(name, drug_id)

        # now look at every drug name in drugs_list; if we cannot
        # find a drug_id, put name in anyways so count is accurate
        drugs_list = []
        for i in range(ord("a"), ord("t") + 1):
            drug_name = self.__meds.get_value(f"pm{chr(i)}", str)
            if not drug_name:
                continue

            # first try exact match
            drug_name = drug_name.strip().lower()
            condensed_drug_name = ALPHA_NUMERIC.sub("", drug_name)
            drug_id = udsmeds.get(condensed_drug_name)

            # next try a prefix lookup
            if not drug_id:
                drug_id = prefix_tree.get_closest_match(condensed_drug_name)

            drugs_list.append(drug_name if drug_id is None else drug_id)

        return sorted(drugs_list)
