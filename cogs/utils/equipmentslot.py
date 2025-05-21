from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple

from .equipment import Equipment
from .equipinventory import EquipInventory

SLOTS = [
    "weapon", "head", "chest", "leggings", "feet",
    "earring", "necklace", "bracelet", "ring1", "ring2"
]

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
    
    def to_dict(self):
        return {
            "weapon":   self.weapon.to_dict(),
            "head":     self.head.to_dict(),
            "chest":    self.chest.to_dict(),
            "leggings": self.leggings.to_dict(),
            "feet":     self.feet.to_dict(),
            "earring":  self.earring.to_dict(),
            "necklace": self.necklace.to_dict(),
            "bracelet": self.bracelet.to_dict(),
            "ring1":    self.ring1.to_dict(),
            "ring2":    self.ring2.to_dict()
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            weapon   = Equipment.from_dict(data["weapon"])   if data.get("weapon")   else None,
            head     = Equipment.from_dict(data["head"])     if data.get("head")     else None,
            chest    = Equipment.from_dict(data["chest"])    if data.get("chest")    else None,
            leggings = Equipment.from_dict(data["leggings"]) if data.get("leggings") else None,
            feet     = Equipment.from_dict(data["feet"])     if data.get("feet")     else None,
            earring  = Equipment.from_dict(data["earring"])  if data.get("earring")  else None,
            necklace = Equipment.from_dict(data["necklace"]) if data.get("necklace") else None,
            bracelet = Equipment.from_dict(data["bracelet"]) if data.get("bracelet") else None,
            ring1    = Equipment.from_dict(data["ring1"])    if data.get("ring1")    else None,
            ring2    = Equipment.from_dict(data["ring2"])    if data.get("ring2")    else None,
        )
    
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
            getattr(equipinventory, slot).append(old_equipment)
            
        setattr(self, slot, equipment)
    
    