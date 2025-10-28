"""Class to handle A1-specific missingness values."""

from typing import Optional

from .missingness_uds import UDSMissingness


class UDSFormA1Missingness(UDSMissingness):
    def _missingness_raceaian(self) -> Optional[int]:
        """Handles missingness for RACEAIAN."""
        return self.handle_v4_missingness("raceaian")

    def _missingness_raceaianx(self) -> Optional[str]:
        """Handles missingness for RACEAIANX."""
        return self.handle_v4_writein("raceaianx")

    def _missingness_raceasian(self) -> Optional[int]:
        """Handles missingness for RACEASIAN."""
        return self.handle_v4_missingness("raceasian")

    def _missingness_ethchinese(self) -> Optional[int]:
        """Handles missingness for ETHCHINESE."""
        return self.handle_v4_missingness("ethchinese")

    def _missingness_ethindia(self) -> Optional[int]:
        """Handles missingness for ETHINDIA."""
        return self.handle_v4_missingness("ethindia")

    def _missingness_ethfilip(self) -> Optional[int]:
        """Handles missingness for ETHFILIP."""
        return self.handle_v4_missingness("ethfilip")

    def _missingness_ethvietnam(self) -> Optional[int]:
        """Handles missingness for ETHVIETNAM."""
        return self.handle_v4_missingness("ethvietnam")

    def _missingness_ethkorean(self) -> Optional[int]:
        """Handles missingness for ETHKOREAN."""
        return self.handle_v4_missingness("ethkorean")

    def _missingness_ethjapan(self) -> Optional[int]:
        """Handles missingness for ETHJAPAN."""
        return self.handle_v4_missingness("ethjapan")

    def _missingness_ethasnoth(self) -> Optional[int]:
        """Handles missingness for ETHASNOTH."""
        return self.handle_v4_missingness("ethasnoth")

    def _missingness_ethasnothx(self) -> Optional[str]:
        """Handles missingness for ETHASNOTHX."""
        return self.handle_v4_writein("ethasnothx")

    def _missingness_raceblack(self) -> Optional[int]:
        """Handles missingness for RACEBLACK."""
        return self.handle_v4_missingness("raceblack")

    def _missingness_ethafamer(self) -> Optional[int]:
        """Handles missingness for ETHAFAMER."""
        return self.handle_v4_missingness("ethafamer")

    def _missingness_ethjamaica(self) -> Optional[int]:
        """Handles missingness for ETHJAMAICA."""
        return self.handle_v4_missingness("ethjamaica")

    def _missingness_ethhaitian(self) -> Optional[int]:
        """Handles missingness for ETHHAITIAN."""
        return self.handle_v4_missingness("ethhaitian")

    def _missingness_ethnigeria(self) -> Optional[int]:
        """Handles missingness for ETHNIGERIA."""
        return self.handle_v4_missingness("ethnigeria")

    def _missingness_ethethiop(self) -> Optional[int]:
        """Handles missingness for ETHETHIOP."""
        return self.handle_v4_missingness("ethethiop")

    def _missingness_ethsomali(self) -> Optional[int]:
        """Handles missingness for ETHSOMALI."""
        return self.handle_v4_missingness("ethsomali")

    def _missingness_ethblkoth(self) -> Optional[int]:
        """Handles missingness for ETHBLKOTH."""
        return self.handle_v4_missingness("ethblkoth")

    def _missingness_ethblkothx(self) -> Optional[str]:
        """Handles missingness for ETHBLKOTHX."""
        return self.handle_v4_writein("ethblkothx")

    def _missingness_ethmexican(self) -> Optional[int]:
        """Handles missingness for ETHMEXICAN."""
        return self.handle_v4_missingness("ethmexican")

    def _missingness_ethpuerto(self) -> Optional[int]:
        """Handles missingness for ETHPUERTO."""
        return self.handle_v4_missingness("ethpuerto")

    def _missingness_ethsalva(self) -> Optional[int]:
        """Handles missingness for ETHSALVA."""
        return self.handle_v4_missingness("ethsalva")

    def _missingness_ethcuban(self) -> Optional[int]:
        """Handles missingness for ETHCUBAN."""
        return self.handle_v4_missingness("ethcuban")

    def _missingness_ethdomin(self) -> Optional[int]:
        """Handles missingness for ETHDOMIN."""
        return self.handle_v4_missingness("ethdomin")

    def _missingness_ethguatem(self) -> Optional[int]:
        """Handles missingness for ETHGUATEM."""
        return self.handle_v4_missingness("ethguatem")

    def _missingness_ethhisoth(self) -> Optional[int]:
        """Handles missingness for ETHHISOTH."""
        return self.handle_v4_missingness("ethhisoth")

    def _missingness_ethhisothx(self) -> Optional[str]:
        """Handles missingness for ETHHISOTHX."""
        return self.handle_v4_writein("ethhisothx")

    def _missingness_racemena(self) -> Optional[int]:
        """Handles missingness for RACEMENA."""
        return self.handle_v4_missingness("racemena")

    def _missingness_ethlebanon(self) -> Optional[int]:
        """Handles missingness for ETHLEBANON."""
        return self.handle_v4_missingness("ethlebanon")

    def _missingness_ethiran(self) -> Optional[int]:
        """Handles missingness for ETHIRAN."""
        return self.handle_v4_missingness("ethiran")

    def _missingness_ethegypt(self) -> Optional[int]:
        """Handles missingness for ETHEGYPT."""
        return self.handle_v4_missingness("ethegypt")

    def _missingness_ethsyria(self) -> Optional[int]:
        """Handles missingness for ETHSYRIA."""
        return self.handle_v4_missingness("ethsyria")

    def _missingness_ethiraqi(self) -> Optional[int]:
        """Handles missingness for ETHIRAQI."""
        return self.handle_v4_missingness("ethiraqi")

    def _missingness_ethisrael(self) -> Optional[int]:
        """Handles missingness for ETHISRAEL."""
        return self.handle_v4_missingness("ethisrael")

    def _missingness_ethmenaoth(self) -> Optional[int]:
        """Handles missingness for ETHMENAOTH."""
        return self.handle_v4_missingness("ethmenaoth")

    def _missingness_ethmenaotx(self) -> Optional[str]:
        """Handles missingness for ETHMENAOTX."""
        return self.handle_v4_writein("ethmenaotx")

    def _missingness_racenhpi(self) -> Optional[int]:
        """Handles missingness for RACENHPI."""
        return self.handle_v4_missingness("racenhpi")

    def _missingness_ethhawaii(self) -> Optional[int]:
        """Handles missingness for ETHHAWAII."""
        return self.handle_v4_missingness("ethhawaii")

    def _missingness_ethsamoan(self) -> Optional[int]:
        """Handles missingness for ETHSAMOAN."""
        return self.handle_v4_missingness("ethsamoan")

    def _missingness_ethchamor(self) -> Optional[int]:
        """Handles missingness for ETHCHAMOR."""
        return self.handle_v4_missingness("ethchamor")

    def _missingness_ethtongan(self) -> Optional[int]:
        """Handles missingness for ETHTONGAN."""
        return self.handle_v4_missingness("ethtongan")

    def _missingness_ethfijian(self) -> Optional[int]:
        """Handles missingness for ETHFIJIAN."""
        return self.handle_v4_missingness("ethfijian")

    def _missingness_ethmarshal(self) -> Optional[int]:
        """Handles missingness for ETHMARSHAL."""
        return self.handle_v4_missingness("ethmarshal")

    def _missingness_ethnhpioth(self) -> Optional[int]:
        """Handles missingness for ETHNHPIOTH."""
        return self.handle_v4_missingness("ethnhpioth")

    def _missingness_ethnhpiotx(self) -> Optional[str]:
        """Handles missingness for ETHNHPIOTX."""
        return self.handle_v4_writein("ethnhpiotx")

    def _missingness_racewhite(self) -> Optional[int]:
        """Handles missingness for RACEWHITE."""
        return self.handle_v4_missingness("racewhite")

    def _missingness_ethenglish(self) -> Optional[int]:
        """Handles missingness for ETHENGLISH."""
        return self.handle_v4_missingness("ethenglish")

    def _missingness_ethgerman(self) -> Optional[int]:
        """Handles missingness for ETHGERMAN."""
        return self.handle_v4_missingness("ethgerman")

    def _missingness_ethirish(self) -> Optional[int]:
        """Handles missingness for ETHIRISH."""
        return self.handle_v4_missingness("ethirish")

    def _missingness_ethitalian(self) -> Optional[int]:
        """Handles missingness for ETHITALIAN."""
        return self.handle_v4_missingness("ethitalian")

    def _missingness_ethpolish(self) -> Optional[int]:
        """Handles missingness for ETHPOLISH."""
        return self.handle_v4_missingness("ethpolish")

    def _missingness_ethscott(self) -> Optional[int]:
        """Handles missingness for ETHSCOTT."""
        return self.handle_v4_missingness("ethscott")

    def _missingness_ethwhioth(self) -> Optional[int]:
        """Handles missingness for ETHWHIOTH."""
        return self.handle_v4_missingness("ethwhioth")

    def _missingness_ethwhiothx(self) -> Optional[str]:
        """Handles missingness for ETHWHIOTHX."""
        return self.handle_v4_writein("ethwhiothx")

    def _missingness_raceunkn(self) -> Optional[int]:
        """Handles missingness for RACEUNKN."""
        return self.handle_v4_missingness("raceunkn")

    def _missingness_genman(self) -> Optional[int]:
        """Handles missingness for GENMAN."""
        return self.handle_v4_missingness("genman")

    def _missingness_genwoman(self) -> Optional[int]:
        """Handles missingness for GENWOMAN."""
        return self.handle_v4_missingness("genwoman")

    def _missingness_gentrman(self) -> Optional[int]:
        """Handles missingness for GENTRMAN."""
        return self.handle_v4_missingness("gentrman")

    def _missingness_gentrwoman(self) -> Optional[int]:
        """Handles missingness for GENTRWOMAN."""
        return self.handle_v4_missingness("gentrwoman")

    def _missingness_gennonbi(self) -> Optional[int]:
        """Handles missingness for GENNONBI."""
        return self.handle_v4_missingness("gennonbi")

    def _missingness_gentwospir(self) -> Optional[int]:
        """Handles missingness for GENTWOSPIR."""
        return self.handle_v4_missingness("gentwospir")

    def _missingness_genoth(self) -> Optional[int]:
        """Handles missingness for GENOTH."""
        return self.handle_v4_missingness("genoth")

    def _missingness_genothx(self) -> Optional[str]:
        """Handles missingness for GENOTHX."""
        return self.handle_v4_writein("genothx")

    def _missingness_gendkn(self) -> Optional[int]:
        """Handles missingness for GENDKN."""
        return self.handle_v4_missingness("gendkn")

    def _missingness_gennoans(self) -> Optional[int]:
        """Handles missingness for GENNOANS."""
        return self.handle_v4_missingness("gennoans")

    def _missingness_sexorngay(self) -> Optional[int]:
        """Handles missingness for SEXORNGAY."""
        return self.handle_v4_missingness("sexorngay")

    def _missingness_sexornhet(self) -> Optional[int]:
        """Handles missingness for SEXORNHET."""
        return self.handle_v4_missingness("sexornhet")

    def _missingness_sexornbi(self) -> Optional[int]:
        """Handles missingness for SEXORNBI."""
        return self.handle_v4_missingness("sexornbi")

    def _missingness_sexorntwos(self) -> Optional[int]:
        """Handles missingness for SEXORNTWOS."""
        return self.handle_v4_missingness("sexorntwos")

    def _missingness_sexornoth(self) -> Optional[int]:
        """Handles missingness for SEXORNOTH."""
        return self.handle_v4_missingness("sexornoth")

    def _missingness_sexornothx(self) -> Optional[str]:
        """Handles missingness for SEXORNOTHX."""
        return self.handle_v4_writein("sexornothx")

    def _missingness_sexorndnk(self) -> Optional[int]:
        """Handles missingness for SEXORNDNK."""
        return self.handle_v4_missingness("sexorndnk")

    def _missingness_sexornnoan(self) -> Optional[int]:
        """Handles missingness for SEXORNNOAN."""
        return self.handle_v4_missingness("sexornnoan")

    def _missingness_adistate(self) -> Optional[int]:
        """Handles missingness for ADISTATE."""
        return self.handle_v4_missingness("adistate", missing_value=999)

    def _missingness_adinat(self) -> Optional[int]:
        """Handles missingness for ADINAT."""
        return self.handle_v4_missingness("adinat", missing_value=999)

    def _missingness_priocc(self) -> Optional[int]:
        """Handles missingness for PRIOCC."""
        return self.handle_v4_missingness("priocc", missing_value=999)
