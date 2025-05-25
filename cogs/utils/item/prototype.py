from dataclasses import dataclass, field
from typing import Optional, Dict
import yaml

from .equipment import Equipment
from .base_item import BaseItem


WEAPON_MAP: Dict = {
    "劍盾": "sword_shield",
    "長槍": "swear",
    "武士刀": "katana",
    "雙劍": "twin_blades",
    "雙槍": "dual_pistols",
    "弓": "bow",
    "步槍": "rifle",
    "火焰法杖": "fire_staff",
    "寒霜法杖": "ice_staff",
    "雷電法杖": "thunder_staff",
    "匕首": "dagger",
    "苦無": "kunai",
    "撲克牌": "playing_cards"
}

##################
# Prototype class
##################
@dataclass
class Prototype(BaseItem):
    # 共有屬性
    item_id: str        # 查表ID
    display_name: str   # 展示名稱
    description: str    # 物品說明
    rarity: str         # 稀有度
    figure_id: str      # 圖片ID
    sell_money: int     # 商店販售價格
    
    item_type: str

    
    def to_dict(self) -> Dict:
        """轉換成字典

        Returns
        -------
        Dict:
            原型武器字典
        """
        
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "display_name": self.display_name,
            "description": self.description,
            "rarity":    self.rarity,
            "figure_id": self.figure_id,
            "sell_money": self.sell_money
        }
        
    @classmethod
    def from_dict(cls, data) -> "Prototype":
        """將字典轉換為原型武器物件

        Parameters
        ----------
        data : dict
            原型武器字典

        Returns
        -------
        ItemInventory
            原型武器物件
        """
        
        return cls(
            item_id = data.get("item_id", ""),
            item_type = data.get("item_type", ""),
            display_name = data.get("display_name", ""),
            description = data.get("description", ""),
            rarity = data.get("rarity", ""),
            figure_id = data.get("figure_id", ""),
            sell_money = data.get("sell_money", 0)
        )
    
    def get_item_id(self) -> str:
        """取得物品的唯一ID

        Returns
        -------
        str
            物品ID
        """
        
        return self.item_id
    
    def get_item_type(self) -> str:
        """取得物品的物品類型

        Returns
        -------
        str
            物品ID
        """
        
        return self.item_type
    
    def get_display_name(self) -> str:
        """取得物品的顯示名稱

        Returns
        -------
        str
            物品顯示名稱
        """
        
        return self.display_name
    
    def get_description(self):
        """取得物品的說明

        Returns
        -------
        str
            物品說明
        """
        return self.description
    
    def get_rarity(self) -> str:
        """取得物品的稀有度

        Returns
        -------
        str
            物品稀有度
        """
        
        return self.rarity
    
    def get_figure_id(self) -> str:
        """取得物品的圖片ID

        Returns
        -------
        str
            物品圖片ID
        """
        
        return self.figure_id
    
    def get_sell_money(self) -> int:
        """取得物品的售價

        Returns
        -------
        str
            物品售價
        """
        
        return self.sell_money
    
    def get_purchase_money(self):
        """取得物品商店購買價格"""
        return super().get_purchase_money()
    
    def exchange_weapon(self, weapon_type: str) -> Optional["Equipment"]:
        """使用貨幣兌換系列武器

        Parameters
        ----------
        weapon_type : str
           兌換武器類型

        Returns
        -------
        Equipment
            兌換武器
        """
        
        with open("yaml/equipments/exchange_weapons.yaml", "r", encoding = "utf-8") as f:
            data = yaml.safe_load(f)
        
        for weapon in data[self.get_item_id()]:
            if weapon["item_id"] == f"{self.get_item_id()}_{weapon_type}":
                return Equipment(**weapon)
        
        return "❌ 沒有這個武器類型！"