"""Tests against the full schema end-to-end.

Mainly sanity checks to make sure modules run at all.
"""

from nacc_attribute_deriver.attribute_deriver import AttributeDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable


def test_uds_form():
    """Test against a minimal UDS form, mainly sanity check."""
    data = {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "module": "uds",
                        "birthmo": 1,
                        "birthyr": 1960,
                        "probadif": 1,
                        "dlbif": 2,
                        "demented": 1,
                        "normcog": 1,
                    }
                }
            }
        }
    }

    form = SymbolTable(data)

    deriver = AttributeDeriver()
    deriver.curate(form, "uds")
    assert form["file.info.derived"] == {
        "naccage": 65,
        "naccalzp": 8,
        "naccautp": 8,
        "naccbvft": 8,
        "naccdage": 888,
        "naccdied": 0,
        "naccetpr": 88,
        "nacclbds": 8,
        "naccnihr": 99,
        "naccppa": 8,
        "nacclbde": 8,
        "nacclbdp": 8,
        "naccnorm": 1,
        "naccudsd": 4,
    }


def test_np_form():
    """Test against a minimal NP form - all derived variables
    should be 9 with no data.
    """
    np_table = SymbolTable()
    np_table["file.info.forms.json.visitdate"] = "2025-01-01"
    np_table["file.info.forms.json.module"] = "np"
    np_table["file.info.forms.json.npdage"] = 80
    np_table["file.info.forms.json.npdodyr"] = "2024"
    np_table["file.info.forms.json.npdodmo"] = "12"
    np_table["file.info.forms.json.npdoddy"] = "19"

    deriver = AttributeDeriver()
    deriver.curate(np_table, "np")
    assert np_table.to_dict() == {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "module": "np",
                        "npdage": 80,
                        "npdodyr": "2024",
                        "npdodmo": "12",
                        "npdoddy": "19",
                    }
                },
            }
        },
        "subject": {
            "info": {
                "derived": {
                    "np_death_age": 80,
                    "np_death_date": "2024-12-19",
                    "np_arte": 9,
                    "np_braa": 9,
                    "np_hem": 9,
                    "np_lewy": 9,
                    "np_micr": 9,
                    "np_neur": 9,
                }
            }
        },
    }

    uds_table = SymbolTable()
    uds_table["subject.info.derived"] = np_table["subject.info.derived"]
    uds_table["file.info.forms.json"] = {
        "visitdate": "2025-01-01",
        "module": "uds",
        "birthmo": 1,
        "birthyr": 1960,
        "normcog": 1,
    }

    deriver = AttributeDeriver()
    deriver.curate(uds_table, "uds")
    assert (
        uds_table["file.info.derived.naccarte"]
        == np_table["subject.info.derived.np_arte"]
    )
    assert (
        uds_table["file.info.derived.naccbraa"]
        == np_table["subject.info.derived.np_braa"]
    )
    assert (
        uds_table["file.info.derived.nacchem"]
        == np_table["subject.info.derived.np_hem"]
    )
    assert (
        uds_table["file.info.derived.nacclewy"]
        == np_table["subject.info.derived.np_lewy"]
    )
    assert (
        uds_table["file.info.derived.naccmicr"]
        == np_table["subject.info.derived.np_micr"]
    )
    assert (
        uds_table["file.info.derived.naccneur"]
        == np_table["subject.info.derived.np_neur"]
    )


def test_ncrad_apoe():
    """Test against NCRAD APOE, which just derives APOE."""
    form = SymbolTable()
    form["file.info.raw"] = {"a1": "E4", "a2": "E2"}

    deriver = AttributeDeriver()
    deriver.curate(form, "apoe")
    assert form["subject.info.genetics"] == {"apoe": 5}
    assert form["subject.info.derived"] == {"naccapoe": 5}


