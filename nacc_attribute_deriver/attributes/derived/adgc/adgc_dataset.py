"""Derived variables for the ADGC dataset that require the UDS namespace.

NOTE: Did not define the following here:
    NAREASON - reports should use NACCETPR directly
    AUTOPSYCONF - reports should compare ADGC values directly
    NEURODIAG - defined in NPFormAttributeCollection
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.derived.modules.uds.form_d1a import (
    UDSFormD1aAttribute,
)
from nacc_attribute_deriver.attributes.derived.modules.uds.form_d1b import (
    UDSFormD1bAttribute,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class ADGCDatasetUDSAttribute(UDSAttributeCollection):
    """Class to collect ADGC dataset attributes requiring the UDS namespace."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)

        # to get derived variables for current form, which is the latest
        self.__d1a = UDSFormD1aAttribute(table=table)
        self.__d1b = UDSFormD1bAttribute(table=table)

        # working namepspace for INITAD
        self.__working = WorkingNamespace(table=table)

        # these attributes rely heavily on NACCETPR, so just compute
        # once and set as an instance variable
        self.__naccetpr = self.__d1b._create_naccetpr()  # noqa: SLF001

    def _create_clindiag(self) -> int:
        """Creates CLINDIAG (clinical diagnosis). Need to evaluate in reverse
        order (exclusionary, MCI, Case, then Control).

        Returns:
            1: Control
            2: Case
            3: MCI
            8: NA (exclusionary conditions)
            -4: Missing/not applicable (different from the CLINDIAG's definition of NA)
        """
        ###############################
        # Exclusionary conditions (8) #
        ###############################
        # attributes we are checking == 1
        raw_attributes = self.uds.group_attributes(
            [
                "pd",
                "park",
                "ftd",
                "pca",
                "cogoth",
                "cogoth2",
                "cogoth3",
                "namndem",
                "othmut",
                "ftldnos",
                "fdgftld",
                "tpetftld",
                "mrftld",
                "datscan",
            ],
            int,
        )
        if any(x == 1 for x in raw_attributes):
            return 8

        # other raw attributes we are checking, but for something
        # other than 1
        if (
            self.uds.get_value("demunif", int) in [1, 2]
            or self.uds.get_value("cancer", int) in [1, 2]
            or self.uds.get_value("hxstroke", int) == 2
            or self.uds.get_value("ftldsubt", int) in [1, 2, 3, 9]
        ):
            return 8

        # derived variables we are checking (computation is a bit more
        # expensive which is why we're checking last)
        if (
            self.__d1a._create_naccbvft() == 1  # noqa: SLF001
            or self.__d1a._create_naccppa() == 1  # noqa: SLF001
            or self.__d1b._create_naccftdm() == 1  # noqa: SLF001
        ):
            return 8

        # get latest NACCUDSD and NACCETPR values, which are also used
        # for the other cases
        naccudsd = self.__d1a._create_naccudsd()  # noqa: SLF001
        if naccudsd == 2 or self.__naccetpr not in [1, 88, 99]:
            return 8

        ######################
        # MCI conditions (3) #
        ######################
        if naccudsd == 3:
            return 3

        #######################
        # Case conditions (2) #
        #######################
        if self.__naccetpr == 1:
            return 2

        probad = self.uds.get_value("probad", int)
        possad = self.uds.get_value("possad", int)
        if probad == 1 or possad == 1:
            return 2

        ##########################
        # Control conditions (1) #
        ##########################
        if naccudsd == 1:
            return 1

        # default (-4)
        return INFORMED_MISSINGNESS

    def _create_initad(self) -> Optional[int]:
        """Creates INITAD - AD at initial visit. Helper variable
        for computing INCAD and PREVAD. Only calculated for the
        initial visit.

        Returns:
            Clinical diagnosis at initial visit.
        """
        if not self.uds.is_initial() or self.uds.is_i4():
            return None

        # return 1 if CLINDIAG != 2 (Case) at initial visit, else 0
        return self._create_clindiag()

    def _create_incad(self) -> int:
        """Creates INCAD - incident AD.

        Returns:
            1 if INITAD != Case (2) and the latest CLINDIAG = Case (2)
            0 otherwise
        """
        initad = self.__working.get_cross_sectional_value("initad", int)
        clindiag = self._create_clindiag()

        return 1 if (initad != 2 and clindiag == 2) else 0

    def _create_prevad(self) -> int:
        """Creates PREVAD - prevalent AD.

        Returns:
            1 if INITAD == Case (2) and the latest CLINDIAG = Case (2)
            0 otherwise
        """
        initad = self.__working.get_cross_sectional_value("initad", int)
        clindiag = self._create_clindiag()

        return 1 if (initad == 2 and clindiag == 2) else 0
