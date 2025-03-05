"""
NCRAD-specific derived variables.

Right now these should all come from the imported APOE data under
    <subject>_apoe_availability.json
"""
from nacc_attribute_deriver.attributes.attribute_collection import NACCAttribute
from nacc_attribute_deriver.symbol_table import SymbolTable


class NCRADAttribute(NACCAttribute):
    """Class to collect NCRAD attributes."""

    def __init__(self,
                 table: SymbolTable,
                 form_prefix: str = 'ncrad.info.raw.') -> None:
        """Override initializer to set prefix to NCRAD-specific data.
        """
        super().__init__(table, form_prefix)

    def _create_naccapoe(self) -> int:
        """Comes from derive.sas and derivenew.sas (same code)

        Should come from the actual imported APOE data
            <subject>_apoe_availability.json

        Location:
            file.info.derived.naccapoe
        Operation:
            update
        Type:
            cross-sectional
        Description:
            APOE genotype
        """
        return self.get_value('apoe', 9)
