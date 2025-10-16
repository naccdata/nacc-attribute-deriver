"""Derived variables from form A4: Subject Medications. These are effectively
just looking at hardcoded strings.

From derivedmeds.sas.

NOTE: Derived variable are only supposed to reflect the last 2 weeks, so
    variables do NOT get carried over (i.e. if they do not submit a meds form
    for that visit, the derived variable is -4/None).
"""

from typing import List, Optional

from nacc_attribute_deriver.attributes.collection.uds_attribute import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingDerivedNamespace,
)
from nacc_attribute_deriver.schema.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.schema.errors import AttributeDeriverError
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormA4Attribute(UDSAttributeCollection):
    """Class to collect UDS A4 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__working = WorkingDerivedNamespace(table=table)
        self.__meds = self.__load_drugs_list()

    @property
    def submitted(self) -> bool:
        # TODO: for v4 this will be modea4
        # SAS looks at anymeds but a4sub seems to be a better indicator
        return self.uds.get_value("a4sub", int) == 1

    def __load_drugs_list(self) -> List[str]:
        """Loads drugs_list from MEDS form data that was saved under
        subject.info.derived.drugs_list.<visitdate>."""
        if not self.submitted:
            return []

        form_date = self.uds.get_value("frmdatea4", str)
        if not form_date:  # try visitdate
            form_date = self.uds.get_value("visitdate", str)

        if not form_date:
            raise AttributeDeriverError("Cannot determine A4 form date")

        drugs = self.__working.get_corresponding_longitudinal_value(
            form_date, "drugs-list", list
        )

        if drugs is None:
            return []

        return [x.strip().lower() for x in drugs]

    def _create_naccamd(self) -> int:
        """Creates NACCAMD - Total number of medications reported at
        each visit.
        """
        if not self.submitted:
            return INFORMED_MISSINGNESS

        return len(self.__meds)

    def check_drugs(self, target_codes: List[str]) -> int:
        """Check if any of the 40 write-in drugs match the target codes.

        Args:
            target_codes: List of target codes to check
        Returns:
            1 if there is a match, 0 otherwise
        """
        if not self.submitted:
            return INFORMED_MISSINGNESS

        if not self.__meds:
            return 0

        return 1 if any(x in target_codes for x in self.__meds) else 0

    def _create_naccaaas(self) -> Optional[int]:
        """Creates NACCAAAS - Reported current use of an antiadenergic agent."""
        return self.check_drugs(
            [
                "d00131",
                "d00138",
                "d00367",
                "d00386",
                "d00725",
                "d00726",
                "d00739",
                "d03151",
                "d03563",
                "d04121",
                "d04797",
                "d07354",
                "d07634",
                "d00044",
                "d00130",
                "d00133",
                "d00717",
            ]
        )

    def _create_naccaanx(self) -> Optional[int]:
        """Creates NACCAANX - Reported current use of an anxiolytic,
        sedative, or hypnotic agent
        """
        return self.check_drugs(
            [
                "d00171",
                "d00335",
                "d00368",
                "d00919",
                "d00923",
                "d03061",
                "d04005",
                "d00040",
                "d00148",
                "d00149",
                "d00168",
                "d00189",
                "d00197",
                "d00238",
                "d00301",
                "d00384",
                "d00397",
                "d00904",
                "d00915",
                "d00917",
                "d00147",
                "d00182",
                "d00212",
                "d00217",
                "d00226",
                "d00288",
                "d00782",
                "d00907",
                "d00909",
                "d00910",
                "d00911",
                "d00912",
                "d00914",
                "d03154",
                "d04058",
                "d04452",
                "d04505",
                "d04806",
                "d05421",
                "d05578",
            ]
        )

    def _create_naccac(self) -> Optional[int]:
        """Creates NACCAC - Reported current use of an anticoagulant
        or antiplatelet agent.
        """
        return self.check_drugs(
            [
                "d00252",
                "d03041",
                "d03812",
                "d04114",
                "d04136",
                "d04659",
                "d07385",
                "d00022",
                "d00519",
                "d03889",
                "d04291",
                "d04698",
                "d04698",
                "d04744",
                "d04865",
                "d07137",
                "d04786",
                "d07356",
                "d00170",
                "d00213",
                "d00514",
                "d04258",
                "d04258",
                "d04382",
                "d04497",
                "d04883",
                "d07409",
                "d07693",
                "d07721",
                "d03811",
                "d04315",
                "d07804",
                "d04316",
            ]
        )

    def _create_naccacei(self) -> Optional[int]:
        """Creates NACCACEI - Reported current use of an angiotensin
        converting enzyme (ACE) inhibitor.
        """
        return self.check_drugs(
            [
                "d00006",
                "d00013",
                "d00242",
                "d00365",
                "d00728",
                "d00730",
                "d00732",
                "d03835",
                "d04008",
                "d04440",
            ]
        )

    def _create_naccadep(self) -> Optional[int]:
        """Creates NACCADEP - Reported current use of an antidepressant."""
        return self.check_drugs(
            [
                "d00181",
                "d04408",
                "d04726",
                "d07740",
                "d00236",
                "d00880",
                "d03157",
                "d03804",
                "d04332",
                "d04332",
                "d04812",
                "d00144",
                "d00145",
                "d00146",
                "d00217",
                "d00259",
                "d00259",
                "d00873",
                "d00874",
                "d00875",
                "d00876",
                "d00882",
                "d00883",
                "d00884",
                "d00976",
                "d00395",
                "d03808",
                "d00877",
                "d04025",
                "d03181",
                "d05355",
                "d06635",
                "d08114",
                "d07113",
            ]
        )

    def _create_naccadmd(self) -> Optional[int]:
        """Creates NACCADMD - Reported current use of a FDA-approved
        medication for Alzheimer's disease symptoms.
        """
        return self.check_drugs(
            [
                "d03176",
                "d04099",
                "d04537",
                "d04750",
                "d04899",
            ]
        )

    def _create_naccahtn(self) -> Optional[int]:
        """Creates NACCAHTN - Reported current use of any type of
        antihypertensive or blood pressure medication.
        """
        return (
            1
            if any(
                [
                    self._create_naccacei(),
                    self._create_naccaaas(),
                    self._create_naccbeta(),
                    self._create_naccccbs(),
                    self._create_naccdiur(),
                    self._create_naccvasd(),
                    self._create_nacchtnc(),
                    self._create_naccangi(),
                ]
            )
            else 0
        )

    def _create_naccangi(self) -> Optional[int]:
        """Creates NACCANGI - Reported current use of an angiotensin
        II inhibitor.
        """
        return self.check_drugs(
            [
                "d03821",
                "d04113",
                "d04222",
                "d04266",
                "d04322",
                "d04364",
                "d04801",
                "d07754",
            ]
        )

    def _create_naccapsy(self) -> Optional[int]:
        """Creates NACCAPSY - Reported current use of an antipsychotic
        agent.
        """
        return self.check_drugs(
            [
                "d00027",
                "d00061",
                "d00896",
                "d00897",
                "d00898",
                "d03462",
                "d03463",
                "d04917",
                "d00064",
                "d00237",
                "d00355",
                "d00356",
                "d00389",
                "d00814",
                "d00855",
                "d00889",
                "d00890",
                "d03152",
                "d00391",
                "d00199",
                "d03180",
                "d04050",
                "d04220",
                "d04747",
                "d04825",
                "d06297",
                "d07441",
                "d07473",
                "d07705",
            ]
        )

    def _create_naccbeta(self) -> Optional[int]:
        """Creates NACCBETA - Reported current use of a beta-adrenergic
        blocking agent (beta-blocker).
        """
        return self.check_drugs(
            [
                "d00004",
                "d00128",
                "d00134",
                "d00176",
                "d00224",
                "d00709",
                "d05265",
                "d00016",
                "d00018",
                "d00032",
                "d00137",
                "d00139",
                "d00332",
                "d00371",
                "d00708",
                "d03847",
            ]
        )

    def _create_naccccbs(self) -> Optional[int]:
        """Creates NACCCCBS - Reported current use of a calcium channel
        blocking agent.
        """
        return self.check_drugs(
            [
                "d00045",
                "d00048",
                "d00051",
                "d00231",
                "d00270",
                "d00315",
                "d00318",
                "d00688",
                "d00689",
                "d03825",
                "d04139",
                "d07312",
            ]
        )

    def _create_naccdbmd(self) -> Optional[int]:
        """Creates NACCDBMD - Reported current use of a diabetes medication."""
        return self.check_drugs(
            [
                "d00042",
                "d00162",
                "d00246",
                "d00248",
                "d00393",
                "d00394",
                "d03864",
                "d03807",
                "d00262",
                "d04511",
                "d04369",
                "d04370",
                "d04371",
                "d04372",
                "d04373",
                "d04374",
                "d04510",
                "d04538",
                "d04697",
                "d04838",
                "d04839",
                "d05278",
                "d05436",
                "d05765",
                "d03846",
                "d04110",
                "d04122",
                "d04434",
                "d04442",
                "d04267",
                "d04743",
                "d04703",
                "d04820",
                "d04823",
                "d05635",
                "d05674",
                "d05856",
                "d06720",
                "d07292",
                "d07709",
                "d07805",
                "d05896",
                "d07467",
                "d07767",
                "d05488",
                "d05529",
                "d07825",
                "d07466",
            ]
        )

    def _create_naccdiur(self) -> Optional[int]:
        """Creates NACCDIUR - Reported current use of a diuretic."""
        return self.check_drugs(
            [
                "d00070",
                "d00179",
                "d00649",
                "d03189",
                "d00169",
                "d00373",
                "d00396",
                "d00190",
                "d00253",
                "d00260",
                "d00299",
                "d00641",
                "d00643",
                "d00644",
                "d00645",
                "d00646",
                "d00647",
                "d00161",
                "d00639",
                "d00640",
                "d00282",
                "d03585",
                "d04207",
            ]
        )

    def _create_naccemd(self) -> Optional[int]:
        """Creates NACCEMD - Reported current use of estrogen hormone
        therapy.
        """
        return self.check_drugs(
            [
                "d00537",
                "d00541",
                "d00542",
                "d00543",
                "d00546",
                "d00545",
            ]
        )

    def _create_naccepmd(self) -> Optional[int]:
        """Creates NACCEPMD - Reported current use of estrogen + progestin
        hormone therapy.
        """
        return self.check_drugs(
            [
                "d05530",
                "d03238",
                "d04375",
                "d04506",
                "d03819",
            ]
        )

    def _create_nacchtnc(self) -> Optional[int]:
        """Creates NACCHTNC - Reported current use of antihypertensive
        combination therapy.
        """
        return self.check_drugs(
            [
                "d03052",
                "d03193",
                "d03247",
                "d03248",
                "d03250",
                "d03251",
                "d03253",
                "d03254",
                "d03255",
                "d03256",
                "d03257",
                "d03258",
                "d03259",
                "d03260",
                "d03261",
                "d03263",
                "d03265",
                "d03266",
                "d03267",
                "d03268",
                "d03269",
                "d03564",
                "d03565",
                "d03566",
                "d03740",
                "d03744",
                "d03778",
                "d03829",
                "d03830",
                "d04060",
                "d04065",
                "d04116",
                "d04141",
                "d04245",
                "d04293",
                "d04509",
                "d04539",
                "d04711",
                "d04737",
                "d04837",
                "d04878",
                "d05048",
                "d05540",
                "d06662",
                "d06905",
                "d07077",
                "d07440",
                "d07486",
                "d07498",
                "d07668",
                "d07678",
                "d07725",
            ]
        )

    def _create_nacclipl(self) -> Optional[int]:
        """Creates NACCLIPL - Reported current use of lipid lowering
        medication.
        """
        return self.check_drugs(
            [
                "d00280",
                "d00348",
                "d00746",
                "d03183",
                "d04105",
                "d04140",
                "d04426",
                "d04851",
                "d07637",
                "d00314",
                "d00353",
                "d00747",
                "d00196",
                "d00245",
                "d04286",
                "d07371",
                "d00193",
                "d00744",
                "d04695",
                "d04824",
                "d04787",
                "d04883",
                "d05048",
                "d05348",
                "d07110",
                "d07891",
                "d07805",
            ]
        )

    def _create_naccnsd(self) -> Optional[int]:
        """Creates NACCNSD - Reported current use of nonsteroidal
        anti-inflammatory medication.
        """
        return self.check_drugs(
            [
                "d00015",
                "d00019",
                "d00026",
                "d00028",
                "d00033",
                "d00039",
                "d00054",
                "d00239",
                "d00273",
                "d00283",
                "d00285",
                "d00310",
                "d00343",
                "d00848",
                "d00851",
                "d00853",
                "d04150",
                "d04271",
                "d04532",
                "d04913",
                "d07631",
                "d07764",
                "d00170",
                "d00208",
                "d00492",
                "d00842",
                "d00843",
                "d00844",
                "d00846",
                "d03651",
                "d03680",
                "d03883",
                "d04380",
                "d04433",
                "d04778",
                "d03437",
                "d03439",
                "d03443",
                "d03447",
                "d03448",
                "d03449",
                "d03453",
                "d03454",
                "d03457",
                "d03458",
                "d04155",
                "d04175",
                "d04333",
                "d05292",
                "d05351",
                "d05775",
                "d05819",
                "d06080",
                "d06833",
                "d07659",
                "d00341",
                "d07768",
            ]
        )

    def _create_naccpdmd(self) -> Optional[int]:
        """Creates NACCPDMD - Reported current use of an antiparkinson
        agent.
        """
        return self.check_drugs(
            [
                "d00175",
                "d00212",
                "d00969",
                "d00970",
                "d00972",
                "d00086",
                "d00178",
                "d00184",
                "d00277",
                "d00976",
                "d00977",
                "d03473",
                "d04112",
                "d04145",
                "d04215",
                "d04282",
                "d04460",
                "d04877",
                "d04991",
                "d05612",
                "d05848",
            ]
        )

    def _create_naccvasd(self) -> Optional[int]:
        """Creates NACCVASD - Reported current use of a vasodilator."""
        return self.check_drugs(
            [
                "d00132",
                "d00135",
                "d00136",
                "d00321",
                "d01387",
                "d04763",
            ]
        )
