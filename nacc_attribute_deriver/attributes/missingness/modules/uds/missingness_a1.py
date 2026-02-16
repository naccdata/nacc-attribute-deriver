"""Class to handle A1-specific missingness values."""

from typing import Optional, Type

from nacc_attribute_deriver.attributes.collection.uds_collection import UDSMissingness
from nacc_attribute_deriver.attributes.namespace.namespace import (
    T,
    WorkingNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS
from nacc_attribute_deriver.utils.errors import AttributeDeriverError


class UDSFormA1Missingness(UDSMissingness):
    def __init__(self, table: SymbolTable):
        super().__init__(table)

        # for dob variables
        self.__working = WorkingNamespace(table=table)

        # set generic default based on formver
        self.__default = INFORMED_MISSINGNESS if self.formver < 4 else 0

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

    def __handle_a1_prev_visit(
        self,
        field: str,
        attr_type: Type[T],
        default: Optional[T] = None,
        provided_fvp: bool = False,
    ) -> T:
        """Handle A1 prev visit.

        May need to ignore values added in FVP.
        """
        # ignore the current value if it is not an initial visit AND it's
        # not a value provided in FVP. this is to handle when they
        # enter something into an FVP form they weren't expected to
        ignore_current_value = not self.uds.is_initial() and not provided_fvp

        return self.handle_prev_visit(
            attribute=field,
            attr_type=attr_type,
            default=default,
            ignore_current_value=ignore_current_value,
        )

    def _missingness_raceaian(self) -> int:
        """Handles missingness for RACEAIAN."""
        return self.__handle_a1_prev_visit("raceaian", int, default=self.__default)

    def _missingness_raceaianx(self) -> str:
        """Handles missingness for RACEAIANX."""
        return self.__handle_a1_prev_visit("raceaianx", str)

    def _missingness_raceasian(self) -> int:
        """Handles missingness for RACEASIAN."""
        return self.__handle_a1_prev_visit("raceasian", int, default=self.__default)

    def _missingness_ethchinese(self) -> int:
        """Handles missingness for ETHCHINESE."""
        return self.__handle_a1_prev_visit("ethchinese", int, default=self.__default)

    def _missingness_ethindia(self) -> int:
        """Handles missingness for ETHINDIA."""
        return self.__handle_a1_prev_visit("ethindia", int, default=self.__default)

    def _missingness_ethfilip(self) -> int:
        """Handles missingness for ETHFILIP."""
        return self.__handle_a1_prev_visit("ethfilip", int, default=self.__default)

    def _missingness_ethvietnam(self) -> int:
        """Handles missingness for ETHVIETNAM."""
        return self.__handle_a1_prev_visit("ethvietnam", int, default=self.__default)

    def _missingness_ethkorean(self) -> int:
        """Handles missingness for ETHKOREAN."""
        return self.__handle_a1_prev_visit("ethkorean", int, default=self.__default)

    def _missingness_ethjapan(self) -> int:
        """Handles missingness for ETHJAPAN."""
        return self.__handle_a1_prev_visit("ethjapan", int, default=self.__default)

    def _missingness_ethasnoth(self) -> int:
        """Handles missingness for ETHASNOTH."""
        return self.__handle_a1_prev_visit("ethasnoth", int, default=self.__default)

    def _missingness_ethasnothx(self) -> str:
        """Handles missingness for ETHASNOTHX."""
        return self.__handle_a1_prev_visit("ethasnothx", str)

    def _missingness_raceblack(self) -> int:
        """Handles missingness for RACEBLACK."""
        return self.__handle_a1_prev_visit("raceblack", int, default=self.__default)

    def _missingness_ethafamer(self) -> int:
        """Handles missingness for ETHAFAMER."""
        return self.__handle_a1_prev_visit("ethafamer", int, default=self.__default)

    def _missingness_ethjamaica(self) -> int:
        """Handles missingness for ETHJAMAICA."""
        return self.__handle_a1_prev_visit("ethjamaica", int, default=self.__default)

    def _missingness_ethhaitian(self) -> int:
        """Handles missingness for ETHHAITIAN."""
        return self.__handle_a1_prev_visit("ethhaitian", int, default=self.__default)

    def _missingness_ethnigeria(self) -> int:
        """Handles missingness for ETHNIGERIA."""
        return self.__handle_a1_prev_visit("ethnigeria", int, default=self.__default)

    def _missingness_ethethiop(self) -> int:
        """Handles missingness for ETHETHIOP."""
        return self.__handle_a1_prev_visit("ethethiop", int, default=self.__default)

    def _missingness_ethsomali(self) -> int:
        """Handles missingness for ETHSOMALI."""
        return self.__handle_a1_prev_visit("ethsomali", int, default=self.__default)

    def _missingness_ethblkoth(self) -> int:
        """Handles missingness for ETHBLKOTH."""
        return self.__handle_a1_prev_visit("ethblkoth", int, default=self.__default)

    def _missingness_ethblkothx(self) -> str:
        """Handles missingness for ETHBLKOTHX."""
        return self.__handle_a1_prev_visit("ethblkothx", str)

    def _missingness_ethmexican(self) -> int:
        """Handles missingness for ETHMEXICAN."""
        return self.__handle_a1_prev_visit("ethmexican", int, default=self.__default)

    def _missingness_ethpuerto(self) -> int:
        """Handles missingness for ETHPUERTO."""
        return self.__handle_a1_prev_visit("ethpuerto", int, default=self.__default)

    def _missingness_ethsalva(self) -> int:
        """Handles missingness for ETHSALVA."""
        return self.__handle_a1_prev_visit("ethsalva", int, default=self.__default)

    def _missingness_ethcuban(self) -> int:
        """Handles missingness for ETHCUBAN."""
        return self.__handle_a1_prev_visit("ethcuban", int, default=self.__default)

    def _missingness_ethdomin(self) -> int:
        """Handles missingness for ETHDOMIN."""
        return self.__handle_a1_prev_visit("ethdomin", int, default=self.__default)

    def _missingness_ethguatem(self) -> int:
        """Handles missingness for ETHGUATEM."""
        return self.__handle_a1_prev_visit("ethguatem", int, default=self.__default)

    def _missingness_ethhisoth(self) -> int:
        """Handles missingness for ETHHISOTH."""
        return self.__handle_a1_prev_visit("ethhisoth", int, default=self.__default)

    def _missingness_ethhisothx(self) -> str:
        """Handles missingness for ETHHISOTHX."""
        return self.__handle_a1_prev_visit("ethhisothx", str)

    def _missingness_racemena(self) -> int:
        """Handles missingness for RACEMENA."""
        return self.__handle_a1_prev_visit("racemena", int, default=self.__default)

    def _missingness_ethlebanon(self) -> int:
        """Handles missingness for ETHLEBANON."""
        return self.__handle_a1_prev_visit("ethlebanon", int, default=self.__default)

    def _missingness_ethiran(self) -> int:
        """Handles missingness for ETHIRAN."""
        return self.__handle_a1_prev_visit("ethiran", int, default=self.__default)

    def _missingness_ethegypt(self) -> int:
        """Handles missingness for ETHEGYPT."""
        return self.__handle_a1_prev_visit("ethegypt", int, default=self.__default)

    def _missingness_ethsyria(self) -> int:
        """Handles missingness for ETHSYRIA."""
        return self.__handle_a1_prev_visit("ethsyria", int, default=self.__default)

    def _missingness_ethiraqi(self) -> int:
        """Handles missingness for ETHIRAQI."""
        return self.__handle_a1_prev_visit("ethiraqi", int, default=self.__default)

    def _missingness_ethisrael(self) -> int:
        """Handles missingness for ETHISRAEL."""
        return self.__handle_a1_prev_visit("ethisrael", int, default=self.__default)

    def _missingness_ethmenaoth(self) -> int:
        """Handles missingness for ETHMENAOTH."""
        return self.__handle_a1_prev_visit("ethmenaoth", int, default=self.__default)

    def _missingness_ethmenaotx(self) -> str:
        """Handles missingness for ETHMENAOTX."""
        return self.__handle_a1_prev_visit("ethmenaotx", str)

    def _missingness_racenhpi(self) -> int:
        """Handles missingness for RACENHPI."""
        return self.__handle_a1_prev_visit("racenhpi", int, default=self.__default)

    def _missingness_ethhawaii(self) -> int:
        """Handles missingness for ETHHAWAII."""
        return self.__handle_a1_prev_visit("ethhawaii", int, default=self.__default)

    def _missingness_ethsamoan(self) -> int:
        """Handles missingness for ETHSAMOAN."""
        return self.__handle_a1_prev_visit("ethsamoan", int, default=self.__default)

    def _missingness_ethchamor(self) -> int:
        """Handles missingness for ETHCHAMOR."""
        return self.__handle_a1_prev_visit("ethchamor", int, default=self.__default)

    def _missingness_ethtongan(self) -> int:
        """Handles missingness for ETHTONGAN."""
        return self.__handle_a1_prev_visit("ethtongan", int, default=self.__default)

    def _missingness_ethfijian(self) -> int:
        """Handles missingness for ETHFIJIAN."""
        return self.__handle_a1_prev_visit("ethfijian", int, default=self.__default)

    def _missingness_ethmarshal(self) -> int:
        """Handles missingness for ETHMARSHAL."""
        return self.__handle_a1_prev_visit("ethmarshal", int, default=self.__default)

    def _missingness_ethnhpioth(self) -> int:
        """Handles missingness for ETHNHPIOTH."""
        return self.__handle_a1_prev_visit("ethnhpioth", int, default=self.__default)

    def _missingness_ethnhpiotx(self) -> str:
        """Handles missingness for ETHNHPIOTX."""
        return self.__handle_a1_prev_visit("ethnhpiotx", str)

    def _missingness_racewhite(self) -> int:
        """Handles missingness for RACEWHITE."""
        return self.__handle_a1_prev_visit("racewhite", int, default=self.__default)

    def _missingness_ethenglish(self) -> int:
        """Handles missingness for ETHENGLISH."""
        return self.__handle_a1_prev_visit("ethenglish", int, default=self.__default)

    def _missingness_ethgerman(self) -> int:
        """Handles missingness for ETHGERMAN."""
        return self.__handle_a1_prev_visit("ethgerman", int, default=self.__default)

    def _missingness_ethirish(self) -> int:
        """Handles missingness for ETHIRISH."""
        return self.__handle_a1_prev_visit("ethirish", int, default=self.__default)

    def _missingness_ethitalian(self) -> int:
        """Handles missingness for ETHITALIAN."""
        return self.__handle_a1_prev_visit("ethitalian", int, default=self.__default)

    def _missingness_ethpolish(self) -> int:
        """Handles missingness for ETHPOLISH."""
        return self.__handle_a1_prev_visit("ethpolish", int, default=self.__default)

    def _missingness_ethscott(self) -> int:
        """Handles missingness for ETHSCOTT."""
        return self.__handle_a1_prev_visit("ethscott", int, default=self.__default)

    def _missingness_ethwhioth(self) -> int:
        """Handles missingness for ETHWHIOTH."""
        return self.__handle_a1_prev_visit("ethwhioth", int, default=self.__default)

    def _missingness_ethwhiothx(self) -> str:
        """Handles missingness for ETHWHIOTHX."""
        return self.__handle_a1_prev_visit("ethwhiothx", str)

    def _missingness_raceunkn(self) -> int:
        """Handles missingness for RACEUNKN."""
        return self.__handle_a1_prev_visit("raceunkn", int, default=self.__default)

    def _missingness_priocc(self) -> int:
        """Handles missingness for PRIOCC."""
        return self.__handle_a1_prev_visit("priocc", int, default=999)

    def _missingness_chldhdctry(self) -> str:
        """Handles missingness for CHLDHDCTRY."""
        return self.__handle_a1_prev_visit("chldhdctry", str)

    # The following are required so no defaults

    def _missingness_birthsex(self) -> int:
        """Handles missingness for BIRTHSEX."""
        return self.__handle_a1_prev_visit("birthsex", int)

    def _missingness_intersex(self) -> int:
        """Handles missingness for INTERSEX."""
        return self.__handle_a1_prev_visit("intersex", int)

    def _missingness_served(self) -> int:
        """Handles missingness for SERVED."""
        return self.__handle_a1_prev_visit("served", int)

    def _missingness_handed(self) -> int:
        """Handles missingness for HANDED."""
        return self.__handle_a1_prev_visit("handed", int)

    def _missingness_educ(self) -> int:
        """Handles missingness for EDUC."""
        return self.__handle_a1_prev_visit("educ", int)

    def _missingness_lvleduc(self) -> int:
        """Handles missingness for LVLEDUC."""
        return self.__handle_a1_prev_visit("lvleduc", int)

    def _missingness_sourcenw(self) -> int:
        """Handles missingness for SOURCENW."""
        return self.__handle_a1_prev_visit("sourcenw", int)

    ##############################################
    # Set every visit, so may potentially change #
    ##############################################

    def _missingness_genman(self) -> int:
        """Handles missingness for GENMAN."""
        return self.__handle_a1_prev_visit(
            "genman", int, default=self.__default, provided_fvp=True
        )

    def _missingness_genwoman(self) -> int:
        """Handles missingness for GENWOMAN."""
        return self.__handle_a1_prev_visit(
            "genwoman", int, default=self.__default, provided_fvp=True
        )

    def _missingness_gentrman(self) -> int:
        """Handles missingness for GENTRMAN."""
        return self.__handle_a1_prev_visit(
            "gentrman", int, default=self.__default, provided_fvp=True
        )

    def _missingness_gentrwoman(self) -> int:
        """Handles missingness for GENTRWOMAN."""
        return self.__handle_a1_prev_visit(
            "gentrwoman", int, default=self.__default, provided_fvp=True
        )

    def _missingness_gennonbi(self) -> int:
        """Handles missingness for GENNONBI."""
        return self.__handle_a1_prev_visit(
            "gennonbi", int, default=self.__default, provided_fvp=True
        )

    def _missingness_gentwospir(self) -> int:
        """Handles missingness for GENTWOSPIR."""
        return self.__handle_a1_prev_visit(
            "gentwospir", int, default=self.__default, provided_fvp=True
        )

    def _missingness_genoth(self) -> int:
        """Handles missingness for GENOTH."""
        return self.__handle_a1_prev_visit(
            "genoth", int, default=self.__default, provided_fvp=True
        )

    def _missingness_genothx(self) -> str:
        """Handles missingness for GENOTHX."""
        return self.__handle_a1_prev_visit("genothx", str, provided_fvp=True)

    def _missingness_gendkn(self) -> int:
        """Handles missingness for GENDKN."""
        return self.__handle_a1_prev_visit(
            "gendkn", int, default=self.__default, provided_fvp=True
        )

    def _missingness_gennoans(self) -> int:
        """Handles missingness for GENNOANS."""
        return self.__handle_a1_prev_visit(
            "gennoans", int, default=self.__default, provided_fvp=True
        )

    def _missingness_sexorngay(self) -> int:
        """Handles missingness for SEXORNGAY."""
        return self.__handle_a1_prev_visit(
            "sexorngay", int, default=self.__default, provided_fvp=True
        )

    def _missingness_sexornhet(self) -> int:
        """Handles missingness for SEXORNHET."""
        return self.__handle_a1_prev_visit(
            "sexornhet", int, default=self.__default, provided_fvp=True
        )

    def _missingness_sexornbi(self) -> int:
        """Handles missingness for SEXORNBI."""
        return self.__handle_a1_prev_visit(
            "sexornbi", int, default=self.__default, provided_fvp=True
        )

    def _missingness_sexorntwos(self) -> int:
        """Handles missingness for SEXORNTWOS."""
        return self.__handle_a1_prev_visit(
            "sexorntwos", int, default=self.__default, provided_fvp=True
        )

    def _missingness_sexornoth(self) -> int:
        """Handles missingness for SEXORNOTH."""
        return self.__handle_a1_prev_visit(
            "sexornoth", int, default=self.__default, provided_fvp=True
        )

    def _missingness_sexornothx(self) -> str:
        """Handles missingness for SEXORNOTHX."""
        return self.__handle_a1_prev_visit("sexornothx", str, provided_fvp=True)

    def _missingness_sexorndnk(self) -> int:
        """Handles missingness for SEXORNDNK."""
        return self.__handle_a1_prev_visit(
            "sexorndnk", int, default=self.__default, provided_fvp=True
        )

    def _missingness_sexornnoan(self) -> int:
        """Handles missingness for SEXORNNOAN."""
        return self.__handle_a1_prev_visit(
            "sexornnoan", int, default=self.__default, provided_fvp=True
        )

    def _missingness_adistate(self) -> int:
        """Handles missingness for ADISTATE."""
        return self.__handle_a1_prev_visit(
            "adistate", int, default=999, provided_fvp=True
        )

    def _missingness_adinat(self) -> int:
        """Handles missingness for ADINAT."""
        return self.__handle_a1_prev_visit(
            "adinat", int, default=999, provided_fvp=True
        )

    ############################W################
    # Legacy variables (only in V3 and earlier) #
    #############################################

    def _missingness_sex(self) -> int:
        """Handles missingness for SEX."""
        return self.__handle_a1_prev_visit("sex", int, provided_fvp=True)

    def _missingness_hispanic(self) -> int:
        """Handles missingness for HISPANIC."""
        return self.__handle_a1_prev_visit("hispanic", int)

    def _missingness_hispor(self) -> int:
        """Handles missingness for HISPOR."""
        hispanic = self.uds.get_value("hispanic", int)
        if self.uds.is_initial() and hispanic != 1:
            return 88

        return self.__handle_a1_prev_visit("hispor", int)

    def _missingness_hisporx(self) -> str:
        """Handles missingness for HISPORX."""
        return self.__handle_a1_prev_visit("hisporx", str)

    def _missingness_race(self) -> int:
        """Handles missingness for RACE."""
        return self.__handle_a1_prev_visit("race", int)

    def _missingness_racex(self) -> str:
        """Handles missingness for RACEX."""
        return self.__handle_a1_prev_visit("racex", str)

    def _missingness_racesec(self) -> int:
        """Handles missingness for RACESEC."""
        return self.__handle_a1_prev_visit("racesec", int)

    def _missingness_racesecx(self) -> str:
        """Handles missingness for RACESECX."""
        return self.__handle_a1_prev_visit("racesecx", str)

    def _missingness_raceter(self) -> int:
        """Handles missingness for RACETER."""
        return self.__handle_a1_prev_visit("raceter", int)

    def _missingness_raceterx(self) -> str:
        """Handles missingness for RACETERX."""
        return self.__handle_a1_prev_visit("raceterx", str)

    def _missingness_primlang(self) -> int:
        """Handles missingness for PRIMLANG."""
        return self.__handle_a1_prev_visit("primlang", int)

    def _missingness_primlanx(self) -> str:
        """Handles missingness for PRIMLANX."""
        return self.__handle_a1_prev_visit("primlanx", str)

    def _missingness_source(self) -> int:
        """Handles missingness for SOURCE."""
        return self.__handle_a1_prev_visit("source", int)

    #####################################
    # Specially-handled DOB variables,
    # set from working metadata instead #
    #####################################

    def _missingness_birthmo(self) -> int:
        """Handles missingness for BIRTHMO."""
        result = self.__working.get_cross_sectional_value(
            "birthmo", int, default=self.uds.get_required("birthmo", int)
        )

        if not result:
            raise AttributeDeriverError("Cannot determine BIRTHMO")

        return result

    def _missingness_birthyr(self) -> int:
        """Handles missingness for BIRTHYR."""
        result = self.__working.get_cross_sectional_value(
            "birthyr", int, default=self.uds.get_required("birthyr", int)
        )

        if not result:
            raise AttributeDeriverError("Cannot determine BIRTHYR")

        return result
