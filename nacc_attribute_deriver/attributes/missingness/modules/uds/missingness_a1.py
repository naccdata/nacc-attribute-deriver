"""Class to handle A1-specific missingness values."""

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class UDSFormA1Missingness(UDSMissingness):
    ###################################################
    # Other / variables with unique missingness logic #
    ###################################################

    def _missingness_residenc(self) -> int:
        """Handles missingness for RESIDENC.

        In V1/V2, could be set to 5: Other. This is recoded to 9.
        """
        if self.formver < 3 and self.uds.get_value("residenc", int) == 5:
            return 9

        return self.generic_missingness("residenc", int)

    def _missingness_maristat(self) -> int:
        """Handles missingness for MARISTAT.

        In V1/V2, could be set to 8: Other. This is recoded to 9.
        """
        if self.formver < 3 and self.uds.get_value("maristat", int) == 8:
            return 9

        return self.generic_missingness("maristat", int)

    ############################################################
    # Generic A1 missingness logic
    #
    # A1 has many variables that are only collected in IVP. So in
    # may need to potentially pull through from the previous visit
    # Per RDD: "Note that although this variable is not collected
    # at follow-up visits, the value from the initial visit will
    # be shown at all follow-up visits"
    ############################################################

    def __handle_generic_a1_missingness(self, field: str) -> int:
        """For most variables the default is 0 in V4, so generalize."""
        default = INFORMED_MISSINGNESS if self.formver < 4 else 0
        return self.handle_prev_visit(field, int, default=default)

    def _missingness_raceaian(self) -> int:
        """Handles missingness for RACEAIAN."""
        return self.__handle_generic_a1_missingness("raceaian")

    def _missingness_raceasian(self) -> int:
        """Handles missingness for RACEASIAN."""
        return self.__handle_generic_a1_missingness("raceasian")

    def _missingness_ethchinese(self) -> int:
        """Handles missingness for ETHCHINESE."""
        return self.__handle_generic_a1_missingness("ethchinese")

    def _missingness_ethindia(self) -> int:
        """Handles missingness for ETHINDIA."""
        return self.__handle_generic_a1_missingness("ethindia")

    def _missingness_ethfilip(self) -> int:
        """Handles missingness for ETHFILIP."""
        return self.__handle_generic_a1_missingness("ethfilip")

    def _missingness_ethvietnam(self) -> int:
        """Handles missingness for ETHVIETNAM."""
        return self.__handle_generic_a1_missingness("ethvietnam")

    def _missingness_ethkorean(self) -> int:
        """Handles missingness for ETHKOREAN."""
        return self.__handle_generic_a1_missingness("ethkorean")

    def _missingness_ethjapan(self) -> int:
        """Handles missingness for ETHJAPAN."""
        return self.__handle_generic_a1_missingness("ethjapan")

    def _missingness_ethasnoth(self) -> int:
        """Handles missingness for ETHASNOTH."""
        return self.__handle_generic_a1_missingness("ethasnoth")

    def _missingness_raceblack(self) -> int:
        """Handles missingness for RACEBLACK."""
        return self.__handle_generic_a1_missingness("raceblack")

    def _missingness_ethafamer(self) -> int:
        """Handles missingness for ETHAFAMER."""
        return self.__handle_generic_a1_missingness("ethafamer")

    def _missingness_ethjamaica(self) -> int:
        """Handles missingness for ETHJAMAICA."""
        return self.__handle_generic_a1_missingness("ethjamaica")

    def _missingness_ethhaitian(self) -> int:
        """Handles missingness for ETHHAITIAN."""
        return self.__handle_generic_a1_missingness("ethhaitian")

    def _missingness_ethnigeria(self) -> int:
        """Handles missingness for ETHNIGERIA."""
        return self.__handle_generic_a1_missingness("ethnigeria")

    def _missingness_ethethiop(self) -> int:
        """Handles missingness for ETHETHIOP."""
        return self.__handle_generic_a1_missingness("ethethiop")

    def _missingness_ethsomali(self) -> int:
        """Handles missingness for ETHSOMALI."""
        return self.__handle_generic_a1_missingness("ethsomali")

    def _missingness_ethblkoth(self) -> int:
        """Handles missingness for ETHBLKOTH."""
        return self.__handle_generic_a1_missingness("ethblkoth")

    def _missingness_ethmexican(self) -> int:
        """Handles missingness for ETHMEXICAN."""
        return self.__handle_generic_a1_missingness("ethmexican")

    def _missingness_ethpuerto(self) -> int:
        """Handles missingness for ETHPUERTO."""
        return self.__handle_generic_a1_missingness("ethpuerto")

    def _missingness_ethsalva(self) -> int:
        """Handles missingness for ETHSALVA."""
        return self.__handle_generic_a1_missingness("ethsalva")

    def _missingness_ethcuban(self) -> int:
        """Handles missingness for ETHCUBAN."""
        return self.__handle_generic_a1_missingness("ethcuban")

    def _missingness_ethdomin(self) -> int:
        """Handles missingness for ETHDOMIN."""
        return self.__handle_generic_a1_missingness("ethdomin")

    def _missingness_ethguatem(self) -> int:
        """Handles missingness for ETHGUATEM."""
        return self.__handle_generic_a1_missingness("ethguatem")

    def _missingness_ethhisoth(self) -> int:
        """Handles missingness for ETHHISOTH."""
        return self.__handle_generic_a1_missingness("ethhisoth")

    def _missingness_racemena(self) -> int:
        """Handles missingness for RACEMENA."""
        return self.__handle_generic_a1_missingness("racemena")

    def _missingness_ethlebanon(self) -> int:
        """Handles missingness for ETHLEBANON."""
        return self.__handle_generic_a1_missingness("ethlebanon")

    def _missingness_ethiran(self) -> int:
        """Handles missingness for ETHIRAN."""
        return self.__handle_generic_a1_missingness("ethiran")

    def _missingness_ethegypt(self) -> int:
        """Handles missingness for ETHEGYPT."""
        return self.__handle_generic_a1_missingness("ethegypt")

    def _missingness_ethsyria(self) -> int:
        """Handles missingness for ETHSYRIA."""
        return self.__handle_generic_a1_missingness("ethsyria")

    def _missingness_ethiraqi(self) -> int:
        """Handles missingness for ETHIRAQI."""
        return self.__handle_generic_a1_missingness("ethiraqi")

    def _missingness_ethisrael(self) -> int:
        """Handles missingness for ETHISRAEL."""
        return self.__handle_generic_a1_missingness("ethisrael")

    def _missingness_ethmenaoth(self) -> int:
        """Handles missingness for ETHMENAOTH."""
        return self.__handle_generic_a1_missingness("ethmenaoth")

    def _missingness_racenhpi(self) -> int:
        """Handles missingness for RACENHPI."""
        return self.__handle_generic_a1_missingness("racenhpi")

    def _missingness_ethhawaii(self) -> int:
        """Handles missingness for ETHHAWAII."""
        return self.__handle_generic_a1_missingness("ethhawaii")

    def _missingness_ethsamoan(self) -> int:
        """Handles missingness for ETHSAMOAN."""
        return self.__handle_generic_a1_missingness("ethsamoan")

    def _missingness_ethchamor(self) -> int:
        """Handles missingness for ETHCHAMOR."""
        return self.__handle_generic_a1_missingness("ethchamor")

    def _missingness_ethtongan(self) -> int:
        """Handles missingness for ETHTONGAN."""
        return self.__handle_generic_a1_missingness("ethtongan")

    def _missingness_ethfijian(self) -> int:
        """Handles missingness for ETHFIJIAN."""
        return self.__handle_generic_a1_missingness("ethfijian")

    def _missingness_ethmarshal(self) -> int:
        """Handles missingness for ETHMARSHAL."""
        return self.__handle_generic_a1_missingness("ethmarshal")

    def _missingness_ethnhpioth(self) -> int:
        """Handles missingness for ETHNHPIOTH."""
        return self.__handle_generic_a1_missingness("ethnhpioth")

    def _missingness_racewhite(self) -> int:
        """Handles missingness for RACEWHITE."""
        return self.__handle_generic_a1_missingness("racewhite")

    def _missingness_ethenglish(self) -> int:
        """Handles missingness for ETHENGLISH."""
        return self.__handle_generic_a1_missingness("ethenglish")

    def _missingness_ethgerman(self) -> int:
        """Handles missingness for ETHGERMAN."""
        return self.__handle_generic_a1_missingness("ethgerman")

    def _missingness_ethirish(self) -> int:
        """Handles missingness for ETHIRISH."""
        return self.__handle_generic_a1_missingness("ethirish")

    def _missingness_ethitalian(self) -> int:
        """Handles missingness for ETHITALIAN."""
        return self.__handle_generic_a1_missingness("ethitalian")

    def _missingness_ethpolish(self) -> int:
        """Handles missingness for ETHPOLISH."""
        return self.__handle_generic_a1_missingness("ethpolish")

    def _missingness_ethscott(self) -> int:
        """Handles missingness for ETHSCOTT."""
        return self.__handle_generic_a1_missingness("ethscott")

    def _missingness_ethwhioth(self) -> int:
        """Handles missingness for ETHWHIOTH."""
        return self.__handle_generic_a1_missingness("ethwhioth")

    def _missingness_raceunkn(self) -> int:
        """Handles missingness for RACEUNKN."""
        return self.__handle_generic_a1_missingness("raceunkn")

    def _missingness_genman(self) -> int:
        """Handles missingness for GENMAN."""
        return self.__handle_generic_a1_missingness("genman")

    def _missingness_genwoman(self) -> int:
        """Handles missingness for GENWOMAN."""
        return self.__handle_generic_a1_missingness("genwoman")

    def _missingness_gentrman(self) -> int:
        """Handles missingness for GENTRMAN."""
        return self.__handle_generic_a1_missingness("gentrman")

    def _missingness_gentrwoman(self) -> int:
        """Handles missingness for GENTRWOMAN."""
        return self.__handle_generic_a1_missingness("gentrwoman")

    def _missingness_gennonbi(self) -> int:
        """Handles missingness for GENNONBI."""
        return self.__handle_generic_a1_missingness("gennonbi")

    def _missingness_gentwospir(self) -> int:
        """Handles missingness for GENTWOSPIR."""
        return self.__handle_generic_a1_missingness("gentwospir")

    def _missingness_genoth(self) -> int:
        """Handles missingness for GENOTH."""
        return self.__handle_generic_a1_missingness("genoth")

    def _missingness_gendkn(self) -> int:
        """Handles missingness for GENDKN."""
        return self.__handle_generic_a1_missingness("gendkn")

    def _missingness_gennoans(self) -> int:
        """Handles missingness for GENNOANS."""
        return self.__handle_generic_a1_missingness("gennoans")

    def _missingness_sexorngay(self) -> int:
        """Handles missingness for SEXORNGAY."""
        return self.__handle_generic_a1_missingness("sexorngay")

    def _missingness_sexornhet(self) -> int:
        """Handles missingness for SEXORNHET."""
        return self.__handle_generic_a1_missingness("sexornhet")

    def _missingness_sexornbi(self) -> int:
        """Handles missingness for SEXORNBI."""
        return self.__handle_generic_a1_missingness("sexornbi")

    def _missingness_sexorntwos(self) -> int:
        """Handles missingness for SEXORNTWOS."""
        return self.__handle_generic_a1_missingness("sexorntwos")

    def _missingness_sexornoth(self) -> int:
        """Handles missingness for SEXORNOTH."""
        return self.__handle_generic_a1_missingness("sexornoth")

    def _missingness_sexorndnk(self) -> int:
        """Handles missingness for SEXORNDNK."""
        return self.__handle_generic_a1_missingness("sexorndnk")

    def _missingness_sexornnoan(self) -> int:
        """Handles missingness for SEXORNNOAN."""
        return self.__handle_generic_a1_missingness("sexornnoan")

    def _missingness_adistate(self) -> int:
        """Handles missingness for ADISTATE."""
        return self.handle_prev_visit("adistate", int, default=99)

    def _missingness_adinat(self) -> int:
        """Handles missingness for ADINAT."""
        return self.handle_prev_visit("adinat", int, default=99)

    def _missingness_priocc(self) -> int:
        """Handles missingness for PRIOCC."""
        return self.handle_prev_visit("priocc", int, default=99)

    # The following are required so no defaults

    def _missingness_birthmo(self) -> int:
        """Handles missingness for BIRTHMO."""
        return self.handle_prev_visit("birthmo", int)

    def _missingness_birthyr(self) -> int:
        """Handles missingness for BIRTHYR."""
        return self.handle_prev_visit("birthyr", int)

    def _missingness_birthsex(self) -> int:
        """Handles missingness for BIRTHSEX."""
        return self.handle_prev_visit("birthsex", int)

    def _missingness_intersex(self) -> int:
        """Handles missingness for INTERSEX."""
        return self.handle_prev_visit("intersex", int)

    def _missingness_served(self) -> int:
        """Handles missingness for SERVED."""
        return self.handle_prev_visit("served", int)

    def _missingness_handed(self) -> int:
        """Handles missingness for HANDED."""
        return self.handle_prev_visit("handed", int)

    def _missingness_educ(self) -> int:
        """Handles missingness for EDUC."""
        return self.handle_prev_visit("educ", int)

    def _missingness_lvleduc(self) -> int:
        """Handles missingness for LVLEDUC."""
        return self.handle_prev_visit("lvleduc", int)

    def _missingness_sourcenw(self) -> int:
        """Handles missingness for SOURCENW."""
        return self.handle_prev_visit("sourcenw", int)

    ######################
    # Write-in variables #
    ######################

    def _missingness_chldhdctry(self) -> str:
        """Handles missingness for CHLDHDCTRY."""
        return self.handle_prev_visit("chldhdctry", str)

    def _missingness_raceaianx(self) -> str:
        """Handles missingness for RACEAIANX."""
        return self.handle_prev_visit("raceaianx", str)

    def _missingness_ethasnothx(self) -> str:
        """Handles missingness for ETHASNOTHX."""
        return self.handle_prev_visit("ethasnothx", str)

    def _missingness_ethblkothx(self) -> str:
        """Handles missingness for ETHBLKOTHX."""
        return self.handle_prev_visit("ethblkothx", str)

    def _missingness_ethhisothx(self) -> str:
        """Handles missingness for ETHHISOTHX."""
        return self.handle_prev_visit("ethhisothx", str)

    def _missingness_ethmenaotx(self) -> str:
        """Handles missingness for ETHMENAOTX."""
        return self.handle_prev_visit("ethmenaotx", str)

    def _missingness_ethnhpiotx(self) -> str:
        """Handles missingness for ETHNHPIOTX."""
        return self.handle_prev_visit("ethnhpiotx", str)

    def _missingness_ethwhiothx(self) -> str:
        """Handles missingness for ETHWHIOTHX."""
        return self.handle_prev_visit("ethwhiothx", str)

    def _missingness_genothx(self) -> str:
        """Handles missingness for GENOTHX."""
        return self.handle_prev_visit("genothx", str)

    def _missingness_sexornothx(self) -> str:
        """Handles missingness for SEXORNOTHX."""
        return self.handle_prev_visit("sexornothx", str)

    ############################W################
    # Legacy variables (only in V3 and earlier) #
    #############################################

    def _missingness_sex(self) -> int:
        """Handles missingness for SEX."""
        return self.handle_prev_visit("sex", int)

    def _missingness_hispanic(self) -> int:
        """Handles missingness for HISPANIC."""
        return self.handle_prev_visit("hispanic", int)

    def _missingness_hispor(self) -> int:
        """Handles missingness for HISPOR."""
        hispanic = self.uds.get_value("hispanic", int)
        if self.uds.is_initial() and hispanic != 1:
            return 88

        return self.handle_prev_visit("hispor", int)

    def _missingness_hisporx(self) -> str:
        """Handles missingness for HISPORX."""
        return self.handle_prev_visit("hisporx", str)

    def _missingness_race(self) -> int:
        """Handles missingness for RACE."""
        return self.handle_prev_visit("race", int)

    def _missingness_racex(self) -> str:
        """Handles missingness for RACEX."""
        return self.handle_prev_visit("racex", str)

    def _missingness_racesec(self) -> int:
        """Handles missingness for RACESEC."""
        return self.handle_prev_visit("racesec", int)

    def _missingness_racesecx(self) -> str:
        """Handles missingness for RACESECX."""
        return self.handle_prev_visit("racesecx", str)

    def _missingness_raceter(self) -> int:
        """Handles missingness for RACETER."""
        return self.handle_prev_visit("raceter", int)

    def _missingness_raceterx(self) -> str:
        """Handles missingness for RACETERX."""
        return self.handle_prev_visit("raceterx", str)

    def _missingness_primlang(self) -> int:
        """Handles missingness for PRIMLANG."""
        return self.handle_prev_visit("primlang", int)

    def _missingness_primlanx(self) -> str:
        """Handles missingness for PRIMLANX."""
        return self.handle_prev_visit("primlanx", str)

    def _missingness_source(self) -> int:
        """Handles missingness for SOURCE."""
        return self.handle_prev_visit("source", int)
