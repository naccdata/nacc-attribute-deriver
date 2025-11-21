"""Tests UDS Form Cx missingness attributes."""

import random

from nacc_attribute_deriver.attributes.missingness.modules.uds.missingness_cx import (
    UDSFormC1C2Missingness,
)
from nacc_attribute_deriver.utils.constants import (
    INFORMED_BLANK,
    INFORMED_MISSINGNESS,
)


class TestUDSFormC1C2Missingness:
    def test_respval_gate(self, uds_table):
        """Test variables gated by RESPVAL."""
        uds_table["file.info.forms.json.respval"] = random.choice([2, 3])
        attr = UDSFormC1C2Missingness(uds_table)

        assert attr._handle_respval_gate("testvar") == 0

        uds_table["file.info.forms.json.respval"] = 1
        assert attr._handle_respval_gate("testvar") == INFORMED_MISSINGNESS

        uds_table["file.info.forms.json.testvar"] = 5
        assert attr._handle_respval_gate("testvar") == 5

    def test_reyxrec_cascade(self, uds_table):
        """Test the REYXREC cascade effect."""
        cascade_value = random.choice([95, 96, 97, 98])
        hundreds_cascade_value = 888 if cascade_value == 88 else cascade_value + 900

        uds_table["file.info.forms.json"].update(
            {
                "formver": 3.2,
                "packet": "T",
                "reydrec": cascade_value,
                "rey1rec": cascade_value,
            }
        )

        attr = UDSFormC1C2Missingness(uds_table)

        # these don't require gate_mresult since
        # REYDREC and REY1REC should be there
        assert attr._missingness_reydint() == hundreds_cascade_value
        assert attr._missingness_reytcor() == cascade_value
        assert attr._missingness_reyfpos() == cascade_value
        assert attr._missingness_rey1int() == hundreds_cascade_value
        assert attr._missingness_rey2rec() == cascade_value
        assert attr._missingness_rey2int() == hundreds_cascade_value

        # these need to call their gate's missingness,
        # e.g. set gate_mresult. should cascade
        assert attr._missingness_rey3rec() == cascade_value
        assert attr._missingness_rey3int() == hundreds_cascade_value
        assert attr._missingness_rey4rec() == cascade_value
        assert attr._missingness_rey4int() == hundreds_cascade_value
        assert attr._missingness_rey5rec() == cascade_value
        assert attr._missingness_rey5int() == hundreds_cascade_value

        assert attr._missingness_reybrec() == cascade_value
        assert attr._missingness_reybint() == hundreds_cascade_value
        assert attr._missingness_rey6rec() == cascade_value
        assert attr._missingness_rey6int() == hundreds_cascade_value

        # set verbaltest to 2 - now should all be 88/888
        uds_table["file.info.forms.json.verbaltest"] = 2
        attr = UDSFormC1C2Missingness(uds_table)

        assert attr._missingness_reydint() == 888
        assert attr._missingness_reytcor() == 88
        assert attr._missingness_reyfpos() == 88
        assert attr._missingness_rey1int() == 888
        assert attr._missingness_rey2rec() == 88
        assert attr._missingness_rey2int() == 888

        assert attr._missingness_rey3rec() == 88
        assert attr._missingness_rey3int() == 888
        assert attr._missingness_rey4rec() == 88
        assert attr._missingness_rey4int() == 888
        assert attr._missingness_rey5rec() == 88
        assert attr._missingness_rey5int() == 888

        assert attr._missingness_reybrec() == 88
        assert attr._missingness_reybint() == 888
        assert attr._missingness_rey6rec() == 88
        assert attr._missingness_rey6int() == 888

        # not part of cascade but affected by verbaltest = 2
        assert attr._missingness_rey1rec() == 88
        assert attr._missingness_reydrec() == 88
        assert attr._missingness_reydti() == 88
        assert attr._missingness_reymethod() == 88

    def test_cerad_variables(self, uds_table):
        """Tests the CERAD* variables, which are all gated by VERBALTEST."""
        uds_table["file.info.forms.json.verbaltest"] = 1
        attr = UDSFormC1C2Missingness(uds_table)

        assert attr._missingness_cerad1rec() == 88
        assert attr._missingness_cerad1read() == 88
        assert attr._missingness_cerad1int() == 888
        assert attr._missingness_cerad2rec() == 88
        assert attr._missingness_cerad2read() == 88
        assert attr._missingness_cerad2int() == 888

        assert attr._missingness_cerad3rec() == 88
        assert attr._missingness_cerad3read() == 88
        assert attr._missingness_cerad3int() == 888
        assert attr._missingness_ceraddti() == 88
        assert attr._missingness_ceradj6rec() == 88
        assert attr._missingness_ceradj6int() == 888

        assert attr._missingness_ceradj7yes() == 88
        assert attr._missingness_ceradj7no() == 88

    def test_memtime(self, uds_table):
        """Tests missingness for MEMTIME."""
        uds_table["file.info.forms.json"].update(
            {"formver": 1.0, "packet": "I", "memtime": 88, "memunits": 97}
        )
        attr = UDSFormC1C2Missingness(uds_table)
        assert attr._missingness_memtime() == INFORMED_MISSINGNESS

        uds_table["file.info.forms.json"].update({"memtime": 88, "memunits": 0})
        attr = UDSFormC1C2Missingness(uds_table)
        assert attr._missingness_memtime() == 99

    def test_trailbx(self, uds_table):
        """Tests TRAILBX variables."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 1.0,
                "packet": "I",
                "trailb": "996",
                "trailbrr": None,
                "trailbli": None,
            }
        )
        attr = UDSFormC1C2Missingness(uds_table)

        # REGRESSION - should NOT subtract 900 in new version
        assert attr._missingness_trailbrr() == 96
        assert attr._missingness_trailbli() == 96

    def test_logidate(self, uds_table):
        """Tests LOGIDATE (LOGINO, LOGIDAY, LOGIYR) variables.

        Should parse from logidate_c1.
        """
        uds_table["file.info.forms.json"].update(
            {"logidate_c1": "2025-06-09", "logiprev": 8}
        )
        attr = UDSFormC1C2Missingness(uds_table)

        # real date, expect values
        assert attr._missingness_logiyr() == 2025
        assert attr._missingness_logimo() == 6
        assert attr._missingness_logiday() == 9

        # need to parse invalid date
        uds_table["file.info.forms.json"].update(
            {
                "logidate_c1": "9999-99-99",
            }
        )
        # convert to 88/88/8888
        assert attr._missingness_logiyr() == 8888
        assert attr._missingness_logimo() == 88
        assert attr._missingness_logiday() == 88

    def test_udsverte_udsverti(self, uds_table):
        """Tests UDSVERTE and UDSVERTI missingness which are most affected by
        the UDSVERX cascade."""
        uds_table["file.info.forms.json"].update(
            {
                "udsverfc": 96,  # this is what gets cascaded down
                "udsverlc": 3,
                "udsvertn": None,
                "udsverte": None,
                "udsverti": None,
            }
        )
        attr = UDSFormC1C2Missingness(uds_table)
        assert attr._missingness_udsverte() == 96
        assert attr._missingness_udsverti() == 96

        uds_table["file.info.forms.json"].update(
            {
                "udsverfc": 13,
                "udsverlc": 97,  # now this gets cascaded down
                "udsvertn": None,
                "udsverte": None,
                "udsverti": None,
            }
        )
        assert attr._missingness_udsverte() == 97
        assert attr._missingness_udsverti() == 97

        uds_table["file.info.forms.json"].update(
            {
                "udsverfc": 13,
                "udsverlc": 5,
                "udsvertn": 98,  # now this gets cascaded down
                "udsverte": None,
                "udsverti": None,
            }
        )
        assert attr._missingness_udsverte() == 98
        assert attr._missingness_udsverti() == 98

    def test_writeins(self, uds_table):
        """Test write-ins."""
        uds_table["file.info.forms.json"].update(
            {
                "formver": 4,
                "npsylan": 1,
                "npsylanx": "should be set blank when not 3 except legacy",
                "mocalan": 1,
                "mocalanx": "should be set blank when not 3",
                "respoth": 3,
                "respothx": "should be set blank when not 1",
                "mmselan": 1,
                "mmselanx": "should be set blank when not 3",
            }
        )
        attr = UDSFormC1C2Missingness(uds_table)

        assert attr._missingness_npsylanx() == INFORMED_BLANK
        assert attr._missingness_mocalanx() == INFORMED_BLANK
        assert attr._missingness_respothx() == INFORMED_BLANK
        assert attr._missingness_mmselanx() == INFORMED_BLANK

        uds_table["file.info.forms.json"].update(
            {
                "npsylan": 3,
                "mocalan": 3,
                "respoth": 1,
                "mmselan": 3,
            }
        )

        assert (
            attr._missingness_npsylanx()
            == "should be set blank when not 3 except legacy"
        )
        assert attr._missingness_mocalanx() == "should be set blank when not 3"
        assert attr._missingness_respothx() == "should be set blank when not 1"
        assert attr._missingness_mmselanx() == "should be set blank when not 3"

        # it seems legacy versions did not override in npsalanx case
        uds_table["file.info.forms.json"].update(
            {
                "formver": random.choice([1, 2, 3]),
                "npsylan": 1,
                "mocalan": 1,
                "respoth": 3,
                "mmselan": 1,
            }
        )
        attr = UDSFormC1C2Missingness(uds_table)

        assert (
            attr._missingness_npsylanx()
            == "should be set blank when not 3 except legacy"
        )
        assert attr._missingness_mocalanx() == INFORMED_BLANK
        assert attr._missingness_respothx() == INFORMED_BLANK
        assert attr._missingness_mmselanx() == INFORMED_BLANK

    def test_mocacomp_gate(self, uds_table):
        """Tests MOCACOMP-gated variables - if MOCACOMP = 0,
        then MOCATOTS and MOCBTOTS should = 88, and all MOC*
        variables should = MOCAREAS.

        For V4, all values on the form they did not fill out
        should be -4.
        """
        uds_table["file.info.forms.json"].update(
            {
                "formver": random.choice([1, 2, 3]),
                "rmmodec2c2t": 1,
                "mocacomp": 0,
                "mocareas": 96,
            }
        )
        attr = UDSFormC1C2Missingness(uds_table)

        # doing legacy first, so both c2/c2t vars affected
        # regardless of what version it was
        assert attr._missingness_mocatots() == 88  # C2-specific
        assert attr._missingness_mocbtots() == 88  # C2t-specific

        # no need to test every variable as they all call the
        # same method the same way, so use candidate ones
        assert attr._missingness_mocatrai() == 96  # only in C2
        assert attr._missingness_mocadigi() == 96  # in both

        # Now V4 - start with a C2T form
        uds_table["file.info.forms.json.formver"] = 4
        attr = UDSFormC1C2Missingness(uds_table)
        assert attr._missingness_mocatots() == INFORMED_MISSINGNESS
        assert attr._missingness_mocbtots() == 88

        assert attr._missingness_mocatrai() == INFORMED_MISSINGNESS
        assert attr._missingness_mocadigi() == 96

        # C2 form
        uds_table["file.info.forms.json.rmmodec2c2t"] = 2
        attr = UDSFormC1C2Missingness(uds_table)
        assert attr._missingness_mocatots() == 88
        assert attr._missingness_mocbtots() == INFORMED_MISSINGNESS

        assert attr._missingness_mocatrai() == 96
        assert attr._missingness_mocadigi() == 96
