"""
NIAGAD-specific derived variables.

Right now these should all come from the imported GWAS data under
    <subject>_niagads_availability.json
"""
from nacc_attribute_deriver.symbol_table import SymbolTable


def _create_ngdsgwas(table: SymbolTable) -> int:
    """NIAGADS GWAS investigator availability.

    Location:
        file.info.derived.ngdsgwas
    Event:
        update
    Type:
        cross-sectional
    Description:
        GWAS available at NIAGADS (y/n)
    """
    return 1 if table.get('niagads.info.raw.niagads_gwas') else 0

def _create_ngdsexom(table: SymbolTable) -> int:
    """NIAGADS ExomeChip investigator availability.

    Location:
        file.info.derived.ngdsexom
    Event:
        update
    Type:
        cross-sectional
    Description:
        ExomeChip available at NIAGADS (y/n)
    """
    return 1 if table.get('niagads.info.raw.niagads_exomechip') else 0

def _create_ngdswgs(table: SymbolTable) -> int:
    """NIAGADS WGS investigator availability.

    Location:
        file.info.derived.ngdswgs
    Event:
        update
    Type:
        cross-sectional
    Description:
        Whole genome sequencing available at NIAGADS (y/n)
    """
    return 1 if table.get('niagads.info.raw.niagads_wgs') else 0

def _create_ngdswes(table: SymbolTable) -> int:
    """NIAGADS WES investigator availability.

    Location:
        file.info.derived.ngdswes
    Event:
        update
    Type:
        cross-sectional
    Description:
        Whole exome sequencing available at NIAGADS (y/n)
    """
    return 1 if table.get('niagads.info.raw.niagads_wes') else 0
