"""
Derived variables from form D1.
"""
from typing import List
from nacc_attribute_deriver.attributes.utils.utils import (
    is_int_value
)
from nacc_attribute_deriver.symbol_table import SymbolTable


####################################
# Helper functions/mappings for D1 #
####################################

class ContributionStatus:
    PRIMARY = 1
    CONTRIBUTING = 2
    NON_CONTRIBUTING = 3

    @classmethod
    def all(cls):
        """Returns all possible statuses."""
        return [
            cls.PRIMARY,
            cls.CONTRIBUTING,
            cls.NON_CONTRIBUTING
        ]

def get_contr_status(table: SymbolTable, fields: List[str]) -> int:
    """Gets the overall contributing status based on the given list.
    Assumes all fields have values null or
        1, 2, or 3 (primary, contributing, or non-contributing)

    Args:
        table: Table with all FW metadata
        fields: Fields to get overall status from
    Returns:
        The overall contributed status, None if none satisfy
    """
    all_statuses = []

    for field in fields:
        all_statuses.append(table.get(f'file.info.forms.json.{field}'))

    for i in ContributionStatus.all():
        if any([x == i for x in all_statuses]):
            return i

    return None


#################################################
# Helper variables to calculate other variables #
#################################################

def _create_mci(table: SymbolTable) -> int:
    """Create MCI, which is not a derived variable itself but
    is used to calculate other derived variables.

    Location:
        tmp.mci
    Event:
        update
    Type:
        intermediate
    Description:
        Mild cognitive impairment
    """

    # all of these fields are null, 0, or 1
    return 1 if any([
        table.get('file.info.forms.json.mciamem'),
        table.get('file.info.forms.json.mciaplus'),
        table.get('file.info.forms.json.mcinon1'),
        table.get('file.info.forms.json.mcinon2')
    ]) else 0


##########################
# NACC DERIVED VARIABLES #
##########################

def _create_naccalzp(table: SymbolTable) -> int:
    """From d1structrdd.sas

    Location:
        file.info.derived.naccalzp
    Event:
        update
    Type:
        longitudinal
    Description:
        Primary, contributing, or non-contributing cause of observed
        cognitive impairment -- Alzheimer's disease (AD)
    """
    if table.get('file.info.forms.json.normcog') == 1:
        return 8

    contr_status = get_contr_status(table, ['probadif', 'possadif', 'alzdisif'])
    if contr_status:
        return contr_status

    # default
    return 7

def _create_nacclbde(table: SymbolTable) -> int:
    """From d1structrdd.sas

    Location:
        file.info.derived.nacclbde
    Event:
        update
    Type:
        longitudinal
    Description:
        Presumptive etilogic diagnosis of the cognitive disorder
        - Lewy body disease (LBD)
    """
    if table.get('file.info.forms.json.normcog') == 1:
        return 8

    if table.get('file.info.forms.json.formver') != 3:
        dlb = table.get('file.info.forms.json.dlb')
        park = table.get('file.info.forms.json.park')

        if dlb == 1 or park == 1:
            return 1
        if dlb == 0 and park == 0:
            return 0

    lbdis = table.get('file.info.forms.json.formver')
    if lbdis in [0, 1]:
        return lbdis

    return None

def _create_nacclbdp(table: SymbolTable) -> int:
    """From d1structrdd.sas. Also relies on another derived variable nacclbde

    Location:
        file.info.derived.nacclbdp
    Event:
        update
    Type:
        longitudinal
    Description:
        Primary, contributing, or non-contributing cause of
        cognitive impairment -- Lewy body disease (LBD)
    """
    if table.get('file.info.forms.json.normcog') == 1:
        return 8

    if table.get('file.info.forms.json.formver') != 3:
        contr_status = get_contr_status(table, ['dlbif', 'parkif'])
        if contr_status:
            return contr_status

    contr_status = get_contr_status(table, ['lbdif'])
    if contr_status:
        return contr_status

    if _create_nacclbde(table) == 0:
        return 7

    return None

def _create_naccudsd(table: SymbolTable) -> int:
    """From Create NACCUDSD.R which in turn is from derive.sas.

    Location:
        file.info.derived.naccudsd
    Event:
        update
    Type:
        longitudinal
    Description:
        Cognitive status at UDS visit
    """
    if _create_mci(table) == 1:
        return 3
    if table.get('file.info.forms.json.demented') == 1:
        return 4
    if table.get('file.info.forms.json.normcog') == 1:
        return 1
    if table.get('file.info.forms.json.impnomci') == 1:
        return 2

    return None

