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


class UDSFormB9RawAttribute(UDSAttributeCollection):
    """Class to collect UDS B9 attributes."""

    def __handle_b9_attribute(self, field: str, prev_code: int) -> Optional[int]:
        """Handles capturing B9 attribute.

        Ignore prev codes (generally 777 for ages and 0 for everything
        else).
        """
        value = self.uds.get_value(field, int)
        if value == prev_code:
            return None

        # REGRESSION: If prev_code == 777, also ignore 888s
        # 888s are the missingness value for blanks in legacy
        # so it's a bit conflated
        if prev_code == 777 and value == 888:
            return None

        # TODO: SAS code may also be not updating the
        # value once its set... leave for now and see
        # how it goes
        return value

    # def _create_decclin(self) -> Optional[int]:
    #     """Captures DECCLIN."""
    #     return self.__handle_b9_attribute("decclin")

    # def _create_cogmem(self) -> Optional[int]:
    #     """Captures COGMEM."""
    #     return self.__handle_b9_attribute("cogmem")

    # def _create_cogattn(self) -> Optional[int]:
    #     """Captures COGATTN."""
    #     return self.__handle_b9_attribute("cogattn")

    # def _create_cogjudg(self) -> Optional[int]:
    #     """Captures COGJUDG."""
    #     return self.__handle_b9_attribute("cogjudg")

    # def _create_coglang(self) -> Optional[int]:
    #     """Captures COGLANG."""
    #     return self.__handle_b9_attribute("coglang")

    # def _create_cogothr(self) -> Optional[int]:
    #     """Captures COGOTHR."""
    #     return self.__handle_b9_attribute("cogothr")

    # def _create_cogmode(self) -> Optional[int]:
    #     """Captures COGMODE."""
    #     return self.__handle_b9_attribute("cogmode")

    # def _create_cogfrst(self) -> Optional[int]:
    #     """Captures COGFRST."""
    #     return self.__handle_b9_attribute("cogfrst")

    # def _create_cogvis(self) -> Optional[int]:
    #     """Captures COGVIS."""
    #     return self.__handle_b9_attribute("cogvis")

    # def _create_beapathy(self) -> Optional[int]:
    #     """Captures BEAPATHY."""
    #     return self.__handle_b9_attribute("beapathy")

    # def _create_bedep(self) -> Optional[int]:
    #     """Captures BEDEP."""
    #     return self.__handle_b9_attribute("bedep")

    # def _create_bevhall(self) -> Optional[int]:
    #     """Captures BEVHALL."""
    #     return self.__handle_b9_attribute("bevhall")

    # def _create_beahall(self) -> Optional[int]:
    #     """Captures BEAHALL."""
    #     return self.__handle_b9_attribute("beahall")

    # def _create_bedel(self) -> Optional[int]:
    #     """Captures BEDEL."""
    #     return self.__handle_b9_attribute("bedel")

    # def _create_bedisin(self) -> Optional[int]:
    #     """Captures BEDISIN."""
    #     return self.__handle_b9_attribute("bedisin")

    # def _create_beirrit(self) -> Optional[int]:
    #     """Captures BEIRRIT."""
    #     return self.__handle_b9_attribute("beirrit")

    # def _create_beagit(self) -> Optional[int]:
    #     """Captures BEAGIT."""
    #     return self.__handle_b9_attribute("beagit")

    # def _create_beperch(self) -> Optional[int]:
    #     """Captures BEPERCH."""
    #     return self.__handle_b9_attribute("beperch")

    # def _create_beothr(self) -> Optional[int]:
    #     """Captures BEOTHR."""
    #     return self.__handle_b9_attribute("beothr")

    # def _create_mogait(self) -> Optional[int]:
    #     """Captures MOGAIT."""
    #     return self.__handle_b9_attribute("mogait")

    # def _create_mofalls(self) -> Optional[int]:
    #     """Captures MOFALLS."""
    #     return self.__handle_b9_attribute("mofalls")

    # def _create_motrem(self) -> Optional[int]:
    #     """Captures MOTREM."""
    #     return self.__handle_b9_attribute("motrem")

    # def _create_moslow(self) -> Optional[int]:
    #     """Captures MOSLOW."""
    #     return self.__handle_b9_attribute("moslow")

    # def _create_course(self) -> Optional[int]:
    #     """Captures COURSE."""
    #     return self.__handle_b9_attribute("course")

    def _create_frstchg(self) -> Optional[int]:
        """Captures FRSTCHG."""
        return self.__handle_b9_attribute("frstchg", prev_code=0)

    # def _create_bemode(self) -> Optional[int]:
    #     """Captures BEMODE."""
    #     return self.__handle_b9_attribute("bemode")

    # def _create_momode(self) -> Optional[int]:
    #     """Captures MOMODE."""
    #     return self.__handle_b9_attribute("momode")

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

    # def _create_befrst(self) -> Optional[int]:
    #     """Captures BEFRST."""
    #     return self.__handle_b9_attribute("befrst")

    # def _create_decclcog(self) -> Optional[int]:
    #     """Captures DECCLCOG."""
    #     return self.__handle_b9_attribute("decclcog")

    # def _create_decclbe(self) -> Optional[int]:
    #     """Captures DECCLBE."""
    #     return self.__handle_b9_attribute("decclbe")

    # def _create_decclmot(self) -> Optional[int]:
    #     """Captures DECCLMOT."""
    #     return self.__handle_b9_attribute("decclmot")

    # def _create_cogfluc(self) -> Optional[int]:
    #     """Captures COGFLUC."""
    #     return self.__handle_b9_attribute("cogfluc")

    def _create_beremago(self) -> Optional[int]:
        """Captures BEREMAGO."""
        return self.__handle_b9_attribute("beremago", prev_code=777)

    def _create_beage(self) -> Optional[int]:
        """Captures BEAGE."""
        return self.__handle_b9_attribute("beage", prev_code=777)
