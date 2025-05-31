from dataclasses import dataclass, field
from typing import Dict, List

from ..item.equipment.equipment import Equipment
from ..iteminventory.iteminventory import ItemInventory

MAX_EQUIP_PER_SLOT = 10

#######################
# EquipInventory class
#######################
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
    
    def to_dict(self) -> Dict[str, List]:
        """轉換成字典

        Returns
        -------
        Dict:
            裝備背包字典
        """
        
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
    def from_dict(cls, data: dict) -> "EquipInventory":
        """將字典轉換為裝備背包物件

        Parameters
        ----------
        data : dict
            裝備背包字典

        Returns
        -------
        EquipInventory
            裝備背包物件
        """
        
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
    
    def get_slot(self, slot_name: str) -> List[Equipment]:
        """取得裝備欄位的裝備

        Parameters
        ----------
        slot : str
            裝備欄位名稱

        Returns
        -------
        List[Equipment]
            裝備欄位的所有裝備

        Raises
        ------
        ValueError
            無效的裝備欄位
        TypeError
            裝備欄位型別不是List
        """
        
        if not hasattr(self, slot_name):
            raise ValueError(f"⚠️ 系統提示：無效的裝備部位: {slot}")
        
        slot = getattr(self, slot_name)
        if not isinstance(slot, list):
            raise TypeError(f"⚠️ 系統提示：欄位 {slot} 不是 list，無法操作裝備")
        
        return slot
    
    def get_equipment(self, slot_name: str, index: int) -> "Equipment":
        """取得裝備資訊

        Parameters
        ----------
        slot : str
            裝備欄位
        index : int
            欄位的索引

        Returns
        -------
        Equipment
            裝備
        """
        
        slot_list = self.get_slot(slot_name)
        
        return slot_list[index]
    
    def get_slot_equipment_name_list(self, slot_name: str) -> List[str]:
        return [item.get_display_name() for item in self.get_slot(slot_name)]

    def list_equipment(self) -> List["Equipment"]:
        """取得所有裝備

        Returns
        -------
        List[Equipment]
            所有裝備
        """
        
        all_equipment = []
        for slot in self.__dataclass_fields__:
            try:
                all_equipment.extend(self.get_slot(slot))
            except (ValueError, TypeError):
                continue
        return all_equipment
    
    def get_overloaded_slots(self) -> Dict[str, int]:
        """回傳所有超過上限的欄位與裝備數量

        Returns
        -------
        Dict[str, int]
            所有超過上限的欄位與裝備數量
        """
        overloaded = {}
        for slot in self.__dataclass_fields__:
            slot_list = self.get_slot(slot)
            if isinstance(slot_list, list) and len(slot_list) > MAX_EQUIP_PER_SLOT:
                overloaded[slot] = len(slot_list)
        
        return overloaded
        
    def add(self, equipment: Equipment) -> None:
        """將裝備加到對應的裝備欄位

        Parameters
        ----------
        equipment : Equipment
            裝備
        """
        
        slot = self.get_slot(equipment.slot)
        slot.append(equipment)

    def remove(self, equipment: Equipment) -> None:
        """將裝備從對應的裝備欄位移除

        Parameters
        ----------
        equipment : Equipment
            裝備
        """
        
        slot = self.get_slot(equipment.slot)
        slot.remove(equipment)

    def sell(self, equipment: Equipment, iteminventory: ItemInventory) -> str:
        """賣出裝備

        Parameters
        ----------
        equipment : Equipment
            要賣的裝備
        iteminventory : ItemInventory
            玩家背包

        Returns
        -------
        str
            販售資訊
        """
        
        slot = self.get_slot(equipment.slot)
        gain_money = equipment.get_sell_money()
        
        try:
            slot.remove(equipment)
        except ValueError:
            return f"⚠️ 系統提示：裝備 **{equipment.get_display_name()}** 不在背包中，無法出售！"
        
        iteminventory.add_money(gain_money)
        return f"⚠️ 系統提示：你出售了**{equipment.get_display_name()}**，獲得💎**{gain_money}**！"