def test_niagads_investigator():
    """Test against NIAGADS investigator data."""
    form = SymbolTable()
    form["file.info.raw"] = {
        "niagads_gwas": "NG00000",
        "niagads_exomechip": "NG00000, NG00001",
        "niagads_wgs": "0",
        "niagads_wes": None,
    }

    deriver = AttributeDeriver()
    deriver.curate(form, "niagads_availability")

    assert "file.info.derived" not in form
    assert form["subject.info.derived"] == {
        "niagads_exome": 1,
        "niagads_gwas": 1,
        "niagads_wes": 0,
        "niagads_wgs": 0,
    }
    assert form["subject.info.genetics"] == {
        "ngdsgwas": True,
        "ngdsexom": True,
        "ngdswgs": False,
        "ngdswes": False,
    }


def test_scan_mri_qc():
    """Test against minimal SCAN MRI QC data."""
    form = SymbolTable()
    form["file.info.raw"] = {"series_type": "T1w", "study_date": "2025-01-01"}

    deriver = AttributeDeriver()
    deriver.curate(form, "scan_mri_qc")
    assert form.to_dict() == {
        "file": {"info": {"raw": {"series_type": "T1w", "study_date": "2025-01-01"}}},
        "subject": {
            "info": {
                "derived": {"scan-mri-dates": ["2025-01-01"]},
                "imaging": {
                    "mri": {"scan": {"types": ["T1w"], "count": 1, "year-count": 1}}
                },
            }
        },
    }


def test_scan_pet_qc():
    """Test against minimal SCAN PET QC data."""
    form = SymbolTable()
    form["file.info.raw"] = {"radiotracer": "2.0", "scan_date": "2025-01-01"}

    deriver = AttributeDeriver()
    deriver.curate(form, "scan_pet_qc")
    assert form["subject.info.derived"] == {"scan-pet-dates": ["2025-01-01"]}
    assert form["subject.info.imaging"] == {
        "pet": {
            "scan": {
                "types": ["amyloid"],
                "count": 1,
                "year-count": 1,
                "tracers": ["pib"],
            }
        }
    }


def test_scan_mri_sbm():
    """Test against minimal SCAN MRI SBM data."""
    form = SymbolTable()
    form["file.info.raw"] = {"cerebrumtcv": "2.5", "wmh": "3.5", "scandt": "2025-01-01"}

    deriver = AttributeDeriver()
    deriver.curate(form, "scan_mri_sbm")
    assert form.to_dict() == {
        "file": {
            "info": {
                "raw": {"cerebrumtcv": "2.5", "wmh": "3.5", "scandt": "2025-01-01"}
            }
        },
        "subject": {
            "info": {
                "imaging": {
                    "mri": {
                        "scan": {
                            "t1": {"brain-volume": True},
                            "flair": {"wmh": True},
                            "analysis-types": ["flair_wmh", "t1_volume"],
                        }
                    }
                }
            }
        },
    }


def test_scan_amyloid_gaain():
    """Test against minimal SCAN PET Amyloid GAAIN data."""
    form = SymbolTable()
    form["file.info.raw"] = {
        "tracer": "3.0",
        "centiloids": "1.5",
        "gaain_summary_suvr": "2.703",
        "amyloid_status": "1",
        "scandate": "2025-01-01",
    }

    # also test aggregation works as expected on analysis-types
    form["subject.info.imaging.pet.scan.analysis-types"] = [
        "amyloid_npdka_suvr",
        "fdg_npdka_suvr",
        "tau_npdka_suvr",
    ]

    deriver = AttributeDeriver()
    deriver.curate(form, "scan_amyloid_pet_gaain")
    assert form.to_dict() == {
        "file": {
            "info": {
                "raw": {
                    "tracer": "3.0",
                    "centiloids": "1.5",
                    "gaain_summary_suvr": "2.703",
                    "amyloid_status": "1",
                    "scandate": "2025-01-01",
                }
            }
        },
        "subject": {
            "info": {
                "imaging": {
                    "pet": {
                        "scan": {
                            "amyloid": {
                                "centiloid": {"min": 1.5},
                                "florbetapir": {  # tracer == 3.0
                                    "centiloid": {"min": 1.5}
                                },
                                "positive-scans": True,
                            },
                            "analysis-types": [
                                "amyloid_gaain_centiloid_suvr",
                                "amyloid_npdka_suvr",
                                "fdg_npdka_suvr",
                                "tau_npdka_suvr",
                            ],
                        }
                    }
                }
            }
        },
    }
