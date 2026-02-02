"""Class to handle A4-specific missingness values."""

import csv
from importlib import resources
from typing import Dict

from nacc_attribute_deriver import config
from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
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

            if drug_id in udsmeds:
                raise AttributeDeriverError(
                    f"Multiple definitions for drug id {drug_id}")

            udsmeds[drug_id] = row["DRUG_NAME_UCASE"]

    return udsmeds


# load this globally so it's only done once per execution
UDSMEDS = load_udsmeds()


class UDSFormA4Missingness(UDSMissingness):
    def __init__(self, table: SymbolTable):
        super().__init__(table)
        working = WorkingNamespace(table=table)

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

    def _missingness_anymeds(self) -> int:
        """Handles missingness for ANYMEDS."""
        # it seems in older versions, they could submit MEDS but
        # still set ANYMEDS to 0, or vice versa, so legacy code
        # fixes it by checking if there are actually drugs and
        # basing ANYMEDS off of that
        if self.formver < 4:
            return 1 if self.__drugs else 0

        return self.generic_missingness("anymeds", int)

    def __handle_rxnormidx(self, field: str) -> str:
        """V4+.

        Handles missingness for all RXNORMIDX (1-40) values. While
        effectively an int, being treated as a string.
        """
        if self.formver < 4:
            return INFORMED_BLANK

        return self.generic_missingness(field, str)

    def _missingness_rxnormid1(self) -> str:
        """Handles missingness for RXNORMID1."""
        return self.__handle_rxnormidx("rxnormid1")

    def _missingness_rxnormid2(self) -> str:
        """Handles missingness for RXNORMID2."""
        return self.__handle_rxnormidx("rxnormid2")

    def _missingness_rxnormid3(self) -> str:
        """Handles missingness for RXNORMID3."""
        return self.__handle_rxnormidx("rxnormid3")

    def _missingness_rxnormid4(self) -> str:
        """Handles missingness for RXNORMID4."""
        return self.__handle_rxnormidx("rxnormid4")

    def _missingness_rxnormid5(self) -> str:
        """Handles missingness for RXNORMID5."""
        return self.__handle_rxnormidx("rxnormid5")

    def _missingness_rxnormid6(self) -> str:
        """Handles missingness for RXNORMID6."""
        return self.__handle_rxnormidx("rxnormid6")

    def _missingness_rxnormid7(self) -> str:
        """Handles missingness for RXNORMID7."""
        return self.__handle_rxnormidx("rxnormid7")

    def _missingness_rxnormid8(self) -> str:
        """Handles missingness for RXNORMID8."""
        return self.__handle_rxnormidx("rxnormid8")

    def _missingness_rxnormid9(self) -> str:
        """Handles missingness for RXNORMID9."""
        return self.__handle_rxnormidx("rxnormid9")

    def _missingness_rxnormid10(self) -> str:
        """Handles missingness for RXNORMID10."""
        return self.__handle_rxnormidx("rxnormid10")

    def _missingness_rxnormid11(self) -> str:
        """Handles missingness for RXNORMID11."""
        return self.__handle_rxnormidx("rxnormid11")

    def _missingness_rxnormid12(self) -> str:
        """Handles missingness for RXNORMID12."""
        return self.__handle_rxnormidx("rxnormid12")

    def _missingness_rxnormid13(self) -> str:
        """Handles missingness for RXNORMID13."""
        return self.__handle_rxnormidx("rxnormid13")

    def _missingness_rxnormid14(self) -> str:
        """Handles missingness for RXNORMID14."""
        return self.__handle_rxnormidx("rxnormid14")

    def _missingness_rxnormid15(self) -> str:
        """Handles missingness for RXNORMID15."""
        return self.__handle_rxnormidx("rxnormid15")

    def _missingness_rxnormid16(self) -> str:
        """Handles missingness for RXNORMID16."""
        return self.__handle_rxnormidx("rxnormid16")

    def _missingness_rxnormid17(self) -> str:
        """Handles missingness for RXNORMID17."""
        return self.__handle_rxnormidx("rxnormid17")

    def _missingness_rxnormid18(self) -> str:
        """Handles missingness for RXNORMID18."""
        return self.__handle_rxnormidx("rxnormid18")

    def _missingness_rxnormid19(self) -> str:
        """Handles missingness for RXNORMID19."""
        return self.__handle_rxnormidx("rxnormid19")

    def _missingness_rxnormid20(self) -> str:
        """Handles missingness for RXNORMID20."""
        return self.__handle_rxnormidx("rxnormid20")

    def _missingness_rxnormid21(self) -> str:
        """Handles missingness for RXNORMID21."""
        return self.__handle_rxnormidx("rxnormid21")

    def _missingness_rxnormid22(self) -> str:
        """Handles missingness for RXNORMID22."""
        return self.__handle_rxnormidx("rxnormid22")

    def _missingness_rxnormid23(self) -> str:
        """Handles missingness for RXNORMID23."""
        return self.__handle_rxnormidx("rxnormid23")

    def _missingness_rxnormid24(self) -> str:
        """Handles missingness for RXNORMID24."""
        return self.__handle_rxnormidx("rxnormid24")

    def _missingness_rxnormid25(self) -> str:
        """Handles missingness for RXNORMID25."""
        return self.__handle_rxnormidx("rxnormid25")

    def _missingness_rxnormid26(self) -> str:
        """Handles missingness for RXNORMID26."""
        return self.__handle_rxnormidx("rxnormid26")

    def _missingness_rxnormid27(self) -> str:
        """Handles missingness for RXNORMID27."""
        return self.__handle_rxnormidx("rxnormid27")

    def _missingness_rxnormid28(self) -> str:
        """Handles missingness for RXNORMID28."""
        return self.__handle_rxnormidx("rxnormid28")

    def _missingness_rxnormid29(self) -> str:
        """Handles missingness for RXNORMID29."""
        return self.__handle_rxnormidx("rxnormid29")

    def _missingness_rxnormid30(self) -> str:
        """Handles missingness for RXNORMID30."""
        return self.__handle_rxnormidx("rxnormid30")

    def _missingness_rxnormid31(self) -> str:
        """Handles missingness for RXNORMID31."""
        return self.__handle_rxnormidx("rxnormid31")

    def _missingness_rxnormid32(self) -> str:
        """Handles missingness for RXNORMID32."""
        return self.__handle_rxnormidx("rxnormid32")

    def _missingness_rxnormid33(self) -> str:
        """Handles missingness for RXNORMID33."""
        return self.__handle_rxnormidx("rxnormid33")

    def _missingness_rxnormid34(self) -> str:
        """Handles missingness for RXNORMID34."""
        return self.__handle_rxnormidx("rxnormid34")

    def _missingness_rxnormid35(self) -> str:
        """Handles missingness for RXNORMID35."""
        return self.__handle_rxnormidx("rxnormid35")

    def _missingness_rxnormid36(self) -> str:
        """Handles missingness for RXNORMID36."""
        return self.__handle_rxnormidx("rxnormid36")

    def _missingness_rxnormid37(self) -> str:
        """Handles missingness for RXNORMID37."""
        return self.__handle_rxnormidx("rxnormid37")

    def _missingness_rxnormid38(self) -> str:
        """Handles missingness for RXNORMID38."""
        return self.__handle_rxnormidx("rxnormid38")

    def _missingness_rxnormid39(self) -> str:
        """Handles missingness for RXNORMID39."""
        return self.__handle_rxnormidx("rxnormid39")

    def _missingness_rxnormid40(self) -> str:
        """Handles missingness for RXNORMID40."""
        return self.__handle_rxnormidx("rxnormid40")

    def __handle_drugx(self, field: str) -> str:
        """V3 and earlier. Handles missingness for all DRUGX (1-40) values.

        Need to map over from the drug list.
        """
        if self.formver >= 4:
            return INFORMED_BLANK

        if self.__drugs:
            index = int(field.replace("drug", "")) - 1
            if len(self.__drugs) > index:
                drug_id = self.__drugs[index]

                # if drug ID doesn't map to a name, set to "*Not Codable*"
                result = UDSMEDS.get(drug_id, "*Not Codable*")
                if not result:
                    raise AttributeDeriverError(f"No drug for index {index}")

                return result

        return self.generic_missingness(field, str)

    def _missingness_drug1(self) -> str:
        """Handles missingness for DRUG1."""
        return self.__handle_drugx("drug1")

    def _missingness_drug2(self) -> str:
        """Handles missingness for DRUG2."""
        return self.__handle_drugx("drug2")

    def _missingness_drug3(self) -> str:
        """Handles missingness for DRUG3."""
        return self.__handle_drugx("drug3")

    def _missingness_drug4(self) -> str:
        """Handles missingness for DRUG4."""
        return self.__handle_drugx("drug4")

    def _missingness_drug5(self) -> str:
        """Handles missingness for DRUG5."""
        return self.__handle_drugx("drug5")

    def _missingness_drug6(self) -> str:
        """Handles missingness for DRUG6."""
        return self.__handle_drugx("drug6")

    def _missingness_drug7(self) -> str:
        """Handles missingness for DRUG7."""
        return self.__handle_drugx("drug7")

    def _missingness_drug8(self) -> str:
        """Handles missingness for DRUG8."""
        return self.__handle_drugx("drug8")

    def _missingness_drug9(self) -> str:
        """Handles missingness for DRUG9."""
        return self.__handle_drugx("drug9")

    def _missingness_drug10(self) -> str:
        """Handles missingness for DRUG10."""
        return self.__handle_drugx("drug10")

    def _missingness_drug11(self) -> str:
        """Handles missingness for DRUG11."""
        return self.__handle_drugx("drug11")

    def _missingness_drug12(self) -> str:
        """Handles missingness for DRUG12."""
        return self.__handle_drugx("drug12")

    def _missingness_drug13(self) -> str:
        """Handles missingness for DRUG13."""
        return self.__handle_drugx("drug13")

    def _missingness_drug14(self) -> str:
        """Handles missingness for DRUG14."""
        return self.__handle_drugx("drug14")

    def _missingness_drug15(self) -> str:
        """Handles missingness for DRUG15."""
        return self.__handle_drugx("drug15")

    def _missingness_drug16(self) -> str:
        """Handles missingness for DRUG16."""
        return self.__handle_drugx("drug16")

    def _missingness_drug17(self) -> str:
        """Handles missingness for DRUG17."""
        return self.__handle_drugx("drug17")

    def _missingness_drug18(self) -> str:
        """Handles missingness for DRUG18."""
        return self.__handle_drugx("drug18")

    def _missingness_drug19(self) -> str:
        """Handles missingness for DRUG19."""
        return self.__handle_drugx("drug19")

    def _missingness_drug20(self) -> str:
        """Handles missingness for DRUG20."""
        return self.__handle_drugx("drug20")

    def _missingness_drug21(self) -> str:
        """Handles missingness for DRUG21."""
        return self.__handle_drugx("drug21")

    def _missingness_drug22(self) -> str:
        """Handles missingness for DRUG22."""
        return self.__handle_drugx("drug22")

    def _missingness_drug23(self) -> str:
        """Handles missingness for DRUG23."""
        return self.__handle_drugx("drug23")

    def _missingness_drug24(self) -> str:
        """Handles missingness for DRUG24."""
        return self.__handle_drugx("drug24")

    def _missingness_drug25(self) -> str:
        """Handles missingness for DRUG25."""
        return self.__handle_drugx("drug25")

    def _missingness_drug26(self) -> str:
        """Handles missingness for DRUG26."""
        return self.__handle_drugx("drug26")

    def _missingness_drug27(self) -> str:
        """Handles missingness for DRUG27."""
        return self.__handle_drugx("drug27")

    def _missingness_drug28(self) -> str:
        """Handles missingness for DRUG28."""
        return self.__handle_drugx("drug28")

    def _missingness_drug29(self) -> str:
        """Handles missingness for DRUG29."""
        return self.__handle_drugx("drug29")

    def _missingness_drug30(self) -> str:
        """Handles missingness for DRUG30."""
        return self.__handle_drugx("drug30")

    def _missingness_drug31(self) -> str:
        """Handles missingness for DRUG31."""
        return self.__handle_drugx("drug31")

    def _missingness_drug32(self) -> str:
        """Handles missingness for DRUG32."""
        return self.__handle_drugx("drug32")

    def _missingness_drug33(self) -> str:
        """Handles missingness for DRUG33."""
        return self.__handle_drugx("drug33")

    def _missingness_drug34(self) -> str:
        """Handles missingness for DRUG34."""
        return self.__handle_drugx("drug34")

    def _missingness_drug35(self) -> str:
        """Handles missingness for DRUG35."""
        return self.__handle_drugx("drug35")

    def _missingness_drug36(self) -> str:
        """Handles missingness for DRUG36."""
        return self.__handle_drugx("drug36")

    def _missingness_drug37(self) -> str:
        """Handles missingness for DRUG37."""
        return self.__handle_drugx("drug37")

    def _missingness_drug38(self) -> str:
        """Handles missingness for DRUG38."""
        return self.__handle_drugx("drug38")

    def _missingness_drug39(self) -> str:
        """Handles missingness for DRUG39."""
        return self.__handle_drugx("drug39")

    def _missingness_drug40(self) -> str:
        """Handles missingness for DRUG40."""
        return self.__handle_drugx("drug40")

    def __handle_drug_idx(self, field: str) -> str:
        """V3 and earlier.

        These are not exactly missingness but are conflated with the
        drug names and similarly mapped over from the drug list.
        """
        if self.formver >= 4:
            return INFORMED_BLANK

        if self.__drugs:
            index = int(field.replace("drug", "")) - 1
            if len(self.__drugs) > index:
                return self.__drugs[index]

        return INFORMED_BLANK

    def _missingness_drug_id1(self) -> str:
        """Handles missingness for DRUG_ID1."""
        return self.__handle_drug_idx("drug1")

    def _missingness_drug_id2(self) -> str:
        """Handles missingness for DRUG_ID2."""
        return self.__handle_drug_idx("drug2")

    def _missingness_drug_id3(self) -> str:
        """Handles missingness for DRUG_ID3."""
        return self.__handle_drug_idx("drug3")

    def _missingness_drug_id4(self) -> str:
        """Handles missingness for DRUG_ID4."""
        return self.__handle_drug_idx("drug4")

    def _missingness_drug_id5(self) -> str:
        """Handles missingness for DRUG_ID5."""
        return self.__handle_drug_idx("drug5")

    def _missingness_drug_id6(self) -> str:
        """Handles missingness for DRUG_ID6."""
        return self.__handle_drug_idx("drug6")

    def _missingness_drug_id7(self) -> str:
        """Handles missingness for DRUG_ID7."""
        return self.__handle_drug_idx("drug7")

    def _missingness_drug_id8(self) -> str:
        """Handles missingness for DRUG_ID8."""
        return self.__handle_drug_idx("drug8")

    def _missingness_drug_id9(self) -> str:
        """Handles missingness for DRUG_ID9."""
        return self.__handle_drug_idx("drug9")

    def _missingness_drug_id10(self) -> str:
        """Handles missingness for DRUG_ID10."""
        return self.__handle_drug_idx("drug10")

    def _missingness_drug_id11(self) -> str:
        """Handles missingness for DRUG_ID11."""
        return self.__handle_drug_idx("drug11")

    def _missingness_drug_id12(self) -> str:
        """Handles missingness for DRUG_ID12."""
        return self.__handle_drug_idx("drug12")

    def _missingness_drug_id13(self) -> str:
        """Handles missingness for DRUG_ID13."""
        return self.__handle_drug_idx("drug13")

    def _missingness_drug_id14(self) -> str:
        """Handles missingness for DRUG_ID14."""
        return self.__handle_drug_idx("drug14")

    def _missingness_drug_id15(self) -> str:
        """Handles missingness for DRUG_ID15."""
        return self.__handle_drug_idx("drug15")

    def _missingness_drug_id16(self) -> str:
        """Handles missingness for DRUG_ID16."""
        return self.__handle_drug_idx("drug16")

    def _missingness_drug_id17(self) -> str:
        """Handles missingness for DRUG_ID17."""
        return self.__handle_drug_idx("drug17")

    def _missingness_drug_id18(self) -> str:
        """Handles missingness for DRUG_ID18."""
        return self.__handle_drug_idx("drug18")

    def _missingness_drug_id19(self) -> str:
        """Handles missingness for DRUG_ID19."""
        return self.__handle_drug_idx("drug19")

    def _missingness_drug_id20(self) -> str:
        """Handles missingness for DRUG_ID20."""
        return self.__handle_drug_idx("drug20")

    def _missingness_drug_id21(self) -> str:
        """Handles missingness for DRUG_ID21."""
        return self.__handle_drug_idx("drug21")

    def _missingness_drug_id22(self) -> str:
        """Handles missingness for DRUG_ID22."""
        return self.__handle_drug_idx("drug22")

    def _missingness_drug_id23(self) -> str:
        """Handles missingness for DRUG_ID23."""
        return self.__handle_drug_idx("drug23")

    def _missingness_drug_id24(self) -> str:
        """Handles missingness for DRUG_ID24."""
        return self.__handle_drug_idx("drug24")

    def _missingness_drug_id25(self) -> str:
        """Handles missingness for DRUG_ID25."""
        return self.__handle_drug_idx("drug25")

    def _missingness_drug_id26(self) -> str:
        """Handles missingness for DRUG_ID26."""
        return self.__handle_drug_idx("drug26")

    def _missingness_drug_id27(self) -> str:
        """Handles missingness for DRUG_ID27."""
        return self.__handle_drug_idx("drug27")

    def _missingness_drug_id28(self) -> str:
        """Handles missingness for DRUG_ID28."""
        return self.__handle_drug_idx("drug28")

    def _missingness_drug_id29(self) -> str:
        """Handles missingness for DRUG_ID29."""
        return self.__handle_drug_idx("drug29")

    def _missingness_drug_id30(self) -> str:
        """Handles missingness for DRUG_ID30."""
        return self.__handle_drug_idx("drug30")

    def _missingness_drug_id31(self) -> str:
        """Handles missingness for DRUG_ID31."""
        return self.__handle_drug_idx("drug31")

    def _missingness_drug_id32(self) -> str:
        """Handles missingness for DRUG_ID32."""
        return self.__handle_drug_idx("drug32")

    def _missingness_drug_id33(self) -> str:
        """Handles missingness for DRUG_ID33."""
        return self.__handle_drug_idx("drug33")

    def _missingness_drug_id34(self) -> str:
        """Handles missingness for DRUG_ID34."""
        return self.__handle_drug_idx("drug34")

    def _missingness_drug_id35(self) -> str:
        """Handles missingness for DRUG_ID35."""
        return self.__handle_drug_idx("drug35")

    def _missingness_drug_id36(self) -> str:
        """Handles missingness for DRUG_ID36."""
        return self.__handle_drug_idx("drug36")

    def _missingness_drug_id37(self) -> str:
        """Handles missingness for DRUG_ID37."""
        return self.__handle_drug_idx("drug37")

    def _missingness_drug_id38(self) -> str:
        """Handles missingness for DRUG_ID38."""
        return self.__handle_drug_idx("drug38")

    def _missingness_drug_id39(self) -> str:
        """Handles missingness for DRUG_ID39."""
        return self.__handle_drug_idx("drug39")

    def _missingness_drug_id40(self) -> str:
        """Handles missingness for DRUG_ID40."""
        return self.__handle_drug_idx("drug40")
