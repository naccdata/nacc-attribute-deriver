"""Tests against the full schema end-to-end.

Mainly sanity checks to make sure modules run at all. Does not test UDS
due to its complexity/length.
"""

from nacc_attribute_deriver.attribute_deriver import AttributeDeriver
from nacc_attribute_deriver.symbol_table import SymbolTable


def test_uds_form(uds_table):
    """UDS is more of a runnable sanity check."""
    uds_table["file.info.forms.json"].update(
        {
            "normcog": 0,
            "impnomci": 1,
            "cdrglob": 1,
            "sex": "1",
            "primlang": 1,
            "educ": 1,
            "probad": 1,
        }
    )
    uds_table.update(
        {
            "subject": {
                "info": {
                    "derived": {
                        "cross-sectional": {
                            "naccnihr": 1,
                            "naccdage": 1,
                            "naccdied": 1,
                        },
                    },
                    "working": {
                        "cross-sectional": {
                            "uds-visitdates": ["2025-01-01"],
                        }
                    },
                }
            },
        }
    )

    deriver = AttributeDeriver()
    deriver.curate(uds_table, "uds")


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
    np_table["file.info.forms.json.formver"] = 11.0

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
                        "formver": 11.0,
                    }
                },
            }
        },
        "subject": {
            "info": {
                "derived": {
                    "cross-sectional": {
                        "naccbraa": 9,
                        "naccneur": 9,
                        "naccmicr": 9,
                        "nacchem": 9,
                        "naccarte": 9,
                        "nacclewy": 9,
                        "naccamy": 9,
                        "naccavas": 9,
                        "naccbrnn": 0,
                        "nacccbd": 9,
                        "naccdiff": 9,
                        "naccdown": 7,
                        "naccinf": 9,
                        "naccnec": 9,
                        "naccothp": 9,
                        "naccpick": 9,
                        "naccprio": 9,
                        "naccprog": 9,
                        "naccvasc": 9,
                    },
                },
                "working": {
                    "cross-sectional": {
                        "np-death-age": 80,
                        "np-death-date": "2024-12-19",
                        "np-form-date": "2025-01-01",
                    }
                },
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
        "formver": 3.0,
    }


def test_ncrad_apoe():
    """Test against NCRAD APOE, which just derives APOE."""
    form = SymbolTable()
    form["file.info.raw"] = {"a1": "E4", "a2": "E2"}

    deriver = AttributeDeriver()
    deriver.curate(form, "apoe")
    assert form["subject.info.derived.cross-sectional"] == {
        "naccapoe": 5,
        "naccne4s": 1,
    }


def test_niagads_investigator():
    """Test against NIAGADS investigator data."""
    form = SymbolTable()
    form["file.info.raw"] = {
        "niagads_gwas": "NG00000",
        "niagads_exomechip": "NG00000, NG00001",
        "niagads_wgs": "0",
        "niagads_wes": 0,
    }

    deriver = AttributeDeriver()
    deriver.curate(form, "niagads_availability")

    assert "file.info.derived" not in form
    assert form["subject.info.derived.cross-sectional"] == {
        "ngdsexom": 1,
        "ngdsgwas": 1,
        "ngdswes": 0,
        "ngdswgs": 0,
        "ngdsgwac": "NG00000",
        "ngdsexac": "NG00000, NG00001",
        "ngdswgac": "88",
        "ngdsweac": "88",
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
                "working": {"cross-sectional": {"scan-mri-dates": ["2025-01-01"]}},
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
    assert form["subject.info.working.cross-sectional"] == {
        "scan-pet-dates": ["2025-01-01"]
    }
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


def test_meds():
    """Test against minimal MEDS data."""
    form = SymbolTable()
    form["file.info.forms.json"] = {
        "frmdatea4g": "2000-01-01",
        "drugs_list": "d00004,d00170",
        "module": "MEDS",
        "formver": 3.0,
    }

    deriver = AttributeDeriver()
    deriver.curate(form, "meds")
    assert form.to_dict() == {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "frmdatea4g": "2000-01-01",
                        "drugs_list": "d00004,d00170",
                        "module": "MEDS",
                        "formver": 3.0,
                    }
                }
            }
        },
        "subject": {
            "info": {
                "working": {
                    "longitudinal": {
                        "drugs-list": [
                            {"date": "2000-01-01", "value": ["d00004", "d00170"]}
                        ]
                    }
                }
            }
        },
    }


def test_cls():
    """Test against minimal CLS data."""
    form = SymbolTable()
    form["file.info.forms.json"] = {
        "visitdate": "2025-01-01",
        "module": "CLS",
        "formver": 3.0,
        "aspkengl": 5,
        "areaengl": 2,
        "awriengl": 4,
        "aundengl": 1,
        "aspkspan": 1,
        "areaspan": 4,
        "awrispan": 7,
        "aundspan": 3,
    }

    deriver = AttributeDeriver()
    deriver.curate(form, "cls")
    assert form.to_dict() == {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "visitdate": "2025-01-01",
                        "module": "CLS",
                        "formver": 3.0,
                        "aspkengl": 5,
                        "areaengl": 2,
                        "awriengl": 4,
                        "aundengl": 1,
                        "aspkspan": 1,
                        "areaspan": 4,
                        "awrispan": 7,
                        "aundspan": 3,
                    }
                }
            }
        },
        "subject": {
            "info": {"derived": {"cross-sectional": {"naccengl": 3.0, "naccspnl": 3.8}}}
        },
    }


def test_ftld():
    """Test against minimal FTLD data."""
    form = SymbolTable()
    form["file.info.forms.json"] = {"module": "FTLD", "visitdate": "2025-01-01"}

    deriver = AttributeDeriver()
    deriver.curate(form, "ftld")

    assert form.to_dict() == {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "module": "FTLD",
                        "visitdate": "2025-01-01",
                    }
                }
            }
        },
        "subject": {"info": {"derived": {"cross-sectional": {"naccftd": 1}}}},
    }


def test_lbd():
    """Test against minimal LBD data."""
    form = SymbolTable()
    form["file.info.forms.json"] = {"module": "LBD", "visitdate": "2025-01-01"}

    deriver = AttributeDeriver()
    deriver.curate(form, "lbd")

    assert form.to_dict() == {
        "file": {
            "info": {
                "forms": {
                    "json": {
                        "module": "LBD",
                        "visitdate": "2025-01-01",
                    }
                }
            }
        },
        "subject": {"info": {"derived": {"cross-sectional": {"nacclbdm": 1}}}},
    }
