"""Tests deriving MQT cognitive variables."""

import pytest
from nacc_attribute_deriver.attributes.mqt.cognitive import CognitiveAttributeCollection
from nacc_attribute_deriver.schema.errors import MissingRequiredError
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope="function")
def table() -> SymbolTable:
    """Create dummy data and return it in an attribute object."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "normcog": 0,
                        "msaif": 1,
                        "pspif": 2,
                        "cortif": 2,
                        "ftldmoif": 2,
                        "ftldnosif": 3,
                        "ftdif": 3,
                        "ppaphif": 3,
                        "cvdif": 2,
                        "vascif": 3,
                        "vascpsif": 3,
                        "strokeif": 3,
                        "amndem": 0,
                        "pca": 0,
                        "namndem": None,
                        "cdrglob": 0.5,
                        "module": "uds",
                        "visitdate": "2025-01-10",
                        "birthyr": 1950,
                        "birthmo": 1,
                        "packet": "I",
                        "formver": "3.0",
                        "naccid": "NACC123456",
                        "adcid": 0,
                        # rest of fields will be None
                    }
                },
                "derived": {
                    "naccalzp": 7,
                    "nacclbde": 8,
                    "nacclbdp": 8,
                    "naccppa": 8,
                    "naccbvft": 8,
                    "nacclbds": 1,
                    "naccnorm": 0,
                    "naccetpr": 99,
                    "naccudsd": 1,
                },
            }
        }
    }

    return SymbolTable(data)


class TestCognitiveAttributeCollection:
    def test_contributing_diagnosis(self, table):
        """Tests _create_contributing_diagnosis."""
        expected_values = []
        for field in ["pspif", "cortif", "ftldmoif", "cvdif"]:  # all == 2
            expected_values.append(
                CognitiveAttributeCollection.DIAGNOSIS_MAPPINGS[field]
            )

        attr = CognitiveAttributeCollection(table)
        assert set(attr._create_contributing_diagnosis()) == set(expected_values)

    def test_dementia(self, table):
        """Tests _create_dementia."""
        attr = CognitiveAttributeCollection(table)
        assert attr._create_dementia() == [
            CognitiveAttributeCollection.DEMENTIA_MAPPINGS["nacclbds"]
        ]

        # test multiple
        table["file.info.forms.json.amndem"] = 1
        table["file.info.forms.json.pca"] = 1

        attr = CognitiveAttributeCollection(table)

        assert set(attr._create_dementia()) == set(
            [
                CognitiveAttributeCollection.DEMENTIA_MAPPINGS["amndem"],
                CognitiveAttributeCollection.DEMENTIA_MAPPINGS["pca"],
                CognitiveAttributeCollection.DEMENTIA_MAPPINGS["nacclbds"],
            ]
        )

    def test_global_cdr(self, table):
        """Tests _create_global_cdr, which just comes from CDRGLOB as a
        string."""
        attr = CognitiveAttributeCollection(table)
        assert attr._create_global_cdr() == 0.5

        table["file.info.forms.json.cdrglob"] = None
        with pytest.raises(MissingRequiredError):
            CognitiveAttributeCollection(table)
