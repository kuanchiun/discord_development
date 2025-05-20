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
    
    def add(self, item: BaseItem, amount: int = 1) -> None:
        """增加物品數量

        Parameters
        ----------
        item : BaseItem
            物品物件
        amount : int, optional
            數量, by default 1
        """
        
        """增加物品數量
        
        Args:
            item (BaseItem): 物品
            amount (int): 數量
        
        Returns:
            None
        """
        
        # 檢查是否持有物品
        if item.get_item_id() in self.inventory:
            self.inventory[item.get_item_id()].quantity += amount
        else:
            self.inventory[item.get_item_id()] = InventoryEntry(item = item, 
                                                                quantity = amount)
    
    def remove(self, item_id: str, amount: int = 1) -> str:
        """減少物品數量

        Parameters
        ----------
        item_id : str
            物品ID
        amount : int, optional
            數量, by default 1

        Returns
        -------
        str
            系統資訊
        """
        
        # 檢查是否持有物品
        if item_id not in self.inventory:
            return "⚠️ 系統提示：你未持有該物品！"
        
        entry = self.inventory[item_id]
        
        # 檢查物品持有量
        if entry.quantity < amount:
            return f"⚠️ 系統提示：物品的持有量不足！"
        
        entry.quantity -= amount
        
        # 如果數量為零，直接刪除
        if entry.quantity == 0:
            del self.inventory[item_id]
        return f"⚠️ 系統提示：你已使用**{amount}**個**{entry.item.get_name()}**！"
    
    def sell(self, item_id: str, amount: int = 1) -> str:
        """販賣物品

        Parameters
        ----------
        item_id : str
            物品ID
        amount : int, optional
            數量, by default 1

        Returns
        -------
        str
            系統資訊
        """
        
        # 檢查是否持有物品
        if item_id not in self.inventory:
            return "⚠️ 系統提示：你未持有該物品！"
        
        entry = self.inventory[item_id]
        
        # 檢查物品持有量
        if entry.quantity < amount:
            return f"⚠️ 系統提示：物品的持有量不足！"
        
        entry.quantity -= amount
        
        # 處理販賣金錢
        gain_money = entry.item.get_sell_money() * amount
        self.money += gain_money
        
        # 如果數量為零，直接刪除
        if entry.quantity == 0:
            del self.inventory[item_id]
        return f"⚠️ 系統提示：你出售了**{amount}**個**{entry.item.get_name()}**，獲得{gain_money}元！"
    
    def get(self, item_id: str) -> Optional[BaseItem]:
        """取得物品資訊

        Parameters
        ----------
        item_id : str
            物品ID

        Returns
        -------
        BaseItem or None
            若有道具則回傳道具資訊, 沒有則回傳無
        """
        
        return self.inventory[item_id].item if item_id in self.inventory else None
    
    def list_all(self) -> list["InventoryEntry"]:
        """列出所有持有物品

        Returns
        -------
        list[InventoryEntry]
            物品列表
        """
        
        return list(self.inventory.values())
    
    