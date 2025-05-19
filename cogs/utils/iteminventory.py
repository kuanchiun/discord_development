from dataclasses import dataclass, field
from typing import Optional, Dict, List, Union

from .base_item import BaseItem
from .scroll import Scroll
from .prototype import Prototype

@dataclass
class InventoryEntry:
    item: BaseItem
    quantity: int

@dataclass
class ItemInventory:
    inventory: Dict[str, "InventoryEntry"] = {}
    money: int = 0
    
    def add(self, item: BaseItem, amount: int = 1):
        if item.get_item_id() in self.inventory:
            self.inventory[item.get_item_id()].quantity += amount
        else:
            self.inventory[item.get_item_id()] = InventoryEntry(item = item, 
                                                                quantity = amount)
    
    def remove(self, item_id: str, amount: int = 1) -> str:
        if item_id not in self.inventory:
            return "⚠️ 系統提示：你未持有該道具！"
        
        entry = self.inventory[item_id]
        
        if entry.quantity < amount:
            return f"⚠️ 系統提示：道具的持有量不足！"
        
        entry.quantity -= amount
        
        if entry.quantity == 0:
            del self.inventory[item_id]
        return f"⚠️ 系統提示：你已使用**{amount}**個**{entry.item.get_name()}**！"
    
    def sell(self, item_id: str, amount: int = 1) -> str:
        if item_id not in self.inventory:
            return "⚠️ 系統提示：你未持有該道具！"
        
        entry = self.inventory[item_id]
        
        if entry.quantity < amount:
            return f"⚠️ 系統提示：道具的持有量不足！"
        
        entry.quantity -= amount
        
        gain_money = entry.item.get_sell_money() * amount
        self.money += gain_money
        
        if entry.quantity == 0:
            del self.inventory[item_id]
        return f"⚠️ 系統提示：你出售了**{amount}**個**{entry.item.get_name()}**，獲得{gain_money}元！"
    
    def get(self, item_id: str) -> Optional[BaseItem]:
        return self.inventory[item_id].item if item_id in self.inventory else None
    
    def list_all(self) -> list["InventoryEntry"]:
        return list(self.inventory.values())
    
    