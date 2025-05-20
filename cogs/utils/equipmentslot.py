from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple

from .equipment import Equipment
from .equipinventory import EquipInventory

@dataclass
class EquipmentSlot:
    weapon: Optional["Equipment"] = None
    head: Optional["Equipment"] = None
    chest: Optional["Equipment"] = None
    leggings: Optional["Equipment"] = None
    feet: Optional["Equipment"] = None
    
    earring: Optional["Equipment"] = None
    necklace: Optional["Equipment"] = None
    bracelet: Optional["Equipment"] = None
    ring1: Optional["Equipment"] = None
    ring2: Optional["Equipment"] = None
    
    def is_already_equipped(self, slot):
        if not hasattr(self, slot):
            raise ValueError(f"❌ 無效的裝備欄位: {slot}")
        
        return getattr(self, slot) is not None
        
    def equip(self, 
              slot: str, 
              equipment: "Equipment", 
              equipinventory: "EquipInventory"):
        
        if getattr(self, slot):
            old_equipment = getattr(self, slot)
            setattr(equipinventory, 
                    slot, 
                    getattr(equipinventory, slot).append(equipment))
            
        setattr(self, slot, equipment)
    
    