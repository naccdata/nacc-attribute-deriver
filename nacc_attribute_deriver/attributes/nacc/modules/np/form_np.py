"""Derived variables from neuropathology form"""
from .np_attribute import NPAttribute


class NPFormAttribute(NPAttribute):
    def _create_naccdage(self) -> int:
        return 0
    
    # Braak stage
    def _create_naccbraa(self) -> int:
        return 0
    
    # C score
    def _create_naccneur(self) -> int:
        return 0
    
    # Microinfarcts
    def _create_naccmicr(self) -> int:
        return 0
    
    # Hemmorrhages and microbleeds
    def _create_naccchem(self) -> int:
        return 0
    
    # Arteriosclerosis
    def _create_naccarte(self) -> int:
        return 0    
    
    # Lewy body disease
    def _create_nacclewy(self) -> int:
        return 0