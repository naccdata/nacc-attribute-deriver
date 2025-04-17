"""Defines the scopes for curation."""

from enum import Enum
from typing import Literal


class Scope(str, Enum):
    pass


class FormScope(Scope):
    # forms
    MDS = "mds"
    MILESTONE = "milestone"
    NP = "np"
    UDS = "uds"


class GeneticsScope(Scope):
    # genetics
    APOE = "apoe"
    NIAGADS_AVAILABILITY = "niagads_availability"
    NCRAD_SAMPLES = "ncrad_samples"


class SCANPETScope(Scope):
    # SCAN - PET
    PET_QC = "scan_pet_qc"
    AMYLOID_PET_GAAIN = "scan_amyloid_pet_gaain"
    AMYLOID_PET_NPDKA = "scan_amyloid_pet_npdka"
    FDG_PET_NPDKA = "scan_fdg_pet_npdka"
    TAU_PET_NPDKA = "scan_tau_pet_npdka"


class SCANMRIScope(Scope):
    # SCAN - MRI
    MRI_QC = "scan_mri_qc"
    MRI_SBM = "scan_mri_sbm"


ScopeLiterals = Literal[
    FormScope.MDS,
    FormScope.MILESTONE,
    FormScope.NP,
    FormScope.UDS,
    GeneticsScope.APOE,
    GeneticsScope.NIAGADS_AVAILABILITY,
    GeneticsScope.NCRAD_SAMPLES,
    SCANPETScope.PET_QC,
    SCANPETScope.AMYLOID_PET_GAAIN,
    SCANPETScope.AMYLOID_PET_NPDKA,
    SCANPETScope.FDG_PET_NPDKA,
    SCANPETScope.TAU_PET_NPDKA,
    SCANMRIScope.MRI_QC,
    SCANMRIScope.MRI_SBM,
]
