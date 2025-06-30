"""Tests deriving MQT demographics variables."""

import pytest
from nacc_attribute_deriver.attributes.mqt.demographics import (
    DemographicsAttributeCollection,
    DerivedDemographicsAttributeCollection,
)
from nacc_attribute_deriver.schema.errors import InvalidFieldError
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {  # needed for DemographicsAttributeCollection
                        "sex": "1",
                        "primlang": "2",
                        "visitdate": "2025-01-01",
                        "module": "uds",
                        "packet": "I",
                        "birthmo": 1,
                        "birthyr": 1950,
                        "formver": 3.0,
                    }
                }
            }
        },
        "subject": {  # needed for DerivedDemographicsAttributeCollection
            "info": {
                "derived": {
                    "np_death_age": 80,
                    "cross-sectional": {
                        "naccnihr": 1,
                        "naccdage": 80,
                        "naccdied": 1,
                    },
                }
            }
        },
    }

    return SymbolTable(data)


class TestDemographicsAttributeCollection:
    def test_create_uds_sex(self, table):
        """Tests _create_uds_sex."""
        attr = DemographicsAttributeCollection(table)
        assert attr._create_uds_sex() == "Male"

        for k, v in DemographicsAttributeCollection.SEX_MAPPING.items():
            table["file.info.forms.json.sex"] = k
            assert attr._create_uds_sex() == v

        # none case
        table["file.info.forms.json.sex"] = None
        with pytest.raises(InvalidFieldError):
            assert attr._create_uds_sex() is None

    def test_create_uds_primary_language(self, table):
        """Tests _create_uds_primary_language."""
        attr = DemographicsAttributeCollection(table)
        assert attr._create_uds_primary_language() == "Spanish"

        for k, v in DemographicsAttributeCollection.PRIMARY_LANGUAGE_MAPPING.items():
            table["file.info.forms.json.primlang"] = k
            assert attr._create_uds_primary_language() == v

        # test None in both initial and followup packet case
        table["file.info.forms.json.primlang"] = None
        with pytest.raises(InvalidFieldError):
            attr._create_uds_primary_language()

        table["file.info.forms.json.primlang"] = 9
        table["file.info.forms.json.packet"] = "F"
        assert attr._create_uds_primary_language() is None


class TestDerivedDemographicsAttributeCollection:
    def test_create_uds_race(self, table):
        """Tests _create_uds_race."""
        attr = DerivedDemographicsAttributeCollection(table)
        assert attr._create_uds_race() == "White"

        for k, v in DerivedDemographicsAttributeCollection.RACE_MAPPING.items():
            table["subject.info.derived.cross-sectional.naccnihr"] = k
            assert attr._create_uds_race() == v

    def test_create_age_at_death(self, table):
        """Tests _create_age_at_death."""
        attr = DerivedDemographicsAttributeCollection(table)
        assert attr._create_age_at_death() == 80

    def test_create_vital_status(self, table):
        """Tests _create_vital_status."""
        attr = DerivedDemographicsAttributeCollection(table)
        assert attr._create_vital_status() == "deceased"

        for (
            k,
            v,
        ) in DerivedDemographicsAttributeCollection.VITAL_STATUS_MAPPINGS.items():
            table["subject.info.derived.cross-sectional.naccdied"] = k
            assert attr._create_vital_status() == v

    def test_create_np_available(self, table):
        """Tests _create_np_available."""
        attr = DerivedDemographicsAttributeCollection(table)
        assert attr._create_np_available()

        # none case
        table["subject.info.derived.np_death_age"] = None
        assert not attr._create_np_available()
