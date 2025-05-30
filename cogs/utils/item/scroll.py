from dataclasses import dataclass
from typing import Optional, Dict
from random import random

from .base_item import BaseItem

###############
# Scroll class
###############
@dataclass
class Scroll(BaseItem):
    # 共有屬性
    item_id: str        # 查表ID
    display_name: str   # 展示名稱
    rarity: str         # 稀有度
    figure_id: str      # 圖片ID
    sell_money: int     # 商店販售價格
    
    # 獨特屬性
    description: str    # 卷軸說明
    probability: float     # 強化成功機率
    destroy_on_fail: bool  # 裝備是否會損壞
    effect: Dict[str, int]  # 卷軸強化數值
    
    item_type: str
    destroy_rate: Optional[float] = None  # 裝備損壞機率
    purchase_money: Optional[int] = None  # 商店購買價格
    
    def to_dict(self) -> Dict:
        """轉換成字典

        Returns
        -------
        Dict:
            卷軸字典
        """
        
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "display_name": self.display_name,
            "rarity":    self.rarity,
            "figure_id": self.figure_id,
            "sell_money": self.sell_money,
            "description": self.description,
            "probability": self.probability,
            "destroy_on_fail": self.destroy_on_fail,
            "destroy_rate": self.destroy_rate,
            "effect": self.effect,
            "purchase_money": self.purchase_money
        }
        
    @classmethod
    def from_dict(cls, data) -> "Scroll":
        """將字典轉換為卷軸物件

        Parameters
        ----------
        data : dict
            卷軸字典

        Returns
        -------
        ItemInventory
            卷軸物件
        """
        
        return cls(
            item_id = data.get("item_id", ""),
            item_type = data.get("item_type", ""),
            display_name = data.get("display_name", ""),
            rarity = data.get("rarity", ""),
            figure_id = data.get("figure_id", ""),
            sell_money = data.get("sell_money", 0),
            description = data.get("description", ""),
            probability = data.get("probability", 1),
            destroy_on_fail = data.get("destroy_on_fail", False),
            destroy_rate = data.get("destroy_rate", None),
            effect = data.get("effect", {}),
            purchase_money = data.get("purchase_money", None)
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
    
    def get_purchase_money(self) -> int:
        """取得物品的商店購買價格

        Returns
        -------
        int
            商店購買價格
        """
        return self.purchase_money
    
    def initialize_attribute(self):
        return super().initialize_attribute()

    def determine_success(self) -> bool:
        """決定強化是否成功

        Returns
        -------
        bool
            是否成功
        """
        
        return random() < self.probability
    
    def determine_destroy(self) -> bool:
        """決定裝備是否損壞

        Returns
        -------
        bool
            是否損壞
        """
        
        return random() < self.destroy_rate
    
    def is_destroy_on_fail(self) -> bool:
        """卷軸強化失敗是否毀損

        Returns
        -------
        bool
            強化失敗是否毀損
        """
        
        return self.destroy_on_fail
    
#######################
# Prevent scroll class
#######################
@dataclass
class PreventScroll(BaseItem):
    # 共有屬性
    item_id: str        # 查表ID
    display_name: str   # 展示名稱
    rarity: str         # 稀有度
    figure_id: str      # 圖片ID
    sell_money: int     # 商店販售價格
    
    # 獨特屬性
    description: str    # 卷軸說明
    item_type: str = "prevent_scroll" 
    purchase_money: Optional[int] = None  # 商店購買價格
    
    def to_dict(self) -> Dict:
        """轉換成字典

        Returns
        -------
        Dict:
            防爆卷軸字典
        """
        
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "display_name": self.display_name,
            "rarity": self.rarity,
            "figure_id": self.figure_id,
            "sell_money": self.sell_money,
            "description": self.description,
            "purchase_money": self.purchase_money
        }
        
    @classmethod
    def from_dict(cls, data) -> "PreventScroll":
        """將字典轉換為原型武器物件

        Parameters
        ----------
        data : dict
            防爆卷軸字典

        Returns
        -------
        ItemInventory
            防爆卷軸物件
        """
        
        return cls(
            item_id = data.get("item_id", ""),
            item_type = data.get("item_type", ""),
            display_name = data.get("display_name", ""),
            rarity = data.get("rarity", ""),
            figure_id = data.get("figure_id", ""),
            sell_money = data.get("sell_money", 0),
            description = data.get("description", ""),
            purchase_money = data.get("purchase_money", None)
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
    
    def get_purchase_money(self) -> int:
        """取得物品的商店購買價格

        Returns
        -------
        int
            商店購買價格
        """
        return self.purchase_money