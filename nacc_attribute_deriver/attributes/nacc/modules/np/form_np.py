"""Derived variables from neuropathology form."""

from datetime import date
from typing import Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    FormNamespace,
)
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.date import create_death_date


class NPFormAttributeCollection(AttributeCollection):
    def __init__(self, table: SymbolTable) -> None:
        """Check that this is an NP form."""
        self.__np = FormNamespace(table=table)

        module = self.__np.get_value("module")
        if not module or module.upper() != "NP":
            msg = f"Current file is not an NP form: found {module}"
            raise InvalidFieldError(msg)

    def _map_gross(self, new: int) -> int:
        npgross = self.__np.get_int_value("npgross")
        if npgross is None:
            return 9
        if npgross == 2:
            return 0
        if npgross == 9:
            return 9

        return new

    def _map_sub4(self, old: int) -> int:
        if old in [1, 2, 3, 4]:
            return 4 - old
        if old == 5:
            return 8

        return 9

    def _map_v9(self, old: int) -> int:
        if old == 1:
            return 1
        if old == 2:
            return 0
        if old == 3:
            return 8

        return 9

    def _map_vasc(self, new: int) -> int:
        npgross = self.__np.get_int_value("npgross")
        npvasc = self.__np.get_int_value("npvasc")
        if npgross == 2 or npvasc == 2:
            return 0
        if npgross == 9 or npvasc == 9:
            return 9
        if npvasc == 3:
            return 8

        return new

    def _map_sub1(self, old: int):
        if old in [1, 2, 3, 4]:
            return old - 1
        if old == 5:
            return 8

        return 9

    def _map_lewy(self) -> int:
        nplewy = self.__np.get_int_value("nplewy")
        if nplewy is None:
            return 9
        if nplewy == 6:
            return 8
        if nplewy == 5:
            return 0

        return nplewy

    def _create_np_braa(self) -> int:
        """Create the NACCBRAA variable.

        Braak stage for neurofibrillary degeneration (B score)
        """
        formver = self.__np.get_int_value("formver")
        npbraak = self.__np.get_int_value("npbraak")
        naccbraa = npbraak if npbraak else 9

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
                naccbraa = self._map_gross(naccbraa)

        return naccbraa if naccbraa is not None else 9

    def _create_np_neur(self) -> int:
        """Create the NACCNEUR variable.

        Density of neocortical neuritic plaques (CERAD score) (C score)
        """
        formver = self.__np.get_value("formver")
        npneur = self.__np.get_value("npneur", 9)
        assert npneur is not None
        naccneur = npneur

        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            naccneur = self._map_sub4(npneur)
        elif formver == 1:
            naccneur = self._map_sub4(npneur) if npneur else self._map_gross(naccneur)

        return naccneur if naccneur is not None else 9

    def _create_np_micr(self) -> int:
        """Create the NACCMICR variable.

        Microinfarcts
        """
        formver = self.__np.get_value("formver")
        npold = self.__np.get_value("npold")
        npmicro = self.__np.get_value("npmicro")
        npmicro = npmicro if npmicro else 9

        naccmicr = npold if npold else 9
        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            naccmicr = self._map_v9(npmicro)
        elif formver == 1:
            naccmicr = self._map_v9(npmicro) if npmicro else self._map_vasc(naccmicr)

        return naccmicr if naccmicr is not None else 9

    def _create_np_hem(self) -> int:
        """Create the NACCHEM variable.

        Hemorrhages and microbleeds
        """
        formver = self.__np.get_value("formver")
        nphem = self.__np.get_value("nphem")
        nphem = nphem if nphem else 9
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
            nacchem = self._map_v9(nphem)
        elif formver == 1:
            nacchem = nphem
            nacchem = self._map_v9(nphem) if nphem else self._map_vasc(nacchem)

        return nacchem if nacchem is not None else 9

    def _create_np_arte(self) -> int:
        """Create the NACCARTE variable.

        Arteriolosclerosis
        """
        formver = self.__np.get_value("formver")
        nparter = self.__np.get_value("nparter")

        if formver in [10, 11]:
            return nparter if nparter is not None else 9
        if formver in [7, 8, 9]:
            return self._map_sub1(nparter) if nparter is not None else 9
        if formver == 1 and nparter is not None:
            return self._map_sub1(nparter)

        return self._map_vasc(9)

    def _create_np_lewy(self) -> int:
        """Create the NACCLEWY variable.

        Lewy body disease
        """
        formver = self.__np.get_value("formver")
        nacclewy = None

        if formver in [10, 11]:
            nplbod = self.__np.get_int_value("nplbod")
            nacclewy = nplbod
            if nplbod == 4:
                nacclewy = 2
            if nplbod == 5:
                nacclewy = 4
        elif formver in [7, 8, 9]:
            nacclewy = self._map_lewy()
        elif formver == 1:
            nplewy = self.__np.get_int_value("nplewy")
            if nplewy is not None:
                nacclewy = self._map_lewy()
            else:
                nacclewy = nplewy
                nacclewy = self._map_gross(9)

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
