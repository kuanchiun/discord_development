from dataclasses import dataclass, field
from typing import Optional, Dict, List, Union

from .equipment import Equipment

@dataclass
class EquipInventory:
    weapon: List["Equipment"] = field(default_factory = [])
    head: List["Equipment"] = field(default_factory = [])
    chest: List["Equipment"] = field(default_factory = [])
    leggings: List["Equipment"] = field(default_factory = [])
    feet: List["Equipment"] = field(default_factory = [])
    
    earring: List["Equipment"] = field(default_factory = [])
    necklace: List["Equipment"] = field(default_factory = [])
    bracelet: List["Equipment"] = field(default_factory = [])
    ring: List["Equipment"] = field(default_factory = [])
    
    def get_equipment(self, slot, index) -> "Equipment":
        if not hasattr(self, slot):
            raise ValueError(f"❌ 無效的裝備欄位: {slot}")
        
        return getattr(self, slot)[index]
    
    def get_slot(self, slot) -> List["Equipment"]:
        if not hasattr(self, slot):
            raise ValueError(f"❌ 無效的裝備欄位: {slot}")
        
        return getattr(self, slot)