"""
All demographic MQT derived variables.
Assumes NACC-derived variables are already set
"""
from datetime import timedelta
from nacc_attribute_deriver.attributes.utils.utils import (
    assert_required
)
from nacc_attribute_deriver.symbol_table import SymbolTable

SEX_MAPPING = {
    1: 'Male',
    2: 'Female',
    8: 'Prefer not to answer',
    9: "Don't know"
}

RACE_MAPPING = {
    1: 'White',
    2: 'Black or African American',
    3: 'American Indian or Alaska Native',
    4: 'Native Hawaiian or Pacific Islander',
    5: 'Asian',
    6: 'Multiracial',
    7: 'Middle Eastern or Northern African',
    8: 'Hispanic or Latino',  # TODO for UDSv4?
    99: 'Unknown or ambiguous'
}

PRIMARY_LANGUAGE_MAPPING = {    
    1: "English",
    2: "Spanish",
    3: "Mandarin",
    4: "Cantonese",
    5: "Russian",
    6: "Japanese",
    8: "Other primary language (specify)",
    9: "Unknown"
}

def _create_uds_age(table: SymbolTable) -> int:
    """UDS age at form date, mapped from NACCAGE

    Location:
        subject.info.demographics.uds.age.initial
        subject.info.demographics.uds.age.latest
    Event:
        initial
        latest
    Type:
        demographics
    Description:
        Age at UDS visit
    """
    result = assert_required('create_uds_age', ['naccage'], table)
    return result['naccage']


def _create_uds_sex(table: SymbolTable) -> str:
    """UDS sex

    Location:
        subject.info.demographics.uds.sex.latest
    Event:
        latest
    Type:
        demographics
    Description:
        Sex at UDS visit
    """
    sex = table.get('file.info.forms.json.sex')
    if sex is None:
        return None

    try:
        return SEX_MAPPING.get(int(sex), None)
    except TypeError:
        return None

    return None


def _create_uds_race(table: SymbolTable) -> str:
    """UDS race

    Location:
        subject.info.demographics.uds.race.latest
    Event:
        latest
    Type:
        demographics
    Description:
        Race at UDS visit
    """
    result = assert_required('create_uds_race', ['naccnihr'], table)
    return RACE_MAPPING.get(result['naccnihr'], 'Unknown or ambiguous')


def _create_uds_primary_language(table: SymbolTable) -> str:
    """UDS primary language

    Location:
        subject.info.demographics.uds.primary-language.latest
    Event:
        latest
    Type:
        demographics
    Description:
        Primary language at UDS visit
    """
    primlang = table.get('file.info.form.json.primlang', 9)
    return PRIMARY_LANGUAGE_MAPPING.get(primlang, 'Unknown')


def _create_uds_education_level(table: SymbolTable) -> int:
    """UDS education level

    Location:
        subject.info.demographics.uds.education-level.latest
    Event:
        latest
    Type:
        demographics
    Description:
        Primary language at UDS visit
    """
    return table.get('file.info.form.json.educ', None)


def _create_age_at_death(table: SymbolTable) -> int:
    """Age at death, mapped from NACCDAGE

    Location:
        subject.info.derived.naccdage
    Event:
        update
    Type:
        demographics
    Description:
        Age at death
    """
    result = assert_required('create_age_at_death', ['naccdage'], table)
    return result['naccdage']


def _create_vital_status(table: SymbolTable) -> str:
    """Creates subject.info.demographics.uds.vital-status.latest

    TODO: sure what this comes from/what it's supposed to look like?

    Location:
        TODO
    Event:
        update
    Type:
        demographics
    Description:
        Vital status
    """
    pass
