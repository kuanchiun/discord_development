from dataclasses import dataclass, field
from typing import Optional, Dict, List, Union

from .equipment import Equipment
from .iteminventory import ItemInventory

@dataclass
class EquipInventory:
    weapon: List["Equipment"] = field(default_factory = list)
    head: List["Equipment"] = field(default_factory = list)
    chest: List["Equipment"] = field(default_factory = list)
    leggings: List["Equipment"] = field(default_factory = list)
    feet: List["Equipment"] = field(default_factory = list)
    
    earring: List["Equipment"] = field(default_factory = list)
    necklace: List["Equipment"] = field(default_factory = list)
    bracelet: List["Equipment"] = field(default_factory = list)
    ring: List["Equipment"] = field(default_factory = list)
    
    def to_dict(self):
        return {
            "weapon":   [equip.to_dict() for equip in self.weapon],
            "head":     [equip.to_dict() for equip in self.head],
            "chest":    [equip.to_dict() for equip in self.chest],
            "leggings": [equip.to_dict() for equip in self.leggings],
            "feet":     [equip.to_dict() for equip in self.feet],
            "earring":  [equip.to_dict() for equip in self.earring],
            "necklace": [equip.to_dict() for equip in self.necklace],
            "bracelet": [equip.to_dict() for equip in self.bracelet],
            "ring":     [equip.to_dict() for equip in self.ring],
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            weapon =   [Equipment.from_dict(e) for e in data.get("weapon", [])],
            head =     [Equipment.from_dict(e) for e in data.get("head", [])],
            chest =    [Equipment.from_dict(e) for e in data.get("chest", [])],
            leggings = [Equipment.from_dict(e) for e in data.get("leggings", [])],
            feet =     [Equipment.from_dict(e) for e in data.get("feet", [])],
            earring =  [Equipment.from_dict(e) for e in data.get("earring", [])],
            necklace = [Equipment.from_dict(e) for e in data.get("necklace", [])],
            bracelet = [Equipment.from_dict(e) for e in data.get("bracelet", [])],
            ring =     [Equipment.from_dict(e) for e in data.get("ring", [])],
        )
    
    def get_equipment(self, slot, index) -> "Equipment":
        if not hasattr(self, slot):
            raise ValueError(f"❌ 無效的裝備欄位: {slot}")
        
        return getattr(self, slot)[index]
    
    def get_slot(self, slot) -> List["Equipment"]:
        if not hasattr(self, slot):
            raise ValueError(f"❌ 無效的裝備欄位: {slot}")
        
        return getattr(self, slot)
    
    def list_equipment(self) -> List["Equipment"]:
        return [item for slot in self.__dataclass_fields__ if isinstance(getattr(self, slot), list) for item in getattr(self, slot)]
    
    def sell(self, slot, index, iteminventory: "ItemInventory"):
        if not hasattr(self, slot):
            raise ValueError(f"❌ 無效的裝備欄位: {slot}")
        
        slot_list = self.get_slot(slot)

        if not (0 <= index < len(slot_list)):
            raise IndexError(f"❌ 裝備索引超出範圍：{slot}[{index}]")

        equipment = slot_list.pop(index)
        gain_money = equipment.get_sell_money()
        iteminventory.money += gain_money
            
        return f"⚠️ 系統提示：你出售了**{equipment.get_display_name()}**，獲得{gain_money}元！"