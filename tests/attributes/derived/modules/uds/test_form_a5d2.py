"""Tests UDS Form A5D2 attributes."""

import random

from nacc_attribute_deriver.attributes.derived.modules.uds.form_a5d2 import (
    UDSFormA5D2Attribute,
)
from nacc_attribute_deriver.utils.constants import INFORMED_MISSINGNESS


class TestUDSFormA5D2Attribute:
    def test_calculate_mrsyear(self, uds_table):
        """Test finding the maximum year."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": random.choice([1, 2]),
                "dummy1yr": 2000,
                "dummy2yr": "2025",
                "dummy3yr": None,
                "dummy4yr": None,
                "dummy5yr": 2020,
                "dummy6yr": "2015",
            }
        )
        attr = UDSFormA5D2Attribute(uds_table)
        assert attr.calculate_mrsyear(prefix="dummy") == 2025

        uds_table["file.info.forms.json"].update(
            {
                "formver": random.choice([1, 2]),
                "dummy1yr": -4,
                "dummy2yr": "8888",
                "dummy3yr": None,
                "dummy4yr": None,
                "dummy5yr": 9999,
                "dummy6yr": "8888",
            }
        )
        assert attr.calculate_mrsyear(prefix="dummy") is None

    def test_naccrheum_v3(self, uds_table):
        """Tests NACCRHEUM, V3 logic."""
        uds_table["file.info.forms.json.formver"] = random.choice([3, 3.2])
        attr = UDSFormA5D2Attribute(uds_table)

        # Case 1: ARTHRIT is blank and ARTH is blank, expect -4
        uds_table["file.info.forms.json"].update(
            {
                "arthrit": None,
                "arth": None,
            }
        )
        assert attr._create_naccrheum() == INFORMED_MISSINGNESS

        # Case 2: ARTHTYPE = 1 or ARTYPE = 1, expect 1
        field = random.choice(["arthtype", "artype"])
        uds_table["file.info.forms.json"].update({"arthrit": 1, "arth": 1, field: 1})
        assert attr._create_naccrheum() == 1

        # Case 3: ARTHTYPE = 2,3 or ARTYPE = 2,3, expect 0
        uds_table["file.info.forms.json"].update({field: random.choice([2, 3])})
        assert attr._create_naccrheum() == 0

        # Case 4: ARTHRIT = 0 or ARTH = 0, expect 8
        other_field = random.choice(["arthrit", "arth"])
        uds_table["file.info.forms.json"].update({field: None, other_field: 0})
        assert attr._create_naccrheum() == 8

        # Case 5: ARTHTYPE = 9 and ARTYPE = 9, expect 9
        uds_table["file.info.forms.json"].update(
            {"arthrit": 8, "arth": 8, "arthtype": 9, "artype": 9}
        )
        assert attr._create_naccrheum() == 9

        # Case 6: technically not possible, but if
        # it hits none of the above expect -4
        uds_table["file.info.forms.json"].update({"arthtype": 9, "artype": 10})
        assert attr._create_naccrheum() == INFORMED_MISSINGNESS

    def test_naccrheum_v4(self, uds_table):
        """Tests NACCRHEUM, V4 logic."""
        uds_table["file.info.forms.json.formver"] = 4
        attr = UDSFormA5D2Attribute(uds_table)

        # Case 1: ARTHRRHEUM is 1, expect 1
        uds_table["file.info.forms.json"].update({"arthrrheum": 1})
        assert attr._create_naccrheum() == 1

        # Case 2: ARTHRIT = 1,2 and ARTHRRHEUM blank and ARTHTYPUNK blank,
        # expect 0
        uds_table["file.info.forms.json"].update(
            {"arthrit": random.choice([1, 2]), "arthrrheum": None, "arthtypunk": None}
        )
        assert attr._create_naccrheum() == 0

        # Case 3: ARTHRIT = 0, expect 8
        uds_table["file.info.forms.json"].update({"arthrit": 0})
        assert attr._create_naccrheum() == 8

        # Case 4: ARTHTYPUNK = 1, expect 9
        uds_table["file.info.forms.json"].update({"arthrit": 8, "arthtypunk": 1})
        assert attr._create_naccrheum() == 9

        # Case 5: default, -4
        uds_table["file.info.forms.json"].update(
            {
                "arthtypunk": 3,
            }
        )
        assert attr._create_naccrheum() == INFORMED_MISSINGNESS

    def test_naccosteo_v3(self, uds_table):
        """Tests NACCOSTEO, V3 logic."""
        uds_table["file.info.forms.json.formver"] = random.choice([3, 3.2])
        attr = UDSFormA5D2Attribute(uds_table)

        # Case 1: ARTHRIT is blank and ARTH is blank, expect -4
        uds_table["file.info.forms.json"].update(
            {
                "arthrit": None,
                "arth": None,
            }
        )
        assert attr._create_naccosteo() == INFORMED_MISSINGNESS

        # Case 2: ARTHTYPE = 2 or ARTYPE = 2, expect 1
        field = random.choice(["arthtype", "artype"])
        uds_table["file.info.forms.json"].update({"arthrit": 1, "arth": 1, field: 2})
        assert attr._create_naccosteo() == 1

        # Case 3: ARTHTYPE = 1,3 or ARTYPE = 1,3, expect 0
        uds_table["file.info.forms.json"].update({field: random.choice([1, 3])})
        assert attr._create_naccosteo() == 0

        # Case 4: ARTHRIT = 0 or ARTH = 0, expect 8
        other_field = random.choice(["arthrit", "arth"])
        uds_table["file.info.forms.json"].update({field: None, other_field: 0})
        assert attr._create_naccosteo() == 8

        # Case 5: ARTHTYPE = 9 and ARTYPE = 9, expect 9
        uds_table["file.info.forms.json"].update(
            {"arthrit": 8, "arth": 8, "arthtype": 9, "artype": 9}
        )
        assert attr._create_naccosteo() == 9

        # Case 6: technically not possible, but if
        # it hits none of the above expect -4
        uds_table["file.info.forms.json"].update({"arthtype": 9, "artype": 10})
        assert attr._create_naccosteo() == INFORMED_MISSINGNESS

    def test_naccasteo_v4(self, uds_table):
        """Tests NACCASTEO, V4 logic."""
        uds_table["file.info.forms.json.formver"] = 4
        attr = UDSFormA5D2Attribute(uds_table)

        # Case 1: ARTHROSTEO is 1, expect 1
        uds_table["file.info.forms.json"].update({"arthrosteo": 1})
        assert attr._create_naccosteo() == 1

        # Case 2: ARTHRIT = 1,2 and ARTHROSTEO blank and ARTHTYPUNK blank,
        # expect 0
        uds_table["file.info.forms.json"].update(
            {"arthrit": random.choice([1, 2]), "arthrosteo": None, "arthtypunk": None}
        )
        assert attr._create_naccosteo() == 0

        # Case 3: ARTHRIT = 0, expect 8
        uds_table["file.info.forms.json"].update({"arthrit": 0})
        assert attr._create_naccosteo() == 8

        # Case 4: ARTHTYPUNK = 1, expect 9
        uds_table["file.info.forms.json"].update({"arthrit": 8, "arthtypunk": 1})
        assert attr._create_naccosteo() == 9

        # Case 5: default, -4
        uds_table["file.info.forms.json"].update(
            {
                "arthtypunk": 3,
            }
        )
        assert attr._create_naccosteo() == INFORMED_MISSINGNESS

    def test_naccartoth_v3(self, uds_table):
        """Tests NACCARTOTH, V3 logic."""
        uds_table["file.info.forms.json.formver"] = random.choice([3, 3.2])
        attr = UDSFormA5D2Attribute(uds_table)

        # Case 1: ARTHRIT is blank and ARTH is blank, expect -4
        uds_table["file.info.forms.json"].update(
            {
                "arthrit": None,
                "arth": None,
            }
        )
        assert attr._create_naccartoth() == INFORMED_MISSINGNESS

        # Case 2: ARTHTYPE = 3 or ARTYPE = 3, expect 1
        field = random.choice(["arthtype", "artype"])
        uds_table["file.info.forms.json"].update({"arthrit": 1, "arth": 1, field: 3})
        assert attr._create_naccartoth() == 1

        # Case 3: ARTHTYPE = 1,2 or ARTYPE = 1,2, expect 0
        uds_table["file.info.forms.json"].update({field: random.choice([1, 2])})
        assert attr._create_naccartoth() == 0

        # Case 4: ARTHRIT = 0 or ARTH = 0, expect 8
        other_field = random.choice(["arthrit", "arth"])
        uds_table["file.info.forms.json"].update({field: None, other_field: 0})
        assert attr._create_naccartoth() == 8

        # Case 5: ARTHTYPE = 9 and ARTYPE = 9, expect 9
        uds_table["file.info.forms.json"].update(
            {"arthrit": 8, "arth": 8, "arthtype": 9, "artype": 9}
        )
        assert attr._create_naccartoth() == 9

        # Case 6: technically not possible, but if
        # it hits none of the above expect -4
        uds_table["file.info.forms.json"].update({"arthtype": 9, "artype": 10})
        assert attr._create_naccartoth() == INFORMED_MISSINGNESS

    def test_naccartothv4(self, uds_table):
        """Tests NACCARTOTH, V4 logic."""
        uds_table["file.info.forms.json.formver"] = 4
        attr = UDSFormA5D2Attribute(uds_table)

        # Case 1: ARTHROTHR is 1, expect 1
        uds_table["file.info.forms.json"].update({"arthrothr": 1})
        assert attr._create_naccartoth() == 1

        # Case 2: ARTHRIT = 1,2 and ARTHROTHR blank and ARTHTYPUNK blank,
        # expect 0
        uds_table["file.info.forms.json"].update(
            {"arthrit": random.choice([1, 2]), "arthrothr": None, "arthtypunk": None}
        )
        assert attr._create_naccartoth() == 0

        # Case 3: ARTHRIT = 0, expect 8
        uds_table["file.info.forms.json"].update({"arthrit": 0})
        assert attr._create_naccartoth() == 8

        # Case 4: ARTHTYPUNK = 1, expect 9
        uds_table["file.info.forms.json"].update({"arthrit": 8, "arthtypunk": 1})
        assert attr._create_naccartoth() == 9

        # Case 5: default, -4
        uds_table["file.info.forms.json"].update(
            {
                "arthtypunk": 3,
            }
        )
        assert attr._create_naccartoth() == INFORMED_MISSINGNESS

    def test_nacccancer(self, uds_table):
        """Tests NACCCANCER.

        V3/V4 have same logic just on different variables.
        """
        formver = random.choice([3, 4])
        cancer = "canceractv" if formver == 4 else "cancer"

        uds_table["file.info.forms.json"].update(
            {
                "formver": formver,
            }
        )
        attr = UDSFormA5D2Attribute(uds_table)

        # Case 1: CANCER = 0, expect 0
        uds_table["file.info.forms.json"].update({cancer: 0})
        assert attr._create_nacccancer() == 0

        # Case 2: CANCER = 1 or 2, expect 1
        uds_table["file.info.forms.json"].update({cancer: random.choice([1, 2])})
        assert attr._create_nacccancer() == 1

        # Case 3: CANCER = 9, expect 9
        uds_table["file.info.forms.json"].update({cancer: 9})
        assert attr._create_nacccancer() == 9

        # Case 4: default -4
        uds_table["file.info.forms.json"].update({cancer: None})
        assert attr._create_nacccancer() == INFORMED_MISSINGNESS

        # ensure setting the other doesn't do anything
        uds_table["file.info.forms.json"].update(
            {"canceractv" if formver < 4 else "cancer": 0}
        )
        assert attr._create_nacccancer() == INFORMED_MISSINGNESS

    def test_naccothcon_v3(self, uds_table):
        """Tests NACCOTHCON, V3 logic. Basically = othcond if not blank,
        -4 otherwise."""
        uds_table["file.info.forms.json.formver"] = 3
        attr = UDSFormA5D2Attribute(uds_table)
        assert attr._create_naccothcon() == INFORMED_MISSINGNESS

        uds_table["file.info.forms.json.othcond"] = 13
        assert attr._create_naccothcon() == 13

    def test_naccothcon_v4(self, uds_table):
        """Tests NACCOTHCON, V4 logic."""
        uds_table["file.info.forms.json.formver"] = 4
        attr = UDSFormA5D2Attribute(uds_table)

        # default: -4 when blank
        assert attr._create_naccothcon() == INFORMED_MISSINGNESS

        # Case 1: OTHERCOND = 1, expect 1
        uds_table["file.info.forms.json.othercond"] = 1
        assert attr._create_naccothcon() == 1

        # Case 2: OTHERCOND = 0 or 2, expect 0
        uds_table["file.info.forms.json.othercond"] = random.choice([0, 2])
        assert attr._create_naccothcon() == 0

        # Case 3: OTHERCOND = 9, expect 9
        uds_table["file.info.forms.json.othercond"] = 9
        assert attr._create_naccothcon() == 9

        # some nonsense caes
        uds_table["file.info.forms.json.othercond"] = 113
        assert attr._create_naccothcon() == INFORMED_MISSINGNESS

    def test_naccdep_legacy(self, uds_table):
        """Tests NACCDEP, V1 - V3 logic."""
        uds_table["file.info.forms.json.formver"] = random.choice([1, 2, 3])
        attr = UDSFormA5D2Attribute(uds_table)

        # Case 1: DEP2YRS or DEPOTHR = 1, expect 1
        field = random.choice(["dep2yrs", "depothr"])
        uds_table["file.info.forms.json"].update({field: 1})
        assert attr._create_naccdep() == 1

        # Case 2: DEP2YRS and DEPOTHR = 0, expect 0
        uds_table["file.info.forms.json"].update({"dep2yrs": 0, "depothr": 0})
        assert attr._create_naccdep() == 0

        # Case 3: DEP2YRS or DEPOTHR = 9, expect 9
        uds_table["file.info.forms.json"].update({field: 9})
        assert attr._create_naccdep() == 9

        # Case 3: DEP2YRS or DEPOTHR = blank, expect -4
        uds_table["file.info.forms.json"].update({field: None})
        assert attr._create_naccdep() == INFORMED_MISSINGNESS

        # # FVP case: DEP2YRS and DEPOTHR are not provided in
        # # FVP visits for V3, so pull through
        # uds_table["file.info.forms.json"].update(
        #     {
        #         "formver": 3,
        #         "packet": "F",
        #         field: 9,  # ensure the 9 is ignored
        #     }
        # )
        # attr = UDSFormA5D2Attribute(uds_table)
        # assert attr._create_naccdep() == INFORMED_MISSINGNESS

        # uds_table.update({"_prev_record": {"info": {"derived": {"naccdep": 1}}}})
        # assert attr._create_naccdep() == 1

    def test_naccdep_v4(self, uds_table):
        """Tests NACCDEP, V4 logic."""
        uds_table["file.info.forms.json.formver"] = 4
        attr = UDSFormA5D2Attribute(uds_table)

        # Case 1: MAJORDEP or OTHERDEP = 1 or 2, expect 1
        field = random.choice(["majordep", "otherdep"])
        uds_table["file.info.forms.json"].update({field: random.choice([1, 2])})
        assert attr._create_naccdep() == 1

        # Case 2: MAJORDEP and OTHERDEP = 0, expect 0
        uds_table["file.info.forms.json"].update({"majordep": 0, "otherdep": 0})
        assert attr._create_naccdep() == 0

        # Case 3: MAJORDEP or OTHERDEP = 9, expect 9
        uds_table["file.info.forms.json"].update({field: 9})
        assert attr._create_naccdep() == 9

        # Case 4: MAJORDEP or OTHERDEP = blank, expect -4
        uds_table["file.info.forms.json"].update({field: None})
        assert attr._create_naccdep() == INFORMED_MISSINGNESS

    def test_naccanx_v3(self, uds_table):
        """Tests NACCDEP, V3 logic."""
        uds_table["file.info.forms.json.formver"] = 3
        attr = UDSFormA5D2Attribute(uds_table)

        # Case 1: ANXIETY or OCD = 1, expect 1
        field = random.choice(["anxiety", "ocd"])
        uds_table["file.info.forms.json"].update({field: 1})
        assert attr._create_naccanx() == 1

        # Case 2: ANXIETY or OCD = 2, expect 2
        uds_table["file.info.forms.json"].update({field: 2})
        assert attr._create_naccanx() == 2

        # Case 3: ANXIETY and OCD = 0, expect 0
        uds_table["file.info.forms.json"].update({"anxiety": 0, "ocd": 0})
        assert attr._create_naccanx() == 0

        # Case 4: ANXIETY or OCD = 9, expect 9
        uds_table["file.info.forms.json"].update({field: 9})
        assert attr._create_naccanx() == 9

        # default: -4
        uds_table["file.info.forms.json"].update({field: None})
        assert attr._create_naccanx() == INFORMED_MISSINGNESS

    def test_naccanx_v4(self, uds_table):
        """Tests NACCDEP, V4 logic.

        Basically just looks at ANXIETY
        """
        uds_table["file.info.forms.json.formver"] = 4
        attr = UDSFormA5D2Attribute(uds_table)
        assert attr._create_naccanx() == INFORMED_MISSINGNESS

        uds_table["file.info.forms.json.anxiety"] = 2
        assert attr._create_naccanx() == 2

    def test_naccsubst(self, uds_table):
        """Tests NACCSUBST."""

        # V1 - V3 rely on ABUSOTHR
        uds_table["file.info.forms.json.formver"] = random.choice([1, 2, 3])
        attr = UDSFormA5D2Attribute(uds_table)

        # default: missing, expect -4
        assert attr._create_naccsubst() == INFORMED_MISSINGNESS

        # Case 1: 0 or 2 then expect 0
        uds_table["file.info.forms.json.abusothr"] = random.choice([0, 2])
        assert attr._create_naccsubst() == 0

        # Case 2: 1 then expect 1
        uds_table["file.info.forms.json.abusothr"] = 1
        assert attr._create_naccsubst() == 1

        # Case 3: 9 then expect 9
        uds_table["file.info.forms.json.abusothr"] = 9
        assert attr._create_naccsubst() == 9

        # V4 rely on SUBSTYEAR
        uds_table["file.info.forms.json.formver"] = 4
        attr = UDSFormA5D2Attribute(uds_table)

        # default: missing, expect -4
        assert attr._create_naccsubst() == INFORMED_MISSINGNESS

        # otherwise equals SUBSTYEAR
        value = random.choice([0, 1, 9])
        uds_table["file.info.forms.json.substyear"] = value
        assert attr._create_naccsubst() == value

    def test_naccheart_v1v2(self, uds_table):
        """Tests NACCHEART - V1/V2 logic. Basically just looks at CVHATT"""
        uds_table["file.info.forms.json.formver"] = random.choice([1, 2])
        attr = UDSFormA5D2Attribute(uds_table)

        # default: missing, expect -4
        assert attr._create_naccheart() == INFORMED_MISSINGNESS

        # otherwise equals CVHATT
        value = random.choice([0, 1, 2, 9])
        uds_table["file.info.forms.json.cvhatt"] = value
        assert attr._create_naccheart() == value

    def test_naccheart_v3(self, uds_table):
        """Tests NACCHEART - V3 logic. Looks at both CVHATT and MYOINF"""
        uds_table["file.info.forms.json.formver"] = 3
        attr = UDSFormA5D2Attribute(uds_table)

        # default: missing, expect -4
        assert attr._create_naccheart() == INFORMED_MISSINGNESS

        # Case 1: If CVHATT or MYOINF == 1, expect 1
        field = random.choice(["cvhatt", "myoinf"])
        uds_table["file.info.forms.json"].update({field: 1})
        assert attr._create_naccheart() == 1

        # Case 2: If CVHATT or MYOINF == 0, expect 0
        uds_table["file.info.forms.json"].update({field: 0})
        assert attr._create_naccheart() == 0

        # Case 3: If CVHATT == 2, expect 2
        uds_table["file.info.forms.json"].update({"cvhatt": 2, "myoinf": 9})
        assert attr._create_naccheart() == 2

        # check not triggerd if MYOINF == 2 (not an allowed value for
        # this variable but sanity check)
        uds_table["file.info.forms.json"].update({"cvhatt": 9, "myoinf": 2})
        assert attr._create_naccheart() == INFORMED_MISSINGNESS

        # Case 4: If CVHATT = 9 and MYOINF = 8 then expect 9
        uds_table["file.info.forms.json"].update({"cvhatt": 9, "myoinf": 8})
        assert attr._create_naccheart() == 9

    def test_naccheart_v4(self, uds_table):
        """Tests NACCHEART - V4 logic. Looks at both HRTATTACK and CARDARREST."""
        uds_table["file.info.forms.json.formver"] = 4
        attr = UDSFormA5D2Attribute(uds_table)

        # default: missing, expect -4
        assert attr._create_naccheart() == INFORMED_MISSINGNESS

        # Case 1: If HRTATTACK or CARDARREST == 1, expect 1
        field = random.choice(["hrtattack", "cardarrest"])
        uds_table["file.info.forms.json"].update({field: 1})
        assert attr._create_naccheart() == 1

        # Case 2: If HRTATTACK or CARDARREST == 2, expect 2
        uds_table["file.info.forms.json"].update({field: 2})
        assert attr._create_naccheart() == 2

        # Case 3: If HRTATTACK or CARDARREST == 0, expect 0
        uds_table["file.info.forms.json"].update({field: 0})
        assert attr._create_naccheart() == 0

        # Case 4: If HRTATTACK and CARDARREST == 9, expect 9
        uds_table["file.info.forms.json"].update({"hrtattack": 9, "cardarrest": 9})
        assert attr._create_naccheart() == 9

        # fallback case: if only one is 9, expect -4
        uds_table["file.info.forms.json"].update({field: 8})
        assert attr._create_naccheart() == INFORMED_MISSINGNESS
