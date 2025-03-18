"""All cognitive MQT derived variables.

Assumes NACC-derived variables are already set
"""
from typing import Dict, List, Optional, Set

from nacc_attribute_deriver.attributes.base.base_attribute import MQTAttribute


class CognitiveAttribute(MQTAttribute):
    """Class to collect cognitive attributes."""

    NACCUDSD_MAPPING = {
        1: "Normal cognition",
        2: "Impaired-not-MCI",
        3: "MCI",
        4: "Dementia",
        5: "All of the above"
    }

    # several labels not consistent with DIAGNOSIS_MAPPINGS
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
        15: "Epilepsy",  # not consistent
        16: "CNS neoplasm",
        17: "Human immunodeficiency virus (HIV)",  # not consistent
        18: "Other neurological, genetic, or infection condition",
        19: "Depression",
        20: "Bipolar disorder",
        21: "Schizophrenia or other psychosis",
        22: "Anxiety disorder",  # not consistent
        23: "Delirium",
        24: "Post-traumatic stress disorder (PTSD)",  # not consistent
        25: "Other psychiatric disease",
        26: "Cognitive impairment due to alcohol abuse",  # not consistent
        27:
        "Cognitive impairment due to other substance abuse",  # not consistent
        28:  # not consistent
        "Cognitive impairment due to systemic disease or medical illness",
        29: "Cognitive impairment due to medications",  # not consistent
        30:  # not consistent
        "Cognitive impairment for other specified reasons (i.e., written-in values)",
        88:
        "Not applicable",  # no corresponding/not relevant to DIAGNOSIS_MAPPINGS
        99:
        "Missing/unknown"  # no corresponding/not relevant to DIAGNOSIS_MAPPINGS
    }

    # maps each diagnosis to their string value
    DIAGNOSIS_MAPPINGS = {
        'file.info.derived.': {
            'naccalzp': "Alzheimer’s disease (AD)",
            'nacclbdp': "Lewy body disease (LBD)"
        },
        'file.info.forms.json.': {
            'msaif': "Multiple system atrophy (MSA)",
            'pspif': "Primary supranuclear palsy (PSP)",
            'cortif': "Corticobasal degeneration (CBD)",
            'ftldmoif': "FTLD with motor neuron disease (MND)",
            'ftldnosif': "FTLD not otherwise specified (NOS)",
            'ftdif': "Behavioral frontotemporal dementia (bvFTD)",
            'ppaphif': "Primary progressive aphasia (PPA)",

            # vascular
            'cvdif': "Vascular brain injury",
            'vascif': "Probable vascular dementia (NINDS/AIREN criteria)",
            'vascpsif': "Possible vascular dementia (NINDS/AIREN criteria)",
            'strokeif': "Stroke",
            'esstreif': "Essential tremor",
            'downsif': "Down syndrome",
            'huntif': "Huntington’s disease",
            'prionif': "Prion disease (CJD, other)",
            'brninjif': "Traumatic brain injury (TBI)",
            'hycephif': "Normal-pressure hydrocephalus (NPH)",
            'epilepif': "Epilepsy Numeric longitudinal",
            'neopif': "CNS neoplasm",
            'hivif': "HIV",
            'othcogif': "Other neurological, genetic, or infection condition",
            'depif': "Depression",
            'bipoldif': "Bipolar disorder",
            'schizoif': "Schizophrenia or other psychosis",
            'anxietif': "Anxiety",
            'delirif': "Delirium",
            'ptsddxif': "PTSD",
            'othpsyif': "Other psychiatric disease",
            'alcdemif': "Alcohol abuse",
            'impsubif': "Other substance abuse",
            'dysillif': "Systemic disease/medical illness",
            'medsif': "Medications",
            'demunif': "Undetermined etiology",
            'cogothif': "Other",
            'cogoth2f': "Other",
            'cogoth3f': "Other"
        }
    }

    DEMENTIA_MAPPINGS = {
        'file.info.forms.json.': {
            'amndem':
            'Amnestic multidomain dementia syndrome',
            'pca':
            'Posterior cortical atrophy syndrome',
            'namndem':
            'Non-amnestic multidomain dementia, not PCA, PPA, bvFTD, or DLb syndrome',
        },
        'file.info.derived.': {
            'naccppa':
            'Primary progressive aphasia (PPA) with cognitive impairment',
            'naccbvft': 'Behavioral variant FTD syndrome (bvFTD)',
            'nacclbds': 'Lewy body dementia syndrome',
        }
    }

    def grab_mappings(self, mapping: Dict[str, Dict[str, str]],
                      target: int) -> List[str]:
        """Grab mappings."""
        mapped_vars: Set[str] = set()

        for prefix, fields in mapping.items():
            aggr = self.aggregate_variables(list(fields.keys()), prefix=prefix)
            mapped_vars = mapped_vars.union(
                set([
                    mapping[prefix][k] for k, v in aggr.items()
                    if self.is_int_value(v, target)
                ]))

        return list(mapped_vars)

    def _create_contributing_diagnosis(self) -> List[str]:
        """Mapped from all possible contributing diagnosis."""
        self.assert_required(['naccalzp', 'nacclbdp'])
        return self.grab_mappings(self.DIAGNOSIS_MAPPINGS, target=2)

    def _create_dementia(self) -> List[str]:
        """Mapped from all dementia types."""
        self.assert_required(['naccppa', 'naccbvft', 'nacclbds'])
        results = self.grab_mappings(self.DEMENTIA_MAPPINGS, target=1)
        return results

    def _create_cognitive_status(self) -> Optional[str]:
        """Mapped from NACCUDSD."""
        result = self.assert_required(['naccudsd'])
        return self.NACCUDSD_MAPPING.get(result['naccudsd'], None)

    def _create_etpr(self) -> str:
        """Mapped from NACCETPR."""
        result = self.assert_required(['naccetpr'])
        return self.PRIMARY_DIAGNOSIS_MAPPINGS.get(result['naccetpr'],
                                                   "Missing/unknown")

    def _create_global_cdr(self) -> Optional[str]:
        """Mapped from CDRGLOB."""
        cdrglob = self.get_value('cdrglob')
        return str(cdrglob) if cdrglob else None

    def _create_normal_cognition(self) -> bool:
        """Mapped from NACCNORM."""
        result = self.assert_required(['naccnorm'])
        return bool(result['naccnorm'])
