"""Class to handle NP form missingness values."""

from typing import Optional

from nacc_attribute_deriver.attributes.collection.missingness_collection import (
    FormMissingnessCollection,
)


class NPMissingness(FormMissingnessCollection):
    """Class to handle NP missingness values."""

    def _missingness_np(self, field: str) -> Optional[int]:
        """Defines general missingness for NP; -4 if missing."""
        return self.generic_missingness(field)

    def _missingness_npinf1b(self) -> Optional[float]:
        """Handles missingness for NPINF1B."""
        return self.generic_float_missingness("npinf1b")

    def _missingness_npinf1d(self) -> Optional[float]:
        """Handles missingness for NPINF1D."""
        return self.generic_float_missingness("npinf1d")

    def _missingness_npinf1f(self) -> Optional[float]:
        """Handles missingness for NPINF1F."""
        return self.generic_float_missingness("npinf1f")

    def _missingness_npinf2b(self) -> Optional[float]:
        """Handles missingness for NPINF2B."""
        return self.generic_float_missingness("npinf2b")

    def _missingness_npinf2d(self) -> Optional[float]:
        """Handles missingness for NPINF2D."""
        return self.generic_float_missingness("npinf2d")

    def _missingness_npinf2f(self) -> Optional[float]:
        """Handles missingness for NPINF2F."""
        return self.generic_float_missingness("npinf2f")

    def _missingness_npinf3b(self) -> Optional[float]:
        """Handles missingness for NPINF3B."""
        return self.generic_float_missingness("npinf3b")

    def _missingness_npinf3d(self) -> Optional[float]:
        """Handles missingness for NPINF3D."""
        return self.generic_float_missingness("npinf3d")

    def _missingness_npinf3f(self) -> Optional[float]:
        """Handles missingness for NPINF3F."""
        return self.generic_float_missingness("npinf3f")

    def _missingness_npinf4b(self) -> Optional[float]:
        """Handles missingness for NPINF4B."""
        return self.generic_float_missingness("npinf4b")

    def _missingness_npinf4d(self) -> Optional[float]:
        """Handles missingness for NPINF4D."""
        return self.generic_float_missingness("npinf4d")

    def _missingness_npinf4f(self) -> Optional[float]:
        """Handles missingness for NPINF4F."""
        return self.generic_float_missingness("npinf4f")

    def _missingness_npfixx(self) -> Optional[str]:
        """Handles missingness for NPFIXX."""
        return self.generic_writein("npfixx")

    def _missingness_nptanx(self) -> Optional[str]:
        """Handles missingness for NPTANX."""
        return self.generic_writein("nptanx")

    def _missingness_npasanx(self) -> Optional[str]:
        """Handles missingness for NPASANX."""
        return self.generic_writein("npasanx")

    def _missingness_nptdpanx(self) -> Optional[str]:
        """Handles missingness for NPTDPANX."""
        return self.generic_writein("nptdpanx")

    def _missingness_nphisox(self) -> Optional[str]:
        """Handles missingness for NPHISOX."""
        return self.generic_writein("nphisox")

    def _missingness_nppathox(self) -> Optional[str]:
        """Handles missingness for NPPATHOX."""
        return self.generic_writein("nppathox")

    def _missingness_npfaut1(self) -> Optional[str]:
        """Handles missingness for NPFAUT1."""
        return self.generic_writein("npfaut1")

    def _missingness_npfaut2(self) -> Optional[str]:
        """Handles missingness for NPFAUT2."""
        return self.generic_writein("npfaut2")

    def _missingness_npfaut3(self) -> Optional[str]:
        """Handles missingness for NPFAUT3."""
        return self.generic_writein("npfaut3")

    def _missingness_npfaut4(self) -> Optional[str]:
        """Handles missingness for NPFAUT4."""
        return self.generic_writein("npfaut4")

    def _missingness_npnit(self) -> Optional[str]:
        """Handles missingness for NPNIT."""
        return self.generic_writein("npnit")

    def _missingness_npcerad(self) -> Optional[str]:
        """Handles missingness for NPCERAD."""
        return self.generic_writein("npcerad")

    def _missingness_npadrda(self) -> Optional[str]:
        """Handles missingness for NPADRDA."""
        return self.generic_writein("npadrda")

    def _missingness_npocrit(self) -> Optional[str]:
        """Handles missingness for NPOCRIT."""
        return self.generic_writein("npocrit")

    def _missingness_npvoth(self) -> Optional[str]:
        """Handles missingness for NPVOTH."""
        return self.generic_writein("npvoth")

    def _missingness_nplewycs(self) -> Optional[str]:
        """Handles missingness for NPLEWYCS."""
        return self.generic_writein("nplewycs")

    def _missingness_npgene(self) -> Optional[str]:
        """Handles missingness for NPGENE."""
        return self.generic_writein("npgene")

    def _missingness_npfhspec(self) -> Optional[str]:
        """Handles missingness for NPFHSPEC."""
        return self.generic_writein("npfhspec")

    def _missingness_nptauhap(self) -> Optional[str]:
        """Handles missingness for NPTAUHAP."""
        return self.generic_writein("nptauhap")

    def _missingness_npprnp(self) -> Optional[str]:
        """Handles missingness for NPPRNP."""
        return self.generic_writein("npprnp")

    def _missingness_npchrom(self) -> Optional[str]:
        """Handles missingness for NPCHROM."""
        return self.generic_writein("npchrom")

    def _missingness_nppnorm(self) -> Optional[str]:
        """Handles missingness for NPPNORM."""
        return self.generic_writein("nppnorm")

    def _missingness_npcnorm(self) -> Optional[str]:
        """Handles missingness for NPCNORM."""
        return self.generic_writein("npcnorm")

    def _missingness_nppadp(self) -> Optional[str]:
        """Handles missingness for NPPADP."""
        return self.generic_writein("nppadp")

    def _missingness_npcadp(self) -> Optional[str]:
        """Handles missingness for NPCADP."""
        return self.generic_writein("npcadp")

    def _missingness_nppad(self) -> Optional[str]:
        """Handles missingness for NPPAD."""
        return self.generic_writein("nppad")

    def _missingness_npcad(self) -> Optional[str]:
        """Handles missingness for NPCAD."""
        return self.generic_writein("npcad")

    def _missingness_npplewy(self) -> Optional[str]:
        """Handles missingness for NPPLEWY."""
        return self.generic_writein("npplewy")

    def _missingness_npclewy(self) -> Optional[str]:
        """Handles missingness for NPCLEWY."""
        return self.generic_writein("npclewy")

    def _missingness_nppvasc(self) -> Optional[str]:
        """Handles missingness for NPPVASC."""
        return self.generic_writein("nppvasc")

    def _missingness_npcvasc(self) -> Optional[str]:
        """Handles missingness for NPCVASC."""
        return self.generic_writein("npcvasc")

    def _missingness_nppftld(self) -> Optional[str]:
        """Handles missingness for NPPFTLD."""
        return self.generic_writein("nppftld")

    def _missingness_npcftld(self) -> Optional[str]:
        """Handles missingness for NPCFTLD."""
        return self.generic_writein("npcftld")

    def _missingness_npphipp(self) -> Optional[str]:
        """Handles missingness for NPPHIPP."""
        return self.generic_writein("npphipp")

    def _missingness_npchipp(self) -> Optional[str]:
        """Handles missingness for NPCHIPP."""
        return self.generic_writein("npchipp")

    def _missingness_nppprion(self) -> Optional[str]:
        """Handles missingness for NPPPRION."""
        return self.generic_writein("nppprion")

    def _missingness_npcprion(self) -> Optional[str]:
        """Handles missingness for NPCPRION."""
        return self.generic_writein("npcprion")

    def _missingness_nppoth1(self) -> Optional[str]:
        """Handles missingness for NPPOTH1."""
        return self.generic_writein("nppoth1")

    def _missingness_npcoth1(self) -> Optional[str]:
        """Handles missingness for NPCOTH1."""
        return self.generic_writein("npcoth1")

    def _missingness_npoth1x(self) -> Optional[str]:
        """Handles missingness for NPOTH1X."""
        return self.generic_writein("npoth1x")

    def _missingness_nppoth2(self) -> Optional[str]:
        """Handles missingness for NPPOTH2."""
        return self.generic_writein("nppoth2")

    def _missingness_npcoth2(self) -> Optional[str]:
        """Handles missingness for NPCOTH2."""
        return self.generic_writein("npcoth2")

    def _missingness_npoth2x(self) -> Optional[str]:
        """Handles missingness for NPOTH2X."""
        return self.generic_writein("npoth2x")

    def _missingness_nppoth3(self) -> Optional[str]:
        """Handles missingness for NPPOTH3."""
        return self.generic_writein("nppoth3")

    def _missingness_npcoth3(self) -> Optional[str]:
        """Handles missingness for NPCOTH3."""
        return self.generic_writein("npcoth3")

    def _missingness_npoth3x(self) -> Optional[str]:
        """Handles missingness for NPOTH3X."""
        return self.generic_writein("npoth3x")
