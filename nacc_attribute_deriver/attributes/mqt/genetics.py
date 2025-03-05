"""
All genetics MQT derived variables.
Assumes NACC-derived variables are already set
"""
from typing import Dict, Tuple
from nacc_attribute_deriver.attributes.attribute_collection import MQTAttribute


class GeneticAttribute(MQTAttribute):
    """Class to collect genetic attributes."""

    def _create_apoe(self) -> str:
        """Mapped from NACCAPOE

        Location:
            subject.info.genetics.naccapoe
        Operation:
            update
        Type:
            genetics
        Description:
            APOE genotype
        """
        a1 = self.table.get('ncrad.info.raw.a1')
        a2 = self.table.get('ncrad.info.raw.a2')

        if not a1 or not a2:
            return 'Missing/unknown/not assessed'

        return f'{a1},{a2}'.lower()

    def _create_ngdsgwas_mqt(self) -> bool:
        """Mapped from NGDSGWAS

        Location:
            subject.info.genetics.ngdsgwas
        Operation:
            update
        Type:
            genetics
        Description:
            GWAS available at NIAGADS
        """
        result = self.assert_required(['ngdsgwas'])
        return bool(result['ngdsgwas'])

    def _create_ngdsexom_mqt(self) -> bool:
        """Mapped from NGDSEXOM

        Location:
            subject.info.genetics.ngdsexom
        Operation:
            update
        Type:
            genetics
        Description:
            ExomeChip available at NIAGADS
        """
        result = self.assert_required(['ngdsexom'])
        return bool(result['ngdsexom'])

    def _create_ngdswgs_mqt(self) -> bool:
        """Mapped from NGDSWGS

        Location:
            subject.info.genetics.ngdswgs
        Operation:
            update
        Type:
            genetics
        Description:
            Whole genome sequencing available at NIAGADS
        """
        result = self.assert_required(['ngdswgs'])
        return bool(result['ngdswgs'])

    def _create_ngdswes_mqt(self) -> bool:
        """Mapped from NGDSWES

        Location:
            subject.info.genetics.ngdswes
        Operation:
            update
        Type:
            genetics
        Description:
            Whole exome sequencing available at NIAGADS
        """
        result = self.assert_required(['ngdswes'])
        return bool(result['ngdswes'])
