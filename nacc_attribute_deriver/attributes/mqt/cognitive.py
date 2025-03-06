"""All cognitive MQT derived variables.

Assumes NACC-derived variables are already set
"""
from typing import Dict, List, Optional

from nacc_attribute_deriver.attributes.attribute_collection import MQTAttribute


class CognitiveAttribute(MQTAttribute):
    """Class to collect cognitive attributes."""

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
        17:
        "Human immunodeficiency virus (HIV)",  # label not consistent with DIAGNOSIS_MAPPINGS
        18: "Other neurological, genetic, or infection condition",
        19: "Depression",
        20: "Bipolar disorder",
        21: "Schizophrenia or other psychosis",
        22: "Anxiety disorder",  # label not consistent with DIAGNOSIS_MAPPINGS
        23: "Delirium",
        24:
        "Post-traumatic stress disorder (PTSD)",  # label not consistent with DIAGNOSIS_MAPPINGS
        25: "Other psychiatric disease",
        26:
        "Cognitive impairment due to alcohol abuse",  # label not consistent with DIAGNOSIS_MAPPINGS
        27:
        "Cognitive impairment due to other substance abuse",  # label not consistent with DIAGNOSIS_MAPPINGS
        28:
        "Cognitive impairment due to systemic disease or medical illness",  # label not consistent with DIAGNOSIS_MAPPINGS
        29:
        "Cognitive impairment due to medications",  # label not consistent with DIAGNOSIS_MAPPINGS
        30:
        "Cognitive impairment for other specified reasons (i.e., written-in values)",  # label not consistent with DIAGNOSIS_MAPPINGS
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
        mapped_vars = set()

        for prefix, fields in mapping.items():
            aggr = self.aggregate_variables(fields, prefix=prefix)
            mapped_vars = mapped_vars.union(
                set([
                    mapping[prefix][k] for k, v in aggr.items()
                    if self.is_int_value(v, target)
                ]))

        return list(mapped_vars)

    def _create_contributing_diagnosis(self) -> List[str]:
        """Mapped from all possible contributing diagnosis.

        Location:
            subject.info.cognitive.uds.other-diagnosis.initial
            subject.info.cognitive.uds.other-diagnosis.latest
            subject.info.cognitive.uds.other-diagnosis.all
        Operation:
            initial
            latest
            set
        Type:
            cognitive
        Description:
            Contributing etiological diagnosis
        """
        self.assert_required(['naccalzp', 'nacclbdp'])
        return self.grab_mappings(self.DIAGNOSIS_MAPPINGS, target=2)

    def _create_dementia(self) -> Optional[str]:
        """Mapped from all dementia types.

        Location:
            subject.info.cognitive.uds.dementia-type.initial
            subject.info.cognitive.uds.dementia-type.latest
            subject.info.cognitive.uds.dementia-type.all
        Operation:
            initial
            latest
            set
        Type:
            cognitive
        Description:
            Type of Dementia syndrome
        """
        self.assert_required(['naccppa', 'naccbvft', 'nacclbds'])
        results = self.grab_mappings(self.DEMENTIA_MAPPINGS, target=1)

        if len(results) > 1:
            raise ValueError(
                f"More than one primary dementia syndrome found: {results}")

        return results[0] if results else None

    def _create_cognitive_status(self) -> str:
        """Mapped from NACCUDSD.

        Location:
            subject.info.cognitive.uds.cognitive-status.initial
            subject.info.cognitive.uds.cognitive-status.latest
            subject.info.cognitive.uds.cognitive-status.all
        Operation:
            initial
            latest
            set
        Type:
            cognitive
        Description:
            Cognitive Status
        """
        result = self.assert_required(['naccudsd'])
        return self.NACCUDSD_MAPPING.get(result['naccudsd'], None)

    def _create_etpr(self) -> str:
        """Mapped from NACCETPR.

        Location:
            subject.info.cognitive.uds.etpr.initial
            subject.info.cognitive.uds.etpr.latest
            subject.info.cognitive.uds.etpr.all
        Operation:
            initial
            latest
            set
        Type:
            cognitive
        Description:
            Primary etiologic diagnosis
        """
        result = self.assert_required(['naccetpr'])
        return self.PRIMARY_DIAGNOSIS_MAPPINGS.get(result['naccetpr'],
                                                   "Missing/unknown")

    def _create_global_cdr(self) -> str:
        """Mapped from CDRGLOB.

        Location:
            subject.info.cognitive.uds.cdrglob.initial
            subject.info.cognitive.uds.cdrglob.latest
            subject.info.cognitive.uds.cdrglob.all
        Operation:
            initial
            latest
            set
        Type:
            cognitive
        Description:
            Global CDR
        """
        cdrglob = self.get_value('cdrglob')
        return str(cdrglob) if cdrglob else None

    def _create_normal_cognition(self) -> bool:
        """Mapped from NACCNORM.

        Location:
            subject.info.derived.naccnorm
        Operation:
            min
        Type:
            cognitive
        Description:
            Normal Cognition
        """
        result = self.assert_required(['naccnorm'])
        return bool(result['naccnorm'])
