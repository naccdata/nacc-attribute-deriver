"""Class to handle D1b-specific missingness values."""

from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

from .helpers.d1_base import UDSFormD1Missingness


class UDSFormD1bMissingness(UDSFormD1Missingness):
    #############################
    # BIOMARKDX-gated variables #
    #############################

    def __handle_biomarkdx_gate(self, field: str) -> int:
        """Handles variables gated by BIOMARKDX, which follow:

        If BIOMARKDX = 0, FIELD should = 0.
        """
        if self.uds.get_value("biomarkdx", int) == 0:
            return 0

        return self.generic_missingness(field, int)

    def _missingness_fluidbiom(self) -> int:
        """Handles missingness for FLUIDBIOM."""
        return self.__handle_biomarkdx_gate("fluidbiom")

    def _missingness_imagingdx(self) -> int:
        """Handles missingness for IMAGINGDX."""
        return self.__handle_biomarkdx_gate("imagingdx")

    def _missingness_petdx(self) -> int:
        """Handles missingness for PETDX."""
        return self.__handle_biomarkdx_gate("petdx")

    def _missingness_fdgpetdx(self) -> int:
        """Handles missingness for FDGPETDX."""
        return self.__handle_biomarkdx_gate("fdgpetdx")

    def _missingness_datscandx(self) -> int:
        """Handles missingness for DATSCANDX."""
        return self.__handle_biomarkdx_gate("datscandx")

    def _missingness_tracothdx(self) -> int:
        """Handles missingness for TRACOTHDX."""
        return self.__handle_biomarkdx_gate("tracothdx")

    def _missingness_structdx(self) -> int:
        """Handles missingness for STRUCTDX."""
        return self.__handle_biomarkdx_gate("structdx")

    def _missingness_othbiom1(self) -> int:
        """Handles missingness for OTHBIOM1."""
        return self.__handle_biomarkdx_gate("othbiom1")

    def _missingness_othbiom2(self) -> int:
        """Handles missingness for OTHBIOM2."""
        return self.__handle_biomarkdx_gate("othbiom2")

    def _missingness_othbiom3(self) -> int:
        """Handles missingness for OTHBIOM3."""
        return self.__handle_biomarkdx_gate("othbiom3")

    def _missingness_autdommut(self) -> int:
        """Handles missingness for AUTDOMMUT."""
        return self.__handle_biomarkdx_gate("autdommut")

    ###########################
    # FORMVER-gated variables #
    ###########################

    def __handle_formver_gate(self, field: str) -> int:
        """Handle where the missingness value depends on the form version."""
        default = None if self.formver < 4 else 0
        return self.generic_missingness(field, int, default=default)

    def _missingness_ftld(self) -> int:
        """Handles missingness for FTLD."""
        return self.__handle_formver_gate("ftld")

    def _missingness_cte(self) -> int:
        """Handles missingness for CTE."""
        return self.__handle_formver_gate("cte")

    def _missingness_caa(self) -> int:
        """Handles missingness for CAA."""
        return self.__handle_formver_gate("caa")

    def _missingness_late(self) -> int:
        """Handles missingness for LATE."""
        return self.__handle_formver_gate("late")

    def _missingness_msa(self) -> int:
        """Handles missingness for MSA."""
        return self.__handle_formver_gate("msa")

    def __handle_formver_ftld_gate(self, field: str) -> int:
        """Handle variables gated by FORMVER and FTLD."""
        value = self.uds.get_value(field, int)
        if value is not None:
            return value

        if self.uds.get_value("ftld", int) is None:
            return 0

        return self.__handle_formver_gate(field)

    def _missingness_psp(self) -> int:
        """Handles missingness for PSP."""
        return self.__handle_formver_ftld_gate("psp")

    def _missingness_cort(self) -> int:
        """Handles missingness for CORT."""
        return self.__handle_formver_ftld_gate("cort")

    def _missingness_ftldmo(self) -> int:
        """Handles missingness for FTLDMO."""
        return self.__handle_formver_ftld_gate("ftldmo")

    def _missingness_ftldnos(self) -> int:
        """Handles missingness for FTLDNOS."""
        return self.__handle_formver_ftld_gate("ftldnos")

    def _missingness_cvd(self) -> int:
        """Handles missingness for CVD."""
        return self.__handle_formver_ftld_gate("cvd")

    def _missingness_downs(self) -> int:
        """Handles missingness for DOWNS."""
        return self.__handle_formver_ftld_gate("downs")

    def _missingness_hunt(self) -> int:
        """Handles missingness for HUNT."""
        return self.__handle_formver_ftld_gate("hunt")

    def _missingness_prion(self) -> int:
        """Handles missingness for PRION."""
        return self.__handle_formver_ftld_gate("prion")

    def _missingness_othcog(self) -> int:
        """Handles missingness for OTHCOG."""
        return self.__handle_formver_ftld_gate("othcog")

    ####################################
    # Cognitive-status-gated variables #
    ####################################

    def _missingness_cteif(self) -> int:
        """Handles missingness for CTEIF."""
        return self.handle_cognitive_impairment_gate("cte", "cteif", ignore_normcog_0=True)

    def _missingness_ctecert(self) -> int:
        """Handles missingness for CTECERT."""
        return self.handle_cognitive_impairment_gate("cte", "ctecert", ignore_normcog_0=True)

    def _missingness_caaif(self) -> int:
        """Handles missingness for CAAIF."""
        return self.handle_cognitive_impairment_gate("caa", "caaif", ignore_normcog_0=True)

    def _missingness_lateif(self) -> int:
        """Handles missingness for LATEIF."""
        return self.handle_cognitive_impairment_gate("late", "lateif", ignore_normcog_0=True)

    def _missingness_msaif(self) -> int:
        """Handles missingness for MSAIF."""
        return self.handle_cognitive_impairment_gate("msa", "msaif", ignore_normcog_0=True)

    def _missingness_pspif(self) -> int:
        """Handles missingness for PSPIF."""
        return self.handle_cognitive_impairment_gate("psp", "pspif", ignore_normcog_0=True)

    def _missingness_cortif(self) -> int:
        """Handles missingness for CORTIF."""
        return self.handle_cognitive_impairment_gate("cort", "cortif", ignore_normcog_0=True)

    def _missingness_ftldmoif(self) -> int:
        """Handles missingness for FTLDMOIF."""
        return self.handle_cognitive_impairment_gate("ftldmo", "ftldmoif", ignore_normcog_0=True)

    def _missingness_ftldnoif(self) -> int:
        """Handles missingness for FTLDNOIF."""
        return self.handle_cognitive_impairment_gate("ftldnos", "ftldnoif", ignore_normcog_0=True)

    def _missingness_ftldsubt(self) -> int:
        """Handles missingness for FTLDSUBT."""
        ftldsubt = self.uds.get_value("ftldsubt", int)
        if self.formver < 4:
            if ftldsubt is None:
                if self.normcog == 1:
                    return 8

                gates = self.uds.group_attributes(
                    ["psp", "cort", "ftldmo", "ftldnos"], int
                )
                if all(x == 0 for x in gates):
                    return INFORMED_MISSINGNESS

                if self.normcog == 0:
                    return 7
            else:
                return ftldsubt

        return self.handle_cognitive_impairment_gate(
            "ftld", "ftldsubt", ignore_normcog_0=True
        )

    def _missingness_cvdif(self) -> int:
        """Handles missingness for CVDIF."""
        return self.handle_cognitive_impairment_gate("cvd", "cvdif", ignore_normcog_0=True)

    def _missingness_downsif(self) -> int:
        """Handles missingness for DOWNSIF."""
        return self.handle_cognitive_impairment_gate("downs", "downsif", ignore_normcog_0=True)

    def _missingness_huntif(self) -> int:
        """Handles missingness for HUNTIF."""
        return self.handle_cognitive_impairment_gate("hunt", "huntif", ignore_normcog_0=True)

    def _missingness_prionif(self) -> int:
        """Handles missingness for PRIONIF."""
        return self.handle_cognitive_impairment_gate("prion", "prionif", ignore_normcog_0=True)

    def _missingness_othcogif(self) -> int:
        """Handles missingness for OTHCOGIF."""
        return self.handle_cognitive_impairment_gate("othcog", "othcogif", ignore_normcog_0=True)
