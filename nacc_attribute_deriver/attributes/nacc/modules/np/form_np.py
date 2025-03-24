"""Derived variables from neuropathology form."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.base_attribute import FormAttribute
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import create_death_date


class NPFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is an NP form."""
        self.__np = FormAttribute(table)

        module = self.__np.get_value("module")
        if not module or module.upper() != "NP":
            raise MissingRequiredError("Current file is not an NP form")

    def _mapgross(self, new) -> Optional[int]:
        npgross = self.__np.get_value("npgross")
        if npgross == 2:
            return 0
        if npgross == 9:
            return 9

        return new

    def _mapsub4(self, old) -> int:
        if old in [1, 2, 3, 4]:
            return 4 - old
        if old == 5:
            return 8

        return 9

    def _mapv9(self, old) -> int:
        if old == 1:
            return 1
        if old == 2:
            return 0
        if old == 3:
            return 8

        return 9

    def _mapvasc(self, new) -> int:
        npgross = self.__np.get_value("npgross")
        npvasc = self.__np.get_value("npvasc")
        if npgross == 2 or npvasc == 2:
            return 0
        if npgross == 9 or npvasc == 9:
            return 9
        if npvasc == 3:
            return 8

        return new

    def _mapsub1(self, old):
        if old in [1, 2, 3, 4]:
            return old - 1
        if old == 5:
            return 8

        return 9

    def _maplewy(self) -> int:
        nplewy = self.__np.get_value("nplewy")
        if nplewy == 6:
            return 8
        if nplewy == 5:
            return 0

        return nplewy

    def _create_naccbraa(self) -> int:
        """Create the NACCBRAA variable.

        Braak stage for neurofibrillary degeneration (B score)
        """
        formver = self.__np.get_value("formver")
        npbraak = self.__np.get_value("npbraak")
        naccbraa = npbraak

        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            if npbraak == 7:
                naccbraa = 0
        elif formver == 1:
            if npbraak:
                if npbraak == 7:
                    naccbraa = 0
            else:
                naccbraa = self._mapgross(naccbraa)

        return naccbraa if naccbraa is not None else 9

    def _create_naccneur(self) -> int:
        """Create the NACCNEUR variable.

        Density of neocortical neuritic plaques (CERAD score) (C score)
        """
        formver = self.__np.get_value("formver")
        npneur = self.__np.get_value("npneur")
        naccneur = npneur

        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            naccneur = self._mapsub4(npneur)
        elif formver == 1:
            if npneur:
                naccneur = self._mapsub4(npneur)
            else:
                naccneur = self._mapgross(naccneur)

        return naccneur if naccneur is not None else 9

    def _create_naccmicr(self) -> int:
        """Create the NACCMICR variable.

        Microinfarcts
        """
        formver = self.__np.get_value("formver")
        npold = self.__np.get_value("npold")
        npmicro = self.__np.get_value("npmicro")

        naccmicr = npold
        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            naccmicr = self._mapv9(npmicro)
        elif formver == 1:
            if npmicro:
                naccmicr = self._mapv9(npmicro)
            else:
                naccmicr = self._mapvasc(naccmicr)

        return naccmicr if naccmicr is not None else 9

    def _create_nacchem(self) -> Optional[int]:
        """Create the NACCHEM variable.

        Hemorrhages and microbleeds
        """
        formver = self.__np.get_value("formver")
        nphem = self.__np.get_value("nphem")
        nacchem = None

        if formver in [10, 11]:
            nphemo = self.__np.get_value("nphemo")
            npoldd = self.__np.get_value("npoldd")

            if nphemo == 1 or npoldd == 1:
                nacchem = 1
            elif nphemo == 0 and npoldd == 0:
                nacchem = 0
            elif nphemo == 8 and npoldd == 8:
                nacchem = 8
            else:
                nacchem = 9
        elif formver in [7, 8, 9]:
            nacchem = nphem
            nacchem = self._mapv9(nphem)
        elif formver == 1:
            nacchem = nphem
            if nphem:
                nacchem = self._mapv9(nphem)
            else:
                nacchem = self._mapvasc(nacchem)

        return nacchem if nacchem is not None else 9

    def _create_naccarte(self) -> Optional[int]:
        """Create the NACCARTE variable.

        Arteriolosclerosis
        """
        formver = self.__np.get_value("formver")
        nparter = self.__np.get_value("nparter")
        naccarte = None

        if formver in [10, 11]:
            naccarte = nparter
        elif formver in [7, 8, 9]:
            naccarte = self._mapsub1(nparter)
        elif formver == 1:
            if nparter:
                naccarte = self._mapsub1(nparter)
            else:
                naccarte = self._mapvasc(naccarte)

        return naccarte if naccarte is not None else 9

    def _create_nacclewy(self) -> Optional[int]:
        """Create the NACCLEWY variable.

        Lewy body disease
        """
        formver = self.__np.get_value("formver")
        nacclewy = None

        if formver in [10, 11]:
            nplbod = self.__np.get_value("nplbod")
            nacclewy = nplbod
            if nplbod == 4:
                nacclewy = 2
            if nplbod == 5:
                nacclewy = 4
        elif formver in [7, 8, 9]:
            nacclewy = self._maplewy()
        elif formver == 1:
            nplewy = self.__np.get_value("nplewy")
            if nplewy:
                nacclewy = self._maplewy()
            else:
                nacclewy = nplewy
                nacclewy = self._mapgross(nacclewy)

        return nacclewy if nacclewy is not None else 9

    def _create_np_death_age(self) -> Optional[int]:
        return self.__np.get_value("npdage")

    def _create_np_death_date(self) -> Optional[date]:
        if self.__np.get_value("npdage") is None:
            return None

        year = self.__np.get_value("npdodyr")
        month = self.__np.get_value("npdodmo")
        day = self.__np.get_value("npdoddy")

        return create_death_date(year=year, month=month, day=day)
