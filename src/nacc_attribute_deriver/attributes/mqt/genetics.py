"""
All genetics MQT derived variables.
Assumes NACC-derived variables are already set
"""
from typing import Dict, Tuple
from nacc_attribute_deriver.attributes.attribute_collection import (
    MQTAttribute,
)


class GeneticAttribute(MQTAttribute):
    """Class to collect genetic attributes."""

    # this encoding is also in the apoe_transformer gear
    # 2 options: 1. Keep a1/a2 in that gear's output/metadata so we don't have to map back
    #            2. Pull this same mapping in the gear
    APOE_ENCODINGS: Dict[Tuple[str, str], int] = {
        ("E3", "E3"): 1,
        ("E3", "E4"): 2,
        ("E4", "E3"): 2,
        ("E3", "E2"): 3,
        ("E2", "E3"): 3,
        ("E4", "E4"): 4,
        ("E4", "E2"): 5,
        ("E2", "E4"): 5,
        ("E2", "E2"): 6
    }

    def _create_apoe(self) -> str:
        """Mapped from NACCAPOE

        Location:
            subject.info.genetics.naccapoe
        Event:
            update
        Type:
            genetics
        Description:
            APOE genotype
        """
        result = self.assert_required(['naccapoe'])

        for encoding, value in self.APOE_ENCODINGS.items():
            if value == result['naccapoe']:
                return f'{encoding[0]},{encoding[1]}'.lower()

        return 'Missing/unknown/not assessed'

    def _create_ngdsgwas_mqt(self) -> bool:
        """Mapped from NGDSGWAS

        Location:
            subject.info.genetics.ngdsgwas
        Event:
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
        Event:
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
        Event:
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
        Event:
            update
        Type:
            genetics
        Description:
            Whole exome sequencing available at NIAGADS
        """
        result = self.assert_required(['ngdswes'])
        return bool(result['ngdswes'])
