"""All cognitive MQT derived variables.

Assumes NACC-derived variables are already set
"""

from types import MappingProxyType
from typing import List, Mapping, Optional

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    DateTaggedValue,
    DerivedNamespace,
)
from nacc_attribute_deriver.attributes.nacc.modules.uds.uds_namespace import (
    UDSNamespace,
)


class CognitiveAttributeCollection(AttributeCollection):
    """Class to collect cognitive attributes."""

    def __init__(self, table):
        self.__uds = UDSNamespace(table)
        self.__derived = DerivedNamespace(table, date_attribute="visitdate")

    # several labels not consistent with DIAGNOSIS_MAPPINGS
    PRIMARY_DIAGNOSIS_MAPPINGS = MappingProxyType(
        {
            1: "Alzheimer\u0027s disease (AD)",
            2: "Lewy body disease (LBD)",
            3: "Multiple system atrophy (MSA)",
            4: "Progressive supranuclear palsy (PSP)",
            5: "Corticobasal degeneration (CBD)",
            6: "FTLD with motor neuron disease (e.g., ALS)",
            7: "FTLD, other",
            8: "Vascular brain injury or vascular dementia including stroke",
            9: "Essential tremor",
            10: "Down syndrome",
            11: "Huntington\u0027s disease",
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
            27: "Cognitive impairment due to other substance abuse",  # not consistent
            28:  # not consistent
            "Cognitive impairment due to systemic disease or medical illness",
            29: "Cognitive impairment due to medications",  # not consistent
            30:  # not consistent
            (
                "Cognitive impairment for other "
                "specified reasons (i.e., written-in values)"
            ),
            88: "Not applicable",  # no corresponding value in DIAGNOSIS_MAPPINGS
            99: "Missing/unknown",  # no corresponding value in DIAGNOSIS_MAPPINGS
        }
    )

    # maps each diagnosis to their string value
    DIAGNOSIS_MAPPINGS = MappingProxyType(
        {
            "naccalzp": "Alzheimer\u0027s disease (AD)",
            "nacclbdp": "Lewy body disease (LBD)",
            "msaif": "Multiple system atrophy (MSA)",
            "pspif": "Primary supranuclear palsy (PSP)",
            "cortif": "Corticobasal degeneration (CBD)",
            "ftldmoif": "FTLD with motor neuron disease (MND)",
            "ftldnosif": "FTLD not otherwise specified (NOS)",
            "ftdif": "Behavioral frontotemporal dementia (bvFTD)",
            "ppaphif": "Primary progressive aphasia (PPA)",
            # vascular
            "cvdif": "Vascular brain injury",
            "vascif": "Probable vascular dementia (NINDS/AIREN criteria)",
            "vascpsif": "Possible vascular dementia (NINDS/AIREN criteria)",
            "strokeif": "Stroke",
            "esstreif": "Essential tremor",
            "downsif": "Down syndrome",
            "huntif": "Huntington\u0027s disease",
            "prionif": "Prion disease (CJD, other)",
            "brninjif": "Traumatic brain injury (TBI)",
            "hycephif": "Normal-pressure hydrocephalus (NPH)",
            "epilepif": "Epilepsy Numeric longitudinal",
            "neopif": "CNS neoplasm",
            "hivif": "HIV",
            "othcogif": "Other neurological, genetic, or infection condition",
            "depif": "Depression",
            "bipoldif": "Bipolar disorder",
            "schizoif": "Schizophrenia or other psychosis",
            "anxietif": "Anxiety",
            "delirif": "Delirium",
            "ptsddxif": "PTSD",
            "othpsyif": "Other psychiatric disease",
            "alcdemif": "Alcohol abuse",
            "impsubif": "Other substance abuse",
            "dysillif": "Systemic disease/medical illness",
            "medsif": "Medications",
            "demunif": "Undetermined etiology",
            "cogothif": "Other",
            "cogoth2f": "Other",
            "cogoth3f": "Other",
        }
    )

    DEMENTIA_MAPPINGS = MappingProxyType(
        {
            "amndem": "Amnestic multidomain dementia syndrome",
            "pca": "Posterior cortical atrophy syndrome",
            "namndem": (
                "Non-amnestic multidomain dementia, "
                "not PCA, PPA, bvFTD, or DLb syndrome"
            ),
            "naccppa": "Primary progressive aphasia (PPA) with cognitive impairment",
            "naccbvft": "Behavioral variant FTD syndrome (bvFTD)",
            "nacclbds": "Lewy body dementia syndrome",
        }
    )

    def __filter_attributes(self, attributes: List[str], expected_value: int):
        """Returns a list of the attributes that have the expected value.

        Args:
          attributes: the list of attributes to filter
          expected_value: the value to test against in filtering
        Returns:
          the list of attributes whose value matches the expected_value
        """
        attribute_list: List[str] = []
        for attribute in attributes:
            value = self.__uds.get_value(attribute)
            if not value:
                value = self.__derived.get_value(attribute)
            if not value:
                continue

            if not self.is_int_value(value, expected_value):
                continue

            attribute_list.append(attribute)

        return attribute_list

    def map_attributes(
        self, mapping: Mapping[str, str], expected_value: int
    ) -> List[str]:
        """Returns the list of string values for the attributes in the mapping
        for which the value matches the expected value.

        Args:
          mapping: the attribute mapping
          expected_value: the expected value to test for
        Returns:
          the list of string values from the attribute mapping for attributes
          with the expected value
        """
        attributes = self.__filter_attributes(
            attributes=list(mapping.keys()), expected_value=expected_value
        )
        return list({mapping[attribute] for attribute in attributes})

    def _create_contributing_diagnosis(self) -> DateTaggedValue[List[str]]:
        """Mapped from all possible contributing diagnosis."""
        self.__derived.assert_required(["naccalzp", "nacclbdp"])
        return DateTaggedValue(
            value=self.map_attributes(self.DIAGNOSIS_MAPPINGS, expected_value=2),
            date=self.__uds.get_date(),
        )

    def _create_dementia(self) -> DateTaggedValue[List[str]]:
        """Mapped from all dementia types."""
        self.__derived.assert_required(["naccppa", "naccbvft", "nacclbds"])
        return DateTaggedValue(
            value=self.map_attributes(self.DEMENTIA_MAPPINGS, expected_value=1),
            date=self.__uds.get_date(),
        )

    def _create_cognitive_status(self) -> DateTaggedValue[Optional[int]]:
        """Mapped from NACCUDSD."""
        self.__derived.assert_required(["naccudsd"])
        cognitive_status = self.__derived.get_value("naccudsd")

        return DateTaggedValue(
            value=cognitive_status,
            date=self.__uds.get_date(),
        )

    def _create_etpr(self) -> DateTaggedValue[str]:
        """Mapped from NACCETPR."""
        self.__derived.assert_required(["naccetpr"])
        return DateTaggedValue(
            value=self.PRIMARY_DIAGNOSIS_MAPPINGS.get(
                self.__derived.get_value("naccetpr"), "Missing/unknown"
            ),
            date=self.__uds.get_date(),
        )

    def _create_global_cdr(self) -> Optional[DateTaggedValue[float]]:
        """Mapped from CDRGLOB."""
        cdrglob = self.__uds.get_value("cdrglob")

        return DateTaggedValue(value=cdrglob, date=self.__uds.get_date())

    def _create_normal_cognition(self) -> bool:
        """Mapped from NACCNORM."""
        self.__derived.assert_required(["naccnorm"])
        return bool(self.__derived.get_value("naccnorm"))
