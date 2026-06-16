"""Derived variables for the ADGC dataset.

Relies primarily on the latest UDS data. As such, variables can also
be treated as UDS cross-sectional variables (e.g. runs in the UDS
namespace).
"""

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.derived.modules.uds.form_d1a import (
    UDSFormD1aAttribute,
)
from nacc_attribute_deriver.attributes.derived.modules.uds.form_d1a import (
    UDSFormD1bAttribute,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


class ADGCDatasetAttribute(UDSAttributeCollection):
    """Class to collect ADGC dataset attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)

        # to get derived variables for current form, which is the latest
        self.__d1a = UDSFormD1aAttribute(table=table)
        self.__d1b = UDSFormD1bAttribute(table=table)

        # these attributes rely heavily on NACCETPR, so just compute
        # once and set as an instance variable
        self.__naccetpr = self.__d1b._create_naccetpr()

    def _create_clindiag(self) -> int:
        """Creates CLINDIAG (clinical diagnosis).
        Need to evaluate in reverse order (exclusionary, MCI, Case, then Control).

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
        raw_attributes = self.uds.group_attributes([
            'pd', 'park', 'ftd', 'pca', 'cogoth', 'cogoth2', 'cogoth3',
            'namndem', 'othmut', 'ftldnos', 'fdgftld', 'tpetftld',
            'mrftld', 'datscan'
        ], int)
        if any(x == 1 for x in raw_attributes):
            return 8

        # other raw attributes we are checking, but for something
        # other than 1
        if (self.uds.get_value('demunif', int) in [1, 2] or
            self.uds.get_value('cancer', int) in [1, 2] or
            self.uds.get_value('hxstroke', int) == 2 or
            self.uds.get_value('ftldsubt', int in [1, 2, 3, 9])
        ):
            return 8

        # derived variables we are checking (computation is a bit more
        # expensive which is why we're checking last)
        if (self.__d1a._create_naccbvft() == 1 or
            self.__d1a._create_naccppa() == 1 or
            self.__d1b._create_naccftdm() == 1 
        ):
            return 8

        # get latest NACCUDSD and NACCETPR values, which are also used
        # for the other cases
        naccudsd = self.__d1a._create_naccudsd()
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
        if nacceptr == 1:
            return 2

        probad = self.uds.get_value('probad', int)
        possad = self.uds.get_value('possad', int)
        if probad == 1 or possad == 1:
            return 2

        ##########################
        # Control conditions (1) #
        ##########################
        if naccudsd == 1:
            return 1

        # default (-4)
        return INFORMED_MISSINGNESS

    # NAREASON - use NACCETPR directly
    # TODO: need updated definitions for NACCETPR = 31 - 34?

    def _create_neurodiag(self) -> int:
        """Creates NEURODIAG - neuropath diagnosis."""

