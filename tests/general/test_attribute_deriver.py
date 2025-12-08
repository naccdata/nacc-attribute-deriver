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
        assert self.__extract_attributes(attr.get_curation_rules("mds"), 6) == {
            "subject.info.derived.cross-sectional.naccmdss",
            "subject.info.working.cross-sectional.mds-death-date",
            "subject.info.working.cross-sectional.mds-death-month",
            "subject.info.working.cross-sectional.mds-vital-status",
            "subject.info.working.cross-sectional.mds-source",
            "subject.info.derived.affiliate",
        }

    def test_get_curation_rules_apoe(self):
        """APOE/NCRAD namespaces."""
        attr = AttributeDeriver()

        assert self.__extract_attributes(attr.get_curation_rules("apoe"), 4) == {
            "subject.info.derived.cross-sectional.naccapoe",
            "subject.info.derived.cross-sectional.naccne4s",
            "file.info.derived.naccapoe",
            "file.info.derived.naccne4s",
        }

        assert self.__extract_attributes(
            attr.get_curation_rules("historic_apoe"), 3
        ) == {
            "subject.info.derived.cross-sectional.naccapoe",
            "subject.info.working.cross-sectional.historic-apoe",
            "subject.info.derived.cross-sectional.naccne4s",
        }
