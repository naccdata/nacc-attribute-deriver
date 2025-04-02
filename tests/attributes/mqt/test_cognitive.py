"""Tests deriving MQT cognitive variables."""

import pytest

from nacc_attribute_deriver.attributes.mqt.cognitive import CognitiveAttributeCollection
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
                        # rest of fields will be None
                    }
                },
                "derived": {
                    "naccalzp": 7,
                    "nacclbde": None,
                    "nacclbdp": None,
                    "naccppa": 8,
                    "naccbvft": 8,
                    "nacclbds": 1,
                    "naccnorm": 0,
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

        attr = CognitiveAttributeCollection.create(table)
        assert set(attr._create_contributing_diagnosis().value) == set(expected_values)  # noqa: SLF001

    def test_dementia(self, table):
        """Tests _create_dementia."""
        attr = CognitiveAttributeCollection.create(table)
        assert attr._create_dementia().value == [  # noqa: SLF001
            CognitiveAttributeCollection.DEMENTIA_MAPPINGS["nacclbds"]
        ]

        # test multiple
        table["file.info.forms.json.amndem"] = 1
        table["file.info.forms.json.pca"] = 1

        attr = CognitiveAttributeCollection.create(table)

        assert set(attr._create_dementia().value) == set(  # noqa: SLF001
            [
                CognitiveAttributeCollection.DEMENTIA_MAPPINGS["amndem"],
                CognitiveAttributeCollection.DEMENTIA_MAPPINGS["pca"],
                CognitiveAttributeCollection.DEMENTIA_MAPPINGS["nacclbds"],
            ]
        )

    def test_cognitive_status(self, table):
        """Tests _create_cognitive_status, which just comes from NACCUDSD."""
        for k, v in CognitiveAttributeCollection.NACCUDSD_MAPPING.items():
            table["file.info.derived.naccudsd"] = k
            attr = CognitiveAttributeCollection.create(table)
            assert attr._create_cognitive_status().value == v  # noqa: SLF001

    def test_etpr(self, table):
        """Tests _create_etpr, which just comes from NACCETPR."""
        for k, v in CognitiveAttributeCollection.PRIMARY_DIAGNOSIS_MAPPINGS.items():
            table["file.info.derived.naccetpr"] = k
            attr = CognitiveAttributeCollection.create(table)
            assert attr._create_etpr().value == v  # noqa: SLF001

    def test_global_cdr(self, table):
        """Tests _create_global_cdr, which just comes from CDRGLOB as a
        string."""
        attr = CognitiveAttributeCollection.create(table)
        assert attr._create_global_cdr().value == 0.5  # noqa: SLF001

        table["file.info.forms.json.cdrglob"] = None
        attr = CognitiveAttributeCollection.create(table)
        assert attr._create_global_cdr().value is None  # noqa: SLF001

    def test_create_normal_cognition(self, table):
        """Tests _create_normal_cognition which just comes from NACCNORM."""
        attr = CognitiveAttributeCollection.create(table)
        assert not attr._create_normal_cognition()  # noqa: SLF001

        table["file.info.derived.naccnorm"] = 1
        attr = CognitiveAttributeCollection.create(table)
        assert attr._create_normal_cognition()  # noqa: SLF001

        table["file.info.derived.naccnorm"] = None
        attr = CognitiveAttributeCollection.create(table)
        assert not attr._create_normal_cognition()  # noqa: SLF001
