"""
All cognitive MQT derived variables.
Assumes NACC-derived variables are already set
"""
from typing import List
from nacc_attribute_deriver.attributes.utils.utils import (
    aggregate_variables,
    assert_required,
    is_int_value,
)
from nacc_attribute_deriver.attributes.nacc.forms.uds.form_d1 import (
    ContributionStatus)
from nacc_attribute_deriver.symbol_table import SymbolTable

#############################
# Helper functions/mappings #
#############################

NACCUDSD_MAPPING = {
    1: "Normal cognition",
    2: "Impaired-not-MCI",
    3: "MCI",
    4: "Dementia",
    5: "All of the above"
}

PRIMARY_DIAGNOSIS_MAPPINGS = {
    1: "Alzheimer’s disease (AD)",
    2: "Lewy body disease (LBD)",

    3: "Multiple system atrophy (MSA)",
    4: "Progressive supranuclear palsy (PSP)",
    5: "Corticobasal degeneration (CBD)",
    6: "FTLD with motor neuron disease (e.g., ALS)",
    7: "FTLD, other",
    8: "Vascular brain injury or vascular dementia including stroke",

    9: "Essential tremor",
    10: "Down syndrome",
    11: "Huntington’s disease",
    12: "Prion disease (CJD, other)",
    13: "Traumatic brain injury (TBI)",
    14: "Normal-pressure hydrocephalus (NPH)",
    15: "Epilepsy",  # label not consistent with DIAGNOSIS_MAPPINGS
    16: "CNS neoplasm",
    17: "Human immunodeficiency virus (HIV)",  # label not consistent with DIAGNOSIS_MAPPINGS
    18: "Other neurological, genetic, or infection condition",

    19: "Depression",
    20: "Bipolar disorder",
    21: "Schizophrenia or other psychosis",
    22: "Anxiety disorder",  # label not consistent with DIAGNOSIS_MAPPINGS
    23: "Delirium",
    24: "Post-traumatic stress disorder (PTSD)",  # label not consistent with DIAGNOSIS_MAPPINGS
    25: "Other psychiatric disease",

    26: "Cognitive impairment due to alcohol abuse",  # label not consistent with DIAGNOSIS_MAPPINGS
    27: "Cognitive impairment due to other substance abuse",  # label not consistent with DIAGNOSIS_MAPPINGS
    28: "Cognitive impairment due to systemic disease or medical illness", # label not consistent with DIAGNOSIS_MAPPINGS
    29: "Cognitive impairment due to medications",  # label not consistent with DIAGNOSIS_MAPPINGS
    30: "Cognitive impairment for other specified reasons (i.e., written-in values)",  # label not consistent with DIAGNOSIS_MAPPINGS
    88: "Not applicable",  # no corresponding/not relevant to DIAGNOSIS_MAPPINGS
    99: "Missing/unknown"  # no corresponding/not relevant to DIAGNOSIS_MAPPINGS
}

# maps each diagnosis to their string value
DIAGNOSIS_MAPPINGS = {
    'file.info.derived.naccalzp': "Alzheimer’s disease (AD)",
    'file.info.derived.nacclbdp': "Lewy body disease (LBD)",

    'file.info.forms.json.msaif': "Multiple system atrophy (MSA)",
    'file.info.forms.json.pspif': "Primary supranuclear palsy (PSP)",
    'file.info.forms.json.cortif': "Corticobasal degeneration (CBD)",
    'file.info.forms.json.ftldmoif': "FTLD with motor neuron disease (MND)",
    'file.info.forms.json.ftldnosif': "FTLD not otherwise specified (NOS)",
    'file.info.forms.json.ftdif': "Behavioral frontotemporal dementia (bvFTD)",
    'file.info.forms.json.ppaphif': "Primary progressive aphasia (PPA)",

    # vascular
    'file.info.forms.json.cvdif': "Vascular brain injury",
    'file.info.forms.json.vascif': "Probable vascular dementia (NINDS/AIREN criteria)",
    'file.info.forms.json.vascpsif': "Possible vascular dementia (NINDS/AIREN criteria)",
    'file.info.forms.json.strokeif': "Stroke",

    'file.info.forms.json.esstreif': "Essential tremor",
    'file.info.forms.json.downsif': "Down syndrome",
    'file.info.forms.json.huntif': "Huntington’s disease",
    'file.info.forms.json.prionif': "Prion disease (CJD, other)",
    'file.info.forms.json.brninjif': "Traumatic brain injury (TBI)",
    'file.info.forms.json.hycephif': "Normal-pressure hydrocephalus (NPH)",
    'file.info.forms.json.epilepif': "Epilepsy Numeric longitudinal",
    'file.info.forms.json.neopif': "CNS neoplasm",
    'file.info.forms.json.hivif': "HIV",
    'file.info.forms.json.othcogif': "Other neurological, genetic, or infection condition",

    'file.info.forms.json.depif': "Depression",
    'file.info.forms.json.bipoldif': "Bipolar disorder",
    'file.info.forms.json.schizoif': "Schizophrenia or other psychosis",
    'file.info.forms.json.anxietif': "Anxiety",
    'file.info.forms.json.delirif': "Delirium",
    'file.info.forms.json.ptsddxif': "PTSD",
    'file.info.forms.json.othpsyif': "Other psychiatric disease",

    'file.info.forms.json.alcdemif': "Alcohol abuse",
    'file.info.forms.json.impsubif': "Other substance abuse",
    'file.info.forms.json.dysillif': "Systemic disease/medical illness",
    'file.info.forms.json.medsif': "Medications",
    'file.info.forms.json.demunif': "Undetermined etiology",
    'file.info.forms.json.cogothif': "Other",
    'file.info.forms.json.cogoth2f': "Other",
    'file.info.forms.json.cogoth3f': "Other"
}

