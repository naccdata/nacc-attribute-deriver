"""Raw form values that need to be pulled across cross-sectionally for B9
derived and missingness work.

See pprevars in b9structrdd.sas. While defined, I don't think a lot of
these actually need to be carried through, so commenting out for until
they cause a problem. Once more confirmed, can also refine which ones
actually should call the working namespace in the missingness/derived
logic.
"""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.uds_collection import (
    UDSAttributeCollection,
)
from nacc_attribute_deriver.attributes.namespace.namespace import (
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class UDSFormB9RawAttribute(UDSAttributeCollection):
    """Class to collect UDS B9 attributes."""

    def __init__(self, table: SymbolTable):
        super().__init__(table)
        self.__working = WorkingNamespace(table=table)

    def __handle_b9_attribute(self, field: str, prev_code: int) -> Optional[int]:
        """Handles capturing B9 attribute.

        Ignore prev codes (generally 777 for ages and 0 for everything
        else).
        """
        value = self.uds.get_value(field, int)
        if value == prev_code:
            return None

        # REGRESSION: If prev_code == 777, also ignore 888s
        # unless there is no other value to fall back to
        # 888s are the missingness value for blanks in legacy
        # so it's a bit conflated
        if prev_code == 777 and value == 888:
            prev_value = self.__working.get_cross_sectional_value(field, int)
            if prev_value is not None:
                return None

        # TODO: SAS code may also be not updating the
        # value once its set... leave for now and see
        # how it goes
        return value

    def _create_frstchg(self) -> Optional[int]:
        """Captures FRSTCHG."""
        return self.__handle_b9_attribute("frstchg", prev_code=0)

    def _create_cogfpred(self) -> Optional[int]:
        """Captures COGFPRED."""
        return self.__handle_b9_attribute("cogfpred", prev_code=0)

    def _create_befpred(self) -> Optional[int]:
        """Captures BEFPRED."""
        return self.__handle_b9_attribute("befpred", prev_code=0)

    def _create_mofrst(self) -> Optional[int]:
        """Captures MOFRST."""
        return self.__handle_b9_attribute("mofrst", prev_code=0)

    def _create_decage(self) -> Optional[int]:
        """Captures DECAGE."""
        return self.__handle_b9_attribute("decage", prev_code=777)

    def _create_cogflago(self) -> Optional[int]:
        """Captures COGFLAGO."""
        return self.__handle_b9_attribute("cogflago", prev_code=777)

    def _create_bevhago(self) -> Optional[int]:
        """Captures BEVHAGO."""
        return self.__handle_b9_attribute("bevhago", prev_code=777)

    def _create_arkage(self) -> Optional[int]:
        """Captures ARKAGE."""
        return self.__handle_b9_attribute("arkage", prev_code=777)

    def _create_alsage(self) -> Optional[int]:
        """Captures ALSAGE."""
        return self.__handle_b9_attribute("alsage", prev_code=777)

    def _create_moage(self) -> Optional[int]:
        """Captures MOAGE."""
        return self.__handle_b9_attribute("moage", prev_code=777)

    def _create_beremago(self) -> Optional[int]:
        """Captures BEREMAGO."""
        return self.__handle_b9_attribute("beremago", prev_code=777)

    def _create_beage(self) -> Optional[int]:
        """Captures BEAGE."""
        return self.__handle_b9_attribute("beage", prev_code=777)

    def _create_parkage(self) -> Optional[int]:
        """Captures PARKAGE."""
        return self.__handle_b9_attribute("parkage", prev_code=777)
