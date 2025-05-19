from dataclasses import dataclass, field
from typing import Optional, Dict, List
from random import random

from .base_item import BaseItem

###############
# Scroll class
###############
@dataclass
class Scroll(BaseItem):
    item_id: str        # 查表ID
    name: str           # 展示給玩家看的
    sell_money: int  # 商店販售價格
    
    figure_name: str    # 圖片ID
    description: str    # 卷軸說明
    rarity: str         # 稀有度
    probability: float     # 強化成功機率
    destroy_on_fail: bool  # 裝備是否會損壞
    destroy_rate: Optional[float] = None  # 裝備損壞機率
    effect: Dict[str, int]  # 卷軸強化數值

    def get_item_id(self) -> str:
        return self.item_id
    
    def get_name(self) -> str:
        return self.name

    def get_sell_money(self) -> int:
        return self.sell_money

    def determine_success(self) -> bool:
        """決定強化是否成功
        
        Returns:
            bool: 是否成功
        """
        
        return random() < self.probability
    
    def determine_destroy(self) -> bool:
        """決定裝備是否損壞
        
        Returns:
            bool: 是否損壞
        """
        
        return random() < self.destroy_rate
    
    def is_destroy_on_fail(self) -> bool:
        """卷軸強化失敗是否毀損
        
        Returns:
            bools: 強化失敗是否毀損
        """
        
        return self.destroy_on_fail