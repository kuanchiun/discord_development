from dataclasses import dataclass
from typing import Optional, Dict

from ..item.equipment.equipment import Equipment
from ..equipinventory.equipinventory import EquipInventory

SLOTS = [
    "weapon", "head", "chest", "leggings", "feet",
    "earring", "necklace", "bracelet", "ring1", "ring2"
]

######################
# EquipmentSlot class
######################
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
    ring: Optional["Equipment"] = None
    ring2: Optional["Equipment"] = None
    
    @staticmethod
    def _safe_to_dict(slot: "Equipment") -> Optional[Dict]:
        """檢測欄位是否為None，並轉換為字典

        Parameters
        ----------
        obj : Equipment
            裝備欄位

        Returns
        -------
        Optional[Dict]
            裝備資訊
        """
        return slot.to_dict() if slot else None
    
    def to_dict(self) -> Dict[str, Dict]:
        """轉換成字典

        Returns
        -------
        Dict:
            裝備欄字典
        """
        
        return {
            "weapon":   self._safe_to_dict(self.weapon),
            "head":     self._safe_to_dict(self.head),
            "chest":    self._safe_to_dict(self.chest),
            "leggings": self._safe_to_dict(self.leggings),
            "feet":     self._safe_to_dict(self.feet),
            "earring":  self._safe_to_dict(self.earring),
            "necklace": self._safe_to_dict(self.necklace),
            "bracelet": self._safe_to_dict(self.bracelet),
            "ring":    self._safe_to_dict(self.ring),
            "ring2":    self._safe_to_dict(self.ring2)
        }
        
    @classmethod
    def from_dict(cls, data: Dict) -> "EquipmentSlot":
        """將字典轉換為裝備物件

        Parameters
        ----------
        data : dict
            裝備欄字典

        Returns
        -------
        EquipmentSlot
            裝備欄物件
        """
        
        return cls(
            weapon   = Equipment.from_dict(data["weapon"])   if data.get("weapon")   else None,
            head     = Equipment.from_dict(data["head"])     if data.get("head")     else None,
            chest    = Equipment.from_dict(data["chest"])    if data.get("chest")    else None,
            leggings = Equipment.from_dict(data["leggings"]) if data.get("leggings") else None,
            feet     = Equipment.from_dict(data["feet"])     if data.get("feet")     else None,
            earring  = Equipment.from_dict(data["earring"])  if data.get("earring")  else None,
            necklace = Equipment.from_dict(data["necklace"]) if data.get("necklace") else None,
            bracelet = Equipment.from_dict(data["bracelet"]) if data.get("bracelet") else None,
            ring    =  Equipment.from_dict(data["ring"])     if data.get("ring")     else None,
            ring2    = Equipment.from_dict(data["ring2"])    if data.get("ring2")    else None
        )
    
    def is_already_equipped(self, slot_name: str) -> bool:
        """檢查裝備欄位是否已經有裝備

        Parameters
        ----------
        slot : str
            裝備欄位

        Returns
        -------
        bool
            是否已經有裝備

        Raises
        ------
        ValueError
            無效的裝備欄位
        """
        
        if not hasattr(self, slot_name):
            raise ValueError(f"⚠️ 系統提示：無效的裝備欄位: {slot_name}")
        
        return getattr(self, slot_name) is not None
    
    def get_slot(self, slot_name: str) -> Equipment:
        
        if not hasattr(self, slot_name):
            raise ValueError(f"⚠️ 系統提示：無效的裝備欄位: {slot_name}")
        return getattr(self, slot_name)
        
    def equip(self, 
              slot_name: str, 
              index: int, 
              equipinventory: "EquipInventory") -> None:
        """將裝備裝備於裝備欄上

        Parameters
        ----------
        slot : str
            裝備欄位
        index : int
            裝備位在背包哪一格
        equipinventory : EquipInventory
            玩家的裝備背包
        """
        
        if getattr(self, slot_name):
            old_equipment = getattr(self, slot_name)
            equipinventory.get_slot(slot_name = slot_name).append(old_equipment)
        
        selected_equipment = equipinventory.get_slot(slot_name = slot_name)[index]
        setattr(self, slot_name, selected_equipment)
        equipinventory.get_slot(slot_name).pop(index)
    
    