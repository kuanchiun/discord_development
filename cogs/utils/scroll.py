from dataclasses import dataclass, field
from typing import Optional, Dict, List
from random import random

from .base_item import BaseItem

###############
# Scroll class
###############
@dataclass
class Scroll(BaseItem):
    # 共有屬性
    item_id: str        # 查表ID
    item_type: str = "scroll" 
    display_name: str   # 展示名稱
    rarity: str         # 稀有度
    figure_id: str      # 圖片ID
    sell_money: int     # 商店販售價格
    
    # 獨特屬性
    description: str    # 卷軸說明
    probability: float     # 強化成功機率
    destroy_on_fail: bool  # 裝備是否會損壞
    destroy_rate: Optional[float] = None  # 裝備損壞機率
    effect: Dict[str, int]  # 卷軸強化數值
    
    def to_dict(self):
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
        }
        
    @classmethod
    def from_dict(cls, data):
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
            destroy_rate = data.get("destroy_rate", 0),
            effect = data.get("effect", {})
        )

    def get_item_id(self) -> str:
        """取得物品的唯一ID

        Returns
        -------
        str
            物品ID
        """
        
        return self.item_id
    
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