from dataclasses import dataclass, field
from typing import Optional, Dict, List

from .equipment import Equipment
from .base_item import BaseItem

##################
# Prototype class
##################
@dataclass
class Prototype(BaseItem):
    item_id: str        # 查表ID
    name: str           # 展示給玩家看的
    sell_money: int  # 商店販售價格
    
    system: str
    
    def get_item_id(self) -> str:
        return self.item_id
    
    def get_name(self) -> str:
        return self.name

    def get_sell_money(self) -> int:
        return self.sell_money
    
    def change_weapon(self, weapon: str):
        pass