"""Tests deriving MQT cognitive variables."""
import pytest

from nacc_attribute_deriver.attributes.mqt.cognitive import CognitiveAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable


@pytest.fixture(scope='function')
def attr() -> CognitiveAttribute:
    """Create dummy data and return it in an attribute object."""
    data = {
        'file': {
            'info': {
                'forms': {
                    'json': {
                        'normcog': 0,
                        'msaif': 1,
                        'pspif': 2,
                        'cortif': 2,
                        'ftldmoif': 2,
                        'ftldnosif': 3,
                        'ftdif': 3,
                        'ppaphif': 3,
                        'cvdif': 2,
                        'vascif': 3,
                        'vascpsif': 3,
                        'strokeif': 3,
                        'amndem': 0,
                        'pca': 0,
                        'namndem': None,
                        'cdrglob': 0.5,

                        # rest of fields will be None
                    }
                },
                'derived': {
                    "naccalzp": 7,
                    "nacclbde": None,
                    "nacclbdp": None,
                    "naccppa": 8,
                    "naccbvft": 8,
                    "nacclbds": 1,
                    'naccnorm': 0
                }
            }
        }
    }

    return CognitiveAttribute(SymbolTable(data))


class TestCognitiveAttribute:

    def test_contributing_diagnosis(self, attr):
        """Tests _create_contributing_diagnosis."""
        expected_values = []
        for field in ['pspif', 'cortif', 'ftldmoif', 'cvdif']:  # all == 2
            expected_values.append(
                CognitiveAttribute.DIAGNOSIS_MAPPINGS['file.info.forms.json.']
                [field])

        assert set(
            attr._create_contributing_diagnosis()) == set(expected_values)

    def test_dementia(self, attr):
        """Tests _create_dementia."""
        assert attr._create_dementia() == \
            [CognitiveAttribute.DEMENTIA_MAPPINGS['file.info.derived.']['nacclbds']]

        # test multiple
        attr.set_value('amndem', 1)
        attr.set_value('pca', 1)

        assert set(attr._create_dementia()) == \
            set([
                CognitiveAttribute.DEMENTIA_MAPPINGS['file.info.forms.json.']['amndem'],
                CognitiveAttribute.DEMENTIA_MAPPINGS['file.info.forms.json.']['pca'],
                CognitiveAttribute.DEMENTIA_MAPPINGS['file.info.derived.']['nacclbds']
            ])

    def test_cognitive_status(self, attr):
        """Tests _create_cognitive_status, which just comes from NACCUDSD."""
        for k, v in CognitiveAttribute.NACCUDSD_MAPPING.items():
            attr.table['file.info.derived.naccudsd'] = k
            assert attr._create_cognitive_status() == v

    def test_etpr(self, attr):
        """Tests _create_etpr, which just comes from NACCETPR."""
        for k, v in CognitiveAttribute.PRIMARY_DIAGNOSIS_MAPPINGS.items():
            attr.table['file.info.derived.naccetpr'] = k
            assert attr._create_etpr() == v

    def test_global_cdr(self, attr):
        """Tests _create_global_cdr, which just comes from CDRGLOB as a
        string."""
        assert attr._create_global_cdr() == "0.5"
        attr.table['file.info.forms.json.cdrglob'] = None
        assert attr._create_global_cdr() is None

    def test_create_normal_cognition(self, attr):
        """Tests _create_normal_cognition which just comes from NACCNORM."""
        assert not attr._create_normal_cognition()
        attr.table['file.info.derived.naccnorm'] = 1
        assert attr._create_normal_cognition()
        attr.table['file.info.derived.naccnorm'] = None
        assert not attr._create_normal_cognition()