DEMENTIA_MAPPINGS = {
    'file.info.forms.json.amndem': 'Amnestic multidomain dementia syndrome',
    'file.info.forms.json.pca': 'Posterior cortical atrophy syndrome',
    'file.info.forms.json.namndem': 'Non-amnestic multidomain dementia, not PCA, PPA, bvFTD, or DLb syndrome',

    'file.info.derived.naccppa': 'Primary progressive aphasia (PPA) with cognitive impairment',
    'file.info.derived.naccbvft': 'Behavioral variant FTD syndrome (bvFTD)',
    'file.info.derived.nacclbds': 'Lewy body dementia syndrome',
}

#########################
# MQT Derived variables #
#########################

def _create_contributing_diagnosis(table: SymbolTable) -> List[str]:
    """Mapped from all possible contributing diagnosis.

    Location:
        subject.info.cognitive.uds.other-diagnosis.initial
        subject.info.cognitive.uds.other-diagnosis.latest
    Event:
        initial
        latest
    Type:
        cognitive
    Description:
        Contributing etiological diagnosis 
    """
    assert_required('create_contributing_diagnosis', ['naccalzp', 'nacclbdp'], table)

    all_vars = aggregate_variables(DIAGNOSIS_MAPPINGS, table)
    contr_diagnosis = set([
        DIAGNOSIS_MAPPINGS[k] for k, v in all_vars.items()
        if is_int_value(v, ContributionStatus.CONTRIBUTING)
    ])
    # needs to check against latest
    return list(contr_diagnosis)


def _create_cognitive_status(table: SymbolTable) -> str:
    """Mapped from NACCUDSD

    Location:
        subject.info.cognitive.uds.cognitive-status.initial
        subject.info.cognitive.uds.cognitive-status.latest
    Event:
        initial
        latest
    Type:
        cognitive
    Description:
        Cognitive Status
    """
    result = assert_required('create_cognitive_status', ['naccudsd'], table)
    return NACCUDSD_MAPPING.get(result['naccudsd'], None)


def _create_etpr(table: SymbolTable) -> str:
    """Mapped from NACCETPR

    Location:
        subject.info.cognitive.uds.etpr.initial
        subject.info.cognitive.uds.etpr.latest
        subject.info.cognitive.uds.etpr.all
    Event:
        initial
        latest
        set
    Type:
        cognitive
    Description:
        Primary etiologic diagnosis
    """
    result = assert_required('create_etpr', ['naccetpr'], table)
    return PRIMARY_DIAGNOSIS_MAPPINGS.get(result['naccetpr'], "Missing/unknown")


def _create_global_cdr(table: SymbolTable) -> str:
    """Mapped from CDRGLOB

    Location:
        subject.info.cognitive.uds.cdrglob.initial
        subject.info.cognitive.uds.cdrglob.latest
        subject.info.cognitive.uds.cdrglob.all
    Event:
        initial
        latest
        set
    Type:
        cognitive
    Description:
        Global CDR
    """
    cdrglob = table.get('file.info.forms.json.cdrglob')
    return str(cdrglob) if cdrglob else None


def _create_dementia(table: SymbolTable) -> List[str]:
    """Mapped from all dementia types

    TODO: initial/latest were set as a single instead
        of set, is there a priority?

    Location:
        subject.info.cognitive.uds.dementia-type.initial
        subject.info.cognitive.uds.dementia-type.latest
        subject.info.cognitive.uds.dementia-type.all
    Event:
        initial
        latest
        set
    Type:
        cognitive
    Description:
        Type of Dementia syndrome
    """
    assert_required('create_dementia', ['naccppa', 'naccbvft', 'nacclbds'], table)
    all_vars = aggregate_variables(DEMENTIA_MAPPINGS, table)

    # collect if == 1 (Present/Yes)
    dementia_types = set([
        DEMENTIA_MAPPINGS[k] for k, v in all_vars.items()
        if is_int_value(v, 1)
    ])

    return list(dementia_types)


def _create_normal_cognition(table: SymbolTable) -> bool:
    """Mapped from NACCNORM

    Location:
        subject.info.derived.naccnorm
    Event:
        max
    Type:
        cognitive
    Description:
        Normal Cognition
    """
    assert_required('create_normal_cognition', ['naccnorm'], table)
    return bool(table.get('file.info.derived.naccnorm'))
