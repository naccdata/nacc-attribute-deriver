"""All cognitive MQT derived variables.

Assumes NACC-derived variables are already set
"""

from types import MappingProxyType
from typing import List, Mapping

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import (
    DateTaggedValue,
    DerivedNamespace,
)
from nacc_attribute_deriver.attributes.base.uds_namespace import (
    UDSNamespace,
)
from nacc_attribute_deriver.symbol_table import SymbolTable


class CognitiveAttributeCollection(AttributeCollection):
    """Class to collect cognitive attributes."""

    def __init__(self, table: SymbolTable):
        self.__uds = UDSNamespace(
            table,
            required=frozenset(
                [
                    "cdrglob",
                ]
            ),
        )
        self.__derived = DerivedNamespace(
            table=table,
            required=frozenset(
                [
                    "naccalzp",
                    "nacclbdp",
                    "naccppa",
                    "naccbvft",
                    "nacclbds",
                    "naccudsd",
                    "naccetpr",
                ]
            ),
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

    def __filter_attributes(
        self, attributes: List[str], expected_value: int
    ) -> List[str]:
        """Returns a list of the attributes that have the expected value.

        Args:
          attributes: the list of attributes to filter
          expected_value: the value to test against in filtering
        Returns:
          the list of attributes whose value matches the expected_value. can be empty
        """
        attribute_list: List[str] = []
        for attribute in attributes:
            value = self.__uds.get_value(attribute, int)
            if not value:
                value = self.__derived.get_value(attribute, int)
            if not value:
                continue

            if not self.is_target_int(value, expected_value):
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
        return DateTaggedValue(
            value=self.map_attributes(self.DIAGNOSIS_MAPPINGS, expected_value=2),
            date=self.__uds.get_date(),
        )

    def _create_dementia(self) -> DateTaggedValue[List[str]]:
        """Mapped from all dementia types."""
        return DateTaggedValue(
            value=self.map_attributes(self.DEMENTIA_MAPPINGS, expected_value=1),
            date=self.__uds.get_date(),
        )

    def _create_cognitive_status(self) -> DateTaggedValue[int]:
        """Mapped from NACCUDSD."""
        return DateTaggedValue(
            value=self.__derived.get_required("naccudsd", int),
            date=self.__uds.get_date(),
        )

    def _create_etpr(self) -> DateTaggedValue[int]:
        """Mapped from NACCETPR."""
        return DateTaggedValue(
            value=self.__derived.get_required("naccetpr", int),
            date=self.__uds.get_date(),
        )

    def _create_global_cdr(self) -> DateTaggedValue[float]:
        """Mapped from CDRGLOB."""
        return DateTaggedValue(
            value=self.__uds.get_required("cdrglob", float), date=self.__uds.get_date()
        )
