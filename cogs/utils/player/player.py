from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, Tuple
from random import choice, choices
from enum import Enum
from pathlib import Path

import yaml

from .baseattribute import BaseAttribute
from ..equipinventory.equipinventory import EquipInventory
from ..iteminventory.iteminventory import ItemInventory
from ..equipmentslot.equipmentslot import EquipmentSlot

PLAYER_SAVEPATH = Path("yaml/players")

###############
# Player class
###############
@dataclass
class Player:
    baseattribute: "BaseAttribute" = None
    equipinventory: "EquipInventory" = None
    equipmentslot: "EquipmentSlot" = None
    iteminventory: "ItemInventory" = None
    
    def __post_init__(self):
        if self.baseattribute is None:
            self.baseattribute = BaseAttribute()
        if self.equipinventory is None:
            self.equipinventory = EquipInventory()
        if self.equipmentslot is None:
            self.equipmentslot = EquipmentSlot()
        if self.iteminventory is None:
            self.iteminventory = ItemInventory()
    
    def to_dict(self) -> Dict:
        """轉換成字典

        Returns
        -------
        Dict:
           玩家字典
        """
        
        return {
            "baseattribute": self.baseattribute.to_dict(),
            "equipinventory": self.equipinventory.to_dict(),
            "equipmentslot": self.equipmentslot.to_dict(),
            "iteminventory": self.iteminventory.to_dict()
        }
    
    @classmethod
    def exists(cls, user_id: int) -> bool:
        """檢查用戶資料是否存在

        Parameters
        ----------
        user_id : int
            用戶ID

        Returns
        -------
        bool
            資料是否存在
        """
        
        file_path = PLAYER_SAVEPATH / f"{user_id}.yaml"
        return file_path.exists()
    
    @classmethod
    def load(cls, user_id: int) -> "Player":
        """載入用戶資料或初始化玩家資料

        Parameters
        ----------
        user_id : int
            用戶ID

        Returns
        -------
        Player
            玩家物件
        """
        
        PLAYER_SAVEPATH.mkdir(exist_ok = True)
        file_path = PLAYER_SAVEPATH / f"{user_id}.yaml"
        
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
            return cls(
                baseattribute = BaseAttribute.from_dict(data["baseattribute"]),
                equipinventory = EquipInventory.from_dict(data["equipinventory"]),
                equipmentslot = EquipmentSlot.from_dict(data["equipmentslot"]),
                iteminventory = ItemInventory.from_dict(data["iteminventory"])
            )
        else:
            return cls(
                baseattribute = BaseAttribute(),
                equipinventory = EquipInventory(),
                equipmentslot = EquipmentSlot(),
                iteminventory = ItemInventory()
            )
    
    def save(self, user_id: int) -> None:
        """儲存用戶資料
        
        Parameters
        ----------
        user_id : int
            用戶ID
        """
        
        PLAYER_SAVEPATH.mkdir(exist_ok = True)
        file_path = PLAYER_SAVEPATH / f"{user_id}.yaml"
        
        with open(file_path, "w", encoding = "utf-8") as file:
            yaml.safe_dump(self.to_dict(), file, allow_unicode = True)
    




















"""
def enhance_equipped_item(self, slot_name, scroll_id, protect_scroll_id=None):
    # 1. 取得裝備
    slot = self.equipment_slot.get(slot_name)
    equipment = slot.current
    if not equipment:
        return "❌ 該欄位沒有裝備"

    # 2. 取得強化卷軸
    scroll = self.item_inventory.get(scroll_id)
    if not scroll:
        return "❌ 強化卷軸不存在"

    # 3. 若需要防爆卷軸，額外取得
    protect_scroll = None
    if scroll.destroy_on_fail:
        if not protect_scroll_id:
            return "⚠️ 此卷軸有爆裝風險，請選擇是否使用防爆卷軸"
        protect_scroll = self.item_inventory.get(protect_scroll_id)
        if not protect_scroll or protect_scroll.type != "protect":
            return "❌ 防爆卷軸無效或不存在"

    # 4. 執行強化
    new_equipment = equipment.attempt_enhance(scroll, protect_scroll)

    # 5. 根據結果更新裝備或爆裝
    if new_equipment is None:
        slot.unequip()
        result = "💥 裝備爆炸！"
    else:
        slot.equip(new_equipment)
        result = "✅ 強化成功！" if new_equipment != equipment else "❌ 強化失敗，裝備未改變"

    # 6. 移除卷軸與防爆卷軸
    self.item_inventory.remove(scroll_id)
    if protect_scroll_id:
        self.item_inventory.remove(protect_scroll_id)

    # 7. 更新屬性
    self.player_attribute.recalculate()

    return result
"""