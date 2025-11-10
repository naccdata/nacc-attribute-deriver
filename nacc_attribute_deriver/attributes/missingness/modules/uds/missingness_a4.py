"""Class to handle A4-specific missingness values."""

import csv
from importlib import resources
from typing import Dict, Optional

from nacc_attribute_deriver import config
from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSMissingness
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
)
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


def load_udsmeds() -> Dict[str, str]:
    """Load UDSMEDS table to map drug ID to drug name."""
    udsmeds_file = resources.files(config).joinpath("UDSMEDS.csv")
    udsmeds: Dict[str, str] = {}

    with udsmeds_file.open("r") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            drug_id = row["DRUG_ID"]

            # there are many clashes; only use first one found
            if drug_id in udsmeds:
                continue

            udsmeds[drug_id] = row["DRUG_NAME_UCASE"]

    return udsmeds


# load this globally so it's only done once per execution
UDSMEDS = load_udsmeds()


class UDSFormA4Missingness(UDSMissingness):
    def __init__(self, table: SymbolTable):
        super().__init__(table)
        working = WorkingDerivedNamespace(table=table)

        # grab corresponding drugs list, curated from MEDS file
        if self.formver < 4:
            form_date = self.uds.get_value("frmdatea4", str)
            if not form_date:  # try visitdate
                form_date = self.uds.get_value("visitdate", str)

            if not form_date:
                raise AttributeDeriverError("Cannot determine A4 form date")

            self.__drugs = working.get_corresponding_longitudinal_value(  # type: ignore
                form_date, "drugs-list", list
            )
        else:
            self.__drugs = None

    def _missingness_anymeds(self) -> Optional[int]:
        """Handles missingness for ANYMEDS."""
        # it seems in older versions, they could submit MEDS but
        # still set ANYMEDS to 0, so legacy code would update/fix it
        if self.formver < 4 and self.__drugs:
            return 1

        return self.generic_missingness("anymeds", int)

    def __handle_rxnormidx(self, field: str) -> Optional[str]:
        """V4+.

        Handles missingness for all RXNORMIDX (1-40) values.
        """
        if self.formver < 4:
            return INFORMED_BLANK

        return self.generic_missingness(field, str)

    def _missingness_rxnormid1(self) -> Optional[str]:
        """Handles missingness for RXNORMID1."""
        return self.__handle_rxnormidx("rxnormid1")

    def _missingness_rxnormid2(self) -> Optional[str]:
        """Handles missingness for RXNORMID2."""
        return self.__handle_rxnormidx("rxnormid2")

    def _missingness_rxnormid3(self) -> Optional[str]:
        """Handles missingness for RXNORMID3."""
        return self.__handle_rxnormidx("rxnormid3")

    def _missingness_rxnormid4(self) -> Optional[str]:
        """Handles missingness for RXNORMID4."""
        return self.__handle_rxnormidx("rxnormid4")

    def _missingness_rxnormid5(self) -> Optional[str]:
        """Handles missingness for RXNORMID5."""
        return self.__handle_rxnormidx("rxnormid5")

    def _missingness_rxnormid6(self) -> Optional[str]:
        """Handles missingness for RXNORMID6."""
        return self.__handle_rxnormidx("rxnormid6")

    def _missingness_rxnormid7(self) -> Optional[str]:
        """Handles missingness for RXNORMID7."""
        return self.__handle_rxnormidx("rxnormid7")

    def _missingness_rxnormid8(self) -> Optional[str]:
        """Handles missingness for RXNORMID8."""
        return self.__handle_rxnormidx("rxnormid8")

    def _missingness_rxnormid9(self) -> Optional[str]:
        """Handles missingness for RXNORMID9."""
        return self.__handle_rxnormidx("rxnormid9")

    def _missingness_rxnormid10(self) -> Optional[str]:
        """Handles missingness for RXNORMID10."""
        return self.__handle_rxnormidx("rxnormid10")

    def _missingness_rxnormid11(self) -> Optional[str]:
        """Handles missingness for RXNORMID11."""
        return self.__handle_rxnormidx("rxnormid11")

    def _missingness_rxnormid12(self) -> Optional[str]:
        """Handles missingness for RXNORMID12."""
        return self.__handle_rxnormidx("rxnormid12")

    def _missingness_rxnormid13(self) -> Optional[str]:
        """Handles missingness for RXNORMID13."""
        return self.__handle_rxnormidx("rxnormid13")

    def _missingness_rxnormid14(self) -> Optional[str]:
        """Handles missingness for RXNORMID14."""
        return self.__handle_rxnormidx("rxnormid14")

    def _missingness_rxnormid15(self) -> Optional[str]:
        """Handles missingness for RXNORMID15."""
        return self.__handle_rxnormidx("rxnormid15")

    def _missingness_rxnormid16(self) -> Optional[str]:
        """Handles missingness for RXNORMID16."""
        return self.__handle_rxnormidx("rxnormid16")

    def _missingness_rxnormid17(self) -> Optional[str]:
        """Handles missingness for RXNORMID17."""
        return self.__handle_rxnormidx("rxnormid17")

    def _missingness_rxnormid18(self) -> Optional[str]:
        """Handles missingness for RXNORMID18."""
        return self.__handle_rxnormidx("rxnormid18")

    def _missingness_rxnormid19(self) -> Optional[str]:
        """Handles missingness for RXNORMID19."""
        return self.__handle_rxnormidx("rxnormid19")

    def _missingness_rxnormid20(self) -> Optional[str]:
        """Handles missingness for RXNORMID20."""
        return self.__handle_rxnormidx("rxnormid20")

    def _missingness_rxnormid21(self) -> Optional[str]:
        """Handles missingness for RXNORMID21."""
        return self.__handle_rxnormidx("rxnormid21")

    def _missingness_rxnormid22(self) -> Optional[str]:
        """Handles missingness for RXNORMID22."""
        return self.__handle_rxnormidx("rxnormid22")

    def _missingness_rxnormid23(self) -> Optional[str]:
        """Handles missingness for RXNORMID23."""
        return self.__handle_rxnormidx("rxnormid23")

    def _missingness_rxnormid24(self) -> Optional[str]:
        """Handles missingness for RXNORMID24."""
        return self.__handle_rxnormidx("rxnormid24")

    def _missingness_rxnormid25(self) -> Optional[str]:
        """Handles missingness for RXNORMID25."""
        return self.__handle_rxnormidx("rxnormid25")

    def _missingness_rxnormid26(self) -> Optional[str]:
        """Handles missingness for RXNORMID26."""
        return self.__handle_rxnormidx("rxnormid26")

    def _missingness_rxnormid27(self) -> Optional[str]:
        """Handles missingness for RXNORMID27."""
        return self.__handle_rxnormidx("rxnormid27")

    def _missingness_rxnormid28(self) -> Optional[str]:
        """Handles missingness for RXNORMID28."""
        return self.__handle_rxnormidx("rxnormid28")

    def _missingness_rxnormid29(self) -> Optional[str]:
        """Handles missingness for RXNORMID29."""
        return self.__handle_rxnormidx("rxnormid29")

    def _missingness_rxnormid30(self) -> Optional[str]:
        """Handles missingness for RXNORMID30."""
        return self.__handle_rxnormidx("rxnormid30")

    def _missingness_rxnormid31(self) -> Optional[str]:
        """Handles missingness for RXNORMID31."""
        return self.__handle_rxnormidx("rxnormid31")

    def _missingness_rxnormid32(self) -> Optional[str]:
        """Handles missingness for RXNORMID32."""
        return self.__handle_rxnormidx("rxnormid32")

    def _missingness_rxnormid33(self) -> Optional[str]:
        """Handles missingness for RXNORMID33."""
        return self.__handle_rxnormidx("rxnormid33")

    def _missingness_rxnormid34(self) -> Optional[str]:
        """Handles missingness for RXNORMID34."""
        return self.__handle_rxnormidx("rxnormid34")

    def _missingness_rxnormid35(self) -> Optional[str]:
        """Handles missingness for RXNORMID35."""
        return self.__handle_rxnormidx("rxnormid35")

    def _missingness_rxnormid36(self) -> Optional[str]:
        """Handles missingness for RXNORMID36."""
        return self.__handle_rxnormidx("rxnormid36")

    def _missingness_rxnormid37(self) -> Optional[str]:
        """Handles missingness for RXNORMID37."""
        return self.__handle_rxnormidx("rxnormid37")

    def _missingness_rxnormid38(self) -> Optional[str]:
        """Handles missingness for RXNORMID38."""
        return self.__handle_rxnormidx("rxnormid38")

    def _missingness_rxnormid39(self) -> Optional[str]:
        """Handles missingness for RXNORMID39."""
        return self.__handle_rxnormidx("rxnormid39")

    def _missingness_rxnormid40(self) -> Optional[str]:
        """Handles missingness for RXNORMID40."""
        return self.__handle_rxnormidx("rxnormid40")

    def __handle_drugx(self, field: str) -> Optional[str]:
        """V3 and earlier. Handles missingness for all DRUGX (1-40) values.

        Need to map over from the drug list.
        """
        if self.formver >= 4:
            return INFORMED_BLANK

        if self.__drugs:
            index = int(field.replace("drug", "")) - 1
            if len(self.__drugs) > index:
                drug_id = self.__drugs[index]

                # if drug ID doesn't map to a name leave as-is
                return UDSMEDS.get(drug_id, drug_id)

        return self.generic_missingness(field, str)

    def _missingness_drug1(self) -> Optional[str]:
        """Handles missingness for DRUG1."""
        return self.__handle_drugx("drug1")

    def _missingness_drug2(self) -> Optional[str]:
        """Handles missingness for DRUG2."""
        return self.__handle_drugx("drug2")

    def _missingness_drug3(self) -> Optional[str]:
        """Handles missingness for DRUG3."""
        return self.__handle_drugx("drug3")

    def _missingness_drug4(self) -> Optional[str]:
        """Handles missingness for DRUG4."""
        return self.__handle_drugx("drug4")

    def _missingness_drug5(self) -> Optional[str]:
        """Handles missingness for DRUG5."""
        return self.__handle_drugx("drug5")

    def _missingness_drug6(self) -> Optional[str]:
        """Handles missingness for DRUG6."""
        return self.__handle_drugx("drug6")

    def _missingness_drug7(self) -> Optional[str]:
        """Handles missingness for DRUG7."""
        return self.__handle_drugx("drug7")

    def _missingness_drug8(self) -> Optional[str]:
        """Handles missingness for DRUG8."""
        return self.__handle_drugx("drug8")

    def _missingness_drug9(self) -> Optional[str]:
        """Handles missingness for DRUG9."""
        return self.__handle_drugx("drug9")

    def _missingness_drug10(self) -> Optional[str]:
        """Handles missingness for DRUG10."""
        return self.__handle_drugx("drug10")

    def _missingness_drug11(self) -> Optional[str]:
        """Handles missingness for DRUG11."""
        return self.__handle_drugx("drug11")

    def _missingness_drug12(self) -> Optional[str]:
        """Handles missingness for DRUG12."""
        return self.__handle_drugx("drug12")

    def _missingness_drug13(self) -> Optional[str]:
        """Handles missingness for DRUG13."""
        return self.__handle_drugx("drug13")

    def _missingness_drug14(self) -> Optional[str]:
        """Handles missingness for DRUG14."""
        return self.__handle_drugx("drug14")

    def _missingness_drug15(self) -> Optional[str]:
        """Handles missingness for DRUG15."""
        return self.__handle_drugx("drug15")

    def _missingness_drug16(self) -> Optional[str]:
        """Handles missingness for DRUG16."""
        return self.__handle_drugx("drug16")

    def _missingness_drug17(self) -> Optional[str]:
        """Handles missingness for DRUG17."""
        return self.__handle_drugx("drug17")

    def _missingness_drug18(self) -> Optional[str]:
        """Handles missingness for DRUG18."""
        return self.__handle_drugx("drug18")

    def _missingness_drug19(self) -> Optional[str]:
        """Handles missingness for DRUG19."""
        return self.__handle_drugx("drug19")

    def _missingness_drug20(self) -> Optional[str]:
        """Handles missingness for DRUG20."""
        return self.__handle_drugx("drug20")

    def _missingness_drug21(self) -> Optional[str]:
        """Handles missingness for DRUG21."""
        return self.__handle_drugx("drug21")

    def _missingness_drug22(self) -> Optional[str]:
        """Handles missingness for DRUG22."""
        return self.__handle_drugx("drug22")

    def _missingness_drug23(self) -> Optional[str]:
        """Handles missingness for DRUG23."""
        return self.__handle_drugx("drug23")

    def _missingness_drug24(self) -> Optional[str]:
        """Handles missingness for DRUG24."""
        return self.__handle_drugx("drug24")

    def _missingness_drug25(self) -> Optional[str]:
        """Handles missingness for DRUG25."""
        return self.__handle_drugx("drug25")

    def _missingness_drug26(self) -> Optional[str]:
        """Handles missingness for DRUG26."""
        return self.__handle_drugx("drug26")

    def _missingness_drug27(self) -> Optional[str]:
        """Handles missingness for DRUG27."""
        return self.__handle_drugx("drug27")

    def _missingness_drug28(self) -> Optional[str]:
        """Handles missingness for DRUG28."""
        return self.__handle_drugx("drug28")

    def _missingness_drug29(self) -> Optional[str]:
        """Handles missingness for DRUG29."""
        return self.__handle_drugx("drug29")

    def _missingness_drug30(self) -> Optional[str]:
        """Handles missingness for DRUG30."""
        return self.__handle_drugx("drug30")

    def _missingness_drug31(self) -> Optional[str]:
        """Handles missingness for DRUG31."""
        return self.__handle_drugx("drug31")

    def _missingness_drug32(self) -> Optional[str]:
        """Handles missingness for DRUG32."""
        return self.__handle_drugx("drug32")

    def _missingness_drug33(self) -> Optional[str]:
        """Handles missingness for DRUG33."""
        return self.__handle_drugx("drug33")

    def _missingness_drug34(self) -> Optional[str]:
        """Handles missingness for DRUG34."""
        return self.__handle_drugx("drug34")

    def _missingness_drug35(self) -> Optional[str]:
        """Handles missingness for DRUG35."""
        return self.__handle_drugx("drug35")

    def _missingness_drug36(self) -> Optional[str]:
        """Handles missingness for DRUG36."""
        return self.__handle_drugx("drug36")

    def _missingness_drug37(self) -> Optional[str]:
        """Handles missingness for DRUG37."""
        return self.__handle_drugx("drug37")

    def _missingness_drug38(self) -> Optional[str]:
        """Handles missingness for DRUG38."""
        return self.__handle_drugx("drug38")

    def _missingness_drug39(self) -> Optional[str]:
        """Handles missingness for DRUG39."""
        return self.__handle_drugx("drug39")

    def _missingness_drug40(self) -> Optional[str]:
        """Handles missingness for DRUG40."""
        return self.__handle_drugx("drug40")
