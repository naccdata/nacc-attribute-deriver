"""
NCRAD-specific derived variables.

Right now these should all come from the imported APOE data under
    <subject>_niagads_availability.json
"""
from nacc_attribute_deriver.symbol_table import SymbolTable


def _create_naccapoe(table: SymbolTable) -> int:
    """Comes from derive.sas and derivenew.sas (same code)

    Should come from the actual imported APOE data
        <subject>_apoe_availability.json

    Location:
        file.info.derived.naccapoe
    Event:
        update
    Type:
        cross-sectional
    Description:
        APOE genotype
    """
    return table.get('apoe.info.raw.apoe', 9)
