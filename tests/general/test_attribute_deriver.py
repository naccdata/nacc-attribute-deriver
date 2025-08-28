"""Tests the AttributeDeriver."""

from typing import List, Set

from nacc_attribute_deriver.attribute_deriver import AttributeDeriver
from nacc_attribute_deriver.schema.schema import CurationRule


class TestAttributeDeriver:
    def __extract_attributes(
        self, curation_rules: List[CurationRule], exp_length: int
    ) -> Set[str]:
        """Extracts the attributes.

        Args:
            curation_rules: The CurationRules
            exp_length: The expected length of extracted attributes
        Returns:
            List of attributes (locations)
        """
        attributes = set()
        for rule in curation_rules:
            for assignment in rule.assignments:
                attributes.add(assignment.attribute)

        assert len(attributes) == exp_length
        return attributes

    def test_get_curation_rules_simple(self):
        """Simple straightforward cases."""
        attr = AttributeDeriver()

        # invalid case
        assert attr.get_curation_rules("invalid") is None

        # mds case - each rule maps to an unique attribute
        assert self.__extract_attributes(attr.get_curation_rules("mds"), 3) == {
            "subject.info.derived.mds_death_date",
            "subject.info.derived.mds_death_month",
            "subject.info.derived.mds_vital_status",
        }

    def test_get_curation_rules_apoe(self):
        """APOE namespaces; both have a single rule that maps to the same 2
        attributes."""
        attr = AttributeDeriver()

        assert self.__extract_attributes(attr.get_curation_rules("apoe"), 2) == {
            "subject.info.derived.cross-sectional.naccapoe",
            "subject.info.genetics.apoe",
        }

        assert self.__extract_attributes(
            attr.get_curation_rules("historic_apoe"), 2
        ) == {
            "subject.info.derived.cross-sectional.naccapoe",
            "subject.info.genetics.apoe",
        }
