"""Tests UDS Form B1 attributes."""

import random

from nacc_attribute_deriver.attributes.derived.modules.uds.form_b1 import (
    UDSFormB1Attribute,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS

ALL_FORMVERS = [1.0, 2.0, 3.0, 3.2, 4.0]


class TestUDSFormB1Attribute:
    def test_get_height(self, uds_table):
        """Test get height."""
        # in V1/V2 max, a height of 99 should return None
        uds_table["file.info.forms.json"].update(
            {"formver": random.choice([1.0, 2.0]), "height": 99.0}
        )
        attr = UDSFormB1Attribute(uds_table)
        assert attr.get_height() is None

        # 88 - 96 should still be valid in V1/V2
        uds_table["file.info.forms.json"].update(
            {"formver": random.choice([1.0, 2.0]), "height": 88.0}
        )
        attr = UDSFormB1Attribute(uds_table)
        assert attr.get_height() == 88.0

        # 88 is NOT valid in V3+
        uds_table["file.info.forms.json"].update(
            {"formver": random.choice([3.0, 4.0]), "height": 88.0}
        )
        attr = UDSFormB1Attribute(uds_table)
        assert attr.get_height() is None

        # test heigdec logic
        # if height ends up below 36, should return None
        uds_table["file.info.forms.json"].update(
            {"formver": random.choice(ALL_FORMVERS), "height": 35.5, "heigdec": 4}
        )
        attr = UDSFormB1Attribute(uds_table)
        assert attr.get_height() is None

        uds_table["file.info.forms.json"].update(
            {"formver": random.choice(ALL_FORMVERS), "height": 35.5, "heigdec": 5}
        )
        attr = UDSFormB1Attribute(uds_table)
        assert attr.get_height() == 36.0

        uds_table["file.info.forms.json"].update(
            {"formver": random.choice(ALL_FORMVERS), "height": 36, "heigdec": None}
        )
        attr = UDSFormB1Attribute(uds_table)
        assert attr.get_height() == 36.0

    def test_create_naccbmi(self, uds_table):
        """Tests NACCBMI."""
        uds_table["file.info.forms.json"].update(
            {"b1sub": 1, "weight": 165, "height": 60}
        )

        attr = UDSFormB1Attribute(uds_table)
        assert attr._create_naccbmi() == 32.2

        # this tests the half case
        uds_table["file.info.forms.json"].update(
            {"b1sub": 1, "weight": 180, "height": 60}
        )

        attr = UDSFormB1Attribute(uds_table)
        assert attr._create_naccbmi() == 35.2

        # tests one or both is missing/unknown
        uds_table["file.info.forms.json"].update(
            {"b1sub": 1, "weight": None, "height": 60}
        )
        attr = UDSFormB1Attribute(uds_table)
        assert attr._create_naccbmi() == 888.8

        uds_table["file.info.forms.json"].update(
            {"b1sub": 1, "weight": 180, "height": 88.8}
        )
        attr = UDSFormB1Attribute(uds_table)
        assert attr._create_naccbmi() == 888.8

        # test form not submitted
        uds_table["file.info.forms.json"].update(
            {"b1sub": 0, "weight": 180, "height": 60}
        )
        attr = UDSFormB1Attribute(uds_table)
        assert attr._create_naccbmi() == INFORMED_MISSINGNESS

    def test_compute_average(self, uds_table):
        """Test _compute_average, which is used to derive most of the variables
        for V4."""
        # test formver != 4
        uds_table["file.info.forms.json.formver"] = random.choice([1.0, 2.0, 3.0, 3.2])
        attr = UDSFormB1Attribute(uds_table)
        assert attr._compute_average("field1", "field2") == INFORMED_MISSINGNESS

        # test form not submitted, V3 and earlier
        uds_table["file.info.forms.json"].update({"b1sub": 0})
        attr = UDSFormB1Attribute(uds_table)
        assert attr._compute_average("field1", "field2") == INFORMED_MISSINGNESS

        # test form not submitted, V4
        uds_table["file.info.forms.json"].update({"modeb1": 0, "formver": 4.0})
        attr = UDSFormB1Attribute(uds_table)
        assert attr._compute_average("field1", "field2") == INFORMED_MISSINGNESS

        # test fields are missing
        uds_table["file.info.forms.json.modeb1"] = 1
        assert attr._compute_average("field1", "field2") == 888

        # test fields are 888
        uds_table["file.info.forms.json"].update({"field1": 1, "field2": 888})
        assert attr._compute_average("field1", "field2") == 888

        # compute average
        uds_table["file.info.forms.json"].update({"field1": 78, "field2": 52})
        assert attr._compute_average("field1", "field2") == 65

    def test_handle_v3_blood_pressure(self, uds_table):
        """Test _handle_v3_blood_pressure, which is just for V3."""
        uds_table["file.info.forms.json"].update(
            {"formver": 3.0, "gate": 777, "field": 123}
        )

        attr = UDSFormB1Attribute(uds_table)
        assert attr._handle_v3_blood_pressure("gate", "field") == 123

        # gate is not 777
        uds_table["file.info.forms.json.gate"] = 888
        assert attr._handle_v3_blood_pressure("gate", "field") == -4
