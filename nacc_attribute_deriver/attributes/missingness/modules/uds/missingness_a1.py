"""Class to handle A1-specific missingness values."""

from typing import Optional, Type

from nacc_attribute_deriver.attributes.namespace.namespace import T
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

from .missingness_uds import UDSMissingness


class UDSFormA1Missingness(UDSMissingness):
    def _handle_a1_missingness(
        self, field: str, attr_type: Type[T], missing_value: T
    ) -> Optional[T]:
        """A1 has many variables that are only collected in IVP. So in general,
        we execute the missingness logic if it's an IVP form, otherwise we pull
        across the resolved value.

        IVP missingnes logic:

        If FORMVER=4 and VAR is blank, VAR should = MISSING_VALUE
        else if FORMVER < 4, VAR should be -4
        """
        if self.formver < 4:
            return attr_type(INFORMED_MISSINGNESS)  # type: ignore

        if self.uds.is_initial():
            if isinstance(attr_type, int):
                result = self.uds.get_value(field, int)
                if result is not None:
                    return None

                return missing_value

            return self.generic_missingness(field, str)  # type: ignore

        return self.handle_prev_visit(field, attr_type)

    def _missingness_raceaian(self) -> Optional[int]:
        """Handles missingness for RACEAIAN."""
        return self._handle_a1_missingness("raceaian", int, missing_value=0)

    def _missingness_raceaianx(self) -> Optional[str]:
        """Handles missingness for RACEAIANX."""
        return self._handle_a1_missingness("raceaianx", str, missing_value="0")

    def _missingness_raceasian(self) -> Optional[int]:
        """Handles missingness for RACEASIAN."""
        return self._handle_a1_missingness("raceasian", int, missing_value=0)

    def _missingness_ethchinese(self) -> Optional[int]:
        """Handles missingness for ETHCHINESE."""
        return self._handle_a1_missingness("ethchinese", int, missing_value=0)

    def _missingness_ethindia(self) -> Optional[int]:
        """Handles missingness for ETHINDIA."""
        return self._handle_a1_missingness("ethindia", int, missing_value=0)

    def _missingness_ethfilip(self) -> Optional[int]:
        """Handles missingness for ETHFILIP."""
        return self._handle_a1_missingness("ethfilip", int, missing_value=0)

    def _missingness_ethvietnam(self) -> Optional[int]:
        """Handles missingness for ETHVIETNAM."""
        return self._handle_a1_missingness("ethvietnam", int, missing_value=0)

    def _missingness_ethkorean(self) -> Optional[int]:
        """Handles missingness for ETHKOREAN."""
        return self._handle_a1_missingness("ethkorean", int, missing_value=0)

    def _missingness_ethjapan(self) -> Optional[int]:
        """Handles missingness for ETHJAPAN."""
        return self._handle_a1_missingness("ethjapan", int, missing_value=0)

    def _missingness_ethasnoth(self) -> Optional[int]:
        """Handles missingness for ETHASNOTH."""
        return self._handle_a1_missingness("ethasnoth", int, missing_value=0)

    def _missingness_ethasnothx(self) -> Optional[str]:
        """Handles missingness for ETHASNOTHX."""
        return self._handle_a1_missingness("ethasnothx", str, missing_value="0")

    def _missingness_raceblack(self) -> Optional[int]:
        """Handles missingness for RACEBLACK."""
        return self._handle_a1_missingness("raceblack", int, missing_value=0)

    def _missingness_ethafamer(self) -> Optional[int]:
        """Handles missingness for ETHAFAMER."""
        return self._handle_a1_missingness("ethafamer", int, missing_value=0)

    def _missingness_ethjamaica(self) -> Optional[int]:
        """Handles missingness for ETHJAMAICA."""
        return self._handle_a1_missingness("ethjamaica", int, missing_value=0)

    def _missingness_ethhaitian(self) -> Optional[int]:
        """Handles missingness for ETHHAITIAN."""
        return self._handle_a1_missingness("ethhaitian", int, missing_value=0)

    def _missingness_ethnigeria(self) -> Optional[int]:
        """Handles missingness for ETHNIGERIA."""
        return self._handle_a1_missingness("ethnigeria", int, missing_value=0)

    def _missingness_ethethiop(self) -> Optional[int]:
        """Handles missingness for ETHETHIOP."""
        return self._handle_a1_missingness("ethethiop", int, missing_value=0)

    def _missingness_ethsomali(self) -> Optional[int]:
        """Handles missingness for ETHSOMALI."""
        return self._handle_a1_missingness("ethsomali", int, missing_value=0)

    def _missingness_ethblkoth(self) -> Optional[int]:
        """Handles missingness for ETHBLKOTH."""
        return self._handle_a1_missingness("ethblkoth", int, missing_value=0)

    def _missingness_ethblkothx(self) -> Optional[str]:
        """Handles missingness for ETHBLKOTHX."""
        return self._handle_a1_missingness("ethblkothx", str, missing_value="0")

    def _missingness_ethmexican(self) -> Optional[int]:
        """Handles missingness for ETHMEXICAN."""
        return self._handle_a1_missingness("ethmexican", int, missing_value=0)

    def _missingness_ethpuerto(self) -> Optional[int]:
        """Handles missingness for ETHPUERTO."""
        return self._handle_a1_missingness("ethpuerto", int, missing_value=0)

    def _missingness_ethsalva(self) -> Optional[int]:
        """Handles missingness for ETHSALVA."""
        return self._handle_a1_missingness("ethsalva", int, missing_value=0)

    def _missingness_ethcuban(self) -> Optional[int]:
        """Handles missingness for ETHCUBAN."""
        return self._handle_a1_missingness("ethcuban", int, missing_value=0)

    def _missingness_ethdomin(self) -> Optional[int]:
        """Handles missingness for ETHDOMIN."""
        return self._handle_a1_missingness("ethdomin", int, missing_value=0)

    def _missingness_ethguatem(self) -> Optional[int]:
        """Handles missingness for ETHGUATEM."""
        return self._handle_a1_missingness("ethguatem", int, missing_value=0)

    def _missingness_ethhisoth(self) -> Optional[int]:
        """Handles missingness for ETHHISOTH."""
        return self._handle_a1_missingness("ethhisoth", int, missing_value=0)

    def _missingness_ethhisothx(self) -> Optional[str]:
        """Handles missingness for ETHHISOTHX."""
        return self._handle_a1_missingness("ethhisothx", str, missing_value="0")

    def _missingness_racemena(self) -> Optional[int]:
        """Handles missingness for RACEMENA."""
        return self._handle_a1_missingness("racemena", int, missing_value=0)

    def _missingness_ethlebanon(self) -> Optional[int]:
        """Handles missingness for ETHLEBANON."""
        return self._handle_a1_missingness("ethlebanon", int, missing_value=0)

    def _missingness_ethiran(self) -> Optional[int]:
        """Handles missingness for ETHIRAN."""
        return self._handle_a1_missingness("ethiran", int, missing_value=0)

    def _missingness_ethegypt(self) -> Optional[int]:
        """Handles missingness for ETHEGYPT."""
        return self._handle_a1_missingness("ethegypt", int, missing_value=0)

    def _missingness_ethsyria(self) -> Optional[int]:
        """Handles missingness for ETHSYRIA."""
        return self._handle_a1_missingness("ethsyria", int, missing_value=0)

    def _missingness_ethiraqi(self) -> Optional[int]:
        """Handles missingness for ETHIRAQI."""
        return self._handle_a1_missingness("ethiraqi", int, missing_value=0)

    def _missingness_ethisrael(self) -> Optional[int]:
        """Handles missingness for ETHISRAEL."""
        return self._handle_a1_missingness("ethisrael", int, missing_value=0)

    def _missingness_ethmenaoth(self) -> Optional[int]:
        """Handles missingness for ETHMENAOTH."""
        return self._handle_a1_missingness("ethmenaoth", int, missing_value=0)

    def _missingness_ethmenaotx(self) -> Optional[str]:
        """Handles missingness for ETHMENAOTX."""
        return self._handle_a1_missingness("ethmenaotx", str, missing_value="0")

    def _missingness_racenhpi(self) -> Optional[int]:
        """Handles missingness for RACENHPI."""
        return self._handle_a1_missingness("racenhpi", int, missing_value=0)

    def _missingness_ethhawaii(self) -> Optional[int]:
        """Handles missingness for ETHHAWAII."""
        return self._handle_a1_missingness("ethhawaii", int, missing_value=0)

    def _missingness_ethsamoan(self) -> Optional[int]:
        """Handles missingness for ETHSAMOAN."""
        return self._handle_a1_missingness("ethsamoan", int, missing_value=0)

    def _missingness_ethchamor(self) -> Optional[int]:
        """Handles missingness for ETHCHAMOR."""
        return self._handle_a1_missingness("ethchamor", int, missing_value=0)

    def _missingness_ethtongan(self) -> Optional[int]:
        """Handles missingness for ETHTONGAN."""
        return self._handle_a1_missingness("ethtongan", int, missing_value=0)

    def _missingness_ethfijian(self) -> Optional[int]:
        """Handles missingness for ETHFIJIAN."""
        return self._handle_a1_missingness("ethfijian", int, missing_value=0)

    def _missingness_ethmarshal(self) -> Optional[int]:
        """Handles missingness for ETHMARSHAL."""
        return self._handle_a1_missingness("ethmarshal", int, missing_value=0)

    def _missingness_ethnhpioth(self) -> Optional[int]:
        """Handles missingness for ETHNHPIOTH."""
        return self._handle_a1_missingness("ethnhpioth", int, missing_value=0)

    def _missingness_ethnhpiotx(self) -> Optional[str]:
        """Handles missingness for ETHNHPIOTX."""
        return self._handle_a1_missingness("ethnhpiotx", str, missing_value="0")

    def _missingness_racewhite(self) -> Optional[int]:
        """Handles missingness for RACEWHITE."""
        return self._handle_a1_missingness("racewhite", int, missing_value=0)

    def _missingness_ethenglish(self) -> Optional[int]:
        """Handles missingness for ETHENGLISH."""
        return self._handle_a1_missingness("ethenglish", int, missing_value=0)

    def _missingness_ethgerman(self) -> Optional[int]:
        """Handles missingness for ETHGERMAN."""
        return self._handle_a1_missingness("ethgerman", int, missing_value=0)

    def _missingness_ethirish(self) -> Optional[int]:
        """Handles missingness for ETHIRISH."""
        return self._handle_a1_missingness("ethirish", int, missing_value=0)

    def _missingness_ethitalian(self) -> Optional[int]:
        """Handles missingness for ETHITALIAN."""
        return self._handle_a1_missingness("ethitalian", int, missing_value=0)

    def _missingness_ethpolish(self) -> Optional[int]:
        """Handles missingness for ETHPOLISH."""
        return self._handle_a1_missingness("ethpolish", int, missing_value=0)

    def _missingness_ethscott(self) -> Optional[int]:
        """Handles missingness for ETHSCOTT."""
        return self._handle_a1_missingness("ethscott", int, missing_value=0)

    def _missingness_ethwhioth(self) -> Optional[int]:
        """Handles missingness for ETHWHIOTH."""
        return self._handle_a1_missingness("ethwhioth", int, missing_value=0)

    def _missingness_ethwhiothx(self) -> Optional[str]:
        """Handles missingness for ETHWHIOTHX."""
        return self._handle_a1_missingness("ethwhiothx", str, missing_value="0")

    def _missingness_raceunkn(self) -> Optional[int]:
        """Handles missingness for RACEUNKN."""
        return self._handle_a1_missingness("raceunkn", int, missing_value=0)

    def _missingness_genman(self) -> Optional[int]:
        """Handles missingness for GENMAN."""
        return self._handle_a1_missingness("genman", int, missing_value=0)

    def _missingness_genwoman(self) -> Optional[int]:
        """Handles missingness for GENWOMAN."""
        return self._handle_a1_missingness("genwoman", int, missing_value=0)

    def _missingness_gentrman(self) -> Optional[int]:
        """Handles missingness for GENTRMAN."""
        return self._handle_a1_missingness("gentrman", int, missing_value=0)

    def _missingness_gentrwoman(self) -> Optional[int]:
        """Handles missingness for GENTRWOMAN."""
        return self._handle_a1_missingness("gentrwoman", int, missing_value=0)

    def _missingness_gennonbi(self) -> Optional[int]:
        """Handles missingness for GENNONBI."""
        return self._handle_a1_missingness("gennonbi", int, missing_value=0)

    def _missingness_gentwospir(self) -> Optional[int]:
        """Handles missingness for GENTWOSPIR."""
        return self._handle_a1_missingness("gentwospir", int, missing_value=0)

    def _missingness_genoth(self) -> Optional[int]:
        """Handles missingness for GENOTH."""
        return self._handle_a1_missingness("genoth", int, missing_value=0)

    def _missingness_genothx(self) -> Optional[str]:
        """Handles missingness for GENOTHX."""
        return self._handle_a1_missingness("genothx", str, missing_value="0")

    def _missingness_gendkn(self) -> Optional[int]:
        """Handles missingness for GENDKN."""
        return self._handle_a1_missingness("gendkn", int, missing_value=0)

    def _missingness_gennoans(self) -> Optional[int]:
        """Handles missingness for GENNOANS."""
        return self._handle_a1_missingness("gennoans", int, missing_value=0)

    def _missingness_sexorngay(self) -> Optional[int]:
        """Handles missingness for SEXORNGAY."""
        return self._handle_a1_missingness("sexorngay", int, missing_value=0)

    def _missingness_sexornhet(self) -> Optional[int]:
        """Handles missingness for SEXORNHET."""
        return self._handle_a1_missingness("sexornhet", int, missing_value=0)

    def _missingness_sexornbi(self) -> Optional[int]:
        """Handles missingness for SEXORNBI."""
        return self._handle_a1_missingness("sexornbi", int, missing_value=0)

    def _missingness_sexorntwos(self) -> Optional[int]:
        """Handles missingness for SEXORNTWOS."""
        return self._handle_a1_missingness("sexorntwos", int, missing_value=0)

    def _missingness_sexornoth(self) -> Optional[int]:
        """Handles missingness for SEXORNOTH."""
        return self._handle_a1_missingness("sexornoth", int, missing_value=0)

    def _missingness_sexornothx(self) -> Optional[str]:
        """Handles missingness for SEXORNOTHX."""
        return self._handle_a1_missingness("sexornothx", str, missing_value="0")

    def _missingness_sexorndnk(self) -> Optional[int]:
        """Handles missingness for SEXORNDNK."""
        return self._handle_a1_missingness("sexorndnk", int, missing_value=0)

    def _missingness_sexornnoan(self) -> Optional[int]:
        """Handles missingness for SEXORNNOAN."""
        return self._handle_a1_missingness("sexornnoan", int, missing_value=0)

    def _missingness_adistate(self) -> Optional[int]:
        """Handles missingness for ADISTATE."""
        return self._handle_a1_missingness("adistate", int, missing_value=999)

    def _missingness_adinat(self) -> Optional[int]:
        """Handles missingness for ADINAT."""
        return self._handle_a1_missingness("adinat", int, missing_value=999)

    def _missingness_priocc(self) -> Optional[int]:
        """Handles missingness for PRIOCC."""
        return self._handle_a1_missingness("priocc", int, missing_value=999)

    ############################################################
    # Need to pull through the following. Used both for derived
    # variable work, and per RDD: "Note that although this
    # variable is not collected at follow-up visits, the value
    # from the initial visit will be shown at all follow-up
    # visits"
    ############################################################

    def _missingness_sex(self) -> Optional[int]:
        """Handles missingness for SEX."""
        return self.handle_prev_visit("sex", int)

    def _missingness_birthsex(self) -> Optional[int]:
        """Handles missingness for BIRTHSEX."""
        return self.handle_prev_visit("birthsex", int)

    def _missingness_hispanic(self) -> Optional[int]:
        """Handles missingness for HISPANIC."""
        return self.handle_prev_visit("hispanic", int)

    def _missingness_hispor(self) -> Optional[int]:
        """Handles missingness for HISPOR."""
        if self.uds.get_value("hispanic", int) != 1:
            return 88

        return self.handle_prev_visit("hispor", int)

    def _missingness_hisporx(self) -> Optional[str]:
        """Handles missingness for HISPORX."""
        return self.handle_prev_visit("hisporx", str)

    def _missingness_race(self) -> Optional[int]:
        """Handles missingness for RACE."""
        return self.handle_prev_visit("race", int)

    def _missingness_racex(self) -> Optional[str]:
        """Handles missingness for RACEX."""
        return self.handle_prev_visit("racex", str)

    def _missingness_racesec(self) -> Optional[int]:
        """Handles missingness for RACESEC."""
        return self.handle_prev_visit("racesec", int)

    def _missingness_racesecx(self) -> Optional[str]:
        """Handles missingness for RACESECX."""
        return self.handle_prev_visit("racesecx", str)

    def _missingness_raceter(self) -> Optional[int]:
        """Handles missingness for RACETER."""
        return self.handle_prev_visit("raceter", int)

    def _missingness_raceterx(self) -> Optional[str]:
        """Handles missingness for RACETERX."""
        return self.handle_prev_visit("raceterx", str)

    def _missingness_primlang(self) -> Optional[int]:
        """Handles missingness for PRIMLANG."""
        return self.handle_prev_visit("primlang", int)

    def _missingness_primlanx(self) -> Optional[str]:
        """Handles missingness for PRIMLANX."""
        return self.handle_prev_visit("primlanx", str)

    def _missingness_handed(self) -> Optional[int]:
        """Handles missingness for HANDED."""
        return self.handle_prev_visit("handed", int)

    def _missingness_educ(self) -> Optional[int]:
        """Handles missingness for EDUC."""
        return self.handle_prev_visit("educ", int)

    def _missingness_lvleduc(self) -> Optional[int]:
        """Handles missingness for LVLEDUC."""
        return self.handle_prev_visit("lvleduc", int)

    def _missingness_source(self) -> Optional[int]:
        """Handles missingness for SOURCE."""
        return self.handle_prev_visit("source", int)

    def _missingness_sourcenw(self) -> Optional[int]:
        """Handles missingness for SOURCENW."""
        return self.handle_prev_visit("sourcenw", int)
