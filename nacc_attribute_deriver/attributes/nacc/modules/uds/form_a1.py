"""Derived variables from form A1."""

from types import MappingProxyType
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import (
    calculate_age,
    datetime_from_form_date,
)

from .uds_attribute import UDSNamespace


class UDSFormA1Attribute(AttributeCollection):
    """Class to collect UDS A1 attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(table)

    # TODO: additional worry that SAS-code was extremely case-sensitive?
    WHITEX_RESPONSES = MappingProxyType(
        {
            "racex": {
                "arab",
                "arabic",
                "armenian",
                "asirian",
                "cicilan",
                "dutch",
                "easterneuropean/jewish",
                "egyptian",
                "europeanamerican",
                "french",
                "frenchamerican",
                "greek",
                "hungarian",
                "iranian",
                "italian",
                "italian-american",
                "jewish",
                "lebanese",
                "middleeast",
                "middleeastern",
                "norweigian",
                "persian",
                "polish",
                "portugese",
                "portuguese",
                "romanian",
                "russian",
                "scandinavian",
                "sicilian",
                "spanish",
                "spanishfromspain",
                "swedish,irish.russian",
                "switzerland",
                "syria,caucasian,arabic,french,hebrew",
                "syrian",
                "turkish",
                "ukrain",
            },
            "racesecx": {  # ONLY IF RACE == 1 and RACESEC == 50
                # in RACEX
                "arabic",
                "armenian",
                "ashkenazijew",
                "assyrian",
                "australian",
                "caucasian",
                "easterneurope",
                "easterneuropean",
                "easterneuropean/jewish",
                "england",
                "english",
                "european",
                "european/english",
                "europeanamerican",
                "french",
                "german",
                "germanic",
                "german/european",
                "grece",
                "greek",
                "hispanic",
                "hollander",
                "iranian",
                "italian",
                "irish",
                "itialianamerican",
                "jewish",
                "lebannon",
                "maltese",
                "middleeasten",
                "middleeasternisraeli",
                "middleeastern",
                "polandromania",
                "polish",
                "portuguese",
                "romanian",
                "russian",
                "russian,polish",
                "somepersian",
                "scotch",
                "scotch/irish",
                "sicilian/french",
                "sephardicjewish",
                "spanish",
                "turkish/arab",
                "westerneurope",
            },
            "raceterx": {"jewish", "portuguese", "romanian", "scotch"},
        }
    )

    BLACKX_RESPONSES = MappingProxyType(
        {
            "racesecx": {
                "black/african-american",
                "africanamerican",
                "bahamanian",
                "caribian",
                "caribbean",
                "haitian",
                "hatian",
                "jamaican",
                "westindian",
                "westindies",
            },
            "racex": {
                "africanamerican",
                "westindian",
                "westindies",
                "bahamas",
                "barbadian",
                "barbardian",
                "eritrian",
                "haitian",
                "hatian",
                "jamaician",
                "jamaica",
                "jamaican",
                "hispanicdominican",
                "dominican/hispanic",
                "nigerian",
                "trinidadian",
                "westindies",
            },
        }
    )

    NATIVEX_RESPONSES = MappingProxyType({"racex": {"nativeamerican", "nativeamerica"}})

    HAWAIIX_RESPONSES = MappingProxyType(
        {"racex": {"tahitian"}, "racesecx": {"samoan"}}
    )

    ASIANX_RESPONSES = MappingProxyType(
        {
            "racex": {
                "asian",
                "asianindian",
                "chinese",
                "chineseamerican",
                "eastindian",
                "filipino",
                "filipinoamerican",
                "korean",
                "japanese",
                "japaneseamerican",
                "india",
                "indian",
                "indiasouthindian",
                "malay",
                "okanawajapanese",
                "phillipino",
                "southasian",
                "srilankan",
                "vietnamese",
            },
            "racesecx": {"asianindian", "eastindian", "korean"},
        }
    )

    MULTIX_RESPONSES = MappingProxyType(
        {
            "racex": {
                "blackhispanic",
                "bi-racial",
                "biracial",
                "caucasian/asian",
                "dutchindonesian",
                "halfhisp/halfwhite",
                "hispanic-mestiza",
                "japanesecaucasian",
                "mestino",
                "mestito",
                "mestiza",
                "mestizo",
                "meztizo",
                "mixblackandwhite",
                "mixed",
                "mixedrace",
                "mulato",
                "moreno/mestizo",
                "mulato/blackandwhite",
                "multiracial",
                "mixedcuban",
                "mututo",
                "white/africanamerican",
            }
        }
    )

    MULTIPX_RESPONSES = MappingProxyType(
        {
            "racex": {
                "africanandamericanindian",
                "mixblackandwhite",
                "mixedblackandwhite",
                "wht/blk",
            },
            "racesecx": {
                "caribbeanindian",
                "dutchindonesian",
                "eastindian",
                "korean",
                "panamanian",
                "puertorican",
                "jamaicanindian",
                "canadianindian",
                "eastindian/jamacican",
                "sicilian",
            },
        }
    )

    UNX_RESPONSES = MappingProxyType(
        {
            "racex": {
                "brazilian",
                "columbian",
                "criollo",
                "cuban",
                "guyanese",
                "hispanic",
                "hispanic/latino",
                "hspanic",
                "human",
                "humana",
                "indian",
                "indio",
                "latin,trigueno",
                "latina",
                "latinahispanic",
                "latino",
                "mexicanamerican",
                "other",
                "puertorican",
                "puertorician",
                "refused",
                "seereport",
                "brown",
                "indigenous",
                "mexican",
                "usa",
            }
        }
    )

    def _create_naccage(self) -> Optional[int]:
        """Creates NACCAGE (age) Generates DOB from BIRTHMO and BIRTHYR and
        compares to form date."""
        dob = self.__uds.generate_uds_dob()
        visitdate = self.__uds.get_value("visitdate", None)
        visitdate = datetime_from_form_date(visitdate)
        if not dob or not visitdate:
            return None

        return calculate_age(dob, visitdate.date())

    def _create_naccnihr(self) -> int:
        """Creates NACCNIHR (race)"""
        return self.generate_naccnihr(
            race=self.__uds.get_value("race"),
            racex=self.__uds.get_value("racex"),
            racesec=self.__uds.get_value("racesec"),
            racesecx=self.__uds.get_value("racesecx"),
            raceter=self.__uds.get_value("raceter"),
            raceterx=self.__uds.get_value("raceterx"),
        )

    @classmethod
    def is_multiracial(cls, racex: Optional[str], racesecx: Optional[str]) -> bool:
        """Returns whether or not the write-in values denote multiracial."""
        if racex:
            mult_satisfied = any(
                [
                    x in racex
                    for x in ["muiti", "mult", "muti", "multi", "mulit", "mutl"]
                ]
            )
            if mult_satisfied and "racial" in racex:
                return True

        if racesecx:
            if "multi" in racesecx and "racial" in racesecx:
                return True

        return False

    @classmethod
    def generate_naccnihr(
        cls,
        race: Optional[int],
        racex: Optional[str],
        racesec: Optional[int],
        racesecx: Optional[str],
        raceter: Optional[int],
        raceterx: Optional[str],
    ) -> int:
        """NACCNIHR values:

        1: "White"
        2: "Black or African American"
        3: "American Indian or Alaska Native"
        4: "Native Hawaiian or Pacific Islander"
        5: "Asian"
        6: "Multiracial"
        99: "Unknown or ambiguous"
        """

        if not race:
            return 99

        # remove whitespace and lowercase all
        # TODO: not sure if the SAS code was extremely case-sensitive
        #   e.g. some capitalizations in RACEX and others in RACESECX
        racex = racex.replace(" ", "").lower() if racex else racex
        racesecx = racesecx.replace(" ", "").lower() if racesecx else racesecx
        raceterx = raceterx.replace(" ", "").lower() if raceterx else raceterx

        whitex = 0
        blackx = 0
        nativex = 0
        hawaiix = 0
        asianx = 0
        multix = 0
        multipx = 0
        unx = 0

        # whitex
        if racex in cls.WHITEX_RESPONSES["racex"]:
            whitex = 1
        if race == 1 and racesec == 50 and racesecx in cls.WHITEX_RESPONSES["racesecx"]:
            whitex = 1
        if raceterx in cls.WHITEX_RESPONSES["raceterx"]:
            whitex = 1

        # blackx
        if racesecx in cls.BLACKX_RESPONSES["racesecx"]:
            blackx = 1
        if racex in cls.BLACKX_RESPONSES["racex"]:
            blackx = 1

        # nativex
        if racex in cls.NATIVEX_RESPONSES["racex"]:
            nativex = 1

        # hawaiix
        if racesecx in cls.HAWAIIX_RESPONSES["racesecx"]:
            hawaiix = 1
        if racex in cls.HAWAIIX_RESPONSES["racex"]:
            hawaiix = 1

        # asianx
        if racex in cls.ASIANX_RESPONSES["racex"]:
            asianx = 1
        if racesecx in cls.ASIANX_RESPONSES["racesecx"]:
            asianx = 1

        # multix
        if racex in cls.MULTIX_RESPONSES["racex"]:
            multix = 1
        if cls.is_multiracial(racex, racesecx):
            multix = 1

        # multipx
        if racex in cls.MULTIPX_RESPONSES["racex"]:
            multipx = 1
        if racesecx in cls.MULTIPX_RESPONSES["racesecx"]:
            multipx = 1
        if race in {2, 3, 4, 5} and racesecx == "irish":
            multipx = 1
        if race == 1 and raceter == 50 and raceterx == "irish":
            multipx = 1
        if race == 50 and racesecx == "german" and raceterx == "centralamericanindian":
            multipx = 1
        if race == 3 and raceterx == "irish":
            multipx = 1
        if racesec == 3 and racex == "european":
            multipx = 1
        if race == 4 and racesecx == "filipino":
            multipx = 1
        if race == 1 and raceterx == "nativeamerican":
            multipx = 1
        if race == 5 and racesecx == "portuguese" and raceterx == "sloven":
            multipx = 1
        if race == 5 and racesecx == "korean" and raceterx == "portuguese":
            multipx = 1
        if race == 1 and racesecx == "westindian":
            multipx = 1

        # unx
        if racex in cls.UNX_RESPONSES["racex"]:
            unx = 1

        naccnihr = race

        # based on the SAS code, everything after this needs to be on an if/else basis
        # these could probably be compressed in some way, but better to leave it as
        # similar to SAS as possible
        # unfortunately this caused all hispanic/latino to be classified as white, so
        # also ended up refactoring the above to match the SAS close more closely

        if (race == 1 or race == 50) and whitex == 1:
            naccnihr = 1
        elif blackx == 1 and race == 50 and racesec == 5:
            naccnihr = 6
        elif blackx == 1 and race == 50 and racesec == 1 and raceter in {2, 3, 4, 5}:
            naccnihr = 6
        elif race == 50 and racesec == 2 and raceter == 3:
            naccnihr = 6
        elif blackx == 1:
            naccnihr = 2
        elif race == 50 and nativex == 1:
            naccnihr = 3
        elif race == 50 and asianx == 1 and hawaiix == 1:
            naccnihr = 6
        elif race == 50 and asianx == 1 and whitex == 1:
            naccnihr = 6
        elif race == 50 and hawaiix == 1:
            naccnihr = 4

        # commented out in SAS, just leaving for now for documentation
        # elif race == 50 and asianx == 1 and multix == 1:
        #     naccnihr = 5

        elif (race == 50 or race == 1) and multix == 1:
            naccnihr = 6
        elif race == 5 and asianx == 1 and whitex == 1:
            naccnihr = 6
        elif (race == 5 or race == 50) and asianx == 1:
            naccnihr = 5
        elif (race == 50 or race == 1) and multix == 1:
            naccnihr = 6
        elif multipx == 1:
            naccnihr = 6
        elif race == 5 and whitex == 1:
            naccnihr = 6
        elif race == 50 and unx == 1:
            naccnihr = 99
        elif race == 1 and racesec in {2, 3, 4, 5, 50}:
            naccnihr = 6
        elif race == 2 and racesec in {1, 3, 4, 5, 50}:
            naccnihr = 6
        elif race == 3 and racesec in {1, 2, 5}:
            naccnihr = 6
        elif race == 4 and racesec in {1, 2, 3, 5}:
            naccnihr = 6
        elif race == 4 and raceter in {1, 2, 3, 5}:
            naccnihr = 6
        elif race == 5 and racesec in {1, 2, 3, 4}:
            naccnihr = 6
        elif race == 50 and racesec == 1:
            naccnihr = 6
        elif race == 50 and racesec == 4 and raceter == 1:
            naccnihr = 6
        elif race == 50 and racesec == 5 and raceter in {1, 2, 3, 4}:
            naccnihr = 6
        elif race == 1 and raceter in {2, 3, 4}:
            naccnihr = 6
        elif race == 2 and raceter in {1, 3}:
            naccnihr = 6
        elif racesec == 5 and raceter in {1, 2, 3}:
            naccnihr = 6
        elif (
            race == 50
            and whitex != 1
            and blackx != 1
            and hawaiix != 1
            and asianx != 1
            and multix != 1
            and multipx != 1
        ):
            naccnihr = 99
        elif race == 99 and racesec in {2, 3}:
            naccnihr = 99

        if racex == "hispanic" and racesecx == "meztiza":
            naccnihr = 6

        return naccnihr
