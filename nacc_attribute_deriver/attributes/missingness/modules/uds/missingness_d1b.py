"""Class to handle D1b-specific missingness values."""

from typing import Optional

from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

from .missingness_d1 import UDSFormD1Missingness


class UDSFormD1bMissingness(UDSFormD1Missingness):
    #############################
    # BIOMARKDX-gated variables #
    #############################

    def __handle_biomarkdx_gate(self, field: str) -> Optional[int]:
        """Handles variables gated by BIOMARKDX, which follow:

        If BIOMARKDX = 0, FIELD should = 0.
        """
        if self.uds.get_value("biomarkdx", int) == 0:
            return 0

        return self.generic_missingness(field)

    def _missingness_fluidbiom(self) -> Optional[int]:
        """Handles missingness for FLUIDBIOM."""
        return self.__handle_biomarkdx_gate("fluidbiom")

    def _missingness_imagingdx(self) -> Optional[int]:
        """Handles missingness for IMAGINGDX."""
        return self.__handle_biomarkdx_gate("imagingdx")

    def _missingness_petdx(self) -> Optional[int]:
        """Handles missingness for PETDX."""
        return self.__handle_biomarkdx_gate("petdx")

    def _missingness_fdgpetdx(self) -> Optional[int]:
        """Handles missingness for FDGPETDX."""
        return self.__handle_biomarkdx_gate("fdgpetdx")

    def _missingness_datscandx(self) -> Optional[int]:
        """Handles missingness for DATSCANDX."""
        return self.__handle_biomarkdx_gate("datscandx")

    def _missingness_tracothdx(self) -> Optional[int]:
        """Handles missingness for TRACOTHDX."""
        return self.__handle_biomarkdx_gate("tracothdx")

    def _missingness_structdx(self) -> Optional[int]:
        """Handles missingness for STRUCTDX."""
        return self.__handle_biomarkdx_gate("structdx")

    def _missingness_othbiom1(self) -> Optional[int]:
        """Handles missingness for OTHBIOM1."""
        return self.__handle_biomarkdx_gate("othbiom1")

    def _missingness_othbiom2(self) -> Optional[int]:
        """Handles missingness for OTHBIOM2."""
        return self.__handle_biomarkdx_gate("othbiom2")

    def _missingness_othbiom3(self) -> Optional[int]:
        """Handles missingness for OTHBIOM3."""
        return self.__handle_biomarkdx_gate("othbiom3")

    def _missingness_autdommut(self) -> Optional[int]:
        """Handles missingness for AUTDOMMUT."""
        return self.__handle_biomarkdx_gate("autdommut")

    ###########################
    # FORMVER-gated variables #
    ###########################

    def __handle_formver_v4_gate(self, field: str) -> Optional[int]:
        """Handle variables gated by FORMVER = 4."""
        value = self.uds.get_value(field, int)
        if value is None:
            if self.formver >= 4:
                return 0
            return INFORMED_MISSINGNESS

        return None

    def _missingness_ftld(self) -> Optional[int]:
        """Handles missingness for FTLD."""
        return self.__handle_formver_v4_gate("ftld")

    def _missingness_cte(self) -> Optional[int]:
        """Handles missingness for CTE."""
        return self.__handle_formver_v4_gate("cte")

    def _missingness_caa(self) -> Optional[int]:
        """Handles missingness for CAA."""
        return self.__handle_formver_v4_gate("caa")

    def _missingness_late(self) -> Optional[int]:
        """Handles missingness for LATE."""
        return self.__handle_formver_v4_gate("late")

    def _missingness_msa(self) -> Optional[int]:
        """Handles missingness for MSA."""
        return self.__handle_formver_v4_gate("msa")

    def __handle_formver_v4_ftld_gate(self, field: str) -> Optional[int]:
        """Handle variables gated by FORMVER = 4 and FTLD."""
        if self.uds.get_value("ftld", int) is None:
            return 0

        return self.__handle_formver_v4_gate(field)

    def _missingness_psp(self) -> Optional[int]:
        """Handles missingness for PSP."""
        return self.__handle_formver_v4_ftld_gate("psp")

    def _missingness_cort(self) -> Optional[int]:
        """Handles missingness for CORT."""
        return self.__handle_formver_v4_ftld_gate("cort")

    def _missingness_ftldmo(self) -> Optional[int]:
        """Handles missingness for FTLDMO."""
        return self.__handle_formver_v4_ftld_gate("ftldmo")

    def _missingness_ftldnos(self) -> Optional[int]:
        """Handles missingness for FTLDNOS."""
        return self.__handle_formver_v4_ftld_gate("ftldnos")

    def _missingness_cvd(self) -> Optional[int]:
        """Handles missingness for CVD."""
        return self.__handle_formver_v4_ftld_gate("cvd")

    def _missingness_downs(self) -> Optional[int]:
        """Handles missingness for DOWNS."""
        return self.__handle_formver_v4_ftld_gate("downs")

    def _missingness_hunt(self) -> Optional[int]:
        """Handles missingness for HUNT."""
        return self.__handle_formver_v4_ftld_gate("hunt")

    def _missingness_prion(self) -> Optional[int]:
        """Handles missingness for PRION."""
        return self.__handle_formver_v4_ftld_gate("prion")

    def _missingness_othcog(self) -> Optional[int]:
        """Handles missingness for OTHCOG."""
        return self.__handle_formver_v4_ftld_gate("othcog")

    ####################################
    # Cognitive-status-gated variables #
    ####################################

    def __handle_cognitive_impairment_gate(
        self, gate: str, field: str, ignore_normcog: bool = False
    ) -> Optional[int]:
        """Handles variables gated by cognitive impairment.

        If DEMENTED = 1 or MCI = 1 or IMPNOMCI = 1 (cognitively impaired)
            and GATE is blank, FIELD = 7
        If NORMCOG = 1 then FIELD = 8
        """
        gate_value = self.uds.get_value(gate, int)
        if self.has_cognitive_impairment() and gate_value is None:
            return 7
        if not ignore_normcog and self.normcog == 1:
            return 8

        return self.generic_missingness(field)

    def _missingness_cteif(self) -> Optional[int]:
        """Handles missingness for CTEIF."""
        return self.__handle_cognitive_impairment_gate("cte", "cteif")

    def _missingness_ctecert(self) -> Optional[int]:
        """Handles missingness for CTECERT."""
        return self.__handle_cognitive_impairment_gate("cte", "ctecert")

    def _missingness_caaif(self) -> Optional[int]:
        """Handles missingness for CAAIF."""
        return self.__handle_cognitive_impairment_gate("caa", "caaif")

    def _missingness_lateif(self) -> Optional[int]:
        """Handles missingness for LATEIF."""
        return self.__handle_cognitive_impairment_gate("late", "lateif")

    def _missingness_msaif(self) -> Optional[int]:
        """Handles missingness for MSAIF."""
        return self.__handle_cognitive_impairment_gate("msa", "msaif")

    def _missingness_pspif(self) -> Optional[int]:
        """Handles missingness for PSPIF."""
        return self.__handle_cognitive_impairment_gate("psp", "pspif")

    def _missingness_cortif(self) -> Optional[int]:
        """Handles missingness for CORTIF."""
        return self.__handle_cognitive_impairment_gate("cort", "cortif")

    def _missingness_ftldmoif(self) -> Optional[int]:
        """Handles missingness for FTLDMOIF."""
        return self.__handle_cognitive_impairment_gate("ftldmo", "ftldmoif")

    def _missingness_ftldnoif(self) -> Optional[int]:
        """Handles missingness for FTLDNOIF."""
        if not self.check_applicable():
            return INFORMED_MISSINGNESS

        return self.__handle_cognitive_impairment_gate("ftldnos", "ftldnoif")

    def _missingness_ftldsubt(self) -> Optional[int]:
        """Handles missingness for FTLDSUBT."""
        return self.__handle_cognitive_impairment_gate(
            "ftld", "ftldsubt", ignore_normcog=True
        )

    def _missingness_cvdif(self) -> Optional[int]:
        """Handles missingness for CVDIF."""
        return self.__handle_cognitive_impairment_gate("cvd", "cvdif")

    def _missingness_downsif(self) -> Optional[int]:
        """Handles missingness for DOWNSIF."""
        return self.__handle_cognitive_impairment_gate("downs", "downsif")

    def _missingness_huntif(self) -> Optional[int]:
        """Handles missingness for HUNTIF."""
        return self.__handle_cognitive_impairment_gate("hunt", "huntif")

    def _missingness_prionif(self) -> Optional[int]:
        """Handles missingness for PRIONIF."""
        return self.__handle_cognitive_impairment_gate("prion", "prionif")

    def _missingness_othcogif(self) -> Optional[int]:
        """Handles missingness for OTHCOGIF."""
        return self.__handle_cognitive_impairment_gate("othcog", "othcogif")

    ######################
    # Write-in variables #
    ######################

    def _missingness_ftldsubx(self) -> Optional[str]:
        """Handles missingness for FTLDSUBX."""
        return self.generic_writein("ftldsubx")

    def _missingness_othcogx(self) -> Optional[str]:
        """Handles missingness for OTHCOGX."""
        return self.generic_writein("othcogx")

    def _missingness_othmutx(self) -> Optional[str]:
        """Handles missingness for OTHMUTX."""
        return self.generic_writein("othmutx")

    def _missingness_bloodothx(self) -> Optional[str]:
        """Handles missingness for BLOODOTHX."""
        return self.generic_writein("bloodothx")

    def _missingness_csfothx(self) -> Optional[str]:
        """Handles missingness for CSFOTHX."""
        return self.generic_writein("csfothx")

    def _missingness_fdgothx(self) -> Optional[str]:
        """Handles missingness for FDGOTHX."""
        return self.generic_writein("fdgothx")

    def _missingness_tracothdxx(self) -> Optional[str]:
        """Handles missingness for TRACOTHDXX."""
        return self.generic_writein("tracothdxx")

    def _missingness_tracerothx(self) -> Optional[str]:
        """Handles missingness for TRACEROTHX."""
        return self.generic_writein("tracerothx")

    def _missingness_othbiomx1(self) -> Optional[str]:
        """Handles missingness for OTHBIOMX1."""
        return self.generic_writein("othbiomx1")

    def _missingness_biomothx1(self) -> Optional[str]:
        """Handles missingness for BIOMOTHX1."""
        return self.generic_writein("biomothx1")

    def _missingness_othbiomx2(self) -> Optional[str]:
        """Handles missingness for OTHBIOMX2."""
        return self.generic_writein("othbiomx2")

    def _missingness_biomothx2(self) -> Optional[str]:
        """Handles missingness for BIOMOTHX2."""
        return self.generic_writein("biomothx2")

    def _missingness_othbiomx3(self) -> Optional[str]:
        """Handles missingness for OTHBIOMX3."""
        return self.generic_writein("othbiomx3")

    def _missingness_biomothx3(self) -> Optional[str]:
        """Handles missingness for BIOMOTHX3."""
        return self.generic_writein("biomothx3")