def _create_naccetpr(table: SymbolTable) -> int:
    """From Create NACCETPR, PRIMDX, SYNMULT.R which in turn
    comes from getd1all.sas

    Looking for primary status here.

    Location:
        file.info.derived.naccetpr
    Event:
        update
    Type:
        longitudinal
    Description:
        Primary etiologic diagnosis (MCI), impaired,
        not MCI, or dementia
    """

    normcog = table.get('file.info.forms.json.normcog')
    if normcog == 1:
        return 88

    # assuming normcog == 0 != 1 after this point
    formver = table.get('file.info.forms.json.formver')

    # get all statuses in a list, then return the first one that == 1 (Primary)
    # result maps to position in list (start index 1)
    all_status = [
        get_contr_status(table, ['probadif', 'possadif', 'alzdisif']),
        formver != 3 and get_contr_status(table, ['dlbif', 'parkif', 'lbdif']),
        get_contr_status(table, ['msaif']),  # could just grab directly for those with only 1 but this is more readable
        get_contr_status(table, ['pspif']),
        get_contr_status(table, ['cortif']),
        get_contr_status(table, ['ftldmoif']),
        get_contr_status(table, ['ftdif', 'ppaphif', 'ftldnoif']),
        get_contr_status(table, ['cdvif', 'vascif', 'vascpsif', 'strokeif']),
        get_contr_status(table, ['esstreif']),
        get_contr_status(table, ['downsif']),
        get_contr_status(table, ['huntif']),
        get_contr_status(table, ['prionif']),
        get_contr_status(table, ['brninjif']),
        get_contr_status(table, ['hycephif']),
        get_contr_status(table, ['epilepif']),
        get_contr_status(table, ['neopif']),
        get_contr_status(table, ['hivif']),
        get_contr_status(table, ['othcogif']),
        get_contr_status(table, ['depif']),
        get_contr_status(table, ['bipoldif']),
        get_contr_status(table, ['schizoif']),
        get_contr_status(table, ['anxietif']),
        get_contr_status(table, ['delirif']),
        get_contr_status(table, ['ptsddxif']),
        get_contr_status(table, ['othpsyif']),
        get_contr_status(table, ['alcdemif']),
        get_contr_status(table, ['impsubif']),
        get_contr_status(table, ['dysillif']),
        get_contr_status(table, ['medsif']),
        get_contr_status(table, ['cogothif', 'cogoth2f', 'cogoth3f']),
    ]

    assert len(all_status) == 30
    for i, status in enumerate(all_status):
        if is_int_value(status, ContributionStatus.PRIMARY):
            return i + 1

    # default for normcog == 0
    return 99

def _create_naccppa(table: SymbolTable) -> int:
    """From d1structdd.sas

    Location:
        file.info.derived.naccppa
    Event:
        update
    Type:
        longitudinal
    Description:
        Primary progressive aphasia (PPA) with
        cognitive impairment
    """
    ppaph = table.get('file.info.forms.json.ppaph')
    ppasyn = table.get('file.info.forms.json.ppasyn')

    if table.get('file.info.forms.json.demented') == 1:
        if ppaph == 1 or ppasyn == 1:
            return 1
        if ppaph == 0 or ppasyn == 0:
            return 0

    formver = table.get('file.info.forms.json.formver')
    nodx = table.get('file.info.forms.json.nodx')

    if table.get('file.info.forms.json.impnomci') == 1 or \
        _create_mci(table) == 1:
        if ppaph == 1 or ppasyn == 1:
            return 1
        if ppaph == 0 or ppasyn == 0:
            return 0
        if (formver != 3 and nodx == 1) or (formver == 3):
            return 7

    return 8

def _create_naccbvft(table: SymbolTable) -> int:
    """From d1structdd.sas

    Location:
        file.info.derived.naccbvft
    Event:
        update
    Type:
        longitudinal
    Description:
        Dementia syndrome -- behavioral variant
        FTD syndrome (bvFTD)
    """
    if table.get('file.info.forms.json.demented') != 1:
        return 8

    # assuming demented == 1 after this point
    ftd = table.get('file.info.forms.json.ftd')
    ftdsyn = table.get('file.info.forms.json.ftdsyn')

    if ftd in [0, 1]:
        return ftd
    if ftdsyn in [0, 1]:
        return ftdsyn

    return 8

def _create_nacclbds(table: SymbolTable) -> int:
    """From d1structdd.sas

    Location:
        file.info.derived.nacclbds
    Event:
        update
    Type:
        longitudinal
    Description:
        Dementia syndrome -- Lewy body dementia syndrome
    """
    if table.get('file.info.forms.json.demented') != 1:
        return 8

    # assuming demented == 1 after this point
    dlb = table.get('file.info.forms.json.dlb')
    lbdsyn = table.get('file.info.forms.json.lbdsyn')

    if dlb in [0, 1]:
        return ftd
    if lbdsyn in [0, 1]:
        return ftdsyn

    return 8

def _create_naccnorm(table: SymbolTable) -> int:
    """Comes from derive.sas and derivenew.sas (same code)

    This one is a static variable that needs to know if
    subject.info.derived.naccnorm exists.

    Location:
        file.info.derived.naccnorm
    Event:
        update
    Type:
        cross-sectional
    Description:
        Normal cognition at all visits to date
    """
    naccnorm = table.get('subject.info.derived.naccnorm')
    if naccnorm is not None:
        return 1 if naccnorm else 0

    # will be 0 or 1
    return table.get('file.info.forms.json.normcog')
