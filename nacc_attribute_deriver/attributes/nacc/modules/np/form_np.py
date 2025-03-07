"""Derived variables from neuropathology form"""
from nacc_attribute_deriver.symbol_table import SymbolTable

from .np_attribute import NPAttribute


class NPFormAttribute(NPAttribute):
    def __init__(self,
                 table: SymbolTable,
                 np_prefix: str = 'np.info.forms.json.') -> None:
        """Override initializer to set NP module prefix."""
        super().__init__(table, np_prefix)
    
    def _mapgross(self, new) -> int:
        npgross = self.get_value('npgross')
        if npgross == 2:
            new = 0
        elif npgross == 9:
            new = 9
        return new
        
    def _mapsub4(self, old, new) -> int:
        if old in [1, 2, 3, 4]:
            new = 4 - old
        elif old == 5:
            new = 8
        else:
            new = 9
        return new
    
    def _mapv9(self, old, new) -> int:
        if old == 1:
            new = 1
        elif old == 2:
            new = 0
        elif old == 3:
            new = 8
        else:
            new = 9
        return new
    
    def _mapvasc(self, new) -> int:
        npgross = self.get_value('npgross')
        npvasc = self.get_value('npvasc')
        if npgross == 2 or npvasc == 2:
            new = 0
        elif npgross == 9 or npvasc == 9:
            new = 9
        elif npvasc == 3:
            new = 8
        return new
    
    def _mapsub1(self, old, new):
        if old in [1, 2, 3, 4]:
            new = old - 1
        elif old == 5:
            new = 8
        else:
            new = 9
        return new
    
    def _maplewy(self) -> int:
        nplewy = self.get_value('nplewy')
        new = nplewy
        if nplewy == 5:
            new = 0
        if nplewy == 6:
            new = 8
        return new
            
    def _create_naccbraa(self) -> int:
        """Create the NACCBRAA variable

        Location:
            file.info.derived.naccbraa
        Operation:
            update
        Type:
            cross-sectional
        Description:
            Braak stage for neurofibrillary degeneration (B score)
        """        
        formver = self.get_value('formver')
        npbraak = self.get_value('npbraak', None)
        naccbraa = npbraak
        
        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            if npbraak == 7:
                naccbraa = 0
        elif formver == 1:
            if npbraak:
                if npbraak == 7:
                    naccbraa = 0
            else:
                naccbraa = self._mapgross(naccbraa)
                
        return naccbraa
        
    def _create_naccneur(self) -> int:
        """Create the NACCNEUR variable

        Location:
            file.info.derived.naccneur
        Operation:
            update
        Type:
            cross-sectional
        Description:
            Density of neocortical neuritic plaques (CERAD score) (C score)
        """           
        formver = self.get_value('formver')
        npneur = self.get_value('npneur', None)
        naccneur = npneur
        
        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            naccneur = self._mapsub4(npneur, naccneur)
        elif formver == 1:
            if npneur:
                naccneur = self._mapsub4(npneur, naccneur)
            else:
                naccneur = self._mapgross(naccneur)
        
        return naccneur
    
    def _create_naccmicr(self) -> int:
        """Create the NACCMICR variable

        Location:
            file.info.derived.naccmicr
        Operation:
            update
        Type:
            cross-sectional
        Description:
            Microinfarcts
        """           
        formver = self.get_value('formver')
        npold = self.get_value('npold', None)
        npmicro = self.get_value('npmicro', None)
        
        naccmicr = npold
        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:
            naccmicr = self._mapv9(npold, naccmicr)
        elif formver == 1:
            if npold:
                naccmicr = self._mapv9(npmicro, naccmicr)
            else:
                naccmicr = self._mapvasc(naccmicr)
        
        return naccmicr
    
    def _create_nacchem(self) -> int:
        """Create the NACCHEM variable

        Location:
            file.info.derived.nacchem
        Operation:
            update
        Type:
            cross-sectional
        Description:
            Hemorrhages and microbleeds
        """           
        formver = self.get_value('formver')
        nphem = self.get_value('nphem', None)        

        if formver in [10, 11]:
            nphemo = self.get_value('nphemo', None)
            npoldd = self.get_value('npoldd', None)            
            if nphemo == 1 or npoldd == 1:
                nacchem = 1
            elif nphemo == 0 and npoldd == 0:
                nacchem = 0
            elif nphemo == 8 and npoldd == 8:
                nacchem = 8
            else:
                nacchem = 9
        elif formver in [7, 8, 9]:
            nacchem = nphem           
            nacchem = self._mapv9(nphem, nacchem)
        elif formver == 1:
            nacchem = nphem
            if nphem:
                nacchem = self._mapv9(nphem, nacchem)
            else:
                nacchem = self._mapvasc(nacchem)
        
        return nacchem        
    
    def _create_naccarte(self) -> int:
        """Create the NACCARTE variable

        Location:
            file.info.derived.naccarte
        Operation:
            update
        Type:
            cross-sectional
        Description:
            Arteriolosclerosis
        """           
        formver = self.get_value('formver')
        nparter = self.get_value('nparter', None)
        naccarte = nparter

        if formver in [10, 11]:
            pass
        elif formver in [7, 8, 9]:          
            naccarte = self._mapsub1(nparter, naccarte)
        elif formver == 1:
            if nparter:
                naccarte = self._mapsub1(nparter, naccarte)
            else:
                naccarte = self._mapvasc(naccarte)
        
        return naccarte    
    
    def _create_nacclewy(self) -> int:
        """Create the NACCLEWY variable

        Location:
            file.info.derived.nacclewy
        Operation:
            update
        Type:
            cross-sectional
        Description:
            Lewy body disease
        """           
        formver = self.get_value('formver')

        if formver in [10, 11]:
            nplbod = self.get_value('nplbod', None)
            nacclewy = nplbod
            if nplbod == 4:
                nacclewy = 2
            if nplbod == 5:
                nacclewy = 4
        elif formver in [7, 8, 9]:          
            nacclewy = self._maplewy()
        elif formver == 1:
            nplewy = self.get_value('nplewy', None)
            if nplewy:
                nacclewy = self._maplewy()
            else:
                nacclewy = nplewy
                nacclewy = self._mapgross(nacclewy)
        
        return nacclewy  