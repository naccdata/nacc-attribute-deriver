"""NIAGAD-specific derived variables.

Right now these should all come from the imported GWAS data under
<subject>_niagads_availability.json
"""

from nacc_attribute_deriver.attributes.attribute_collection import AttributeCollection
from nacc_attribute_deriver.attributes.base.namespace import RawNamespace
from nacc_attribute_deriver.symbol_table import SymbolTable


class NIAGADSAttributeCollection(AttributeCollection):
    """Class to collect NIAGADS attributes."""

    def __init__(self, table: SymbolTable) -> None:
        """Override initializer to set prefix to NIAGADS-specific data."""
        self.__niagads = RawNamespace(
            table,
            required=frozenset(
                [
                    "niagads_gwas",
                    "niagads_exomechip",
                    "niagads_wgs",
                    "niagads_wes",
                ]
            ),
        )

    def _evaluate_investigator_status(self, attribute: str) -> int:
        """Evaluate investigator status. If 0, return 0, otherwise it's assumed
        to be an investigator ID (e.g. NG00000) and return 1.

        Args:
            attribute: name of attribute
        """
        value = self.__niagads.get_required(attribute, str)
        return 1 if value != "0" else 0

    def _create_ngdsgwas(self) -> int:
        """NIAGADS GWAS investigator availability."""
        return self._evaluate_investigator_status("niagads_gwas")

    def _create_ngdsexom(self) -> int:
        """NIAGADS ExomeChip investigator availability."""
        return self._evaluate_investigator_status("niagads_exomechip")

    def _create_ngdswgs(self) -> int:
        """NIAGADS WGS investigator availability."""
        return self._evaluate_investigator_status("niagads_wgs")

    def _create_ngdswes(self) -> int:
        """NIAGADS WES investigator availability."""
        return self._evaluate_investigator_status("niagads_wes")

    def _evaluate_accession(self, attribute: str) -> str:
        """Evaluate accession number. Returns 88 if missing.

        Args:
            attribute: name of attribute
        """
        value = self.__niagads.get_required(attribute, str)
        return "88" if not value or value == "0" else value

    def _create_ngdsgwac(self) -> str:
        """NGDSGWAC - NIAGADS GWAS accession number."""
        return self._evaluate_accession("niagads_gwas")

    def _create_ngdsexac(self) -> str:
        """NGDSEXAC - NIAGADS ExomeChip accession number."""
        return self._evaluate_accession("niagads_exomechip")

    def _create_ngdswgac(self) -> str:
        """NGDSWGAC - NIAGADS whole genome sequencing accession number."""
        return self._evaluate_accession("niagads_wgs")

    def _create_ncdsweac(self) -> str:
        """NCDSWEAC - NIAGADS whole exome sequencing accession number."""
        return self._evaluate_accession("niagads_wes")
