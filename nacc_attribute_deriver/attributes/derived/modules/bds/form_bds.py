"""Handles the BDS form."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.attribute_collection import (
    AttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    FormNamespace,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)
from nacc_attribute_deriver.utils.errors import (
    AttributeDeriverError,
    InvalidFieldError,
)


class BDSFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        self.__bds = FormNamespace(table=table, required=frozenset(["module"]))

        module = self.__bds.get_required("module", str)
        if module.upper() != "BDS":
            msg = f"Current file is not a BDS form: found {module}"
            raise InvalidFieldError(msg)

        self.__working = WorkingNamespace(table=table)

    def _create_bds_naccdage(self) -> int:
        """Creates BDS NACCDAGE - age at death.

        BDS forms are designed specifically to submit an NP form,
        so we always expect an NP form, which will always provide
        an age of death.

        If an NP form is not provided, just return 999.
        """
        age_at_death = self.__working.get_cross_sectional_value("np-death-age", int)
        if not age_at_death:
            return 999

        # enforce minimum of 18
        return max(18, age_at_death)

    ##############################################################
    # Cross-sectional demographics, only derived from the BDS    #
    # when the participant has no UDS visits. UDS always wins.   #
    ##############################################################

    def __has_uds(self) -> bool:
        """Whether the participant has UDS visits.

        Relies on BDS being curated after UDS, so that the UDS
        visitdates are already recorded under subject.info.working.
        """
        return bool(self.__working.get_cross_sectional_value("uds-visitdates", list))

    def __bds_only_value(self, attribute: str) -> Optional[int]:
        """Returns the BDS value for a direct-copy cross-sectional variable,
        None if the participant has UDS, or -4 if blank."""
        if self.__has_uds():
            return None

        value = self.__bds.get_value(attribute, int)
        return value if value is not None else INFORMED_MISSINGNESS

    def _create_bds_naccsex(self) -> Optional[int]:
        """Creates NACCSEX from the BDS if there is no UDS.

        NACCSEX = SEX, else -4 if blank
        """
        return self.__bds_only_value("sex")

    def _create_bds_nacchisp(self) -> Optional[int]:
        """Creates NACCHISP from the BDS if there is no UDS.

        NACCHISP = HISPANIC, else -4 if blank
        """
        return self.__bds_only_value("hispanic")

    def _create_bds_nacclang(self) -> Optional[int]:
        """Creates NACCLANG from the BDS if there is no UDS.

        PRIMLANG 3 (Mandarin) and 4 (Cantonese) both map to 3 (Chinese
        dialect); everything else maps to itself. -4 if blank.
        """
        if self.__has_uds():
            return None

        primlang = self.__bds.get_value("primlang", int)
        if primlang is None:
            return INFORMED_MISSINGNESS

        primlang_mappings = {1: 1, 2: 2, 3: 3, 4: 3, 5: 5, 6: 6, 8: 8, 9: 9}
        if primlang not in primlang_mappings:
            raise AttributeDeriverError(
                "Unable to derive NACCLANG (BDS): unsupported primlang value: "
                + f"{primlang}"
            )

        return primlang_mappings[primlang]

    def _create_bds_nacclangx(self) -> Optional[str]:
        """Creates NACCLANGX from the BDS if there is no UDS.

        NACCLANGX = PRIMLANX
        """
        if self.__has_uds():
            return None

        primlanx = self.__bds.get_value("primlanx", str)
        return primlanx if primlanx else INFORMED_BLANK

    def _create_bds_naccnihr(self) -> Optional[int]:
        """Creates NACCNIHR from the BDS if there is no UDS.

        BDSRACE 1-6 map to themselves, 9 maps to 99, -4 if blank.
        """
        if self.__has_uds():
            return None

        bdsrace = self.__bds.get_value("bdsrace", int)
        if bdsrace is None:
            return INFORMED_MISSINGNESS

        if bdsrace in [1, 2, 3, 4, 5, 6]:
            return bdsrace
        if bdsrace == 9:
            return 99

        raise AttributeDeriverError(
            f"Unable to derive NACCNIHR (BDS): unsupported bdsrace value: {bdsrace}"
        )
